from __future__ import annotations

"""검수된 선지 근거를 이용해 짧은 풀이 알고리듬의 마지막 판단 단계를 보강한다."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"


def normalize(text: str) -> str:
    text = re.sub(r"^(정답(?:인 잘못된)? 선지[.:]?|정답[.:]?)\s*", "", text.strip())
    return text[:1].lower() + text[1:] if text else text


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    changed = 0
    for q in payload["questions"]:
        lecture = q.get("lectureNumber", "")
        if not lecture.isdigit() or int(lecture) > 32:
            continue
        exp = q.get("explanation") or {}
        steps = exp.get("reasoningSteps", [])
        choices = exp.get("choiceExplanations", [])
        answers = [a for a in q.get("answers", []) if 1 <= a <= len(choices)]
        if len(steps) >= 4 or not answers:
            continue
        facts = [normalize(choices[a - 1]).rstrip(".") for a in answers]
        # 화면에는 풀이 행동을 지시하는 문장이 아니라 실제 의학적 근거만 남긴다.
        # "정답 후보를 확인한다"는 말은 학습 정보를 주지 않고 정답을 다시 말할 뿐이다.
        if len(facts) == 1:
            final = f"{facts[0]}."
        else:
            final = " / ".join(facts) + "."
        exp["reasoningSteps"] = list(steps) + [final]
        changed += 1

    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"REASONING_STEPS_ENHANCED questions={changed}")


if __name__ == "__main__":
    main()
