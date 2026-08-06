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
        if len(facts) == 1:
            final = f"마지막으로 정답 후보의 직접 근거를 확인한다. {facts[0]}."
        else:
            final = "마지막으로 각 정답 후보의 독립 근거를 확인한다. " + " / ".join(facts) + "."
        exp["reasoningSteps"] = list(steps) + [final]
        changed += 1

    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"REASONING_STEPS_ENHANCED questions={changed}")


if __name__ == "__main__":
    main()
