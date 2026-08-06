from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from difflib import SequenceMatcher
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "site" / "data" / "questions.json"
GENERIC = {
    "정답", "오답", "선지", "해당", "문항", "환자", "경우", "때문", "필요", "있다", "없다",
    "아니다", "맞다", "않다", "한다", "된다", "대한", "위한", "보통", "현재", "따라",
}


def body(text: str) -> str:
    return text.split(". ", 1)[-1].strip()


def tokens(text: str) -> list[str]:
    words = re.findall(r"[가-힣A-Za-z0-9]+", body(text).lower())
    return [word for word in words if len(word) >= 2 and word not in GENERIC]


def token_cosine(left: str, right: str) -> float:
    a, b = Counter(tokens(left)), Counter(tokens(right))
    if not a or not b:
        return 0.0
    dot = sum(a[key] * b[key] for key in a.keys() & b.keys())
    norm_a = sum(value * value for value in a.values()) ** 0.5
    norm_b = sum(value * value for value in b.values()) ** 0.5
    return dot / (norm_a * norm_b)


def char_ratio(left: str, right: str) -> float:
    normalize = lambda value: re.sub(r"\s+", "", body(value))
    return SequenceMatcher(None, normalize(left), normalize(right), autojunk=False).ratio()


def shared_claim(left: str, right: str) -> tuple[float, list[str]]:
    a, b = set(tokens(left)), set(tokens(right))
    shared = sorted(a & b)
    union = a | b
    return (len(shared) / len(union) if union else 0.0), shared


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--fail", action="store_true")
    parser.add_argument("--limit", type=int, default=80)
    parser.add_argument("--through", type=int, default=32)
    args = parser.parse_args()
    questions = json.loads(args.data.read_text(encoding="utf-8"))["questions"]
    rows = []
    generic_rows = []
    exact_rows = []
    gtpals_checked = 0
    banned = ("생리량의 변화 방향", "제시된 조치다", "답으로 채택하려면", "후보이므로", "검사 시점은")
    for question in questions:
        lecture = question.get("lectureNumber", "")
        if not lecture.isdigit() or not 1 <= int(lecture) <= args.through:
            continue
        explanations = (question.get("explanation") or {}).get("choiceExplanations", [])
        if len(explanations) != 5:
            continue
        for index, explanation in enumerate(explanations):
            if any(phrase in explanation for phrase in banned):
                generic_rows.append((question["id"], index + 1))
        is_gtpal = all(re.fullmatch(r"\d-\d-\d-\d", choice.strip()) for choice in question.get("choices", []))
        if is_gtpal:
            signatures = [body(text).removeprefix("오류 항목: ") for text in explanations]
            if len(set(signatures)) != 5:
                rows.append((1.0, 1.0, 1.0, 1.0, question, 0, 1, ["GTPAL 오류 항목 중복"]))
            gtpals_checked += 1
            continue
        for left, right in combinations(range(5), 2):
            cosine = token_cosine(explanations[left], explanations[right])
            ratio = char_ratio(explanations[left], explanations[right])
            jaccard, shared = shared_claim(explanations[left], explanations[right])
            score = max(cosine, ratio, jaccard)
            if body(explanations[left]) == body(explanations[right]):
                exact_rows.append((question["id"], left + 1, right + 1))
            if cosine >= 0.82 or ratio >= 0.86 or jaccard >= 0.72:
                rows.append((score, cosine, ratio, jaccard, question, left, right, shared))
    rows.sort(key=lambda row: row[0], reverse=True)
    print(
        f"SEMANTIC_CHOICE_AUDIT candidates={len(rows)} exact={len(exact_rows)} "
        f"generic={len(generic_rows)} gtpalChecked={gtpals_checked}"
    )
    for score, cosine, ratio, jaccard, question, left, right, shared in rows[: args.limit]:
        explanations = question["explanation"]["choiceExplanations"]
        print(f"\n{question['id']} L{question['lectureNumber']} {left + 1}<->{right + 1} max={score:.3f} cos={cosine:.3f} seq={ratio:.3f} jac={jaccard:.3f}")
        print(f"shared={','.join(shared)}")
        print(f"A {body(explanations[left])}")
        print(f"B {body(explanations[right])}")
    if generic_rows:
        print("GENERIC_ROWS " + ", ".join(f"{qid}#{number}" for qid, number in generic_rows))
    if exact_rows:
        print("EXACT_ROWS " + ", ".join(f"{qid}#{left}-{right}" for qid, left, right in exact_rows))
    if args.fail and (rows or generic_rows or exact_rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
