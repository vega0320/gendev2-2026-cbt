from __future__ import annotations

"""해설의 상투문구, 짧은 풀이, 선지 혼입 회귀를 읽기 전용으로 검사한다."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"
BANNED = (
    "재출제 포인트",
    "사례를 그 원칙에 대입",
    "먼저 문제 요구를 확인한다",
    "각 선지를 이 단서와 대조",
    "정답 조건과 맞지 않는다",
    "관련되지 않는다",
    "마지막으로 정답 후보의 직접 근거를 확인한다",
    "마지막으로 각 정답 후보의 독립 근거를 확인한다",
    "문제의 내용에 따라",
    "정답 후보를 선택한다",
)


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    failures: list[str] = []
    reviewed = 0
    for q in payload["questions"]:
        lecture = q.get("lectureNumber", "")
        if not lecture.isdigit() or int(lecture) > 32:
            continue
        reviewed += 1
        exp = q.get("explanation") or {}
        blob = json.dumps(exp, ensure_ascii=False)
        for marker in BANNED:
            if marker in blob:
                failures.append(f"{q['id']}: banned={marker}")
        if q.get("questionMode") != "self-check" and len(exp.get("reasoningSteps", [])) < 4:
            failures.append(f"{q['id']}: reasoningSteps<4")
        if q.get("questionMode") != "self-check" and len(exp.get("choiceExplanations", [])) != len(q.get("choices", [])):
            failures.append(f"{q['id']}: choice explanation count mismatch")
        review = exp.get("conceptReview", "")
        for choice in q.get("choices", []):
            choice = re.sub(r"\s+", " ", choice).strip()
            if len(choice) >= 18 and choice in review:
                failures.append(f"{q['id']}: choice copied into conceptReview")

    regressions = {
        "gendev2-09-2023-q016": (4, r"에스트로겐|복합호르몬|MEC|혈전", r"\bACE\b"),
        "gendev2-01-2025-q052": (0, r"항이뇨호르몬|수분 재흡수", r"목덜미|NT는"),
        "gendev2-08-2022-q048": (4, r"태반|융모막|lambda", r"\bACE\b"),
    }
    by_id = {q["id"]: q for q in payload["questions"]}
    for qid, (index, required, forbidden) in regressions.items():
        text = by_id[qid]["explanation"]["choiceExplanations"][index]
        if not re.search(required, text, re.I) or re.search(forbidden, text, re.I):
            failures.append(f"{qid}: semantic regression at choice {index + 1}")

    if failures:
        raise SystemExit("\n".join(failures[:50]))
    print(f"EXPLANATION_INTEGRITY_AUDIT_PASS questions={reviewed} min_steps=4 regressions={len(regressions)}")


if __name__ == "__main__":
    main()
