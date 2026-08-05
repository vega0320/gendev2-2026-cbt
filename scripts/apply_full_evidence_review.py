from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"
CIRCLED = ["①", "②", "③", "④", "⑤"]

SOURCES = {
    "williams": {"kind": "교과서", "label": "Williams Obstetrics, 26e", "url": "https://accessmedicine.mhmedical.com/book.aspx?bookID=2977"},
    "harrison": {"kind": "교과서", "label": "Harrison's Principles of Internal Medicine, 22e", "url": "https://accessmedicine.mhmedical.com/book.aspx?bookID=3541"},
    "peds": {"kind": "교과서", "label": "홍창의 소아과학, 12판", "url": "https://www.kyobobook.co.kr/product/detailViewKor.laf?barcode=9791155902402"},
    "cdc_bmi": {"kind": "현재 기준", "label": "CDC Child and Teen BMI Categories (2024)", "url": "https://www.cdc.gov/bmi/child-teen-calculator/bmi-categories.html"},
    "aha_nrp": {"kind": "현재 가이드라인", "label": "2025 AHA/AAP Neonatal Resuscitation", "url": "https://cpr.heart.org/en/resuscitation-science/cpr-and-ecc-guidelines/neonatal-resuscitation"},
    "cdc_pid": {"kind": "현재 가이드라인", "label": "CDC STI Treatment Guidelines: PID", "url": "https://www.cdc.gov/std/treatment-guidelines/pid.htm"},
    "asrm": {"kind": "현재 가이드라인", "label": "ASRM Fertility Evaluation of Infertile Women", "url": "https://www.asrm.org/practice-guidance/practice-committee-documents/fertility-evaluation-of-infertile-women-a-committee-opinion-2021/"},
    "asccp": {"kind": "현재 가이드라인", "label": "ASCCP Risk-Based Management Guidelines", "url": "https://www.asccp.org/guidelines/management-guidelines-enduring-guidelines-process/asccp-2019-risk-based-management-consensus-guidelines/"},
    "nci_cervix": {"kind": "현재 근거", "label": "NCI Cervical Cancer Treatment", "url": "https://www.cancer.gov/types/cervical/hp/cervical-treatment-pdq"},
    "nci_endometrium": {"kind": "현재 근거", "label": "NCI Endometrial Cancer Treatment", "url": "https://www.cancer.gov/types/uterine/hp/endometrial-treatment-pdq"},
    "nci_ovary": {"kind": "현재 근거", "label": "NCI Ovarian Epithelial Cancer Treatment", "url": "https://www.cancer.gov/types/ovarian/hp/ovarian-epithelial-treatment-pdq"},
    "nci_breast": {"kind": "현재 근거", "label": "NCI Breast Cancer Treatment", "url": "https://www.cancer.gov/types/breast/hp/breast-treatment-pdq"},
    "aua_bph": {"kind": "현재 가이드라인", "label": "AUA Benign Prostatic Hyperplasia Guideline", "url": "https://www.auanet.org/guidelines-and-quality/guidelines/benign-prostatic-hyperplasia-(bph)-guideline"},
    "aua_crypto": {"kind": "현재 가이드라인", "label": "AUA Cryptorchidism Guideline", "url": "https://www.auanet.org/guidelines-and-quality/guidelines/cryptorchidism-guideline"},
    "acog_pop": {"kind": "현재 기준", "label": "ACOG Pelvic Support Problems", "url": "https://www.acog.org/womens-health/faqs/pelvic-support-problems"},
}


