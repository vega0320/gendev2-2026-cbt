from __future__ import annotations

"""9강 산욕기 문항을 문제별 임상 알고리듬과 현재 근거로 다시 작성한다."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"
REVIEW_DATE = "2026-08-06"

WILLIAMS = {"kind": "교과서", "label": "Williams Obstetrics 26e, The Puerperium", "url": "https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=249764077"}
CDC_MEC = {"kind": "현재 지침", "label": "CDC U.S. Selected Practice Recommendations for Contraceptive Use, 2024", "url": "https://www.cdc.gov/mmwr/volumes/73/rr/rr7303a1.htm"}
ACOG_BREAST = {"kind": "현재 지침", "label": "ACOG Breastfeeding Challenges, Committee Opinion 820", "url": "https://www.acog.org/clinical/clinical-guidance/committee-opinion/articles/2021/02/breastfeeding-challenges"}
ABM_MASTITIS = {"kind": "현재 지침", "label": "Academy of Breastfeeding Medicine Protocol #36: The Mastitis Spectrum, Revised 2022", "url": "https://www.bfmed.org/assets/ABM%20Protocol%20%2336.pdf"}
CDC_HBV = {"kind": "현재 지침", "label": "CDC Hepatitis B or C Infections and Breastfeeding", "url": "https://www.cdc.gov/breastfeeding-special-circumstances/hcp/illnesses-conditions/hepatitis-b-c.html"}
WHO_INFECTION = {"kind": "현재 지침", "label": "WHO Recommendations for Prevention and Treatment of Maternal Peripartum Infections", "url": "https://www.who.int/publications/i/item/9789241549363"}
LACTMED = {"kind": "약물 근거", "label": "NIH LactMed: Antineoplastic Agents", "url": "https://www.ncbi.nlm.nih.gov/books/NBK501922/"}


def explanation(concept: str, key: str, steps: list[str], choices: list[str], review: str,
                sources: list[dict], criteria: list[str] | None = None,
                numbers: list[str] | None = None) -> dict:
    return {
        "conceptGroup": concept,
        "keyJudgment": key,
        "reasoningSteps": steps,
        "choiceExplanations": choices,
        "conceptReview": review,
        "diagnosticCriteria": criteria or [],
        "numericReference": numbers or [],
        "numericReview": {
            "status": "applicable" if numbers else "not-applicable",
            "reason": "정답 판단에 직접 쓰이는 시간·수치 기준만 표시" if numbers else "별도 수치 절단값이 정답을 가르지 않음",
            "reviewedAt": REVIEW_DATE,
        },
        "evidenceStatus": "OpenEvidence로 근거 후보 탐색 후 교과서·공식 지침 원문 재검증 · 2026-08-06",
        "sources": sources,
    }


ENDO_CHOICES = [
    "metronidazole 단독은 혐기성균은 덮지만 장내 그람음성균과 일부 그람양성균을 포함한 산후 자궁내막염의 다균성 범위를 충분히 치료하지 못한다.",
    "Clindamycin은 혐기성균·그람양성균을, gentamicin은 호기성 그람음성균을 주로 덮어 제왕절개 후 산후 자궁내막염의 고전적 경험적 정맥요법이 된다.",
    "Vancomycin 단독은 MRSA·일부 그람양성균에는 유효하지만 혐기성균과 그람음성균을 빠뜨리므로 다균성 골반감염의 단독 경험치료가 아니다.",
    "Azithromycin 1회 투여는 산후 자궁내막염의 광범위 다균성 감염을 치료하는 요법이 아니다.",
    "자궁마사지는 자궁무력 출혈에 쓰며 발열·자궁압통·악취 오로로 나타난 감염을 치료하지 못한다.",
]

ENDO_OLD_CHOICES = [
    "Vancomycin 단독은 그람양성균 위주라 혐기성균과 그람음성균을 포함한 다균성 산후 감염을 충분히 덮지 못한다.",
    "Clindamycin과 gentamicin의 조합은 혐기성·호기성 그람음성균을 함께 덮는 제왕절개 후 산후 자궁내막염의 표준 경험적 정맥요법이다.",
    "Levofloxacin과 penicillin의 조합은 이 상황의 표준 경험요법이 아니며 혐기성균 범위를 안정적으로 확보하지 못한다.",
    "Metronidazole 단독은 혐기성균만으로 치료 범위가 치우쳐 다균성 자궁내막염에 부족하다.",
    "Imipenem은 광범위 대안이 될 수 있지만 내성·중증 감염 단서가 없는 환자에서 더 좁은 표준 조합보다 우선하지 않는다.",
]

CONTRACEPTION_CHOICES = [
    "프로게스틴 단일 피임약은 에스트로겐이 없어 산후 초기 혈전위험을 추가하지 않고 수유 중 사용할 수 있다.",
    "에스트로겐-프로게스틴 복합피임은 산후 초기 정맥혈전색전증 위험을 높이고 유즙 생성에 영향을 줄 수 있어 시작 시점을 미뤄야 한다.",
    "DMPA는 프로게스틴 단독 주사제이므로 에스트로겐에 의한 유즙 감소가 핵심 문제가 아니다.",
    "프로게스틴 피하 임플란트는 수유 중 사용할 수 있는 고효율 장기지속형 가역피임법이다.",
    "프로게스틴 방출 질내제는 에스트로겐 함유 복합제와 달리 산후 초기 혈전위험·유즙 감소를 묻는 대표 답이 아니다.",
]


def endometritis(q: dict) -> dict:
    predicted = q["id"].endswith("2026-q951")
    return explanation(
        "산후 자궁내막염",
        "제왕절개와 양막파수 뒤 산후 4일째 발열에 자궁·골반 통증 또는 악취 오로가 동반되어 다균성 산후 자궁내막염이 가장 가깝다. 경험적 정맥 clindamycin+gentamicin을 시작한다.",
        [
            "산후 발열을 확인하면 먼저 활력징후와 패혈증 여부를 보고, 유방·요로·호흡기·수술상처·자궁을 각각 진찰한다.",
            "제왕절개와 장시간 양막파수는 상행성 자궁내막 감염 위험을 높이고, 자궁압통·골반통·악취 오로는 감염 부위를 자궁으로 좁힌다.",
            "원인균은 단일균보다 질·장내의 호기성·혐기성 혼합균이 흔하므로 한 균만 겨냥한 약보다 광범위 정맥 병합요법이 필요하다.",
            "48~72시간 안에 호전하지 않으면 잔류태반, 골반농양, 상처감염, 장구균 또는 패혈성 골반혈전정맥염을 재평가한다.",
        ],
        ENDO_CHOICES if predicted else ENDO_OLD_CHOICES,
        "산후 자궁내막염은 임상진단이다. 항생제 시작 전 배양을 고려하되 안정적인 환자에서도 결과를 기다리느라 치료를 늦추지 않는다. 표준 병합요법에 반응하지 않을 때만 감염원과 항균 범위를 단계적으로 넓힌다.",
        [WILLIAMS, WHO_INFECTION],
        ["산후 발열의 다른 원인과 비교해 자궁압통·악취 오로·골반통 및 제왕절개/막파수 위험인자를 확인한다."],
        ["적절한 치료 뒤 48~72시간 지속 발열이면 농양·잔류조직·혈전정맥염·장구균을 재평가"],
    )


def contraception(q: dict) -> dict:
    qid = q["id"]
    if qid.endswith("2026-q952"):
        choices = [
            "프로게스틴 단일 피임약은 에스트로겐이 없어 수유 중 사용할 수 있다.",
            "Etonogestrel 임플란트는 수유 중에도 가능한 고효율 장기지속형 가역피임법이다.",
            "구리 자궁내장치는 호르몬이 없으므로 유즙량을 줄이지 않는다. 삽입 시점에는 산후 자궁 상태와 감염 여부를 함께 본다.",
            "에스트로겐 함유 복합피임은 산후 14일인 현재 U.S. MEC 4로 사용하면 안 되며, 혈전위험과 수유 확립 문제를 동시에 만든다.",
            "DMPA는 프로게스틴 단독 주사제라 에스트로겐 함유 복합제와 같은 금기 이유가 없다.",
        ]
        answer = "산후 2주는 정맥혈전색전증 위험이 특히 높은 시기다. 수유 여부와 관계없이 21일 미만에는 에스트로겐 함유 복합피임이 U.S. MEC 4이므로 피한다."
    else:
        choices = CONTRACEPTION_CHOICES.copy()
        if qid.endswith("2019-note-q077"):
            choices[4] = "레보노르게스트렐 자궁내장치는 에스트로겐이 없어 유즙 감소를 일으키는 대표 방법이 아니다."
        answer = "유즙 감소와 산후 혈전위험을 함께 만드는 성분은 에스트로겐이다. 따라서 프로게스틴 단독법이 아니라 에스트로겐-프로게스틴 복합피임을 고른다."
    return explanation(
        "수유 중 산후 피임",
        answer,
        [
            "먼저 출산 후 경과일과 완전모유수유 여부를 확인한다. 피임 효과만 비교하면 산후 에스트로겐 금기를 놓친다.",
            "선지를 에스트로겐 함유 복합법과 프로게스틴 단독·비호르몬법으로 나눈다. 혈전위험과 유즙 억제 우려는 전자에 집중된다.",
            "CDC 기준에서 수유 중 21일 미만 복합호르몬피임은 MEC 4, 21~29일은 MEC 3이다. 30~42일은 추가 VTE 위험인자 유무에 따라 MEC 3 또는 2다.",
            "따라서 산후 초기에는 프로게스틴 단독법·임플란트·적절한 시기의 IUD 등으로 상담하고, 복합제는 경과일과 위험인자를 다시 확인한 뒤 고려한다.",
        ],
        choices,
        "산후 피임의 핵심 변수는 경과일, 수유, VTE 위험인자다. 수유 중 복합호르몬피임은 21일 미만 MEC 4, 21~29일 MEC 3, 30~42일에는 VTE 위험인자가 있으면 3·없으면 2, 42일 초과는 2다. LAM은 무월경·완전 또는 거의 완전 수유·산후 6개월 미만을 모두 충족할 때만 성립한다.",
        [CDC_MEC, WILLIAMS],
        ["산후 경과일, 수유 여부, VTE 위험인자, 에스트로겐 포함 여부를 순서대로 판정한다."],
        ["수유 중 CHC: <21일 MEC 4; 21~<30일 MEC 3; 30~42일 VTE 위험 시 3/없으면 2; >42일 MEC 2"],
    )


def mastitis(q: dict) -> dict:
    qid = q["id"]
    if qid.endswith("2026-q953"):
        choices = [
            "수유를 갑자기 중단하면 유즙 정체가 심해질 수 있다. 대개 환측 수유를 계속하되 과도한 펌핑은 피한다.",
            "국소 발적·통증과 발열이 있는 세균성 유방염에는 냉찜질·NSAID·생리적 수유와 함께 dicloxacillin 또는 cephalexin 같은 항포도알균제를 사용한다.",
            "유방절제술은 감염성 유방염의 치료가 아니다. 배액이 필요한 농양도 보통 경피 배액이나 작은 절개로 치료한다.",
            "에스트로겐은 감염을 치료하지 않고 유즙 생성을 억제할 수 있다.",
            "전신증상을 동반한 국소 염증을 2주 방치하면 농양으로 진행할 수 있어 평가와 치료가 필요하다.",
        ]
    else:
        choices = [
            "깊고 강한 마사지는 부종과 미세혈관 손상을 악화시킬 수 있다. 부드러운 수유, 냉찜질과 진통소염을 사용한다.",
            "발열과 국소 홍반·압통이 있는 세균성 유방염에는 dicloxacillin 같은 항포도알균 경구제가 적절하다.",
            "환측 모유는 아기에게 안전하며 생리적 수유를 계속하는 것이 권장된다. 다만 이 문항의 단일 정답표는 항생제 ②를 선택했다.",
            "파동성 종괴가 없고 첫 내원인 경우 초음파가 반드시 첫 처치는 아니다. 24~48시간 내 호전이 없거나 종괴가 생기면 농양을 찾는다.",
            "유방촬영은 급성 수유기 유방염의 일차 검사가 아니다. 농양 의심 시 초음파가 우선이다.",
        ]
        q["answerReviewStatus"] = "족보 정답 ② 유지 · 현재 근거상 ③ 환측 수유 지속도 함께 권장되어 단일정답 문구가 다소 모호함"
    return explanation(
        "수유기 유방염과 농양",
        "산후 3주, 한쪽 유방의 국소 발적·통증과 발열은 수유기 유방염에 맞는다. 파동성 종괴가 없으므로 농양 배액보다 보존적 항염치료·생리적 수유를 유지하고 세균성 유방염이면 항포도알균제를 사용한다.",
        [
            "양측성으로 단단하고 열이 없는 산후 3~5일 울혈과, 한쪽의 국소 홍반·통증·발열을 보이는 유방염을 먼저 구분한다.",
            "염증성 유방염은 냉찜질·NSAID·생리적 수유로 24~48시간 관찰할 수 있지만, 지속 전신증상이나 세균성 봉와직염 양상이면 항생제를 시작한다.",
            "파동성 종괴가 없으므로 당장 배액할 농양 근거는 약하다. 반응이 없거나 종괴가 생기면 초음파와 배양을 시행한다.",
            "치료 중에도 환측 수유는 대개 안전하다. 과도한 펌핑과 깊은 마사지는 염증·부종을 악화시킬 수 있어 피한다.",
        ],
        choices,
        "유방염은 유즙 정체에서 염증성 유방염, 세균성 유방염, 농양으로 이어지는 스펙트럼이다. 모든 통증에 즉시 항생제를 쓰거나 유방을 완전히 비우는 것이 아니라 전신증상·봉와직염·경과를 보고 항생제와 영상을 단계적으로 추가한다.",
        [ABM_MASTITIS, ACOG_BREAST],
        ["양측 울혈인지, 국소 염증인지, 파동성 종괴인지와 24~48시간 치료 반응을 구분한다."],
        ["유방울혈은 흔히 산후 3~5일; 보존치료 24~48시간에도 악화/불응하면 세균감염·농양 재평가"],
    )


def mixed_2023(q: dict) -> dict:
    q["answerReviewStatus"] = "족보 정답 ⑤ 유지 · ①의 ‘출산 직후’, ②의 일률적 항생제 표현은 현재 근거상 문구가 부정확해 복수오답 가능성 주의"
    return explanation(
        "산후 유방질환·HBV 수유·피임",
        "정답표의 핵심 오류는 산후 2~3주에 수유 산모에게 복합 에스트로겐-프로게스틴 피임을 일률 처방한다는 주장이다. CDC 2024에서 수유 중 21일 미만은 MEC 4, 21~29일은 MEC 3이다.",
        [
            "‘옳지 않은 것’을 찾는 문제이므로 유방울혈, 유방염, 농양, HBV 수유, 산후 피임을 서로 다른 판단축으로 분리한다.",
            "유방울혈은 보통 산후 3~5일의 양측성 팽만이며 보존치료가 중심이다. 국소 홍반·발열이 지속되는 세균성 유방염은 항포도알균제를, 농양은 영상 확인 후 배액을 추가한다.",
            "HBsAg 양성 산모라도 신생아가 출생 12시간 이내 HBIG와 B형간염 백신을 받으면 모유수유를 미룰 필요가 없다.",
            "피임 선지에는 정확한 산후 날짜를 적용한다. 2주는 MEC 4이고 3주도 21~29일 구간이면 MEC 3이므로 ‘2~3주부터 처방 가능’이라는 일괄 표현은 틀리다.",
            "다만 유방울혈을 ‘출산 직후’라고 한 표현과 모든 염증에 항생제를 준다는 표현도 현대 기준에서는 부정확하므로, 이 문항은 정답표 ⑤를 유지하되 문항 오류 가능성을 함께 표시한다.",
        ],
        [
            "유방울혈은 출산 직후 즉시라기보다 대개 산후 3~5일 젖 분비가 늘 때 생긴다. 양측 팽만·열감·압통이고 열이나 국소 홍반이 없으면 냉찜질, 진통, 올바른 젖물림과 최소한의 유즙 표현으로 관리한다.",
            "수유기 유방염은 산후 첫 6주에 흔하지만 염증성 단계와 세균성 단계를 나눠야 한다. 세균성 소견이면 dicloxacillin 또는 cephalexin이 흔한 1차 약이고, erythromycin을 모든 경우의 표준으로 일반화하기는 어렵다.",
            "유방농양은 항생제만으로 해결되지 않아 초음파로 확인하고 바늘흡인·카테터 또는 절개배농으로 감염원을 제거한다.",
            "HBV 전파 위험은 신생아가 출생 12시간 이내 HBIG와 백신을 받으면 매우 낮다. 완전 면역될 때까지 모유수유를 지연할 필요가 없다.",
            "수유 중 복합호르몬피임은 산후 21일 미만 MEC 4, 21~29일 MEC 3이다. 따라서 산후 2~3주부터 조건 없이 처방할 수 있다는 설명은 틀리다.",
        ],
        "산후 유방 증상은 시점과 분포로 푼다. 산후 3~5일 양측 팽만은 울혈, 한쪽 국소 홍반·발열은 유방염, 파동성 종괴는 농양을 시사한다. 피임은 에스트로겐 포함 여부와 산후 일수·수유·VTE 위험을 함께 적용하고, HBV 수유는 신생아의 출생 직후 능동·수동면역 여부가 핵심이다.",
        [ACOG_BREAST, ABM_MASTITIS, CDC_HBV, CDC_MEC, WILLIAMS],
        ["울혈·유방염·농양을 분포, 발열, 종괴와 경과로 구분하고 산후 피임에는 CDC MEC를 적용한다."],
        ["유방울혈 산후 3~5일", "HBIG+백신 출생 12시간 이내", "수유 중 CHC <21일 MEC 4; 21~<30일 MEC 3"],
    )


def chemotherapy(q: dict) -> dict:
    return explanation(
        "모유수유 금기와 항암치료",
        "과거 한쪽 유방수술·방사선, HBV 또는 HPV 감염보다 현재 투여 중인 세포독성 항암제가 영아에게 직접 약물 노출과 골수억제 위험을 줄 수 있어 가장 강한 수유 금기다.",
        [
            "먼저 현재 진행 중인 노출과 과거 치료를 분리한다. 과거 수술·방사선은 수유량과 해부학을 바꾸지만 약물이 계속 노출되는 상태는 아니다.",
            "현재 항암제의 종류·반감기·투여 간격을 확인한다. 세포독성 약물은 영아의 빠르게 분열하는 조직에 위해를 줄 수 있어 치료 중 직접 수유를 피한다.",
            "HBV는 신생아 면역예방을 시행하면 수유 가능하고 HPV도 일반적인 모유수유 금기가 아니다.",
            "따라서 과거 국소 치료보다 현재 전신 항암치료가 절대 금기 여부를 결정한다. 재개 시점은 약물별 LactMed·종양내과 지침으로 따로 판단한다.",
        ],
        [
            "한쪽 유방절제술은 그 유방의 수유는 불가능하지만 반대쪽 유방의 수유 자체를 금지하지 않는다.",
            "과거 방사선치료는 치료받은 유방의 유즙 생성 저하를 만들 수 있으나 반대쪽 수유의 절대 금기는 아니다.",
            "세포독성 항암제는 모유로 전달되어 영아 골수억제·위장관 독성 등 위해를 줄 수 있으므로 투여 중 모유수유를 중단한다.",
            "HBsAg 양성 산모라도 신생아가 HBIG와 백신을 출생 직후 받으면 모유수유할 수 있다.",
            "산모의 HPV 감염은 모유수유를 금지하는 표준 적응증이 아니다.",
        ],
        "모유수유 가능 여부는 질병명만 외우지 말고 현재 약물의 영아독성, 감염의 실제 전파경로, 반대쪽 유방 기능을 분리해 판단한다. 항암제는 약물마다 중단기간이 달라 임의로 공통 기간을 적용하지 않는다.",
        [LACTMED, CDC_HBV, WILLIAMS],
    )


def wound(q: dict) -> dict:
    return explanation(
        "제왕절개 수술상처 감염",
        "발적·압통·농성 분비와 창상 벌어짐은 수술부위감염이다. 항생제를 시작하고 봉합선을 열어 배농·세척하며 괴사조직과 근막 손상 여부를 확인한다.",
        [
            "먼저 패혈증 활력징후와 창상 깊이를 평가한다. 특히 근막이 벌어졌는지는 단순 피부감염과 응급 재수술을 가르는 핵심이다.",
            "농성 분비와 벌어짐은 감염원이 갇혀 있다는 뜻이므로 항생제만 주거나 경과관찰하지 않고 배농과 배양을 시행한다.",
            "괴사조직을 제거하고 근막이 온전한지 확인한 뒤, 감염이 조절될 때까지 개방치료 또는 음압치료를 고려한다.",
            "깨끗하지 않은 상처를 즉시 다시 봉합하면 감염을 가둘 수 있다. 지연봉합은 감염과 조직상태가 호전된 뒤 판단한다.",
        ],
        [
            "화농성 분비와 창상 벌어짐이 있어 관찰만 하면 감염이 깊어지거나 근막 열개를 놓칠 수 있다.",
            "항생제는 주변 봉와직염과 전신감염을 치료하고, 배농은 고름과 괴사조직이라는 감염원을 제거하므로 둘을 함께 시행한다.",
            "고용량 스테로이드는 감염을 치료하지 않고 면역반응과 창상치유를 방해할 수 있다.",
            "오염된 상처를 즉시 재봉합하면 감염을 내부에 가둘 수 있어 먼저 개방·배농·괴사조직 제거가 필요하다.",
            "급성 농성 창상감염은 임상적으로 진단하며 종양성 병변을 찾는 조직검사가 우선 처치가 아니다.",
        ],
        "제왕절개 창상 문제는 피부·피하 감염, 농양, 근막 열개, 괴사성 연조직감염을 구분한다. 근막 열개나 통증에 비해 빠른 진행·수포·가스·독성이 있으면 즉시 수술 평가가 필요하다.",
        [WILLIAMS, WHO_INFECTION],
        ["농성 배액, 창상 벌어짐, 근막 온전성, 전신독성을 확인한다."],
    )


def secondary_pph(q: dict) -> dict:
    return explanation(
        "이차 산후출혈과 잔류조직",
        "산후 10일 대량출혈, 빈맥, 충분히 단단하지 않은 자궁과 자궁강 혼합에코는 자궁퇴축부전·혈괴·잔류태반조직을 시사한다. 안정화와 자궁수축제·감염평가를 먼저 하고, 단순 혼합에코만으로 즉시 소파술을 고정하지 않는다.",
        [
            "출혈량과 활력징후를 먼저 재평가하고 큰 정맥로·혈액검사·교차시험을 준비한다. 정상 혈압만으로 안정적이라고 보지 않고 맥박 115회를 저혈량 경고로 본다.",
            "산후 24시간 이후 출혈은 잔류태반조직, 자궁내막염, 태반부착부 퇴축부전과 응고장애를 우선 감별한다.",
            "자궁이 충분히 단단하지 않으면 oxytocin·methylergonovine 같은 자궁수축제를 고려하고, 감염 가능성이 있으면 적절한 항생제를 병행한다.",
            "초음파 혼합에코는 혈괴와 잔류조직을 완전히 구분하지 못한다. 지속 대량출혈, 혈류가 풍부한 잔류조직 또는 감염이 확인될 때 영상유도 제거·자궁경 치료를 선택한다.",
        ],
        [
            "초음파 유도 소파술도 잔류조직이 확실하고 출혈이 지속될 때는 필요할 수 있다. 그러나 작은 혼합에코만 보고 첫 단계로 바로 시행하면 혈괴를 불필요하게 제거하거나 산후 자궁 천공·유착 위험을 만들 수 있다.",
            "Methylergonovine은 자궁퇴축부전성 출혈에서 수축을 강화할 수 있지만 고혈압·자간전증에서는 피한다.",
            "Oxytocin은 충분히 수축하지 않는 산후 자궁의 1차 자궁수축제로 사용할 수 있다.",
            "이차 산후출혈에 감염·잔류조직이 의심되면 항생제를 고려한다. 다만 azithromycin 또는 doxycycline만을 모든 산후 자궁내막염의 표준 정맥요법으로 일반화해서는 안 된다.",
            "빈맥과 간헐적 대량출혈이 있어 활력징후, 출혈량, 소변량과 혈색소를 연속 관찰해야 한다.",
        ],
        "이차 산후출혈은 출산 24시간 이후 발생하는 비정상 출혈이다. 초음파의 자궁강 물질은 잔류조직과 혈괴가 겹쳐 보일 수 있어 임상 출혈, 감염소견과 도플러 혈류를 함께 본다. 처치는 소생·자궁수축·항생제·원인 제거를 동시에 설계한다.",
        [WILLIAMS],
        ["잔류조직, 자궁내막염, 태반부착부 퇴축부전, 응고장애를 감별한다."],
        ["이차 산후출혈: 출산 24시간 이후부터 대개 12주 이내의 비정상 출혈"],
    )


def apply() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    questions = [q for q in payload["questions"] if q.get("lectureNumber") == "09"]
    for q in questions:
        qid = q["id"]
        if qid.endswith("2026-q951") or qid.endswith(("2022-q011", "2021-q008", "2020-q018", "2019-note-q058")):
            exp = endometritis(q)
        elif qid.endswith(("2026-q952", "2021-q007", "2020-q017", "2019-note-q077")):
            exp = contraception(q)
        elif qid.endswith(("2026-q953", "2022-q049")):
            exp = mastitis(q)
        elif qid.endswith("2023-q016"):
            exp = mixed_2023(q)
        elif qid.endswith("2025-q061"):
            exp = chemotherapy(q)
        elif qid.endswith("2025-q062"):
            exp = wound(q)
        elif qid.endswith("2023-q085"):
            exp = secondary_pph(q)
        else:
            raise SystemExit(f"unmapped lecture 09 question: {qid}")
        predicted_pitfalls = {
            "gendev2-09-2026-q951": "산후 발열을 모두 자궁내막염으로 묶지 않는다. 자궁압통·악취 오로와 제왕절개·막파수 위험인자가 함께 있을 때 자궁 감염의 우선순위가 높아진다.",
            "gendev2-09-2026-q952": "피임 효과만 비교하면 산후 경과일에 따른 에스트로겐의 혈전 금기를 놓친다. 수유 여부와 VTE 위험인자를 동시에 확인한다.",
            "gendev2-09-2026-q953": "통증이 있다고 유방을 세게 비우거나 모든 염증에 즉시 항생제를 쓰지 않는다. 국소성·전신증상·24~48시간 경과와 종괴를 구분한다.",
        }
        if qid in predicted_pitfalls:
            exp["commonPitfall"] = predicted_pitfalls[qid]
        if len(exp["choiceExplanations"]) != len(q.get("choices", [])):
            raise SystemExit(f"{qid}: choice explanation count mismatch")
        q["explanation"] = exp
        q["explanationReviewStatus"] = "manual-evidence-review-lecture09-2026-08-06"
        q["semanticChoiceReviewStatus"] = "manual-semantic-audit-2026-08-06"

    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"LECTURE09_EVIDENCE_REVIEW_PASS questions={len(questions)}")


if __name__ == "__main__":
    apply()
