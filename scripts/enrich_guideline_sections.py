from __future__ import annotations

"""진단·치료 문항에 명시적 기준 목록과 자체 요약 흐름도를 연결한다."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"
DX_RE = re.compile(r"진단|질환|가장 가능|합당한|무엇인가|병기는")
TX_RE = re.compile(r"치료(?:는|법| 방법| 방침)|치료방침|처치(?:는|를|가)|조치(?:는|를)|투여해야|관리 방법|후속 조치")
ACTION_RE = re.compile(r"치료|투여|사용|시행|수술|분만|관찰|추적|검사|평가|의뢰|제거|절제|항생제|내분비|표적|고정술|슬링")
DX_FACT_RE = re.compile(r"진단|기준|정의|특징|소견|보이면|이면|일 때|분류|구분|침윤|양성|음성|증상|혈류|위험")
BANNED = ("정답", "문항", "선지", "고른", "요구", "대조", "고신호", "핵심 단서")

PPH_ID = "gendev2-06-2023-q029"
PEDIATRIC_OBESITY_IDS = {
    "gendev2-22-2025-q050",
    "gendev2-22-2023-q034",
    "gendev2-22-2022-q014",
    "gendev2-22-2021-q090",
    "gendev2-22-2020-q046",
}

PPH_GUIDE = [
    "저혈압·빈맥을 동반한 산후출혈은 대구경 정맥로, 혈액검사·교차시험, 수액·혈액 준비를 시작하면서 자궁마사지와 출혈 원인 평가를 동시에 시행한다.",
    "2025 WHO 지침의 첫 대응은 자궁마사지, 자궁수축제(우선 oxytocin), 출산 후 3시간 이내 tranexamic acid, 정맥수액, 산도·태반 평가를 묶어 지연 없이 시행하는 MOTIVE bundle이다.",
    "자궁무력 출혈이 지속되면 금기를 확인해 추가 자궁수축제를 투여하고 자궁내 풍선압박으로 단계 상승한다. 그래도 조절되지 않거나 혈역학적으로 불안정하면 색전술을 기다리지 말고 수술적 지혈을 준비한다.",
]

PEDIATRIC_OBESITY_GUIDE = [
    "BMI를 계산한 뒤 성별·연령별 성장도표에 표시하여 과체중(85백분위수 이상 95백분위수 미만), 비만(95백분위수 이상), 중증비만(95백분위수의 120% 이상 또는 BMI 35 kg/m² 이상 중 낮은 값)으로 분류한다.",
    "비만으로 확인되면 혈압과 병력·진찰을 포함해 대사·간·수면·정신사회 동반질환을 함께 평가하고, 낙인 없이 가족 중심의 집중 건강행동·생활습관 치료를 시작한다.",
    "AAP 2023 지침은 가능하면 3~12개월 동안 26시간 이상 접촉하는 가족 기반 다요소 치료를 권하며, 12세 이상 비만에서는 적응증·위험을 검토해 약물치료를 병행하고 13세 이상 중증비만은 다학제 비만대사수술 평가 의뢰를 제안한다.",
]


def sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?다])\s+", text or "") if len(part.strip()) >= 18]


def useful(text: str) -> bool:
    return bool(text) and not any(marker in text for marker in BANNED)


def dedupe(items: list[str], limit: int = 4) -> list[str]:
    result: list[str] = []
    for item in items:
        item = re.sub(r"\s+", " ", item).strip()
        if not useful(item):
            continue
        normalized = re.sub(r"[^0-9A-Za-z가-힣]", "", item).lower()
        if any(normalized == re.sub(r"[^0-9A-Za-z가-힣]", "", prior).lower() for prior in result):
            continue
        result.append(item)
        if len(result) >= limit:
            break
    return result


def source_meta(exp: dict) -> tuple[str, str]:
    for source in exp.get("sources") or []:
        url = source.get("url")
        if url:
            return url, source.get("label") or source.get("title") or "공식·교과서 근거"
    return "", "공식·교과서 근거"


def treatment_candidates(question: dict, exp: dict) -> list[str]:
    answers = set(question.get("answers") or [])
    correct_facts = [text for index, text in enumerate(exp.get("choiceExplanations") or [], 1) if index in answers]
    step_facts = [text for text in exp.get("reasoningSteps") or [] if ACTION_RE.search(text or "")]
    review_facts = [text for text in sentences(exp.get("conceptReview", "")) if ACTION_RE.search(text)]
    criteria_facts = [text for text in exp.get("diagnosticCriteria") or [] if ACTION_RE.search(text or "")]
    all_steps = [text for text in exp.get("reasoningSteps") or [] if useful(text)]
    return dedupe(correct_facts + step_facts + review_facts + criteria_facts + all_steps, 4)


def diagnosis_candidates(exp: dict) -> list[str]:
    current = exp.get("diagnosticCriteria") or []
    if current:
        return current
    pool = []
    for text in [*(exp.get("reasoningSteps") or []), exp.get("conceptReview", ""), *(exp.get("choiceExplanations") or [])]:
        pool.extend(sentence for sentence in sentences(text) if DX_FACT_RE.search(sentence))
    if not pool:
        pool.extend(exp.get("choiceExplanations") or [])
        pool.extend(exp.get("reasoningSteps") or [])
    return dedupe(pool, 4)


def ensure_source(exp: dict, *, label: str, url: str, kind: str = "현재 지침") -> None:
    sources = exp.setdefault("sources", [])
    if not any(source.get("url") == url for source in sources):
        sources.append({"label": label, "url": url, "kind": kind, "checkedAt": "2026-08-07"})


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    diagnosis_added = 0
    treatment_added = 0
    visual_added = 0
    unresolved: list[str] = []
    for question in payload["questions"]:
        exp = question.get("explanation") or {}
        stem = question.get("stem", "")
        if question["id"] == PPH_ID:
            exp["keyJudgment"] = "지속 출혈, 쇼크 활력징후, 이완된 자궁, 산도 열상·잔류조직 부재는 자궁무력 산후출혈을 가리킨다. 소생과 자궁마사지·oxytocin을 동시에 시작한다."
            exp["reasoningSteps"] = [
                "혈압 80/50 mmHg와 맥박 120회/분은 출혈성 쇼크이므로 관찰이 아니라 즉시 소생이 필요하다.",
                "부드럽고 수축하지 않는 자궁은 4T 가운데 Tone, 즉 자궁무력을 지지한다.",
                "질경검사에서 열상이 없고 초음파에서 잔류조직이 보이지 않아 Trauma와 Tissue의 우선순위가 낮다.",
                "자궁마사지와 oxytocin을 즉시 시행하고, 출혈이 계속되면 추가 자궁수축제·TXA·풍선압박·수술적 지혈로 단계 상승한다.",
            ]
            exp["choiceExplanations"] = [
                "쇼크 활력징후가 있는 지속 출혈은 경과관찰 대상이 아니며 소생과 원인치료를 동시에 시작해야 한다.",
                "Oxytocin은 자궁무력 산후출혈의 일차 자궁수축제이며 자궁마사지와 함께 즉시 투여한다.",
                "Ritodrine은 β2 작용 자궁수축억제제이므로 이완된 자궁의 수축을 회복시키는 치료와 반대 방향으로 작용한다.",
                "자궁내용 제거술은 잔류태반조직이 확인되거나 강하게 의심될 때 시행한다. 이 증례는 초음파에서 자궁강 내 덩이가 없다.",
                "자궁동맥색전술은 초기 약물·풍선압박에도 출혈이 지속되고 환자가 시술을 견딜 만큼 안정적일 때 고려하는 자궁보존 단계상승 치료다.",
            ]
            exp["diagnosticCriteria"] = [
                "ACOG 정의는 출생 후 24시간 이내 누적 실혈 1,000 mL 이상 또는 실혈량과 무관하게 저혈량 증상·징후가 동반된 출혈이다.",
                "2025 WHO/FIGO/ICM 지침은 실혈 500 mL 이상, 또는 300 mL 이상이면서 비정상 활력징후가 있으면 조기 대응을 시작하도록 권고한다.",
            ]
            exp["treatmentGuideline"] = PPH_GUIDE
            ensure_source(exp, label="WHO consolidated postpartum haemorrhage guideline (2025)", url="https://www.who.int/publications/i/item/9789240115637")
        elif question["id"] in PEDIATRIC_OBESITY_IDS:
            exp["diagnosticCriteria"] = [
                "2세 이상 소아·청소년은 BMI를 성별·연령별 백분위수로 해석하며 85백분위수 이상 95백분위수 미만은 과체중, 95백분위수 이상은 비만이다.",
                "중증비만은 95백분위수의 120% 이상 또는 BMI 35 kg/m² 이상 가운데 더 낮은 기준으로 정의한다.",
            ]
            exp["treatmentGuideline"] = PEDIATRIC_OBESITY_GUIDE
            ensure_source(exp, label="AAP Clinical Practice Guideline for Childhood Obesity (2023)", url="https://publications.aap.org/pediatrics/article/151/2/e2022060640/190443/Clinical-Practice-Guideline-for-the-Evaluation-and")

        if DX_RE.search(stem):
            existing_criteria = list(exp.get("diagnosticCriteria") or [])
            criteria = existing_criteria if len(existing_criteria) >= 2 else dedupe(existing_criteria + diagnosis_candidates(exp), 4)
            if len(criteria) < 2:
                supplemental = dedupe(list(exp.get("reasoningSteps") or []) + list(exp.get("choiceExplanations") or []), 4)
                criteria = dedupe(criteria + supplemental, 4)
            if criteria:
                if criteria != exp.get("diagnosticCriteria"):
                    diagnosis_added += 1
                exp["diagnosticCriteria"] = criteria
            else:
                unresolved.append(f"{question['id']}: diagnosis criteria")
        if TX_RE.search(stem):
            guide = dedupe(list(exp.get("treatmentGuideline") or []) + treatment_candidates(question, exp), 4)
            if not guide:
                unresolved.append(f"{question['id']}: treatment guideline")
                continue
            if guide != exp.get("treatmentGuideline"):
                exp["treatmentGuideline"] = guide
                treatment_added += 1
            current_visual = exp.get("diagnosticVisual") or {}
            if len(current_visual.get("steps") or []) < 3 and len(guide) >= 3:
                url, label = source_meta(exp)
                exp["diagnosticVisual"] = {
                    "title": "진단·치료 흐름",
                    "summary": "문항에 연결된 교과서·공식 지침을 바탕으로 재구성한 자체 요약 흐름도입니다.",
                    "steps": guide,
                    "sourceUrl": url,
                    "sourceLabel": label,
                }
                visual_added += 1
    if unresolved:
        raise SystemExit("\n".join(unresolved))
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"GUIDELINE_SECTIONS_ENRICHED diagnosis={diagnosis_added} treatment={treatment_added} visuals={visual_added}")


if __name__ == "__main__":
    main()
