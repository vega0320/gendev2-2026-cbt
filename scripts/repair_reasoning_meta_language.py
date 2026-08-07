from __future__ import annotations

"""한 단계씩 풀이에서 정답 선택을 지시할 뿐인 메타 문구를 제거한다."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"

PREFIXES = (
    "마지막으로 정답 후보의 직접 근거를 확인한다. ",
    "마지막으로 각 정답 후보의 독립 근거를 확인한다. ",
)

REPLACEMENTS = {
    "성별·연령 성장도표에 대입한다.": "계산값을 같은 성별·연령의 BMI 백분위수와 비교해 저체중·정상·과체중·비만으로 분류한다.",
    "원인에 맞는 배란유도·유착박리·IVF·ICSI를 선택한다.": "무배란 PCOS는 letrozole 배란유도, 양측 난관폐쇄는 IVF, 중증 남성요인은 ICSI처럼 확인된 원인에 치료를 연결한다.",
    "악성 위험과 가임력에 맞춰 추적 또는 병기설정 가능한 수술을 선택한다.": "가임기 단순 낭종은 주기 후 초음파 추적이 기본이고, 지속·증대하거나 악성 소견이 있으면 가임력 보존 범위와 병기설정을 고려해 수술한다.",
    "현재 임신 15주라는 시기를 보고 양수천자를 선택한다.": "임신 15주는 융모막융모검사의 일반적 시기보다 늦고 양수천자가 가능한 시기이므로, 양수 세포의 핵형·염색체검사를 진행한다.",
    "따라서 문제의 숫자가 전체 축적량인지 일일 섭취량인지 일일 흡수량인지 단위를 확인해 답을 고른다.": "전체 추가 요구량은 mg/임신 전체, 권장 섭취량은 mg/일 경구 투여, 실제 흡수 요구량은 mg/일 흡수량이므로 단위와 시간축을 구분한다.",
}


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    changed_questions = 0
    removed_prefixes = 0
    replaced_steps = 0
    for question in payload["questions"]:
        explanation = question.get("explanation") or {}
        steps = explanation.get("reasoningSteps") or []
        question_changed = False
        if (
            any("핵심 생리·임상 단서를 먼저 찾는다" in step for step in steps)
            and any("나머지 선지는 맞아지는 조건과 비교한다" in step for step in steps)
        ):
            useful = [
                step for step in steps
                if "핵심 생리·임상 단서를 먼저 찾는다" not in step
                and "나머지 선지는 맞아지는 조건과 비교한다" not in step
            ]
            answers = set(question.get("answers") or [])
            differentials = []
            for index, text in enumerate(explanation.get("choiceExplanations") or [], 1):
                if index in answers:
                    continue
                fact = re.sub(r"^(정답|오답|부적절하다|적절하다)[.:]?\s*", "", text.strip())
                if fact and fact not in useful and fact not in differentials:
                    differentials.append(fact)
            steps = (useful[:1] + differentials[:2] + useful[1:])[:5]
            explanation["reasoningSteps"] = steps
            replaced_steps += 2
            question_changed = True
        updated: list[str] = []
        for step in steps:
            new_step = REPLACEMENTS.get(step, step)
            if new_step != step:
                replaced_steps += 1
                question_changed = True
            for prefix in PREFIXES:
                if new_step.startswith(prefix):
                    new_step = new_step[len(prefix):].strip()
                    removed_prefixes += 1
                    question_changed = True
                    break
            if new_step:
                updated.append(new_step)
        if question_changed:
            explanation["reasoningSteps"] = updated
            changed_questions += 1
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        "REASONING_META_LANGUAGE_REPAIRED "
        f"questions={changed_questions} prefixes={removed_prefixes} replacements={replaced_steps}"
    )


if __name__ == "__main__":
    main()
