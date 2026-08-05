from __future__ import annotations

import json
from pathlib import Path

from apply_full_evidence_review import NUMERIC_DEFAULTS


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"

ACOG_CFDNA = {"kind": "현재 가이드라인", "label": "ACOG Screening for Fetal Chromosomal Abnormalities (2026)", "url": "https://www.acog.org/clinical/clinical-guidance/practice-advisory/articles/2026/01/screening-for-fetal-chromosomal-abnormalities"}
ACC_AORTA = {"kind": "현재 가이드라인", "label": "2022 ACC/AHA Aortic Disease Guideline", "url": "https://www.acc.org/latest-in-cardiology/ten-points-to-remember/2022/11/01/12/21/2022-guideline-on-aortic-disease-2-gl-ad"}
SMFM_FGR = {"kind": "현재 가이드라인", "label": "SMFM Consult #52: Fetal Growth Restriction", "url": "https://publications.smfm.org/publications/289-society-for-maternal-fetal-medicine-consult-series-52/"}
SMFM_TTTS = {"kind": "현재 가이드라인", "label": "SMFM Consult #72: Twin-Twin Transfusion Syndrome", "url": "https://publications.smfm.org/publications/574-society-for-maternal-fetal-medicine-consult-series-72/"}
SMFM_CERVIX = {"kind": "현재 가이드라인", "label": "SMFM Consult #70: Short Cervix", "url": "https://publications.smfm.org/publications/560-society-for-maternal-fetal-medicine-consult-series-70/"}
ACOG_CHAP = {"kind": "현재 가이드라인", "label": "ACOG CHAP Integration Guidance (reaffirmed 2025)", "url": "https://www.acog.org/clinical/clinical-guidance/practice-advisory/articles/2022/04/clinical-guidance-for-the-integration-of-the-findings-of-the-chronic-hypertension-and-pregnancy-chap-study"}
ACOG_FHR = {"kind": "현재 가이드라인", "label": "ACOG Intrapartum Fetal Heart Rate Monitoring (2025)", "url": "https://www.acog.org/clinical/clinical-guidance/clinical-practice-guideline/articles/2025/10/intrapartum-fetal-heart-rate-monitoring-interpretation-and-management"}
ACOG_EPL = {"kind": "현재 가이드라인", "label": "ACOG Early Pregnancy Loss", "url": "https://www.acog.org/clinical/clinical-guidance/practice-bulletin/articles/2018/11/early-pregnancy-loss"}


