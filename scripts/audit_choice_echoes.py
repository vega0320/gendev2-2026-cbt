from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def audit(path: Path) -> tuple[int, list[str]]:
    questions = json.loads(path.read_text(encoding="utf-8"))["questions"]
    errors: list[str] = []
    scanned = 0
    for q in questions:
        explanations = (q.get("explanation") or {}).get("choiceExplanations", [])
        for index, (choice, explanation) in enumerate(zip(q.get("choices", []), explanations), 1):
            scanned += 1
            text = str(explanation).strip()
            if re.match(r"^(?:(?:정답 선지|선지 해설)\s*)?[‘'\"]", text):
                errors.append(f"{q['id']} choice {index}: quoted choice prefix remains")
            if re.match(r"^(?:정답|오답)\.?\s*[‘'\"]", text):
                errors.append(f"{q['id']} choice {index}: verdict plus quoted choice remains")
            raw = str(choice).strip()
            if len(raw) >= 12 and (f"‘{raw}’" in text or f"'{raw}'" in text or f'"{raw}"' in text):
                errors.append(f"{q['id']} choice {index}: quoted full choice copied into explanation")
    return scanned, errors


def main() -> None:
    targets = [ROOT / "data" / "questions.json"]
    site = ROOT / "site" / "data" / "questions.json"
    if site.exists():
        targets.append(site)
    total = 0
    errors: list[str] = []
    for path in targets:
        scanned, found = audit(path)
        total += scanned
        errors.extend(f"{path.relative_to(ROOT)}: {item}" for item in found)
    if errors:
        print("CHOICE_ECHO_AUDIT_FAIL")
        print("\n".join(f"- {item}" for item in errors))
        raise SystemExit(1)
    print(f"CHOICE_ECHO_AUDIT_PASS files={len(targets)} choices={total}")


if __name__ == "__main__":
    main()