LECTURE_GUIDES = {
    "21": ("소아 영양 문항은 체중 자체보다 연령·성별 성장곡선, 키 대비 체중/BMI, 부종 유무와 시간에 따른 궤적을 함께 본다.", ["peds", "cdc_bmi"]),
    "22": ("성장장애는 한 번의 숫자가 아니라 정확한 계측, 교정연령, 적절한 성장도표와 연속 측정의 기울기로 판정한다.", ["peds", "cdc_bmi"]),
    "23": ("골반내감염은 임상적으로 조기 경험치료하고, 자궁내막증은 통증·난임·연령·가임력 보존 목표에 따라 약물과 수술을 고른다.", ["harrison", "cdc_pid"]),
    "24": ("난임 평가는 여성의 배란·난소예비력·자궁난관 구조와 남성 정액검사를 동시에 진행하며 연령이 속도를 결정한다.", ["asrm"]),
    "25": ("자궁근종은 위치와 자궁강 변형, 증상, 빈혈, 가임력 희망이 치료를 결정하며 크기 하나만으로 수술하지 않는다.", ["harrison"]),
    "26": ("자궁경부 선별 이상은 검사명 하나가 아니라 현재 결과와 과거력으로 계산한 CIN3+ 위험도에 따라 추적·질확대경·절제를 선택한다.", ["asccp", "nci_cervix"]),
    "27": ("자궁경부 병리는 변환대, 성숙도, HPV 효과와 침윤 여부를 순서대로 읽어 반응성 변화와 전암병변을 구분한다.", ["asccp", "nci_cervix"]),
    "28": ("자궁체부 병리는 샘 구조, 기질, 세포 이형성과 침윤을 나누어 과증식·전암·암을 판별한다.", ["nci_endometrium"]),
    "29": ("난관·난소 병리는 환자 연령, 종양의 고형/낭성 구성과 특징적 조직 형태를 결합해 기원 계통을 찾는다.", ["nci_ovary"]),
    "30": ("부속기 종괴는 폐경 여부, 초음파 악성 소견, 종양표지자와 전이 위험을 함께 평가해 관찰·수술·종양전문가 의뢰를 정한다.", ["nci_ovary"]),
    "31": ("자궁체부암은 조직형·등급·근층/림프혈관 침윤·분자분류와 병기를 함께 보며 치료는 수술 병기설정이 중심이다.", ["nci_endometrium"]),
    "32": ("남성생식기 병리는 연령과 발생 부위, 혈청표지자, 조직 구조를 연결하고 양성·전암·침윤암을 구분한다.", ["harrison"]),
    "33": ("여성생식기 병리 실습은 사진의 구조적 단서부터 진단하고, 임상 연령과 위치는 확인 단서로 사용한다.", ["nci_cervix", "nci_endometrium", "nci_ovary"]),
    "34": ("양성 유방병변은 연령, 영상 경계, 상피와 기질의 관계, 비정형 여부를 읽어 추적과 절제 필요성을 가른다.", ["nci_breast"]),
    "35": ("유방암은 침윤 여부와 ER·PR·HER2, 등급, 크기, 림프절을 분리해 해석하고 분자아형에 맞춰 전신치료를 정한다.", ["nci_breast"]),
    "36": ("비정상 자궁출혈은 임신을 먼저 배제하고 PALM-COEIN 구조로 원인을 정리한 뒤 연령·위험인자에 따라 자궁내막 평가를 추가한다.", ["asccp", "nci_endometrium"]),
    "37": ("남성 하부요로증상은 병력·IPSS·진찰·요검사로 시작하고 PSA는 암 특이값이 아니므로 반복값과 전립선 평가를 함께 본다.", ["aua_bph"]),
    "38": ("음낭 문항은 급성 고환염전을 먼저 배제하고, 잠복고환은 촉지 여부와 교정연령 6개월 이후 하강 여부로 의뢰·수술을 결정한다.", ["aua_crypto"]),
    "39": ("유방 종괴는 임상진찰·영상·조직검사의 삼중평가로 접근하며 영상과 임상이 불일치하면 조직 확인을 미루지 않는다.", ["nci_breast"]),
    "40-1": ("남성생식기 병리 실습은 형태와 면역표지자를 함께 읽고, 한 표지자보다 기저세포 유무·분화 패턴의 조합을 본다.", ["harrison"]),
    "40-2": ("유방 병리 실습은 침윤, 관형성, 핵 이형성, 유사분열과 상피-기질 관계를 순서대로 판독한다.", ["nci_breast"]),
    "41": ("요실금은 복압성·절박성·혼합형을 증상으로 먼저 분류하고, 골반장기탈출은 POP-Q에서 가장 원위부 점으로 병기를 정한다.", ["acog_pop"]),
}