REVISIONS = {
    "gendev2-01-2026-q951": ("생리적 호흡성 알칼리증에서는 낮은 PaCO₂와 신장 보상으로 낮아진 HCO₃⁻가 함께 보여야 한다. pH만 보고 대사성 알칼리증으로 분류하면 안 된다.", "PaCO₂ 감소와 HCO₃⁻ 감소가 같은 방향으로 보이는 ‘보상된 호흡성 알칼리증’을 산-염기 순서대로 판독한다."),
    "gendev2-01-2026-q952": ("임신 2삼분기 Hb 10.6 g/dL은 빈혈 기준 바로 위이고 ferritin과 MCV도 철결핍을 지지하지 않는다. 피로만으로 철결핍빈혈이라 하지 않는다.", "Hb의 임신 삼분기 기준 → MCV → ferritin 순으로 해석해 생리적 혈액희석과 철결핍을 구분한다."),
    "gendev2-01-2026-q953": ("임신 중 신장 포도당 역치가 낮아져 정상 혈당에서도 glycosuria가 생길 수 있다. 그러나 소변당은 임신성당뇨 선별검사를 대신하지 않는다.", "소변당과 혈당을 분리하고, 무증상 생리 변화와 24–28주 정규 선별 시점을 함께 묻는다."),
    "gendev2-02-2026-q951": ("장기 미조절 임신전 당뇨의 높은 HbA1c는 기관형성기 기형 위험 신호다. 임신 확인 뒤 약만 바꾸는 것이 임신 전 상담의 대체가 아니다.", "현재 혈당 정상화와 동시에 망막·신장·갑상선 등 장기합병증, 엽산, 기형 선별 계획을 병렬로 세운다."),
    "gendev2-02-2026-q952": ("과거 자연조산이 있어도 현재 자궁목 29 mm는 짧은 자궁목 기준을 넘는다. 병력만으로 cerclage를 자동 시행하지 않는다.", "과거 조산력과 현재 질초음파 자궁목길이를 서로 다른 축으로 놓고 연속 감시와 중재 적응증을 구분한다."),
    "gendev2-02-2026-q953": ("Marfan에서 대동맥근부 4.7 cm는 임신 전 예방수술 권고선 4.5 cm를 넘는다. 임신 중 추적만 하자는 선택지는 위험을 과소평가한다.", "유전성 대동맥질환에서는 임신 전 지름 기준, 성장 속도, 가족력과 다학제 계획을 먼저 본다."),
    "gendev2-03-2026-q951": ("cfDNA는 가장 민감한 선별검사 중 하나지만 진단검사가 아니다. 초음파가 정상이어도 양성 선별 결과를 ‘정상’으로 덮지 않는다.", "선별 양성 → 유전상담·정밀초음파 → 임신주수에 맞는 CVS/양수검사 제안 순서를 적용한다."),
    "gendev2-03-2026-q952": ("BPP 4점은 36주에서 관찰만 하기 어려운 비정상 결과다. NST 하나가 아니라 총점, 양수와 임신주수를 합쳐 분만 필요성을 판단한다.", "각 BPP 항목의 0/2점을 합산한 뒤 4점 이하 비정상이라는 분류와 만삭 근접 임신주수를 결합한다."),
    "gendev2-03-2026-q953": ("REDV는 단순 ‘작은 태아’가 아니라 태반 저항이 심하게 증가한 고위험 도플러 소견이다. 외래 주 1회 추적은 부족하다.", "severe FGR과 REDV를 확인하면 입원·스테로이드·빈번한 CTG, 32주 미만이면 MgSO₄, 30–32주 분만 계획을 한 묶음으로 판단한다."),
    "gendev2-04-2026-q951": ("10분 6회 수축과 후기감속이면 원인인 옥시토신을 중단하고 자궁수축을 줄이며 체위·수액 등 자궁내 소생술을 동시에 한다.", "복수정답에서 각 조치가 ‘원인 제거·관류 개선·수축 완화’에 실제로 기여하는지 따로 확인한다."),
    "gendev2-04-2026-q952": ("기저선 서맥, 변이도 소실, 반복 감속은 Category III 조합이다. 초기 소생술에도 지속되면 원인교정과 신속 분만 준비를 병행한다.", "Category III의 정의를 먼저 충족하는지 본 뒤 ‘지속성’과 ‘소생술 불응’을 분만 결정에 연결한다."),
    "gendev2-04-2026-q953": ("6 cm는 활동기 시작점이고 230 MVU는 충분한 수축이다. 4시간 동안 개대가 멈췄다면 활동기 정지 기준을 만족한다.", "자궁목 6 cm 이상, 양막파수, 수축의 충분성, 정지 시간을 네 칸 체크해 진단한다."),
    "gendev2-05-2026-q951": ("32주 PPROM이지만 감염·태아곤란·진통이 없다. 즉시 분만이 아니라 입원, 항생제, 스테로이드와 감시가 기본이다.", "PPROM에서는 임신주수보다 먼저 융모양막염·태반조기박리·태아상태 이상이라는 즉시분만 예외를 찾는다."),
    "gendev2-05-2026-q952": ("조산력 없는 단태임신 21주, 자궁목 18 mm는 질 프로게스테론 권고 대상이다. 개대가 없는데 cerclage를 먼저 고르지 않는다.", "조산력 유무 → 단태/다태 → 24주 전 TVUS 길이 → 실제 개대 순서로 중재를 고른다."),
    "gendev2-05-2026-q953": ("19주 무통성 개대와 양막 돌출은 고전적 자궁목무력증 병력이다. 현재 임신에서는 병력기반 cerclage를 12–14주 무렵 고려한다.", "이전 손실의 임신주수뿐 아니라 ‘진통 없이 개대’라는 기전을 읽어 일반 조산 예방과 구분한다."),
    "gendev2-06-2026-q951": ("무통성 선홍색 출혈과 전치태반 위험인자가 있으면 디지털 내진 전에 초음파로 태반 위치를 확인한다.", "출혈량이 적고 활력이 안정적이어도 전치태반이 배제되기 전 손가락 내진은 대량출혈을 유발할 수 있음을 우선한다."),
    "gendev2-06-2026-q952": ("통증·지속적 자궁압통·긴장항진·태아서맥은 태반조기박리와 급성 태아위험을 시사한다. 초음파 음성이어도 배제되지 않는다.", "산모 소생을 시작하면서 생존 태아의 지속 서맥이면 응급분만 준비를 지연하지 않는다."),
    "gendev2-06-2026-q953": ("태반이 완전하고 자궁이 물렁하면 4T 중 Tone, 즉 자궁무력증이 우선이다. 천식에서는 carboprost를 피하고 다른 자궁수축제를 고른다.", "출혈량·쇼크를 동시에 소생하면서 Tone-Trauma-Tissue-Thrombin을 빠르게 확인하고 금기를 대조한다."),
    "gendev2-07-2026-q951": ("단백뇨가 없어도 혈소판 92,000/µL는 중증소견이다. 고혈압 뒤 장기기능 이상이 있으면 자간전증 진단이 가능하다.", "단백뇨를 필수조건으로 오인하지 말고 혈소판·신장·간·폐·신경 증상을 각각 확인한다."),
    "gendev2-07-2026-q952": ("CHAP 이후 만성고혈압 임신의 약물 시작/증량 기준은 140/90 mmHg로 낮아졌다. 예전 160/110까지 기다리는 기준과 혼동하지 않는다.", "만성고혈압의 치료 시작선과 급성 중증고혈압의 응급치료선을 별개 숫자로 기억한다."),
    "gendev2-07-2026-q953": ("산후에도 자간은 발생한다. 발작 중 기도·안전을 확보하고 magnesium sulfate로 재발을 막으며 중증 혈압도 신속히 치료한다.", "발작 중 즉시 조치와 발작 후 혈압·원인 평가를 시간순으로 나눠 고른다."),
    "gendev2-08-2026-q951": ("MCDA에서 수혜아 다한수, 공여아 양수과소와 방광 미관찰이면 Quintero stage II 이상이다. 23주는 태아경 레이저 적응 시기다.", "양수 기준 → 공여아 방광 → 도플러 → 수종 순서로 stage를 올리고 16–26주 치료 기준에 연결한다."),
    "gendev2-08-2026-q952": ("25주 EFW 2백분위수는 조기 severe FGR이다. 정상 도플러라도 정밀 구조평가와 유전진단 제안을 생략하지 않는다.", "‘도플러 정상’은 태반 기능이 현재 보존됐다는 뜻이지 조기 severe FGR의 원인평가가 끝났다는 뜻이 아니다."),
    "gendev2-08-2026-q953": ("REDV 자체도 고위험인데 반복 prolonged deceleration까지 생기면 스테로이드 완료를 기다리는 이득보다 저산소 위험이 크다.", "권장 분만 주수는 태아감시가 안정적일 때의 목표다. 비안심 CTG는 더 빠른 분만을 정당화한다."),
    "gendev2-09-2026-q951": ("제왕절개·양막파수 뒤 발열, 자궁압통, 악취 오로는 산후 자궁내막염의 전형적 묶음이다. 배양 결과를 기다리지 않고 광범위 정주항생제를 시작한다.", "발열 원인을 유방·요로·상처·혈전과 비교하되 자궁 국소 소견과 산과 위험인자를 가장 무겁게 본다."),
    "gendev2-09-2026-q952": ("산후 2주는 혈전위험이 높고 수유 확립기다. estrogen 포함 복합호르몬피임은 피하고 progestin 단독·장벽법·IUD를 상황에 맞춰 고른다.", "피임 효과만 보지 말고 산후 경과주수, 수유, 정맥혈전색전증 위험을 동시에 확인한다."),
    "gendev2-09-2026-q953": ("국소 발적·통증·발열이 있고 농양은 없으므로 유선염이 우선이다. 모유 배출을 지속하고 적절한 항생제를 쓰며 24–48시간 반응을 본다.", "모유수유 중단은 울혈을 악화시킬 수 있다. 파동성 종괴나 치료 불응이면 초음파로 농양을 찾는다."),
    "gendev2-10-2026-q951": ("CRL 7.4 mm에서 심박동이 없으면 보수적 확정 기준을 충족한다. 다만 측정 오차와 환자 선호를 설명한 뒤 기대·약물·수술 중 선택한다.", "불확실한 생존성과 확정된 임신실패를 CRL/MSD 절단값으로 구분하고 성급한 처치를 피한다."),
    "gendev2-10-2026-q952": ("PUL에서 48시간 hCG 상승이 느리다는 이유만으로 자궁외임신을 확진하지 않는다. 안정하면 연속 hCG와 반복 TVUS로 위치와 생존성을 추적한다.", "단일 hCG와 discriminatory zone을 치료 적응증으로 쓰지 말고 파열 경고증상과 추적 가능성을 함께 본다."),
    "gendev2-10-2026-q953": ("저혈압·빈맥·복강내 액체·빈 자궁은 파열 자궁외임신의 출혈성 쇼크다. hCG 재검이나 MTX가 아니라 소생과 응급수술이 우선이다.", "불안정성을 먼저 판정한 뒤 안정 환자용 진단·약물 알고리듬을 즉시 배제한다."),
}


