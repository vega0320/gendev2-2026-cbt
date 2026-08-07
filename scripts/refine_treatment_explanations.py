from __future__ import annotations

"""치료 문항의 증례 판단과 치료 알고리듬을 분리해 중복 표시를 없앤다."""

import json
import re
from difflib import SequenceMatcher
from pathlib import Path

from enrich_guideline_sections import TX_RE


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"
DATE = "2026-08-07"
STAGE_LABELS = ("초기 평가", "적응증 판단", "권고 처치", "추적·단계 상승")
PPH_ID = "gendev2-06-2023-q029"
OBESITY_IDS = {
    "gendev2-22-2025-q050", "gendev2-22-2023-q034", "gendev2-22-2022-q014",
    "gendev2-22-2021-q090", "gendev2-22-2020-q046",
}


def normalize(text: str) -> str:
    return re.sub(r"[^0-9A-Za-z가-힣]", "", text or "").lower()


def unique(items: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in items:
        item = re.sub(r"\s+", " ", item or "").strip()
        key = normalize(item)
        if len(key) < 12 or key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def clean_answer_language(text: str) -> str:
    """치료 지침에는 시험 정답 번호가 아니라 실제 임상 행동만 남긴다."""
    text = re.sub(r"\s*따라서\s*[①②③④⑤1-5][^.]*(?:정답이다|정답입니다)\.?", "", text or "")
    text = re.sub(r"\s*[①②③④⑤1-5][^.]*(?:가|이)\s*정답이다\.?", "", text)
    return re.sub(r"\s+", " ", text).strip()


def similar(left: str, right: str) -> bool:
    a, b = normalize(left), normalize(right)
    if not a or not b:
        return False
    return a in b or b in a or SequenceMatcher(None, a, b).ratio() >= 0.72


def choose(candidates: list[str], selected: list[str]) -> str:
    for candidate in unique([clean_answer_language(item) for item in candidates]):
        if len(candidate) >= 22 and not any(similar(candidate, prior) for prior in selected):
            return candidate
    raise ValueError("서로 다른 치료 단계 네 개를 구성할 근거가 부족함")


def detailed_guide(question: dict, exp: dict) -> list[str]:
    """역할이 다른 근거를 골라 '풀이 문장 네 개 복사'를 피한다."""
    reasoning = list(exp.get("reasoningSteps") or [])
    answers = [int(item) for item in question.get("answers") or []]
    choice_explanations = list(exp.get("choiceExplanations") or [])
    correct = [choice_explanations[index - 1] for index in answers if 0 < index <= len(choice_explanations)]
    criteria = list(exp.get("diagnosticCriteria") or []) + list(exp.get("numericReference") or [])
    selected: list[str] = []
    role_candidates = [
        [*(reasoning[:1]), exp.get("keyJudgment", "")],
        [*criteria, *(reasoning[1:2]), exp.get("keyJudgment", "")],
        [*correct, exp.get("keyJudgment", ""), *(reasoning[1:])],
        [exp.get("commonPitfall", ""), exp.get("conceptReview", ""), *reversed(reasoning), *(exp.get("treatmentGuideline") or [])],
    ]
    for candidates in role_candidates:
        selected.append(choose(candidates, selected))
    return [f"{label} — {text}" for label, text in zip(STAGE_LABELS, selected)]


def compact_flow(title: str, steps: list[str], source: dict) -> dict:
    return {
        "title": title,
        "summary": "공식 지침의 의사결정 순서를 짧게 재구성한 자체 흐름도입니다. 자세한 조건과 예외는 아래 치료 가이드라인에서 확인합니다.",
        "steps": steps,
        "sourceUrl": source.get("url", ""),
        "sourceLabel": source.get("label") or source.get("title") or "공식 지침",
    }


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    changed = 0
    flows = 0
    for question in payload["questions"]:
        if not TX_RE.search(question.get("stem", "")):
            continue
        exp = question.get("explanation") or {}
        guide = detailed_guide(question, exp)
        exp["treatmentGuideline"] = guide
        exp["treatmentReviewStatus"] = f"증례 판단·치료 알고리듬 분리 검수({DATE})"
        # 치료 문항은 같은 네 문장을 '한 단계씩 풀이'와 흐름도에 되풀이하지 않는다.
        exp["showReasoningWithTreatment"] = False
        exp.pop("diagnosticVisual", None)
        source = next((item for item in exp.get("sources") or [] if item.get("url")), {})
        if question["id"] == PPH_ID:
            exp["diagnosticVisual"] = compact_flow(
                "산후출혈 초기 대응 흐름",
                ["출혈량·활력징후 확인과 소생 시작", "MOTIVE bundle 동시 시행", "지속 출혈이면 풍선압박·수술적 지혈로 단계 상승"],
                source,
            )
            flows += 1
        elif question["id"] in OBESITY_IDS:
            exp["diagnosticVisual"] = compact_flow(
                "소아 비만 치료 흐름",
                ["연령·성별 BMI 백분위수 분류", "동반질환 평가와 가족 기반 집중 생활치료", "연령·중증도에 따라 약물·수술 평가"],
                source,
            )
            flows += 1
        changed += 1

    # 발견된 조산 예방 문항의 무관한 선지 해설도 같은 공식 지침에 맞춰 바로잡는다.
    by_id = {question["id"]: question for question in payload["questions"]}
    preterm = by_id["gendev2-02-2026-q952"]["explanation"]
    preterm["choiceExplanations"] = [
        "17-OHPC는 재발성 자연조산 예방 효과가 확인되지 않아 FDA 승인이 철회되었고 현재 권고하지 않는다.",
        "과거 자연조산력만 있고 현재 자궁목이 짧지 않다면 질 프로게스테론을 자동 투여하지 않고 연속 자궁목길이 감시 결과로 결정한다.",
        "이전 자연조산이 있는 단태임신은 임신 16~24주에 질초음파 자궁목길이를 연속 측정하고, 25 mm 이하로 짧아지면 프로게스테론 또는 원형결찰 적응증을 개별 평가한다.",
        "병력 적응 원형결찰은 반복된 무통성 중기 유산 등 자궁목무력증 병력이 뚜렷한 경우에 고려하며 모든 과거 조산 환자에게 시행하지 않는다.",
        "절대안정은 조산 예방 효과가 입증되지 않았고 감염이나 PPROM이 없는 무증상 환자에게 예방적 항생제를 투여하지 않는다.",
    ]
    preterm["treatmentGuideline"] = [
        "초기 평가 — 이전 분만이 자연조산이었는지, 현재 임신이 단태인지 확인하고 임신 16~24주에 질초음파 자궁목길이를 연속 측정한다.",
        "적응증 판단 — 현재 29 mm는 짧은 자궁목 기준인 25 mm 이하에 해당하지 않으므로 병력만으로 약물이나 원형결찰을 시작하지 않는다.",
        "권고 처치 — 현재는 연속 자궁목길이 감시를 지속한다. 17-OHPC는 권고하지 않으며 자궁목이 짧아질 때 질 프로게스테론 또는 원형결찰을 개별 논의한다.",
        "추적·단계 상승 — 자궁목이 25 mm 이하로 짧아지거나 개대가 확인되면 과거 조산 시기·자궁목무력증 병력과 함께 중재 적응증을 다시 평가한다.",
    ]
    preterm["sources"] = [item for item in preterm.get("sources") or [] if "Aortic Disease" not in item.get("label", "")]

    cfdna = by_id["gendev2-03-2026-q901"]["explanation"]
    cfdna["reasoningSteps"] = [
        "고위험 cfDNA 결과는 21번 삼염색체증 가능성을 높이는 선별 결과이지 태아의 핵형을 확정한 결과가 아니다.",
        "정상 초음파는 주요 구조 이상이 보이지 않는다는 뜻이며 양성 cfDNA 결과를 음성으로 바꾸지 않는다.",
        "임신 15주는 양수천자를 시행할 수 있는 시기이고, 융모막융모검사의 일반적인 10~13주 시기는 지났다.",
        "양수 세포의 염색체 진단검사로 결과를 확정한 뒤 유전상담을 거쳐 임신 관리 선택지를 논의한다.",
    ]
    cfdna["choiceExplanations"][1] = "임신 15주에는 양수천자로 태아 유래 세포를 얻어 핵형검사 또는 적절한 염색체 진단검사를 시행할 수 있으므로 이 증례의 확진 방법이다."
    cfdna["treatmentGuideline"] = [
        "초기 평가 — 검사실의 양성예측도와 검사 범위를 확인하고 고위험 cfDNA 결과가 확진이 아님을 설명한다. 정상 초음파만으로 21번 삼염색체증 위험이 배제되지는 않는다.",
        "적응증 판단 — 양성 선별 결과 뒤에는 유전상담, 상세 초음파와 침습적 진단검사를 제안한다. 검사 선택은 임신 주수, 태반 위치, 시술 위험과 환자 선호를 함께 반영한다.",
        "권고 처치 — 임신 15주에는 양수천자로 태아 유래 세포를 채취해 핵형검사 또는 적절한 염색체 진단검사를 시행한다. cfDNA 재검이나 정상 초음파로 확진을 대신하지 않는다.",
        "추적·단계 상승 — 진단검사 결과가 나온 뒤 유전상담으로 결과의 의미와 임신 지속·관리 선택지를 논의한다. 확진 전에는 선별 결과만으로 치료유산을 결정하지 않는다.",
    ]

    # 자동 생성 근거에 다른 산과 주제가 섞여 있던 네 문항은 현재 지침의 실제 의사결정 순서로 고정한다.
    pprom = by_id["gendev2-05-2026-practice-q001"]["explanation"]
    pprom["treatmentGuideline"] = [
        "초기 평가 — 멸균 질경검사로 양수 고임·누출을 확인하고 나이트라진·양치엽 검사로 보조한다. 태아심박, 진통, 임상적 융모양막염, 태반조기박리와 제대탈출을 함께 평가하며 손가락 질검사는 피한다.",
        "적응증 판단 — 32주 PPROM에서 산모와 태아가 안정되고 감염·태반조기박리·비안심 태아상태·진행 진통이 없으므로 즉시 유도분만보다 입원 기대요법이 적절하다.",
        "권고 처치 — 7일 안 조산 가능성이 높으므로 단회 산전 코르티코스테로이드를 투여하고, 임신을 연장하며 감염을 줄이기 위한 7일 잠복기 항생제와 GBS 검사·예방 계획을 병행한다.",
        "추적·단계 상승 — 체온·자궁압통·악취 분비물·백혈구와 태아심박을 반복 확인한다. 융모양막염, 태반조기박리, 비안심 태아상태 또는 분만 진행이 생기면 주수와 관계없이 분만하며, 안정 상태의 계획 분만 시점은 기관의 최신 PPROM 지침으로 정한다.",
    ]
    pprom.setdefault("sources", []).append({
        "label": "ACOG Practice Bulletin 217: Prelabor Rupture of Membranes (reaffirmed 2023)",
        "url": "https://www.acog.org/clinical/clinical-guidance/practice-bulletin/articles/2020/03/prelabor-rupture-of-membranes",
        "kind": "현재 지침",
    })

    augmentation = by_id["gendev2-04-2018-note-q049"]["explanation"]
    augmentation["treatmentGuideline"] = [
        "초기 평가 — 활성기 8 cm에서 2시간 변화가 없으면 양막 상태, 태아 위치·하강, 태아심박과 자궁수축 강도를 함께 확인한다. 150 MVU는 통상 충분한 수축으로 보는 200 MVU에 못 미친다.",
        "적응증 판단 — 활동기 정지는 양막파수 후 6 cm 이상에서 4시간의 충분한 수축 또는 옥시토신을 사용해도 6시간의 불충분한 수축 동안 경부 변화가 없을 때 진단한다. 이 증례는 아직 그 기준을 채우지 않는다.",
        "권고 처치 — 태아상태가 안심되고 질식분만 금기가 없다면 양막절개 여부를 확인하고 옥시토신으로 수축을 보강해 적절한 자궁활동과 경부 변화를 만든다.",
        "추적·단계 상승 — 옥시토신 중 태아심박과 수축 빈도를 계속 감시하고 빈수축이나 비안심 태아심박이 생기면 감량·중단한다. 충분히 보강한 뒤 활동기 정지 기준을 충족하면 제왕절개를 고려한다.",
    ]

    descent = by_id["gendev2-04-2017-note-q026"]["explanation"]
    descent["treatmentGuideline"] = [
        "초기 평가 — 완전개대 후 3시간 동안 station +1에서 하강이 없으면 실제 힘주기 시간, 수축 강도, 태아 머리 위치·회전, 골반 적합성과 태아심박을 다시 평가한다.",
        "적응증 판단 — 300 MVU의 충분한 수축에도 회전·하강이 전혀 없다는 소견은 단순 수축 부족보다 하강 정지나 아두골반불균형 가능성을 높인다. 분만 방식은 산모·태아 상태와 안전한 기구분만 가능성을 함께 판단한다.",
        "권고 처치 — +1 station에서 하강이 없고 안전한 질식 또는 기구분만 조건이 갖춰지지 않았다면 제왕절개로 분만한다. 진공·겸자는 숙련자가 태아 위치를 정확히 알고 충분히 낮은 선진부 등 안전 조건을 충족할 때만 선택한다.",
        "추적·단계 상승 — 수술 준비 중 태아심박을 계속 감시하고 감염·출혈 위험과 수액 상태를 교정한다. 태아곤란이 새로 생기면 지체하지 않고 응급 분만으로 전환한다.",
    ]

    abruption = by_id["gendev2-06-2017-note-q021"]["explanation"]
    abruption["treatmentGuideline"] = [
        "초기 평가 — 통증성 출혈과 지속 자궁긴장항진이면 태반조기박리를 의심하고 두 개의 큰 정맥로, 혈액검사·교차시험·응고검사와 태아심박 연속감시를 동시에 시작한다.",
        "적응증 판단 — 생존 태아에게 심한 지속 태아곤란이 있고 질식분만이 임박하지 않았으므로 임신 33주라는 이유로 기대관찰할 수 없다. 모체 저혈량과 응고장애도 즉시 교정한다.",
        "권고 처치 — 결정질액과 필요 시 혈액제제로 소생하면서 응급 제왕절개를 시행한다. 진단 확정을 위해 초음파 결과를 기다리거나 태아 폐성숙 스테로이드 완료를 기다리지 않는다.",
        "추적·단계 상승 — 출혈량, 소변량, 혈색소·혈소판·피브리노겐을 반복 평가하고 대량수혈 프로토콜을 준비한다. 태아가 사망했고 산모가 안정적이면 산모의 수술 출혈을 줄이기 위해 질식분만을 우선할 수 있다.",
    ]
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"TREATMENT_EXPLANATIONS_REFINED questions={changed} compactFlows={flows}")


if __name__ == "__main__":
    main()