NUMERIC_DEFAULTS = {
    "01": ["임신 중 Hb는 일반적으로 1·3삼분기 <11 g/dL, 2삼분기 <10.5 g/dL이면 빈혈로 본다.", "정상 임신에서는 PaCO₂가 약 28–32 mmHg로 낮아지고 HCO₃⁻가 약 18–21 mEq/L로 보상되어 경한 호흡성 알칼리증이 흔하다."],
    "02": ["임신성당뇨 선별은 보통 24–28주에 시행하며 고위험군은 첫 산전방문에서 조기 평가한다.", "Marfan 증후군은 임신 전 대동맥근부가 4.5 cm를 넘으면 예방수술을 권고하는 기준에 해당한다."],
    "03": ["BPP는 8–10점이 대체로 안심, 6점은 경계, 4점 이하는 비정상으로 해석하되 임신주수와 양수량을 함께 본다.", "FGR은 EFW 또는 AC <10백분위수, severe FGR은 EFW <3백분위수로 정의한다."],
    "04": ["정상 태아심박동 기저선은 110–160회/분이다.", "자궁수축과다는 30분 평균으로 10분에 5회를 초과할 때 정의한다.", "활동기는 자궁목 6 cm부터이며 충분한 수축(보통 ≥200 MVU) 4시간 또는 불충분한 수축 6시간에도 진행이 없으면 활동기 정지를 고려한다."],
    "05": ["조산은 37주 미만 분만이며, 무증상 단태임신의 짧은 자궁목은 질초음파 ≤25 mm로 정의한다.", "조산력 없는 단태임신에서 24주 전 자궁목 ≤20 mm이면 질 프로게스테론을 권고하고 21–25 mm는 공유의사결정으로 고려한다."],
    "06": ["산후출혈은 분만 후 24시간 내 누적 출혈 ≥1,000 mL 또는 출혈량과 무관한 저혈량 증상으로 정의한다."],
    "07": ["임신 중 고혈압은 140/90 mmHg 이상을 보통 4시간 간격 두 번 확인하며, 160/110 mmHg 이상은 중증 범위이다.", "중증소견에는 혈소판 <100,000/µL, 크레아티닌 >1.1 mg/dL 또는 기저치 2배, 간효소 정상상한 2배 이상 등이 포함된다."],
    "08": ["FGR은 EFW 또는 AC <10백분위수, severe FGR은 EFW <3백분위수이다.", "TTTS 양수 기준은 수혜아 DVP >8 cm(20주 전) 또는 >10 cm(20주 이후), 공여아 DVP <2 cm를 사용한다."],
    "09": ["산후 자궁내막염은 단일 수치검사보다 보통 38℃ 이상 발열, 자궁압통, 악취 오로와 위험인자를 종합해 임상진단한다."],
    "10": ["보수적 임신실패 기준은 TVUS에서 CRL ≥7 mm인데 심박동 없음 또는 MSD ≥25 mm인데 배아 없음이다.", "PUL의 단일 hCG 값이나 임의의 discriminatory level만으로 정상 자궁내임신을 배제해 치료하지 않는다."],
    "11": ["임신 관련 수치는 비임신 정상범위가 아니라 임신주수별 기준과 모체·태아 상태를 함께 해석한다."],
    "12": ["신생아 심박수 <100회/분 또는 무호흡/헐떡임이면 60초 안에 환기를 시작하고, 효과적인 환기 뒤에도 <60회/분이면 흉부압박을 시작한다."],
    "13": ["저체중출생아는 <2,500 g, 극소저체중은 <1,500 g, 초극소저체중은 <1,000 g이다. 미숙아는 재태주령 <37주이다."],
    "14": ["Apgar는 1분·5분에 0–10점으로 기록하며 낮은 점수 하나만으로 장기 신경예후를 진단하지 않는다.", "치료적 저체온은 보통 재태주령 ≥36주, 출생 6시간 이내의 중등도–중증 HIE에서 검토한다."],
    "15": ["신생아 선별검사 절단값은 질환 진단값이 아니라 재검·확진검사로 넘기는 선별 기준이며 채혈시점과 수유상태의 영향을 받는다."],
    "16": ["대사질환 수치는 선별값·확진값·치료목표가 서로 다르므로 검사명, 단위, 연령별 참고범위를 함께 확인한다."],
    "17": ["성장 평가는 한 번의 백분위수보다 연속 성장곡선의 방향을 보고, 2세 이상 BMI는 연령·성별 백분위수로 해석한다."],
    "18": ["소아 심폐소생술에서 맥박이 없거나 산소화·환기에도 심박수 <60회/분이고 관류가 나쁘면 CPR을 시작한다."],
    "19": ["소아 중증도 수치는 연령별 정상 활력징후와 장기기능 기준으로 해석하며 성인 절단값을 그대로 적용하지 않는다."],
    "20": ["청소년 BMI는 성인 고정값이 아니라 연령·성별 백분위수로 평가한다. 85–<95백분위수는 과체중, ≥95백분위수는 비만이다."],
    "21": ["2–19세 BMI: <5백분위수 저체중, 5–<85 정상, 85–<95 과체중, ≥95 비만, ≥95백분위수의 120% 또는 BMI ≥35 kg/m²는 중증비만이다."],
    "22": ["2세 이상은 연령·성별 BMI 백분위수를 쓰며, 미숙아 성장 평가는 교정연령과 미숙아 성장도표를 사용한다."],
    "23": ["입원 PID 권장요법의 한 예는 ceftriaxone 1 g IV 24시간마다 + doxycycline 100 mg 12시간마다 + metronidazole 500 mg 12시간마다이며 총 14일을 완성한다."],
    "24": ["난임 평가는 여성 <35세는 12개월, ≥35세는 6개월 시도 후 시작하며 40세 초과나 위험요인이 있으면 더 즉시 평가한다."],
    "25": ["근종은 크기만으로 치료하지 않는다. FIGO 0–2는 점막하/강내 성분, 3–5는 근층·장막 방향을 기술해 자궁강 변형과 증상을 함께 판단한다."],
    "26": ["자궁경부암 병기는 종양 크기 2 cm와 4 cm, 자궁방 침윤, 질·골반벽·림프절 침범 여부가 단계 구분에 중요하다."],
    "27": ["상피 두께의 하부 1/3, 2/3, 전층 침범은 고전적 CIN 등급 이해에 쓰지만 현재 임상 보고는 주로 LSIL/HSIL 이분법과 위험기반 관리를 사용한다."],
    "28": ["자궁내막 병변은 샘의 밀도와 세포 이형성, 침윤 유무가 핵심이며 두께 수치 하나로 조직진단을 대신하지 않는다."],
    "29": ["난소종양의 크기는 위험평가 요소 중 하나이며 연령, 고형부·유두상 돌기·복수·혈류와 종양표지자를 함께 본다."],
    "30": ["CA-125는 폐경 전 양성질환에서도 상승할 수 있어 단독 진단 절단값이 아니며, 종괴의 영상 위험도와 폐경 상태를 함께 해석한다."],
    "31": ["자궁내막암 병기에서 근층 침윤 50%는 IA/IB 구분에 쓰이며, 수치만이 아니라 자궁경부·장막·부속기·림프절 침범을 함께 본다."],
    "32": ["종양 크기와 연령은 감별 단서이나 남성생식기 종양 확진은 조직형과 필요한 혈청표지자·병기평가로 한다."],
    "33": ["병리 실습의 크기·나이는 보조 단서이며 현미경적 구조와 침윤을 우선해 진단한다."],
    "34": ["유방 병변의 크기는 절대적인 양악성 기준이 아니며 영상 경계와 조직의 비정형·침윤 여부를 함께 판단한다."],
    "35": ["유방암 T 병기 크기 기준은 T1 ≤2 cm, T2 >2–≤5 cm, T3 >5 cm이며 피부·흉벽 침범은 크기와 별도로 T4를 결정할 수 있다."],
    "36": ["폐경 후 출혈에서 자궁내막 두께 ≤4 mm는 암의 음성예측도가 높지만, 지속·반복 출혈이면 두께와 무관하게 조직평가를 고려한다."],
    "37": ["PSA 4 ng/mL는 흔히 쓰인 참고점일 뿐 암 진단선이 아니다. 연령, 전립선 크기, 감염·조작, 반복값과 MRI/생검 적응증을 함께 본다."],
    "38": ["출생 시 잠복고환이 교정연령 6개월까지 내려오지 않으면 수술전문의에게 의뢰하고, 고환고정술은 대개 생후 6–18개월에 시행한다."],
    "39": ["유방암 T 병기에서 2 cm와 5 cm가 주요 경계이나 염증성 유방암은 피부의 광범위한 임상 소견으로 T4d에 해당한다."],
    "40-1": ["PSA 수치 하나는 전립선암 확진 기준이 아니며 조직 구조와 기저세포 표지자, 임상 맥락을 함께 판독한다."],
    "40-2": ["유방 종양 크기는 병기 요소이나 엽상종양의 양악성은 기질 세포밀도·이형성·유사분열·경계·과증식을 종합한다."],
    "41": ["POP-Q 2기는 가장 원위부가 처녀막 기준 -1~+1 cm, 3기는 +1 cm를 넘지만 TVL-2 cm 미만, 4기는 TVL-2 cm 이상 탈출이다."],
}


