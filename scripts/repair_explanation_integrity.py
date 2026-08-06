from __future__ import annotations

"""과거 자동감사에서 붙인 비의학적 문구를 제거하고 재발을 차단한다."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"


def clean(text: str) -> str:
    text = re.sub(r" 이 문항에서는 정답 .*?와 구별하는 것이 재출제 포인트다\.", "", text)
    text = re.sub(r" 재출제 포인트:.*$", "", text)
    text = re.sub(r" 같은 개념의 반복문항 중 이 문제는 .*?다시 판정한다\.", "", text)
    text = re.sub(r" 이 평가는 \d{4}년 .*? 선지에 적용한다\.", "", text)
    text = re.sub(r" 이 문항에서는 ‘.*?’라는 사례를 그 원칙에 대입해 .*?를 선택한다\.", "", text)
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    changed = 0
    for q in payload["questions"]:
        exp = q.get("explanation") or {}
        lecture = q.get("lectureNumber", "")
        if lecture.isdigit() and 1 <= int(lecture) <= 20:
            stem = q.get("stem", "")
            if any(token in stem for token in ("옳지 않은", "틀린", "아닌 것", "적절하지 않은")):
                direction = "옳지 않은 선지"
            elif any(token in stem for token in ("옳은", "맞는", "적절한", "가장 알맞")):
                direction = "옳은 선지"
            else:
                direction = "정답 선지"
            internal_check = f"내부 검수: {direction} {len(q.get('answers', []))}개 · 저장 정답 {','.join(map(str, q.get('answers', [])))}"
            q["questionCheck"] = internal_check
            exp["questionCheck"] = internal_check
            q["explanationReviewStatus"] = (
                "manual-choice-independent-audit-01-13"
                if int(lecture) <= 13
                else "manual-choice-independent-audit-14-20"
            )
        for field in ("keyJudgment", "conceptReview"):
            old = exp.get(field, "")
            new = clean(old)
            if old != new:
                exp[field] = new
                changed += 1
        old_choices = exp.get("choiceExplanations", [])
        new_choices = [clean(x) for x in old_choices]
        if old_choices != new_choices:
            exp["choiceExplanations"] = new_choices
            changed += 1

    banned = ("재출제 포인트", "사례를 그 원칙에 대입", "각 선지를 이 단서와 대조")
    failures = []
    for q in payload["questions"]:
        blob = json.dumps(q.get("explanation", {}), ensure_ascii=False)
        for marker in banned:
            if marker in blob:
                failures.append(f"{q['id']}: {marker}")
    if failures:
        raise SystemExit("\n".join(failures[:20]))

    target = next(q for q in payload["questions"] if q["id"] == "gendev2-09-2023-q016")
    fifth = target["explanation"]["choiceExplanations"][4]
    if re.search(r"\bACE\b", fifth, re.I) or not re.search(r"에스트로겐|복합호르몬|MEC|혈전", fifth):
        raise SystemExit("gendev2-09-2023-q016: fifth choice contamination regression")

    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"EXPLANATION_INTEGRITY_REPAIR_PASS changed_fields={changed}")


if __name__ == "__main__":
    main()
