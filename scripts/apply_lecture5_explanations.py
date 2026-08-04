from __future__ import annotations

import json
from pathlib import Path

from apply_early_lecture_explanations import explanation

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"

SOURCES = {
    "w45": {"label": "Williams Obstetrics 26e, Ch. 45 Preterm Birth", "url": "https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=263821201", "kind": "교과서"},
    "acog_ptl": {"label": "ACOG: Preterm Labor and Birth", "url": "https://www.acog.org/womens-health/faqs/preterm-labor-and-birth", "kind": "현재 지침"},
    "acog_prom": {"label": "ACOG Practice Bulletin 217: Prelabor Rupture of Membranes", "url": "https://www.acog.org/clinical/clinical-guidance/practice-bulletin/articles/2020/03/prelabor-rupture-of-membranes", "kind": "현재 지침"},
    "acog_steroid": {"label": "ACOG: Antenatal Corticosteroid Therapy for Fetal Maturation", "url": "https://www.acog.org/clinical/clinical-guidance/committee-opinion/articles/2017/08/antenatal-corticosteroid-therapy-for-fetal-maturation", "kind": "현재 지침"},
    "smfm_cervix": {"label": "SMFM Consult Series 70: Management of Short Cervix", "url": "https://publications.smfm.org/publications/560-society-for-maternal-fetal-medicine-consult-series-70/", "kind": "현재 지침"},
}


def make(concept, judgment, steps, choices, review, source_ids, status="Williams 26e·ACOG/SMFM 공식지침 대조 · 2026-08"):
    value = explanation(concept, judgment, steps, choices, review, [])
    value["sources"] = [SOURCES[source_id] for source_id in source_ids]
    value["evidenceStatus"] = status
    return value


