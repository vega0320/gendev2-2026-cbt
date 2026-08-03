from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "questions.json"
OUTPUT = ROOT / "site" / "data" / "questions.json"


PILOT_EXPLANATIONS = {
    "gendev2-01-2025-q051": {
        "conceptGroup": "임신 중 철 대사",
        "keyJudgment": "문제는 보충제로 먹는 용량이 아니라 임신 중반 이후 몸이 실제로 흡수해 써야 하는 철 요구량을 묻는다. 정답은 6–7 mg/일이다.",
        "reasoningSteps": [
            "정상 임신 전체에 약 1,000 mg의 추가 철이 필요하다.",
            "철 사용은 임신 후반부에 집중되므로 중반 이후 실제 요구량이 평균 6–7 mg/일까지 오른다.",
            "장 흡수가 제한되므로 먹는 원소철 권장량은 실제 흡수 요구량보다 크다. 두 숫자를 구분한다.",
        ],
        "choiceExplanations": [
            "너무 적다. 임신 초기의 낮은 요구량과 혼동하기 쉽다.",
            "임신 중반 이후의 평균 실제 요구량에 못 미친다.",
            "정답. Williams 26판은 임신 중반 이후 평균 요구량을 6–7 mg/일로 설명한다.",
            "평균값보다 높다. 특정 철 결핍 치료 용량을 묻는 문제가 아니다.",
            "평균 생리적 요구량보다 높다.",
        ],
        "conceptReview": "약 1,000 mg 중 태아·태반 약 300 mg, 정상 배설 약 200 mg, 모체 적혈구량 증가 약 500 mg이 필요하다. ACOG의 임신 영양 기준 27 mg/일이나 WHO 예방 보충 30–60 mg/일은 먹는 원소철 용량이고, 문제의 6–7 mg/일은 몸이 실제로 필요로 하는 양이다.",
        "evidenceStatus": "교과서·현재 공식 지침 확인",
        "sources": [
            {"label": "Williams Obstetrics 26e, Ch. 4", "url": "https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=254987027", "kind": "교과서"},
            {"label": "WHO: Daily iron and folic acid supplementation (2024 확인)", "url": "https://www.who.int/tools/elena/interventions/daily-iron-pregnancy", "kind": "현재 지침"},
            {"label": "ACOG: Healthy Eating During Pregnancy", "url": "https://www.acog.org/womens-health/faqs/healthy-eating-during-pregnancy", "kind": "현재 안내"},
        ],
    },
    "gendev2-01-2025-q052": {
        "conceptGroup": "임신 중 갑상샘 생리",
        "keyJudgment": "hCG는 TSH 수용체를 약하게 자극해 유리 T4를 올리고, 음성 되먹임으로 뇌하수체 TSH를 낮춘다.",
        "reasoningSteps": [
            "임신 초기에 크게 증가하는 태반 호르몬을 찾는다.",
            "hCG와 TSH는 당단백 호르몬으로 구조가 일부 비슷하다.",
            "hCG의 갑상샘 자극 → 유리 T4 증가 → 뇌하수체 TSH 억제 순서로 판단한다.",
        ],
        "choiceExplanations": [
            "ADH는 수분 균형을 조절하며 이 문제의 생리적 TSH 저하 원인이 아니다.",
            "정답. 높은 hCG가 갑상샘을 약하게 자극하고 그 결과 TSH가 낮아진다.",
            "옥시토신은 분만과 수유에 중요하지만 정상 임신 초기 TSH 저하의 주된 설명이 아니다.",
            "프로락틴은 유방 발달과 수유에 관여하며 정답 기전이 아니다.",
            "태반 성장호르몬은 모체 대사를 조절하지만 TSH 억제의 대표 기전은 아니다.",
        ],
        "conceptReview": "임신 초기 hCG가 최고일 때 TSH가 약간 낮아질 수 있다. 정상 생리 변화이므로 비임신 참고범위만으로 갑상샘항진증을 진단하지 않고 임신 주수별 범위와 임상 소견을 함께 본다.",
        "evidenceStatus": "교과서·2026 ATA 지침 존재 확인",
        "sources": [
            {"label": "Williams Obstetrics 26e, Ch. 4", "url": "https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=254987027", "kind": "교과서"},
            {"label": "American Thyroid Association: 2026 pregnancy guideline", "url": "https://www.thyroid.org/new-ata-guidelines-for-thyroid-disease-in-preconception-pregnancy-and-postpartum/", "kind": "현재 지침"},
        ],
    },
    "gendev2-01-2023-q053": {
        "conceptGroup": "임신 중 철 대사",
        "keyJudgment": "태아와 태반으로 이동하는 철은 약 300 mg이므로 ①이 맞다.",
        "reasoningSteps": [
            "각 선지를 정상 임신의 방향성 변화와 비교한다.",
            "철 배분 수치 300 mg은 태아·태반 몫과 일치한다.",
            "요당, 심박수, 콜레스테롤은 한 단어의 방향이 뒤집힌 오답이다.",
        ],
        "choiceExplanations": [
            "정답. 임신 전체 추가 철 약 1,000 mg 중 약 300 mg이 태아와 태반으로 전달된다.",
            "예방 보충은 현재 지침상 가능한 한 이르게 시작할 수 있지만, 이 선지는 원 족보의 단정적 표현과 교과서 문맥이 불명확해 검수 필요다. 정답 근거는 ①에서 명확하다.",
            "임신에서는 사구체여과율 증가와 신장 포도당 역치 변화로 요당이 나타날 수 있어 요당만으로 당뇨를 진단하지 않는다.",
            "정상 임신에서 심박수는 대체로 증가한다.",
            "정상 임신에서는 총콜레스테롤과 중성지방이 대체로 증가한다.",
        ],
        "conceptReview": "정상 임신은 혈장량과 심박출량이 증가하고, 생리적 고지혈증과 때때로 요당이 나타난다. 검사 한 가지를 비임신 기준으로 해석하지 않는다.",
        "evidenceStatus": "교과서 확인·② 선지 표현 검수 필요",
        "sources": [
            {"label": "Williams Obstetrics 26e, Ch. 4", "url": "https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=254987027", "kind": "교과서"},
            {"label": "WHO: Daily iron and folic acid supplementation", "url": "https://www.who.int/tools/elena/interventions/daily-iron-pregnancy", "kind": "현재 지침"},
        ],
    },
}