LECTURE_SOURCES = {
    "02": [ACC_AORTA], "03": [ACOG_CFDNA, SMFM_FGR], "04": [ACOG_FHR],
    "05": [SMFM_CERVIX], "07": [ACOG_CHAP], "08": [SMFM_TTTS, SMFM_FGR], "10": [ACOG_EPL],
}


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    revised = 0
    for question in payload["questions"]:
        revision = REVISIONS.get(question["id"])
        if not revision:
            continue
        pitfall, decision_check = revision
        exp = question["explanation"]
        exp["commonPitfall"] = pitfall
        base_steps = [step for step in exp.get("reasoningSteps", []) if not step.startswith("최종 재확인:")]
        exp["reasoningSteps"] = base_steps + [f"최종 재확인: {decision_check}"]
        base_review = exp.get("conceptReview", "").split(" 재출제 포인트:", 1)[0].rstrip()
        exp["conceptReview"] = base_review + f" 재출제 포인트: {decision_check}"
        exp["numericReference"] = NUMERIC_DEFAULTS[question["lectureNumber"]]
        exp["evidenceStatus"] = "강의 case·과거 반복개념을 반영해 고난도 예상문제로 재검수(2026-08-05); 교과서와 현재 공식 지침 분리 확인"
        existing_urls = {source.get("url") for source in exp.get("sources", [])}
        for source in LECTURE_SOURCES.get(question["lectureNumber"], []):
            if source["url"] not in existing_urls:
                exp.setdefault("sources", []).append(source)
        question["examStatus"] = "2026 예상문제 · 실제 출제 아님"
        question["predictionBasis"] = "2026 강의 case·강조점과 과거 유사문항을 변형한 고난도 연습문제"
        question["difficulty"] = "고난도"
        question["predictionReviewDate"] = "2026-08-05"
        revised += 1
    if revised != 30:
        raise SystemExit(f"expected 30 predicted revisions, got {revised}")
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PREDICTED_QUALITY_REVISION_APPLIED revised={revised}")


if __name__ == "__main__":
    main()
