from __future__ import annotations

"""선지 카드에 이미 보이는 선지 원문을 선지별 해설에서 제거한다."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "data" / "questions.json"]


def strip_echo(text: str, choice: str) -> str:
    value = str(text or "").strip()
    escaped = re.escape(str(choice).strip())
    patterns = [
        rf"^(?:정답|오답)\.\s*핵심 단서\s*‘.*?’를 적용하면\s*‘{escaped}’가\s*.*?해당한다\.\s*",
        rf"^오답\.\s*‘{escaped}’는\s*핵심 단서\s*‘.*?’에 맞는\s*.*?아니다\.\s*이 강의에서는 다음 판단축을 적용한다:\s*",
        rf"^(?:정답 선지|선지 해설)\s*[‘'\"]{escaped}[’'\"]\s*[—-]\s*(?:정답(?:\(틀린 진술\))?|오답|제외\(옳은 진술\))?\.?\s*",
        rf"^[‘'\"]{escaped}[’'\"]\s*[—-]\s*(?:정답(?:\(틀린 진술\))?|오답|제외\(옳은 진술\))?\.?\s*",
        rf"^(?:정답|오답)\.?\s*[‘'\"]{escaped}[’'\"]\s*(?:은|는)?\s*",
    ]
    for pattern in patterns:
        value = re.sub(pattern, "", value, count=1, flags=re.S)
    return value.strip()


def main() -> None:
    changed = 0
    scanned = 0
    for path in TARGETS:
        payload = json.loads(path.read_text(encoding="utf-8"))
        for question in payload["questions"]:
            explanations = (question.get("explanation") or {}).get("choiceExplanations", [])
            for index, choice in enumerate(question.get("choices", [])):
                if index >= len(explanations):
                    continue
                scanned += 1
                cleaned = strip_echo(explanations[index], choice)
                if cleaned != explanations[index]:
                    explanations[index] = cleaned
                    changed += 1
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"CHOICE_ECHO_REMOVAL_PASS scanned={scanned} changed={changed}")


if __name__ == "__main__":
    main()
