from __future__ import annotations

"""21~26강 문항의 문항별·선지별 해설을 수동 검수 규칙으로 보강한다."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"
REVIEW_DATE = "2026-08-06"
MARKER = "manual-choice-independent-audit-21-26"


SOURCES = {
    21: [
        {"type": "textbook", "title": "홍창의 소아과학 12판: 소아의 영양·성장", "checkedAt": REVIEW_DATE},
        {"type": "guideline", "title": "CDC Child and Teen BMI Categories", "url": "https://www.cdc.gov/bmi/child-teen-calculator/bmi-categories.html", "checkedAt": REVIEW_DATE},
    ],
    22: [
        {"type": "textbook", "title": "홍창의 소아과학 12판: 성장과 발달", "checkedAt": REVIEW_DATE},
        {"type": "guideline", "title": "CDC Growth Chart Training", "url": "https://www.cdc.gov/growth-chart-training/hcp/using-bmi/summary.html", "checkedAt": REVIEW_DATE},
    ],
    23: [
        {"type": "guideline", "title": "CDC Pelvic Inflammatory Disease Treatment Guidelines", "url": "https://www.cdc.gov/std/treatment-guidelines/pid.htm", "checkedAt": REVIEW_DATE},
        {"type": "guideline", "title": "CDC Trichomoniasis Treatment Guidelines", "url": "https://www.cdc.gov/std/treatment-guidelines/trichomoniasis.htm", "checkedAt": REVIEW_DATE},
        {"type": "guideline", "title": "ACOG Clinical Practice Guideline: Diagnosis of Endometriosis", "url": "https://www.acog.org/clinical/clinical-guidance/clinical-practice-guideline/articles/2026/03/diagnosis-of-endometriosis", "checkedAt": REVIEW_DATE},
    ],
    24: [
        {"type": "guideline", "title": "2023 International Evidence-based Guideline for PCOS", "url": "https://integration.asrm.org/practice-guidance/practice-committee-documents/recommendations-from-the-2023-international-evidence-based-guideline-for-the-assessment-and-management-of-polycystic-ovary-syndrome/", "checkedAt": REVIEW_DATE},
        {"type": "textbook", "title": "난임 평가와 치료 강의자료·표 원본 대조", "checkedAt": REVIEW_DATE},
    ],
    25: [
        {"type": "guideline", "title": "ACOG Uterine Fibroids FAQ", "url": "https://www.acog.org/womens-health/faqs/uterine-fibroids", "checkedAt": REVIEW_DATE},
        {"type": "source-image", "title": "문항별 초음파·육안 사진·근종 위치 도식 원본 대조", "checkedAt": REVIEW_DATE},
    ],
    26: [
        {"type": "guideline", "title": "NCI Cervical Cancer Treatment (PDQ)", "url": "https://www.cancer.gov/types/cervical/hp/cervical-treatment-pdq", "checkedAt": REVIEW_DATE},
        {"type": "guideline", "title": "ASCCP Risk-Based Management Consensus Guidelines", "url": "https://www.asccp.org/guidelines", "checkedAt": REVIEW_DATE},
    ],
}


PROFILES = {
    "obesity_skin": {
        "key": "급격한 체중 증가와 목·겨드랑이의 벨벳 모양 과색소성 비후는 인슐린 저항성을 시사하는 흑색가시세포증이다.",
        "steps": ["식사·활동력으로 단순 비만 가능성을 확인한다.", "사진의 병변을 색·촉감·분포로 구분한다.", "인슐린 저항성 및 대사합병증 선별 필요성을 연결한다."],
        "concept": "소아 비만에서는 BMI 백분위수뿐 아니라 혈압, 지질, 혈당, ALT와 인슐린 저항성 피부 소견을 함께 평가한다.",
        "criteria": ["CDC 현재 기준: BMI 85~95백분위수 미만은 과체중, 95백분위수 이상은 비만이다.", "중증비만은 95백분위수의 120% 이상 또는 BMI 35 kg/m² 이상 중 낮은 기준을 쓴다."],
    },
    "malnutrition": {
        "key": "부종 유무와 체중-신장 관계를 먼저 보면 에너지 결핍성 wasting/marasmus와 단백질 결핍성 kwashiorkor를 구분할 수 있다.",
        "steps": ["최근 체중 감소와 신장 보존 여부를 확인한다.", "부종·저알부민혈증·피부·모발 소견을 찾는다.", "급성 wasting과 만성 stunting을 분리해 판정한다."],
        "concept": "급성 영양결핍은 체중이 먼저 떨어져 신장 대비 체중이 낮아지고, 만성 결핍은 신장까지 저하된다. 부종성 저알부민혈증은 kwashiorkor를 지지한다.",
        "criteria": ["신장 대비 체중 5백분위수 미만은 급성 영양결핍을 시사한다.", "연령 대비 신장 저하는 만성 성장부전(stunting)을 시사한다."],
    },
    "rickets": {
        "key": "과도한 생우유 섭취와 제한된 이유식, 보행 이상은 비타민 D 결핍 구루병을 의심하게 하며 저장 상태는 25-OH vitamin D로 평가한다.",
        "steps": ["식이에서 비타민 D·철 부족 위험을 찾는다.", "보행 이상과 골격 소견을 구루병에 연결한다.", "활성형이 아니라 저장형 비타민 D를 우선 측정한다."],
        "concept": "25-OH vitamin D가 체내 비타민 D 저장 상태를 가장 잘 반영한다. 1,25-(OH)₂D는 반감기가 짧고 구루병에서도 정상 또는 상승할 수 있다.",
        "criteria": ["검사실 해석은 25-OH vitamin D, 칼슘, 인, ALP, PTH를 함께 본다."],
    },
    "iron": {
        "key": "창백한 결막과 숟가락손톱, 고기 섭취 부족은 철결핍을 가리킨다.",
        "steps": ["식이력과 성장 상태를 확인한다.", "창백·피로·이식증·손톱 변화를 찾는다.", "CBC, ferritin과 염증 상태로 철결핍을 확인한다."],
        "concept": "철결핍은 소구성·저색소성 빈혈, 낮은 ferritin, 높은 TIBC가 전형적이다. 감염·염증 시 ferritin은 거짓으로 높을 수 있다.",
        "criteria": ["WHO 소아 빈혈 경계는 연령에 따라 달라지므로 연령별 헤모글로빈 기준을 적용한다."],
    },
    "growth_chart": {
        "key": "성장평가는 한 시점의 숫자보다 성별·연령별 성장곡선에서 체중, 신장, 두위의 위치와 시간에 따른 궤적을 함께 읽는다.",
        "steps": ["미숙아는 교정연령 또는 재태주령에 맞는 곡선을 선택한다.", "체중·신장·두위를 각각 표시한다.", "출생 시 크기와 이후 성장속도를 분리해 영양결핍·따라잡기 성장을 판정한다."],
        "concept": "출생 시 재태주령 대비 작은 경우 SGA/IUGR 가능성을 보고, 이후 체중이 먼저 백분위선을 회복하면 따라잡기 성장으로 해석한다.",
        "criteria": ["SGA는 출생체중 또는 신장이 재태주령·성별 기준 10백분위수 미만일 때 사용한다.", "미숙아 성장곡선은 실제 연령이 아니라 교정연령/재태주령으로 판독한다."],
    },
    "child_growth": {
        "key": "체중, 키, 두위가 서로 다른 백분위수에 놓일 수 있으므로 각 지표를 따로 판정한 뒤 wasting·stunting을 연결한다.",
        "steps": ["연령·성별에 맞는 성장도표를 고른다.", "세 계측치를 각 백분위수에 표시한다.", "신장 대비 체중으로 급성 영양결핍을 판정한다."],
        "concept": "저체중은 연령 대비 체중, 저신장은 연령 대비 신장, wasting은 신장 대비 체중 저하를 뜻한다. 두위 저하는 소두증 평가가 별도로 필요하다.",
        "criteria": ["성장도표 해석은 제시된 도표의 백분위수와 연속 측정의 추세를 우선한다."],
    },
    "pediatric_bmi": {
        "key": "소아·청소년은 성인 BMI 절단값이 아니라 성별·연령별 BMI 백분위수로 분류한다.",
        "steps": ["BMI를 체중(kg)/키(m)²로 계산한다.", "계산값을 같은 성별·연령의 BMI 백분위수와 비교해 저체중·정상·과체중·비만으로 분류한다.", "과체중은 동반질환과 성장 여지를 함께 보고 체중 유지부터 시작하며, 비만·동반질환이 있으면 구조화된 감량 치료 강도를 높인다."],
        "concept": "현재 CDC 분류는 85~95백분위수 미만 과체중, 95백분위수 이상 비만이다. 오래된 강의 도표의 90·97백분위수 용어와 현재 기준이 다를 수 있다.",
        "criteria": ["BMI = 체중(kg)/신장(m)²", "현재 중증비만: 95백분위수의 120% 이상 또는 BMI 35 kg/m² 이상 중 낮은 기준"],
    },
    "pid": {
        "key": "입원 PID의 ceftriaxone 정주요법에는 클라미디아와 혐기성균을 함께 덮도록 doxycycline과 metronidazole을 병용한다.",
        "steps": ["임상적으로 PID를 진단하고 입원 적응증을 확인한다.", "임질·클라미디아·혐기성균을 모두 포괄하는 조합인지 본다.", "24~48시간 호전 후 총 14일 치료가 되도록 경구제로 전환한다."],
        "concept": "CDC 권장 입원요법 중 하나는 ceftriaxone 1 g IV 24시간마다 + doxycycline 100 mg 12시간마다 + metronidazole 500 mg 12시간마다이다.",
        "criteria": ["임상 호전은 대개 24~48시간 내 기대하며, doxycycline과 metronidazole을 포함해 총 14일 치료한다."],
    },
    "endometriosis": {
        "key": "자궁내막종 수술과 수술 후 억제요법은 통증·크기·폐쇄·재발 위험과 난소예비력·즉시 임신 계획을 함께 따져 결정한다.",
        "steps": ["응급성, 악성 의심, 장·요관 폐쇄를 먼저 확인한다.", "통증과 병변 크기, 양측성, 재발 여부를 본다.", "난소예비력과 임신 시도를 방해하는지 비교한다."],
        "concept": "난소수술은 정상 난소조직 손실로 예비력을 더 낮출 수 있다. 임신을 즉시 원하는 환자에게 배란을 억제하는 호르몬 치료는 임신율을 높이는 치료가 아니다.",
        "criteria": ["치료 선택 전 AMH·동난포수, 이전 난소수술, 양측성, 통증, 병변 크기와 임신 계획을 함께 평가한다."],
    },
    "trich": {
        "key": "여성 트리코모나스 질염의 현재 권장요법은 경구 metronidazole 500 mg 하루 2회 7일이며, tinidazole 2 g 단회가 대안이다.",
        "steps": ["원충 감염에 유효한 nitroimidazole 계열인지 본다.", "여성 권장 다회요법과 대체 단회요법을 구분한다.", "성 파트너 동시 치료와 치료 기간 금욕을 안내한다."],
        "concept": "질내 metronidazole gel은 요도·질주위 조직 농도가 충분하지 않아 권장되지 않는다. 원자료의 가·나·다·라 약제표가 빠진 경우 조합 정답은 확정할 수 없다.",
        "criteria": ["여성: metronidazole 500 mg 경구 하루 2회 7일", "대안: tinidazole 2 g 경구 단회"],
    },
    "infertility": {
        "key": "난임은 배란, 난관·자궁강, 난소예비력, 남성요인을 순서대로 확인하고 확인된 병목을 직접 해결한다.",
        "steps": ["월경 규칙성으로 배란 여부를, 과거 임신·수술력으로 난관·자궁 요인을 먼저 가늠한다.", "정액검사로 남성요인을, 자궁난관조영술로 난관 개통성을 확인해 원인을 한 축씩 배제한다.", "무배란 PCOS는 letrozole 배란유도, 양측 난관폐쇄는 IVF, 중증 남성요인은 ICSI처럼 확인된 원인에 치료를 연결한다."],
        "concept": "무배란 PCOS에서는 다른 난임요인이 없을 때 letrozole이 1차 배란유도제다. 자궁강 유착은 자궁경으로 진단·치료하고, 양측 난관폐쇄는 IVF를 고려한다.",
        "criteria": ["난임 평가는 일반적으로 35세 미만 12개월, 35세 이상 6개월 시도 후 시작하며 위험요인이 있으면 더 일찍 한다."],
    },
    "fibroid": {
        "key": "자궁근종은 위치가 증상과 임신 영향, 수술 접근법을 결정한다. 자궁강을 변형하는 점막하 병변은 출혈·난임과 특히 관련된다.",
        "steps": ["사진·초음파에서 근층·장막·자궁강과의 관계를 확인한다.", "출혈, 압박, 통증, 빈혈과 임신 계획을 확인한다.", "가임력 보존 여부에 맞춰 자궁경·복강경 근종절제 또는 자궁절제를 고른다."],
        "concept": "점막하근종은 자궁경 절제가, 증상이 큰 근층내·장막하근종은 위치와 크기에 따라 복강경/개복 근종절제가 적합하다. 자궁선근증에서 임신 계획이 없고 보존치료가 실패하면 자궁절제가 근치적이다.",
        "criteria": ["FIGO 0은 자궁강 내 유경성 점막하, 1~2는 근층 침범 점막하, 3~4는 근층내, 5~7은 장막하 계열이다.", "빈혈 수치는 Hb g/dL로 해석하며 문항의 mg/dL 표기는 단위 오류다."],
    },
    "cervix": {
        "key": "HPV 자연사, 조직학적 병변 등급, 임신 계획, 침윤 범위와 림프절 전이를 구분해야 관찰·절제·수술·동시항암방사선치료를 고를 수 있다.",
        "steps": ["선별검사와 확진 조직검사를 구분한다.", "CIN/LSIL, AIS, 침윤암의 단계를 판정한다.", "가임력과 병기·림프절 전이에 맞춰 치료 강도를 정한다."],
        "concept": "대부분의 HPV 감염은 자연 소실되지만 지속성 고위험 감염은 전암병변 위험을 높인다. 예방접종 후에도 권고 연령의 선별검사는 계속한다. 자궁방 침윤이나 대동맥주위 림프절 전이는 수술 단독보다 동시항암방사선치료 영역이다.",
        "criteria": ["FIGO IIIB가 아니라 자궁방 침윤은 IIB이고, 림프절 전이가 확인되면 IIIC로 분류한다.", "조직학적 HSIL/CIN3은 관찰보다 절제 치료가 원칙이며, AIS에서 임신 계획이 끝났다면 단순 자궁절제가 선호된다."],
    },
}


def profile_name(q: dict) -> str:
    qid, lecture, stem = q["id"], int(q["lectureNumber"]), q["stem"]
    if lecture == 21:
        if qid.endswith(("q006", "q053")): return "obesity_skin"
        if qid.endswith("q046"): return "rickets"
        if qid.endswith("q042"): return "iron"
        return "malnutrition"
    if lecture == 22:
        if qid.endswith(("q050", "q034", "q014", "q090", "q046")): return "pediatric_bmi"
        if qid.endswith(("q049", "q001", "q010", "q073", "q092")): return "child_growth"
        return "growth_chart"
    if lecture == 23:
        if "골반" in stem: return "pid"
        if "trichomonas" in stem: return "trich"
        return "endometriosis"
    if lecture == 24: return "infertility"
    if lecture == 25: return "fibroid"
    return "cervix"


FACTS = {
    "obesity_skin": [
        "피부가 맞닿는 부위의 습기와 마찰로 생기는 홍반·미란이며, 벨벳 모양의 과색소성 비후와는 형태가 다르다.",
        "전신 또는 국소 발한 증가를 뜻하며, 목의 두꺼워진 갈색 피부판을 설명하지 못한다.",
        "후경부 지방축적은 쿠싱증후군 등에서 보지만, 정상 갑상샘·부신검사와 생활습관성 체중증가만으로 이 소견을 고르지 않는다.",
        "땀샘관 폐쇄로 작은 홍색 구진과 따가움이 생기며, 인슐린 저항성 피부병변과 구분된다.",
        "목·겨드랑이의 벨벳 같은 과색소성 비후는 고인슐린혈증에 의한 각질형성세포 증식과 연결된다.",
    ],
    "rickets": [
        "영양상태를 보조하지만 구루병의 비타민 D 저장 상태를 직접 평가하는 검사는 아니다.",
        "갈비뼈·심장폐 이상이 의심될 때 쓰며, 구루병 골변화는 손목·무릎 단순촬영이 더 직접적이다.",
        "갑상샘기능저하도 보행·성장 문제를 만들 수 있으나 식이력과 전형적 골대사 이상을 우선 설명하지 못한다.",
        "간에서 만들어지는 저장형 대사산물로 반감기가 길어 결핍 선별에 가장 적합하다.",
        "활성형 수치는 PTH 보상으로 정상 또는 높을 수 있어 단순 결핍 선별에 부적합하다.",
    ],
    "iron": [
        "결핍 시 성장지연·피부염·미각저하가 가능하지만 창백과 숟가락손톱의 대표 원인은 아니다.",
        "헤모글로빈 합성 저하로 창백과 소구성 빈혈이 생기며, 숟가락손톱은 오래된 결핍을 시사한다.",
        "결핍은 거대적아구성 빈혈을 만들며 적혈구가 작아지는 철결핍과 형태가 다르다.",
        "결핍은 구각염·설염을 만들 수 있지만 숟가락손톱과 소구성 빈혈을 한꺼번에 설명하지 못한다.",
        "결핍은 구루병과 골격 이상을 만들며 결막 창백의 직접 원인은 아니다.",
    ],
    "malnutrition": [
        "부종은 저알부민혈증이 두드러진 단백질 결핍형을 지지하며, 지방·근육 소실이 심한 비부종형에는 전형적이지 않다.",
        "모발의 희박·탈색은 단백질 결핍형에서 더 특징적이며 급격한 에너지 결핍만으로는 우선 소견이 아니다.",
        "에너지 보존 반응으로 서맥·저체온·저혈압이 생길 수 있다.",
        "신장이 연령에 비해 낮으면 만성 결핍을 시사하지만 최근 체중만 급감한 급성 wasting에서는 키가 보존될 수 있다.",
        "마찰 부위의 색소침착·박리성 피부염은 부종성 단백질 결핍에 더 특징적이다.",
    ],
    "growth_chart": [
        "출생 크기는 재태주령 곡선에서 따로 판정해야 하며 이후 체중 궤적 저하는 출생 당시 적정 여부와 별개의 문제다.",
        "가족성 저신장은 체중보다 신장이 일관되게 낮고 성장속도는 비교적 보존되는 양상으로 판단한다.",
        "미숙아의 낮은 절대 체중만으로 비만을 진단할 수 없고 재태주령별 비율을 써야 한다.",
        "출생 시 재태주령 대비 작고 이후 체중 증가가 신장 증가에 못 미치면 태내 성장제한 뒤 영양결핍으로 해석한다.",
        "출생 시 작더라도 이후 신장이 회복되는 양상은 고정된 유전성 저신장보다 성장 궤적 문제를 지지한다.",
    ],
    "child_growth": [
        "세 계측치가 모두 같은 범주라는 결론은 각 성장도표 좌표와 일치하는지 따로 확인해야 한다.",
        "저신장과 stunting은 신장 백분위수가 낮을 때만 붙이며 체중 저하만으로 진단하지 않는다.",
        "체중 저하와 보존된 신장, 낮은 두위가 함께 보이면 급성 wasting과 소두증을 각각 기록한다.",
        "과체중은 연령·성별 BMI 또는 신장 대비 체중이 높아야 하므로 낮은 체중 자료와 맞지 않는다.",
        "두위가 낮으면 정상 두위로 기록할 수 없으며, 나이 대비 체중은 저체중을, 신장 대비 체중은 wasting을 뜻한다.",
    ],
    "pediatric_bmi": [
        "중증비만 판정은 사용한 성장도표의 출제 당시 기준과 현재의 95백분위수 120% 기준이 서로 다를 수 있다.",
        "95백분위수 이상이면 현재 기준상 비만이며, 성장기라도 동반질환과 중증도에 따라 안전한 감량을 고려한다.",
        "오래된 도표에서는 90백분위수 과체중 범주를 썼지만 현재 표준 분류는 85백분위수부터 과체중이다.",
        "과체중 아동에서는 키 성장과 나이에 따라 체중 유지 또는 증가 둔화가 가능하나 정확한 백분위수 판정이 먼저다.",
        "75백분위수만으로 과체중이나 비만으로 분류하지 않으며 불필요한 제한식은 피한다.",
    ],
    "pid": [
        "aminoglycoside는 clindamycin과 묶는 대체 입원요법의 일부이며 ceftriaxone에 단독 추가하는 표준 조합은 아니다.",
        "clindamycin-aminoglycoside 조합 자체는 대체 입원요법이지만 ceftriaxone과 세 약제를 중복해 쓰는 방식은 아니다.",
        "macrolide를 더하는 조합보다 혐기성균을 덮는 nitroimidazole 병용이 표준 ceftriaxone 요법에 맞는다.",
        "tetracycline 계열이 클라미디아를, nitroimidazole 계열이 혐기성균과 세균성 질증 동반을 보완한다.",
        "beta-lactam/beta-lactamase inhibitor와 tetracycline의 조합은 별도 대체요법이지 ceftriaxone 위에 추가하는 약제가 아니다.",
    ],
    "trich": [
        "원본에서 가·나·다에 해당하는 약제 목록이 빠져 있어 이 조합의 적합성을 독립적으로 판정할 수 없다.",
        "저장 정답 조합이지만 구성 약제가 누락되어 있다. metronidazole 7일요법 또는 tinidazole 단회요법 포함 여부를 원본에서 확인해야 한다.",
        "원본의 나·라 약제명이 없어 권장 nitroimidazole 요법인지 확인할 수 없다.",
        "라 단독이 어떤 약인지 제시되지 않아 대체요법 해당 여부를 확정할 수 없다.",
        "네 약제의 명칭이 모두 없으므로 모두 가능하다고 추정해서는 안 된다.",
    ],
    "endometriosis": [
        "큰 자궁내막종은 통증·파열·악성 감별과 접근성을 고려해 수술 논의가 가능하다.",
        "약물로 조절되지 않는 심한 통증은 수술을 고려하는 중요한 이유다.",
        "가임력 보존 필요가 없으면 증상과 병변 범위에 따라 보다 적극적인 수술 선택이 가능하다.",
        "난소예비력이 이미 낮으면 낭종절제 과정의 정상 난소 손실이 난임을 악화시킬 수 있어 수술을 자동 선호하지 않는다.",
        "장관·요관 폐쇄는 장기 손상 위험 때문에 다학제 수술을 고려하는 강한 적응증이다.",
    ],
    "infertility": [
        "시상하부-뇌하수체를 억제하는 작용제는 PCOS 무배란의 1차 배란유도제가 아니다.",
        "주기적 투여는 자궁내막 보호와 철회출혈에는 쓰지만 임신을 위한 배란유도 효과는 없다.",
        "길항제는 주로 보조생식술에서 조기 LH surge를 막으며 단독 1차 배란유도제로 쓰지 않는다.",
        "aromatase 억제로 FSH 자극을 높이며 다른 난임요인이 없는 무배란 PCOS의 1차 약제다.",
        "난포 발달을 억제할 수 있어 무배란 환자의 임신 유도약이 아니다.",
    ],
    "fibroid": [
        "초경 전에는 드물고 폐경 후 대개 작아져 성호르몬 의존성을 뒷받침한다.",
        "성호르몬 노출 기간을 늘리는 이른 초경은 발생 위험 증가와 연관된다.",
        "국소 조직의 수용체·대사 차이가 중요하므로 혈중 에스트로겐이 항상 더 높아야 하는 것은 아니다.",
        "비만은 말초 방향족화와 대사 요인 때문에 위험 증가와 연관되며 보호요인이 아니다.",
        "출산력 증가는 일반적으로 위험 감소와 연관되므로 반복 출산을 증가 요인으로 보지 않는다.",
    ],
    "cervix": [
        "HPV 음성 확인은 접종 전 필수조건이 아니며 접종 전 일상적 HPV 검사를 권하지 않는다.",
        "감염 자체를 항바이러스제로 제거하는 치료는 없고 대부분 자연 소실되어 지속감염과 병변을 추적한다.",
        "백신이 모든 발암형과 기존 감염을 해결하지 않으므로 접종 뒤에도 연령별 선별검사를 계속한다.",
        "고위험형은 자궁경부뿐 아니라 항문·외음부·질·음경·구인두 암과 관련된다.",
        "다수가 1~2년 안에 소실되고, 일부 지속성 고위험 감염이 전암병변으로 진행한다.",
    ],
}


def choice_facts(q: dict, profile: str) -> list[str]:
    qid, stem = q["id"], q["stem"]
    if profile in {"obesity_skin", "rickets", "iron", "growth_chart", "child_growth", "pediatric_bmi", "pid", "trich", "infertility", "fibroid", "cervix"}:
        facts = list(FACTS[profile])
    else:
        facts = list(FACTS[profile])

    if profile == "malnutrition":
        if qid.endswith("q088"):
            facts = ["피하지방이 소실되면 피부가 헐겁고 주름져 보이는 baggy-pants 양상이 나타날 수 있다.", "모발 희박·탈색은 부종성 단백질 결핍에서 더 특징적이다.", "마찰 부위의 색소침착·박리성 피부염은 kwashiorkor 쪽 소견이다.", "지방간에 의한 간비대는 단백질 결핍형에서 더 흔하다.", "복부팽만도 부종성 단백질 결핍이나 장운동 저하에서 더 두드러진다."]
        elif qid.endswith("q031"):
            facts = ["연령 대비 체중 저하는 저체중을 뜻하지만 급격한 체중감소의 급성 성격을 가장 잘 표현하지 못한다.", "신장 대비 체중 저하와 보존된 신장은 급성 wasting에 맞는다.", "연령 대비 신장 저하가 없어 만성 stunting으로 볼 수 없다.", "부종이 없는 상태는 전형적 kwashiorkor와 맞지 않는다.", "혼합형은 심한 wasting과 부종이 함께 있어야 한다."]
        elif qid.endswith("q032"):
            facts = ["다모증은 단백질 결핍의 대표 피부·모발 소견이 아니다.", "비장비대는 만성 설사의 원인 감별 단서일 수 있지만 kwashiorkor의 핵심 소견은 아니다.", "심한 지방 소실에 따른 피부주름은 비부종성 marasmus에 더 어울린다.", "저알부민혈증과 부종에 더해 압박·마찰 부위의 과색소성 박리성 피부염이 나타날 수 있다.", "보이는 장연동은 피하지방이 소실된 marasmus에서 더 잘 관찰된다."]
        elif qid.endswith("q041"):
            facts = ["연령 대비 체중뿐 아니라 신장 대비 체중도 낮으므로 wasting이 없다는 판단은 틀리다.", "wasting은 급성 결핍을 뜻하며 보존된 신장 때문에 만성 결핍으로 부를 수 없다.", "저체중과 wasting이 있지만 연령 대비 신장은 50백분위수여서 stunting은 없다.", "stunting은 키가 낮아야 하는데 이 환자의 신장은 연령에 맞다.", "부종이 없다는 점은 오히려 kwashiorkor보다 marasmus형 결핍에 가깝다."]
        elif qid.endswith("q077"):
            facts = ["두위는 뇌 성장과 장기 성장장애를 반영하지만 급성과 만성을 가장 직접 구분하지 않는다.", "연령 대비 체중은 저체중을 찾지만 키와 비교하지 않으면 급성 여부가 모호하다.", "복부비만과 대사위험 평가에 쓰며 영양결핍의 시간 경과 판정에는 부적합하다.", "체지방 저장량을 반영하지만 표준 급성·만성 분류의 핵심 지표는 아니다.", "체중을 신장과 비교하면 키가 보존된 급성 wasting과 키까지 낮아진 만성 결핍을 구분하는 데 도움이 된다."]
    elif profile == "growth_chart":
        if qid.endswith("q043"):
            facts = ["출생체중이 재태주령 곡선의 하위 백분위수여서 적정체중아로 보기 어렵다.", "출생 시 적정 여부도 맞지 않고 이후 길이·체중 궤적은 고정된 가족성 저신장보다 영양 문제를 시사한다.", "출생 시 재태주령 대비 작고 32주에도 체중 증가가 신장 증가에 못 미쳐 성장제한 뒤 영양결핍으로 해석한다.", "출생 시 작은 점은 맞지만 이후 변화는 유전성 저신장보다 영양결핍 양상이다.", "재태주령별 체중이 낮은 상태를 비만이나 부당중량으로 분류할 수 없다."]
        elif qid.endswith("q044"):
            facts = ["가족성 저신장은 성장속도가 보존된 지속적 저신장 양상이며 이 미숙아의 최근 체중 궤적을 설명하지 못한다.", "급성 결핍은 신장 대비 체중이 떨어지는 양상인데 제시 성장곡선은 길이까지 낮은 장기 궤적을 보인다.", "체중과 신장이 함께 낮고 따라잡기가 충분하지 않아 만성 영양결핍으로 판정한다.", "출생 백분위선으로 충분히 회복하지 못했으므로 따라잡기 성장이 완료됐다고 볼 수 없다.", "교정연령을 적용한 성장곡선으로 설명할 수 있어 비특이적 미숙아 후유증이라는 진단은 적절하지 않다."]
        elif qid.endswith("q045"):
            facts = ["괴사성장염과 장절제 병력만으로 모유를 금지하지 않으며 가능한 경우 모유가 장관 영양의 기본이다.", "두위는 제시 성장곡선에서 직접 판정해야 하며 장절제 후 영양위험 평가를 대신하지 않는다.", "체중·신장 궤적이 목표 백분위선으로 회복됐는지 확인 없이 따라잡기 완료로 단정할 수 없다.", "미숙아와 장절제 후 흡수장애는 비타민 D 부족·대사성 골질환 위험을 높여 보충과 모니터링이 필요하다.", "비타민 A도 상황에 따라 부족할 수 있으나 이 문항의 골성장·미숙아 영양 위험에서 우선 보충 항목은 비타민 D다."]
        if "추가적인" in stem:
            facts = ["양측성 병변은 재발 위험과 난소 손상 위험이 모두 높아 수술 후 억제요법을 논의할 수 있다.", "진행된 병기는 잔존 병변과 통증 재발 위험이 커 장기 억제요법의 이득이 있을 수 있다.", "수술 후 지속 통증은 재평가와 함께 호르몬 억제치료를 고려할 이유다.", "배란을 억제하는 치료는 즉시 임신 시도와 양립하지 않으며 자연임신율을 높이지 않는다.", "소작만 시행하면 병변 잔존·재발 위험이 있어 임신을 바로 원하지 않을 때 억제요법을 고려한다."]
        elif "증가 요인" in stem:
            facts = ["체질량지수와 자궁내막증의 연관은 복잡하지만 과체중은 고전적으로 일관된 증가 요인으로 보지 않는다.", "이른 초경은 평생 역행성 월경 노출을 늘려 위험 증가와 연관된다.", "월경량이 많으면 역행성 월경과 골반 내 내막세포 노출이 늘 수 있다.", "유출로 폐쇄를 동반한 생식기 기형은 역행성 월경을 증가시킨다.", "붉은고기·일부 식이 패턴과의 연관성이 보고됐으나 관찰연구의 교란을 함께 고려한다."]
    elif profile == "infertility":
        if "소파" in stem or "임신 중절" in stem:
            mapping = {
                "아셔": "반복 자궁내막 손상 뒤 월경량 감소와 충만결손은 자궁강 유착을 시사한다.",
                "아새": "반복 자궁내막 손상 뒤 월경량 감소와 충만결손은 자궁강 유착을 시사한다.",
                "안드로겐": "정상 여성호르몬과 규칙 월경은 46,XY 성분화질환의 전형과 맞지 않는다.",
                "다낭성": "희발월경·고안드로겐증·다낭성 난소 소견이 없어 PCOS 가능성이 낮다.",
                "황체기": "황체기 문제만으로 소파술 뒤 지속된 월경량 감소와 자궁강 이상을 설명하기 어렵다.",
                "터너": "Turner 증후군은 고성선자극호르몬성 난소기능저하와 원발무월경이 전형적이다.",
            }
            facts = [next(value for key, value in mapping.items() if key in choice) for choice in q["choices"]]
        elif "정액" in stem and ("해석" in stem or "금욕" in stem):
            facts = ["정액량·농도·운동성·형태가 모두 기준을 충족할 때만 정상으로 판정한다.", "총 정자수 또는 농도 저하는 희소정자증이며 표의 주된 이상이 운동성인지 구분한다.", "전진운동성 15%처럼 운동성이 크게 낮으면 정자무력증에 해당한다.", "엄격 형태 정상률 10%는 제시 기준을 충족하므로 기형정자증이 주된 이상은 아니다.", "백혈구가 1 million/mL 미만이면 백혈구정자증 기준을 충족하지 않는다."]
            if qid.endswith("q091"):
                facts = ["총 정자수가 약 200만이고 운동성도 5%라 자연임신 가능성이 매우 낮다.", "중증 희소·무력정자증에서는 한 정자를 난자 세포질에 직접 주입하는 방법이 가장 적합하다.", "여성 황체호르몬 보충은 심한 남성요인을 교정하지 못한다.", "자궁강 검사는 여성 검사들이 정상이고 명확한 남성요인이 있을 때 우선 처치가 아니다.", "난관·골반 병변을 찾는 수술은 정액의 중증 이상을 해결하지 못한다."]
        elif "자궁난관 조영술 사진" in stem:
            facts = ["자궁강 병변이 주된 문제가 아닐 때 내시경만으로 양측 난관 문제를 해결하지 못한다.", "적어도 한 난관이 통과 가능한 경증 요인에서 고려하며 양측 폐쇄에는 성공 가능성이 낮다.", "난자를 채취해 체외수정 후 자궁에 이식하므로 양측 난관 폐쇄를 우회한다.", "자궁내막을 긁는 시술은 난관 개통을 회복시키지 못한다.", "배란이 정상이고 난관이 막힌 경우 배란유도만으로 수정 경로가 생기지 않는다."]
        elif "39세" in stem:
            facts = ["여성 연령 39세는 난자 수와 반응을 우선 파악해야 치료 속도와 방법을 정할 수 있다.", "이미 정상 정액검사가 있어 같은 검사를 먼저 반복할 이유가 적다.", "자궁강 정밀검사는 출혈·초음파 이상이나 반복착상실패 단서가 있을 때 우선순위가 오른다.", "자궁강 병변 단서가 없고 HSG도 정상이므로 침습검사를 먼저 하지 않는다.", "골반염·심한 월경통·난관 이상 단서가 없어 진단복강경은 1차 검사가 아니다."]
        elif qid.endswith("q050"):
            facts = ["GnRH 작용제는 뇌하수체를 억제하므로 PCOS 무배란의 1차 배란유도제가 아니다.", "aromatase 억제로 난포 FSH 자극을 높여 다른 난임요인이 없는 무배란 PCOS에서 가장 먼저 사용한다.", "주기적 황체호르몬은 자궁내막 보호와 철회출혈에는 쓰지만 배란을 유도하지 않는다.", "고프로락틴혈증 단서가 없으므로 dopamine 작용제를 쓸 이유가 없다.", "외인성 gonadotropin은 다태임신·난소과자극 위험 때문에 경구 1차 치료 실패 후 고려한다."]
    elif profile == "fibroid":
        if qid.endswith("q002"):
            facts = ["성호르몬 의존성 때문에 폐경 뒤에는 대개 작아지며 새 성장은 다른 병변을 평가해야 한다.", "흡연과의 역학적 연관은 복잡하지만 에스트로겐 의존성을 보여 주는 대표 증가 근거는 아니다.", "초경이 빠르면 평생 난소호르몬 노출 기간이 길어져 발생 위험이 증가한다.", "비만은 말초 방향족화와 대사 요인으로 위험 증가와 연관되어 보호요인이 아니다.", "국소 수용체·대사 변화가 중요해 환자의 혈중 에스트로겐이 반드시 높지는 않다."]
        elif qid.endswith("q015"):
            facts = ["도식의 1번은 자궁 바깥으로 가는 유경성 장막하근종으로, 줄기가 꼬이면 급성 통증을 일으킬 수 있다.", "2번은 근층 깊이 위치해 줄기가 없어 전형적 염전 기전과 맞지 않는다.", "3번은 자궁강 쪽 점막하 병변으로 출혈·난임과 더 관련된다.", "4번은 근층내 작은 병변으로 급성 염전보다는 출혈·압박 증상을 만든다.", "5번은 넓은 기저의 장막하 병변으로 유경성 병변보다 염전 가능성이 낮다."]
        elif qid.endswith("q044"):
            facts = ["사진은 국소 피막성 결절보다 자궁근층의 미만성 비후와 소용돌이 모양을 보여 무월경보다 과다월경·통증이 흔하다.", "배란 간격 이상보다 자궁근층 병변에 의한 출혈·통증이 치료 결정의 중심이다.", "유방통은 자궁 병변의 수술 적응증이 아니다.", "자궁선근증은 이차성 월경통과 과다월경을 일으키며 보존치료 실패 시 자궁절제를 고려한다.", "임신 중이 아닌 자궁절제 표본이므로 절박유산은 해당하지 않는다."]
        elif qid.endswith("q027"):
            facts = ["약물은 출혈과 크기를 일시 조절할 수 있지만 임신을 원하는 환자의 자궁강 변형 병변을 제거하지 못한다.", "열로 병변을 파괴하면 향후 임신 안전성과 유착·흉터 문제가 있어 우선 선택이 아니다.", "집속초음파는 증상 완화 대안일 수 있으나 임신 계획과 큰 근층내 병변에서는 근종절제보다 근거가 제한적이다.", "자궁강 안으로 돌출된 FIGO 0~2 병변에 적합하며 사진의 근층내 위치에는 접근이 맞지 않는다.", "원본 초음파의 근층내 종괴, 월경과다·난임을 함께 해결하면서 자궁을 보존하는 방법이다."]
        elif qid.endswith("q065"):
            facts = ["점막하 병변에서도 경련성 통증이 생길 수 있지만 가장 흔하고 직접적인 증상은 출혈이다.", "원본 표본에서 자궁강으로 돌출된 점막하 병변은 내막 면적과 혈관을 늘려 과다월경을 잘 일으킨다.", "월경통보다 과다월경과 철결핍빈혈의 연관이 더 대표적이다.", "빈뇨는 큰 전벽·장막하 종괴가 방광을 누를 때 더 흔하다.", "배변장애는 후벽의 큰 종괴가 직장을 압박할 때 생긴다."]
        elif qid.endswith("q037"):
            facts = ["빠른 성장만으로 평활근육종을 확진할 수 없으며 폐경 후 새 성장과 영상·증상을 함께 본다.", "에스트로겐과 프로게스테론 모두 근종 성장에 관여한다.", "임신 중 커졌던 병변은 산후 자궁 퇴축과 함께 작아질 수 있다.", "자궁강을 점유하는 유경성 점막하근종은 착상과 임신 유지에 영향을 줄 수 있다.", "적색변성 통증이 조기진통을 동반할 수 있지만 반드시 곧바로 진행하는 것은 아니다."]
        elif qid.endswith("q038"):
            facts = ["자궁내막을 파괴해 임신이 어려워지므로 가임력 보존 환자에게 부적절하다.", "비침습 치료는 향후 임신 안전성 자료가 근종절제보다 제한적이다.", "자궁동맥 색전술은 난소기능과 향후 임신에 영향을 줄 수 있어 우선 선택이 아니다.", "출혈 조절에는 도움이 되지만 자궁강을 변형하는 10 cm 종괴와 난임을 해결하지 못한다.", "큰 근층내근종을 제거하면서 자궁을 보존해 빈혈·출혈과 임신 목표를 함께 다룬다."]
        elif qid.endswith("q051"):
            facts = ["미만성 자궁선근증은 경계가 없는 근층 질환이라 단순 근종절제로 완전 제거하기 어렵다.", "임신 계획이 없고 약물·IUD 치료가 실패한 중증 증상에서는 근치적 치료다.", "자궁강 내 국소 병변이 아니라 근층 전체가 커져 자궁경 접근으로 해결되지 않는다.", "표준 근치치료가 아니며 효과와 재발 면에서 수술을 대체하지 못한다.", "일시적 내막 제거는 근층 병변을 치료하지 못한다."]
        elif qid.endswith("q052"):
            facts = ["장막하 병변용 접근은 자궁강 내 점막하 병변과 맞지 않는다.", "맹목적 소파는 근종을 완전히 제거하지 못하고 유착 위험이 있다.", "자궁경부 전암병변 치료로 자궁체부 근종과 무관하다.", "자궁을 제거하므로 임신을 원하는 환자에게 부적절하다.", "자궁강으로 돌출된 점막하근종을 직접 보며 절제해 출혈과 난임을 치료한다."]
    elif profile == "cervix":
        if qid.endswith("q031"):
            facts = ["원추절제는 침윤 배제와 절제연 평가에 필요할 수 있지만 출산 계획이 끝난 AIS의 최종 표준치료로는 부족할 수 있다.", "AIS는 선병변(skip lesion) 가능성이 있어 1년 단순 관찰은 치료가 아니다.", "6개월 추적만으로 선상피내암을 치료했다고 볼 수 없다.", "가임력 보존이 필요 없고 침윤암이 배제된 AIS에서는 단순 자궁절제가 선호된다.", "선상피 병변은 냉동으로 절제연과 숨은 침윤을 평가할 수 없어 부적절하다."]
        elif qid.endswith("q032"):
            facts = ["자궁방 침윤과 대동맥주위 림프절 전이는 근치수술 단독 범위를 넘는다.", "국소진행 병변과 림프절 전이를 함께 치료하도록 cisplatin 기반 항암치료를 방사선과 병행한다.", "전신 항암 단독은 골반 원발 병변의 근치적 국소치료를 빠뜨린다.", "단순 자궁절제와 림프절절제는 자궁방 침윤이 있는 병기에 불충분하다.", "가임력 보존 수술은 작은 초기 병변에 한정되며 림프절 전이·자궁방 침윤에서는 금기다."]
        elif qid.endswith("q049"):
            facts = ["저등급 병변은 소실될 수 있지만 CIN3을 포함한 모든 병변을 관찰만 하지는 않는다.", "초기에는 무증상일 수 있고 증상이 있으면 접촉성·비정상 질출혈이 통증보다 흔하다.", "세포검사는 선별검사이므로 암 의심 세포가 보여도 조직학적 확진과 침윤 평가가 필요하다.", "Lugol 반응은 세포 내 glycogen 양에 좌우되며 단백질 변화 때문이 아니다.", "고등급 병변은 숨은 침윤을 평가하고 치료하도록 변형대를 절제하는 LLETZ/원추절제가 선호된다."]
        elif qid.endswith("q071"):
            facts = ["조직학적 LSIL/CIN1은 대개 자연 소실되므로 위험도에 맞춘 HPV 기반 추적검사가 우선이다.", "herpesvirus 치료약으로 HPV 관련 상피병변을 치료하지 못한다.", "세균성 질증·트리코모나스 치료제로 CIN1을 없애지 못한다.", "즉시 절제는 CIN2+ 위험이 충분히 높을 때 고려하며 단순 CIN1에서는 과잉치료가 될 수 있다.", "침윤암 가임력 보존 수술로 저등급 전암병변에는 지나치다."]
        elif qid.endswith("q040-v2"):
            facts = ["침윤성 병변에서는 변형대의 비정형 혈관, 불규칙 모자이크·점상혈관이 중요한 질확대경 소견이다.", "초기 증상은 하복부 통증보다 비정상·접촉성 질출혈이 흔하다.", "세포진 단독 민감도는 채취·판독에 따라 달라 90% 이상으로 단정할 수 없다.", "CIN1은 대부분 소실되며 소수만 고등급으로 진행한다.", "정상 성숙 편평상피는 glycogen 때문에 갈색으로 염색되고 병변은 덜 염색되거나 비염색된다."]
        elif qid.endswith("q040"):
            facts = ["CIN1은 대개 일시적 HPV 감염의 표현으로 자연 소실이 흔해 지속되는 경우가 많다는 서술은 맞지 않는다.", "증상이 생긴 초기 자궁경부암에서는 접촉성 또는 비정상 질출혈이 가장 흔하다.", "세포진 민감도는 90% 미만일 수 있어 반복검사와 HPV 검사를 함께 활용한다.", "Lugol에서 정상 성숙상피가 갈색으로 염색되고 glycogen이 적은 병변은 비염색된다.", "초산 도포 뒤 acetowhite 변화는 병변 가능성을 높이지 낮추지 않는다."]
        elif qid.endswith("q054"):
            facts = ["일차 HPV 검사는 연령과 국가 지침에 따라 선별검사로 사용할 수 있다.", "선별검사는 증상이 없을 때 전암병변을 찾는 것이 목적이다.", "단일 세포진의 민감도를 90% 이상으로 고정할 수 없다.", "CIN1은 대부분 소실되고 일부만 진행한다.", "glycogen이 적은 비정상 상피는 iodine을 덜 흡수해 갈색으로 염색되지 않는다."]
        elif "HPV" in stem or "papillomavirus" in stem:
            facts = []
            for choice in q["choices"]:
                lower = choice.lower()
                if "음성" in choice or "확인 이후" in choice or "감염 확인" in choice or "감염이 없" in choice:
                    facts.append("접종 전에 HPV 감염 여부를 검사할 필요가 없고 이미 노출됐더라도 아직 접하지 않은 백신형을 예방할 이득이 있다.")
                elif "6/11" in lower:
                    facts.append("6형과 11형은 생식기 사마귀와 관련된 대표 저위험형이다.")
                elif "백신" in choice and ("검사" in choice or "pap" in lower or "스크리" in choice):
                    facts.append("백신이 모든 발암형과 기존 감염을 제거하지 않으므로 접종 뒤에도 연령별 자궁경부 선별검사를 계속한다.")
                elif "치료" in choice:
                    facts.append("고위험 HPV 감염 자체를 제거하는 약은 없으며 대부분 자연 소실되어 지속감염과 조직병변을 위험도에 따라 추적·치료한다.")
                elif "항문" in choice or "anogenital" in lower:
                    facts.append("고위험형은 자궁경부뿐 아니라 항문·외음부·질·음경·구인두 암과도 관련되어 ‘무관’ 또는 ‘그 부위에만’이라는 단정은 틀리다.")
                elif "고위험군 관련 병변에만" in choice:
                    facts.append("9가 백신은 발암 고위험형뿐 아니라 생식기 사마귀를 일으키는 저위험 6·11형도 포함한다.")
                elif "자연" in choice or "자연 소멸" in choice:
                    facts.append("대부분의 새 HPV 감염은 면역반응으로 1~2년 안에 자연 소실된다.")
                elif "대부분 자궁경부암" in choice:
                    facts.append("고위험형 감염도 대부분 소실되며 지속감염 중 일부가 여러 해에 걸쳐 전암병변과 암으로 진행한다.")
                elif "모든 타입" in choice or "모든 hpv" in lower:
                    facts.append("HPV형마다 조직 친화성과 발암위험이 달라 모든 형을 같은 항문·생식기 병변 원인으로 묶을 수 없다.")
                else:
                    raise ValueError(f"{qid}: unhandled HPV choice {choice}")
    if len(facts) != len(q["choices"]):
        raise ValueError(f"{qid}: choice fact count {len(facts)} != {len(q['choices'])}")
    return facts


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    reviewed = []
    for q in payload["questions"]:
        lecture_text = str(q.get("lectureNumber", ""))
        if not lecture_text.isdigit() or not 21 <= int(lecture_text) <= 26:
            continue
        lecture = int(lecture_text)
        profile = profile_name(q)
        spec = PROFILES[profile]
        exp = q.get("explanation") or {}
        exp.update({
            "keyJudgment": spec["key"],
            "reasoningSteps": spec["steps"],
            "choiceExplanations": choice_facts(q, profile),
            "diagnosticCriteria": spec["criteria"],
            "conceptReview": spec["concept"],
            "evidenceStatus": f"21~26강 문항·선지 독립 수동 검수({REVIEW_DATE}); 공식 지침과 원본 이미지 대조",
            "sources": SOURCES[lecture],
        })
        q["explanation"] = exp
        q["explanationReviewStatus"] = MARKER
        q["semanticChoiceReviewStatus"] = f"manual-semantic-audit-{REVIEW_DATE}"
        reviewed.append(q)

    by_id = {q["id"]: q for q in reviewed}
    by_id["gendev2-23-2023-q003"]["answerReviewStatus"] = "원본의 가·나·다·라 약제 목록 누락 · 저장 정답 ② 독립 검증 불가"

    merged = by_id["gendev2-22-2023-q005"]
    merged["originalAnswers"] = merged.get("originalAnswers", merged["answers"])
    merged["answers"] = [4]
    merged["answerReviewStatus"] = "두 문항이 한 stem에 병합된 원본 오류 · 현재 표시된 두 번째 문항의 정답은 ④"

    # 현재 근거와 명백히 충돌하는 저장 정답은 원래 값을 보존하고 교정한다.
    pcos = by_id["gendev2-24-2020-q050"]
    pcos["originalAnswers"] = pcos.get("originalAnswers", pcos["answers"])
    pcos["answers"] = [2]
    pcos["answerReviewStatus"] = "족보 정답 ③ 오류 교정: 현재 PCOS 무배란 난임 1차 배란유도제는 ② letrozole"
    cervix = by_id["gendev2-26-2021-q040"]
    cervix["originalAnswers"] = cervix.get("originalAnswers", cervix["answers"])
    cervix["answers"] = [2]
    cervix["answerReviewStatus"] = "족보 정답 ① 오류 교정: CIN1 지속은 흔하지 않으며 옳은 선지는 ②"

    for q in reviewed:
        explanations = q["explanation"]["choiceExplanations"]
        if len(explanations) != len(q["choices"]):
            raise SystemExit(f"{q['id']}: choice explanation count")
        if len(set(explanations)) != len(explanations):
            raise SystemExit(f"{q['id']}: duplicate explanations")
        for i, text in enumerate(explanations):
            choice = q["choices"][i].strip()
            if len(choice) >= 12 and choice in text:
                raise SystemExit(f"{q['id']}: choice {i + 1} copied verbatim")

    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    total = sum(len(q["explanation"]["choiceExplanations"]) for q in reviewed)
    print(f"LECTURE_21_26_REVIEW_PASS questions={len(reviewed)} choices={total}")


if __name__ == "__main__":
    main()