CONCEPT_KEYWORDS = (
    (("cfDNA", "NIPT", "태아 DNA", "삼염색체", "다운증후군"), "산전 염색체 선별·진단"),
    (("양수지수", "양수과소", "양수과다"), "양수량 평가"),
    (("탯줄동맥", "도플러", "태아성장제한", "예상태아체중"), "태아성장제한 감시"),
    (("비수축검사", "NST", "태동"), "태아 안녕평가"),
    (("자간전증", "전자간증", "고혈압", "단백뇨"), "임신성 고혈압질환"),
    (("조산", "자궁수축", "자궁경부길이"), "조산의 진단과 처치"),
    (("전치태반", "태반조기박리", "산후출혈"), "산과 출혈"),
    (("자궁외임신", "이소성 임신"), "자궁외임신"),
    (("임신성 당뇨", "당부하", "인슐린"), "임신 중 당 대사"),
    (("철", "헤모글로빈", "빈혈"), "임신 중 철·빈혈"),
    (("갑상샘", "갑상선", "TSH", "hCG"), "임신 중 갑상샘"),
    (("폐경", "골다공증", "호르몬 대체"), "폐경과 호르몬 치료"),
    (("자궁경부암", "HPV", "CIN"), "자궁경부 병변"),
    (("자궁내막암", "내막증식"), "자궁내막 병변"),
    (("난소암", "난소종괴", "CA-125"), "난소 종양"),
    (("유방암", "유방종괴", "BI-RADS"), "유방 질환"),
    (("무월경", "다낭성난소", "PCOS"), "무월경·배란장애"),
    (("불임", "난임", "배란유도", "정액검사"), "난임 평가와 치료"),
    (("피임", "경구피임약", "자궁내장치"), "피임"),
    (("골반염", "PID", "질염", "성매개"), "여성생식기 감염"),
    (("요실금", "골반장기탈출"), "비뇨부인과"),
    (("사춘기", "성조숙증", "성분화"), "성발달"),
)