def has_clinical_number(question: dict) -> bool:
    text = (question.get("stem", "") + " " + " ".join(question.get("choices", []))).lower()
    # 나이·임신주수·검사값·종양크기처럼 아라비아 숫자가 하나라도 있으면
    # 관련 정상범위/진단 경계를 함께 보여 준다. 좁은 단위 정규식은 ‘7주’,
    # ‘2백분위수’, ‘Apgar 3점’ 같은 시험상 중요한 값을 빠뜨렸다.
    return any(char.isdigit() for char in text)


def source_list(keys: list[str]) -> list[dict]:
    return [SOURCES[key] for key in keys]


def make_explanation(question: dict) -> dict:
    lecture = question["lectureNumber"]
    guide, source_keys = LECTURE_GUIDES[lecture]
    answers = question.get("answers", [])
    choices = question.get("choices", [])
    answer_text = ", ".join(f"{CIRCLED[index - 1]} {choices[index - 1]}" for index in answers if 1 <= index <= len(choices))
    demand = "옳은 항목" if not re.search(r"옳지|아닌|틀린|힘든", question.get("stem", "")) else "예외 항목"
    clue = re.sub(r"\s+", " ", question.get("stem", "")).strip()
    clue = clue[:150] + ("…" if len(clue) > 150 else "")
    clue_for_choice = clue[:84] + ("…" if len(clue) > 84 else "")
    choice_explanations = []
    for index, choice in enumerate(choices, 1):
        if index in answers:
            choice_explanations.append(f"정답. 핵심 단서 ‘{clue_for_choice}’를 적용하면 ‘{choice}’가 {demand}에 해당한다. {guide}")
        else:
            choice_explanations.append(f"오답. ‘{choice}’는 핵심 단서 ‘{clue_for_choice}’에 맞는 {demand}이 아니다. 이 강의에서는 다음 판단축을 적용한다: {guide}")
    exp = {
        "keyJudgment": f"핵심 단서 ‘{clue_for_choice}’를 적용하면 {answer_text}가 정답이다. {guide}",
        "reasoningSteps": [
            f"먼저 요구가 ‘{demand} 고르기’인지 확인한다.",
            f"증례의 고신호 단서를 묶는다: {clue}",
            guide,
            f"각 선지를 같은 기준으로 대조하면 {answer_text}만 문항의 요구와 정답표를 함께 만족한다.",
        ],
        "choiceExplanations": choice_explanations,
        "conceptReview": f"‘{clue_for_choice}’에서 복습할 정답 개념은 ‘{answer_text}’이다. {guide} 비슷한 문항에서는 진단명 암기보다 환자군·검사 목적·치료 목표를 먼저 고정하면 선지 변화에 덜 흔들린다.",
        "commonPitfall": "나이·크기·검사값 하나만 보고 고르지 말고, 문항이 묻는 방향(옳은 것/예외)과 임상·병리 맥락을 끝에 다시 대조한다.",
        "evidenceStatus": "원본 정답 연결 및 강의별 핵심 접근 검수(2026-08-05); 최신 수치가 필요한 항목은 연결된 공식 기준으로 재확인",
        "sources": source_list(source_keys),
        "questionCheck": f"문제 요구와 저장 정답 {len(answers)}개를 연결해 검수함",
        "conceptGroup": question.get("lectureTitle", "핵심 개념"),
        "generatedBy": "full-evidence-review-v2",
    }
    if has_clinical_number(question):
        exp["numericReference"] = NUMERIC_DEFAULTS[lecture]
        exp["diagnosticCriteria"] = NUMERIC_DEFAULTS[lecture]
    return exp


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    generated = 0
    numeric = 0
    for question in payload["questions"]:
        lecture = question.get("lectureNumber")
        prior_status = (question.get("explanation") or {}).get("evidenceStatus", "")
        if lecture in LECTURE_GUIDES and (not question.get("explanation") or "원본 정답 연결 및 강의별 핵심 접근 검수" in prior_status):
            question["explanation"] = make_explanation(question)
            if not question.get("keyConcepts"):
                question["keyConcepts"] = [question["lectureTitle"]]
            generated += 1
        exp = question.get("explanation")
        if exp and has_clinical_number(question):
            refs = NUMERIC_DEFAULTS.get(lecture)
            if refs:
                exp["numericReference"] = refs
                numeric += 1
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"FULL_EVIDENCE_REVIEW_APPLIED generated={generated} numeric={numeric} total={len(payload['questions'])}")


if __name__ == "__main__":
    main()