EXPLANATIONS = {
    "gendev2-05-2025-q001": make(
        "32주 조기양막파수의 태아 폐성숙",
        "32주에 물 같은 분비물과 양성 nitrazine 검사는 조기양막파수(PPROM)를 시사한다. 감염·태아곤란·진행 진통이 없다면 임신 연장을 시도하면서 7일 이내 조산 위험에 대비해 antenatal corticosteroid를 투여하므로 ③이다.",
        ["PPROM을 확인하고 융모양막염·태반조기박리·태아곤란을 먼저 배제한다.", "24–33+6주에 7일 내 출산 위험이 있으면 단회 스테로이드 과정을 시행한다.", "PPROM에서는 잠복기 항생제와 GBS 평가도 함께 고려하며 감염 소견이 생기면 분만한다."],
        ["32주 PPROM을 단순 관찰만 해서는 감염 예방과 태아 폐성숙 기회를 놓친다.", "감염·태아곤란 없는 32주 PPROM에서 즉시 옥시토신 유도분만이 기본은 아니다.", "정답. Betamethasone 또는 dexamethasone은 RDS, IVH 등 조산 합병증을 줄인다.", "양수주입은 산전 PPROM의 양수량을 보충하는 표준 치료가 아니다.", "32주 파수 뒤 cerclage를 새로 시행하면 감염·손상 위험이 있어 적응이 아니다."],
        "PPROM은 파수 확인 뒤 임신주수와 감염 여부로 갈린다. 34주 미만의 안정 환자는 기대요법, 스테로이드, 잠복기 항생제가 중심이며 MgSO4 신경보호는 보통 32주 미만의 임박한 분만에서 고려한다.", ["w45", "acog_prom", "acog_steroid"]),
    "gendev2-05-2025-q002": make(
        "병력 적응증 자궁목원형묶음술",
        "과거 19주에 통증 없이 자궁목이 열려 유산한 병력은 전형적인 자궁목무력증이다. 현재 13주이므로 병력 적응증 예방적 cerclage를 시행하는 ⑤가 맞다.",
        ["중기 무통성 개대·유산 병력을 확인한다.", "현재 감염·출혈·진통·파수가 없는지 확인한다.", "병력 적응증 cerclage는 보통 임신 초기 말에 계획한다."],
        ["반복 중기 손실의 강한 병력이 있어 관찰만 하기 어렵다.", "감염 증거가 없으므로 예방적 항생제만으로 자궁목의 구조적 문제를 해결할 수 없다.", "스테로이드는 임박한 조산 때 태아 성숙을 위한 약이지 13주 재발 예방 치료가 아니다.", "자궁수축이 없는 13주에 tocolytic을 예방적으로 쓰지 않는다.", "정답. 과거 무통성 중기 개대·유산은 history-indicated cerclage에 부합한다."],
        "짧은 자궁목 치료는 병력에 따라 달라진다. 조산 병력 없는 단태아의 무증상 짧은 자궁목은 질 progesterone이 우선이며, 단순 길이 감소만으로 cerclage를 일률적으로 하지 않는다.", ["w45", "smfm_cervix"]),
    "gendev2-05-2023-q014": make(
        "30주 조기진통의 단기 자궁수축 억제",
        "30주에 규칙적 수축과 3 cm 개대가 있어 조기진통이다. 스테로이드 투여·전원 시간을 확보하기 위한 단기 tocolysis가 필요하므로 출제 당시 약제인 ritodrine ④가 정답이다.",
        ["수축만이 아니라 자궁목 변화를 확인해 조기진통을 진단한다.", "24–34주에서는 금기가 없으면 약 48시간 분만을 지연해 스테로이드 효과를 확보한다.", "32주 미만 임박 분만이면 MgSO4 신경보호도 평가한다."],
        ["3 cm 개대와 규칙적 수축이 있어 단순 관찰 대상이 아니다.", "Progesterone은 주로 짧은 자궁목의 예방에 쓰며 진행 중인 조기진통 치료가 아니다.", "Oxytocin은 진통을 강화하므로 반대다.", "정답. Ritodrine은 β2 작용 tocolytic이다. 다만 빈맥·고혈당·폐부종 등 부작용 때문에 현재는 nifedipine/indomethacin 등을 더 흔히 사용한다.", "활동성 수축과 개대가 있는 30주에는 응급 cerclage가 적절하지 않다."],
        "Tocolytic은 조산을 장기간 예방하는 약이 아니라 보통 48시간을 벌기 위한 치료다. 융모양막염, 심한 출혈, 태아곤란 등 분만이 더 안전한 상황에서는 사용하지 않는다.", ["w45", "acog_ptl"], "족보 약제 정답과 현재 선호 약제 차이 표시 · 2026-08"),
    "gendev2-05-2023-q050": make(
        "33주 PPROM의 잠복기 항생제",
        "33주 PPROM이지만 진통·감염·태아곤란이 없다. 34주 미만 기대요법에서 잠복기 항생제는 감염을 줄이고 임신기간을 연장하므로 ①이 맞다.",
        ["파수를 확인하고 감염·태아상태를 평가한다.", "34주 미만 안정 PPROM은 입원 기대요법과 latency antibiotics를 시행한다.", "스테로이드도 병행하고 분만 임박 여부에 따라 추가 처치를 결정한다."],
        ["정답. 잠복기 항생제는 PPROM에서 분만까지 시간을 늘리고 감염성 합병증을 줄인다.", "33주 안정 PPROM에서 즉시 유도분만이 유일한 기본 처치는 아니다.", "PPROM에서 tocolysis는 일률적으로 사용하지 않으며 감염이 있으면 금기다.", "MgSO4 신경보호는 일반적으로 32주 미만 임박 분만에서 고려하므로 33주 무진통 상황과 맞지 않는다.", "태아가 안정된 두위이고 응급 적응증이 없어 제왕절개가 필요하지 않다."],
        "PPROM의 세 축은 감염 감시, 태아 성숙, 분만 시점이다. 발열·자궁압통·악취성 분비물·태아빈맥 등 융모양막염 소견이 있으면 임신주수와 무관하게 분만을 고려한다.", ["w45", "acog_prom"]),
    "gendev2-05-2022-q036": make(
        "자궁목 변화 없는 불규칙 수축",
        "34+4주 불규칙 수축이 있으나 자궁목은 닫혀 있고 길이 3.0 cm로 변화가 없다. 조기진통이 성립하지 않으므로 경과관찰 ④가 적절하다.",
        ["수축 빈도보다 자궁목의 진행성 개대·소실 여부를 본다.", "태아상태와 파수 여부가 정상임을 확인한다.", "변화가 없으면 불필요한 tocolytic·cerclage를 피하고 재평가한다."],
        ["Progesterone은 이 시점의 일시적 수축을 즉시 치료하는 약이 아니다.", "자궁목 변화 없는 수축에는 ritodrine을 투여하지 않는다.", "34주 이후 닫힌 정상 길이 자궁목에 cerclage를 하지 않는다.", "정답. 현재는 threatened preterm labor보다 생리적 수축 가능성이 높아 관찰한다.", "7일 내 출산 위험이 뚜렷하지 않아 스테로이드를 자동 투여하지 않는다."],
        "조기진통은 규칙적 수축과 자궁목 변화의 조합이다. 증상만 있고 자궁목 변화가 없으면 과치료를 피하되 증상 지속 시 반복 평가한다.", ["w45", "acog_ptl"]),
    "gendev2-05-2022-q064": make(
        "31주 진행성 조기진통",
        "31주에 규칙적 수축과 1시간 사이 1→2 cm 진행성 개대가 있어 조기진통이다. 금기가 없다면 스테로이드 효과와 전원 시간을 확보하기 위한 단기 자궁수축억제 ③이 적절하다.",
        ["진행성 자궁목 변화로 조기진통을 확정한다.", "감염·출혈·태아곤란 등 tocolysis 금기를 배제한다.", "단기 tocolysis와 스테로이드, 32주 미만 MgSO4 신경보호를 함께 검토한다."],
        ["진행성 개대가 있어 관찰만 하기 어렵다.", "양막파수나 감염 증거가 없는 intact-membrane 조기진통에 항생제를 일률적으로 쓰지 않는다.", "정답. 단기 tocolysis로 태아 성숙 치료 시간을 번다.", "규칙적 수축 중 bulging membrane에 응급 cerclage를 하면 파수·감염 위험이 크다.", "태아상태가 정상이고 단지 31주 조기진통이라는 이유만으로 즉시 제왕절개하지 않는다."],
        "분만 지연 자체가 최종 목표가 아니다. 스테로이드, MgSO4, 적절한 NICU로 전원할 시간을 확보하는 것이 목적이다.", ["w45", "acog_ptl"]),
    "gendev2-05-2021-q085": make(
        "28주 조기진통의 초기 관리",
        "28주에 규칙적 통증과 자궁목 소실·개대가 있어 조기진통이다. 양막이 보존되고 태아상태가 안정적이므로 단기 자궁수축억제제 ③이 맞다.",
        ["수축과 자궁목 변화로 조기진통을 확인한다.", "분만을 지연하면 이득이 있는 28주이므로 금기를 확인한 뒤 tocolysis를 고려한다.", "스테로이드와 MgSO4 신경보호를 함께 준비한다."],
        ["양막이 보존되고 감염 소견이 없어 항생제 단독 치료가 아니다.", "Oxytocin은 수축을 강화한다.", "정답. Tocolytic은 태아 성숙 치료를 위한 짧은 시간을 확보한다.", "활동성 진통 중 응급 cerclage는 적절하지 않다.", "태아가 둔위라도 28주 안정 조기진통 단계에서 곧바로 응급 제왕절개하지 않는다."],
        "태위는 실제 분만 방식 판단에 중요하지만, 조기진통의 첫 단계에서는 태아상태와 분만 임박성, 임신 연장의 이득을 먼저 평가한다.", ["w45", "acog_ptl"]),
    "gendev2-05-2021-q086": make(
        "33주 PPROM 진행 진통과 스테로이드",
        "33주 PPROM에 7 cm 개대로 분만이 임박했다. Tocolysis로 억지로 막기보다 출산을 준비하면서 아직 투여하지 않았다면 corticosteroid ③을 가능한 한 신속히 투여한다.",
        ["파수와 진행성 진통을 확인한다.", "7 cm 개대는 분만을 멈추기 어려운 단계이므로 안전한 분만을 준비한다.", "스테로이드는 완전 과정 전이라도 일부 이득이 있을 수 있어 투여를 시작한다."],
        ["Progesterone은 조산 예방 약으로 진행성 진통 치료가 아니다.", "Prostaglandin은 자궁목 숙성과 유도분만에 사용해 수축을 강화한다.", "정답. 33주 임박 분만에서 antenatal corticosteroid를 투여한다.", "7 cm 진행 진통과 PPROM에서는 ritodrine으로 분만을 억제하지 않는다.", "Ergonovine은 산후 자궁무력 출혈 치료 약으로 분만 전 사용하지 않는다."],
        "스테로이드 이득을 기다린다는 이유로 의학적으로 필요한 분만을 지연하지 않는다. 32주 미만이었다면 MgSO4 신경보호도 함께 고려한다.", ["w45", "acog_ptl", "acog_steroid"]),
    "gendev2-05-2020-q011": make(
        "30주 PPROM 치료 근거",
        "30주 PPROM에서 무작위시험의 잠복기 항생제는 임신기간과 일부 신생아 이환을 개선하지만 생존율 차이는 명확하지 않았다. 따라서 ②가 옳다.",
        ["각 선택지가 임신 연장, 감염, 신생아 결과 중 무엇을 말하는지 나눈다.", "근거가 있는 처치는 잠복기 항생제와 단회 스테로이드다.", "침상안정·반복 스테로이드·산전 양수주입을 일률적 표준으로 보지 않는다."],
        ["침상안정과 수액이 조기진통을 예방한다는 근거는 부족하고 혈전 등 위해가 있다.", "정답. 항생제는 latency를 늘렸지만 모든 연구에서 신생아 생존율을 높인 것은 아니다.", "심한 양수과소 자체만으로 산전 양수주입을 표준 시행하지 않는다.", "PPROM은 다균성 상행감염과 관련되므로 Ureaplasma 하나만을 주원인으로 단정한 설명은 틀리다.", "정기적 반복 과정은 권하지 않는다. 다만 현재는 34주 미만, 7일 내 출산 위험, 첫 과정 후 14일 초과 등 선택 조건에서 단회 rescue course를 고려할 수 있다."],
        "교과서 이후 가장 중요한 변화는 반복 스테로이드를 무조건 금지하거나 무조건 투여하지 않고, 엄격한 조건에서 단 한 차례 재투여를 고려한다는 점이다.", ["w45", "acog_prom", "acog_steroid"]),
    "gendev2-05-2020-q012": make(
        "조산 위험 예측과 예방의 한계",
        "족보 정답은 ②(가·나·마)다. 핵심은 fetal fibronectin 양성이 조산 위험을 높이고, bacterial vaginosis 치료가 모든 조산을 예방하지는 않는다는 점이다. 다만 ‘항생제가 금기’라는 가 문장은 현재 기준에서는 지나치게 강한 표현이다.",
        ["fetal fibronectin은 특히 음성일 때 단기간 조산 가능성이 낮다는 점이 유용하다.", "Cerclage는 병력·자궁목 개대 등 선택된 환자에서만 효과가 있다.", "Tocolytic은 장기 조산 예방이 아니라 약 48시간 지연 목적이다.", "족보 조합과 현재 표현 차이를 분리한다."],
        ["족보가 채택한 조합이지만, 가의 ‘금기’는 부정확하다. intact-membrane 조기진통에서 조산 예방만을 위한 routine antibiotics를 권하지 않는다는 뜻으로 읽어야 한다.", "족보 정답 조합. 가의 표현 주의와 함께 나·마를 포함한다.", "다는 모든 짧은 자궁목에 cerclage가 효과적이라는 식으로 일반화해 부적절하다.", "Ritodrine은 일시적으로 분만을 지연할 수 있으나 조산을 장기적으로 의미 있게 예방하지 못한다.", "나와 마는 현재도 타당하지만, 원본 정답은 ⑤가 아니라 가를 포함한 ②로 기록돼 있다."],
        "현재 조산 예방은 병력과 자궁목 길이에 따라 질 progesterone 또는 cerclage를 선택한다. 무증상 저위험 짧은 자궁목에 cerclage를 일률 적용하지 않으며, 항생제도 감염 적응증 없이 예방 목적으로 쓰지 않는다.", ["w45", "acog_ptl", "smfm_cervix"], "족보 정답 유지 / 가 선지의 ‘금기’ 표현은 현재 지침상 과도함 · 2026-08"),
}


def main():
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    by_id = {question["id"]: question for question in payload["questions"]}
    missing = sorted(set(EXPLANATIONS) - set(by_id))
    if missing:
        raise SystemExit(f"문항 ID 없음: {missing}")
    for qid, value in EXPLANATIONS.items():
        by_id[qid]["explanation"] = value
        by_id[qid]["explanationReviewStatus"] = value["evidenceStatus"]
    by_id["gendev2-05-2023-q014"]["answerReviewStatus"] = "족보 약제: ritodrine · 현재 선호 약제와 차이"
    by_id["gendev2-05-2020-q012"]["answerReviewStatus"] = "가 선지 ‘항생제 금기’ 표현 검수 필요"
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"LECTURE5_EXPLANATIONS_APPLIED count={len(EXPLANATIONS)}")


if __name__ == "__main__":
    main()