def derive_key_concepts(question: dict) -> list[str]:
    concepts: list[str] = []
    explanation = question.get("explanation") or {}
    if explanation.get("conceptGroup"):
        concepts.append(explanation["conceptGroup"])
    searchable = " ".join([
        str(question.get("stem", "")),
        " ".join(str(choice) for choice in question.get("choices", [])),
    ]).lower()
    for keywords, label in CONCEPT_KEYWORDS:
        if any(keyword.lower() in searchable for keyword in keywords):
            concepts.append(label)
    lecture = str(question.get("lectureTitle") or "핵심 개념 복습").strip()
    concepts.append(lecture)
    return list(dict.fromkeys(concepts))[:3]

PILOT_EXPLANATIONS.update({
    "gendev2-01-2023-q075": {
        "conceptGroup": "임신 중 호흡·당 대사",
        "keyJudgment": "임신 중 progesterone의 호흡자극으로 일회호흡량(tidal volume)이 증가한다. 정답은 ③이다.",
        "reasoningSteps": ["호흡수보다 한 번에 들이마시는 공기량 증가가 핵심이다.", "분시환기량이 증가해 경한 만성 호흡성 알칼리증 방향으로 간다.", "임신 후기 인슐린 저항 때문에 말초 포도당 흡수는 감소하고 공복혈당은 낮아진다."],
        "choiceExplanations": ["폐활량은 대체로 유지된다.", "잔기량은 자궁에 의한 횡격막 상승으로 감소한다.", "정답. 일회호흡량이 증가한다.", "말초 인슐린 저항으로 포도당 흡수는 감소한다.", "공복혈당은 경하게 낮아진다."],
        "conceptReview": "정상 임신에서는 tidal volume과 minute ventilation은 증가하고, functional residual capacity와 residual volume은 감소한다. 공복 저혈당·식후 고혈당·고인슐린혈증이 함께 나타난다.",
        "evidenceStatus": "Williams 26e Chapter 4 대조",
        "sources": [{"label":"Williams Obstetrics 26e, Ch. 4","url":"https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=254987027","kind":"교과서"}],
    },
    "gendev2-01-2022-q024": {
        "conceptGroup": "임신 중 심혈관·철 대사",
        "keyJudgment": "정상 임신에서 전신혈관저항은 증가가 아니라 감소한다. 옳지 않은 것은 ⑤다.",
        "reasoningSteps": ["임신 초기부터 혈관 확장으로 전신혈관저항이 낮아진다.", "심박수와 심박출량은 증가한다.", "후기 임신의 앙와위는 자궁이 정맥환류를 눌러 심박출량을 낮출 수 있다."],
        "choiceExplanations": ["맞다. 태아·태반으로 약 300 mg의 철이 이동한다.", "문항의 뜻은 실제 생리적 요구량으로, 임신 중반 이후 약 6–7 mg/일이다.", "맞다. 후기 임신에 왼쪽으로 돌아누우면 앙와위보다 심박출량이 약 20% 오를 수 있다.", "맞다. 안정 시 심박수는 대략 10회/분 증가한다.", "정답. 전신혈관저항은 감소한다."],
        "conceptReview": "심박출량 증가는 심박수·일회박출량 증가와 전신혈관저항 감소가 함께 만든다. 앙와위 저혈압은 큰 자궁의 대정맥 압박이 핵심이다.",
        "evidenceStatus": "Williams 26e Chapter 4 대조",
        "sources": [{"label":"Williams Obstetrics 26e, Ch. 4","url":"https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=254987027","kind":"교과서"}],
    },
    "gendev2-01-2022-q047": {
        "conceptGroup": "임신 중 호흡·당 대사",
        "keyJudgment": "횡격막 상승으로 functional residual capacity가 감소한다. 정답은 ⑤다.",
        "reasoningSteps": ["임신 후기 인슐린 저항 때문에 인슐린 농도와 식후혈당은 증가한다.", "호흡은 tidal volume 중심으로 증가한다.", "호기예비량과 잔기량 감소가 FRC 감소로 이어진다."],
        "choiceExplanations": ["인슐린 농도는 감소하지 않고 대체로 증가한다.", "식후혈당은 더 높고 오래 지속되는 방향이다.", "tidal volume은 증가한다.", "resting minute ventilation은 증가한다.", "정답. functional residual capacity는 감소한다."],
        "conceptReview": "FRC=ERV+RV다. 두 성분이 줄어 FRC가 감소하지만 vital capacity는 대체로 유지된다.",
        "evidenceStatus": "Williams 26e Chapter 4 대조",
        "sources": [{"label":"Williams Obstetrics 26e, Ch. 4","url":"https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=254987027","kind":"교과서"}],
    },
    "gendev2-01-2021-q001": {
        "conceptGroup": "임신 중 호흡·심혈관 생리",
        "keyJudgment": "후기 임신에 앙와위에서 좌측와위로 바꾸면 정맥환류가 회복되어 심박출량이 약 20% 증가할 수 있다. 정답은 ⑤다.",
        "reasoningSteps": ["자궁이 하대정맥을 누르는 자세 효과를 먼저 찾는다.", "호흡수 자체보다 tidal volume 증가가 더 뚜렷하다.", "잔기량은 증가가 아니라 감소한다."],
        "choiceExplanations": ["호흡수는 크게 변하지 않거나 약간 증가하며 핵심 변화는 tidal volume 증가다.", "residual volume은 감소한다.", "횡격막은 상승하지만 tidal volume은 증가한다.", "심박수는 감소가 아니라 증가한다.", "정답. 좌측와위가 대정맥 압박을 풀어 심박출량을 올린다."],
        "conceptReview": "앙와위 저혈압증후군은 큰 자궁이 하대정맥을 압박해 정맥환류와 심박출량을 낮추는 현상이다. 좌측와위가 기본 교정이다.",
        "evidenceStatus": "Williams 26e Chapter 4 대조",
        "sources": [{"label":"Williams Obstetrics 26e, Ch. 4","url":"https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=254987027","kind":"교과서"}],
    },
    "gendev2-01-2021-q002": {
        "conceptGroup": "임신 중 탄수화물 대사",
        "keyJudgment": "정상 임신 후기에는 말초 인슐린 저항이 나타난다. 정답은 ④다.",
        "reasoningSteps": ["태반 호르몬이 모체 인슐린 감수성을 낮춘다.", "그 결과 식후 포도당을 태아에게 더 오래 공급한다.", "공복에는 모체가 지방을 쓰며 혈당이 오히려 낮아진다."],
        "choiceExplanations": ["고인슐린혈증 방향이므로 감소가 아니다.", "공복 유리지방산은 증가한다.", "공복혈당은 경하게 감소한다.", "정답. 말초 인슐린 저항이 특징이다.", "식후혈당은 감소가 아니라 상승·지속한다."],
        "conceptReview": "임신 대사는 식후에는 고혈당·고인슐린, 공복에는 저혈당·지방 사용 증가라는 두 얼굴을 보인다.",
        "evidenceStatus": "Williams 26e Chapter 4 대조",
        "sources": [{"label":"Williams Obstetrics 26e, Ch. 4","url":"https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=254987027","kind":"교과서"}],
    },
    "gendev2-01-2020-q001": {
        "conceptGroup": "정상 임신 모성생리",
        "keyJudgment": "횡격막 상승으로 residual volume이 감소한다. 보기 중 가장 맞는 것은 ②다.",
        "reasoningSteps": ["호흡기 용적의 방향을 확인한다.", "요당은 임신의 신장 생리 변화로 생길 수 있어 당뇨 확진 소견이 아니다.", "좌측와위는 심박출량을 감소시키지 않고 증가시킨다."],
        "choiceExplanations": ["음식과 저장 철만으로 임신 전체 요구량을 충족하기 어려워 예방 보충을 고려한다.", "정답. residual volume과 FRC가 감소한다.", "요당만으로 당뇨를 진단하지 않는다.", "좌측와위에서 심박출량은 증가한다.", "ESR은 감소가 아니라 증가하는 방향이다."],
        "conceptReview": "임신의 생리 변화는 비임신 참고범위와 다르다. 검사 하나만으로 질환을 붙이지 말고 임신 주수와 전체 맥락을 본다.",
        "evidenceStatus": "Williams 26e Chapter 4 대조",
        "sources": [{"label":"Williams Obstetrics 26e, Ch. 4","url":"https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=254987027","kind":"교과서"}],
    },
    "gendev2-01-2020-q002": {
        "conceptGroup": "임신 중 탄수화물 대사",
        "keyJudgment": "족보 답 ①은 교과서 생리와 맞지 않는다. 말초 인슐린 저항으로 포도당 흡수가 감소하므로 교과서 대조 정답은 ③이다.",
        "reasoningSteps": ["정상 임신은 고인슐린혈증과 말초 인슐린 저항 상태다.", "공복혈당은 낮고 식후혈당은 높게 오래 지속된다.", "공복에는 유리지방산이 증가하므로 ①은 반대다."],
        "choiceExplanations": ["오류 의심 선지. 공복 유리지방산은 증가한다.", "인슐린 농도는 감소가 아니라 증가한다.", "교과서 대조 정답. 인슐린 저항 때문에 말초 포도당 흡수가 감소한다.", "공복혈당은 증가가 아니라 경하게 감소한다.", "식후혈당은 감소가 아니라 증가하고 오래 지속된다."],
        "conceptReview": "이 문항은 원본 족보 답과 교과서가 충돌한다. 사이트는 원답을 기록으로 남기되 교과서 대조 ③으로 채점하고 오류토의 대상으로 표시한다.",
        "evidenceStatus": "족보 정답 충돌 · Williams 26e Chapter 4 수동 대조",
        "sources": [{"label":"Williams Obstetrics 26e, Ch. 4","url":"https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=254987027","kind":"교과서"}],
    },
})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot", action="store_true")
    args = parser.parse_args()
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    for question in payload["questions"]:
        if question["id"] in PILOT_EXPLANATIONS:
            question["explanation"] = PILOT_EXPLANATIONS[question["id"]]
            question["relatedIds"] = [
                other for other in PILOT_EXPLANATIONS if other != question["id"]
                and PILOT_EXPLANATIONS[other]["conceptGroup"] == question["explanation"]["conceptGroup"]
            ]
        question["keyConcepts"] = derive_key_concepts(question)
    if args.pilot:
        allowed = set(PILOT_EXPLANATIONS)
        payload["questions"] = [q for q in payload["questions"] if q["id"] in allowed]
        payload["lectures"] = [lecture for lecture in payload["lectures"] if lecture["number"] == "01"]
        payload["buildMode"] = "pilot"
    else:
        payload["buildMode"] = "full"
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"SITE_DATA_READY mode={payload['buildMode']} questions={len(payload['questions'])}")


if __name__ == "__main__":
    main()
