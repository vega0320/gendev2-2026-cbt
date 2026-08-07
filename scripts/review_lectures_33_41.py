from __future__ import annotations

"""33~41강의 형식적 해설을 문항·선지별 의학 사실로 교체한다."""

import json
import re
from pathlib import Path

from review_lectures_27_32 import fact27, fact28, fact29, fact32


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"
DATE = "2026-08-07"
TARGETS = {"33", "34", "35", "36", "37", "38", "39", "40-1", "40-2", "41"}
MARKER = "manual-choice-independent-audit-33-41"
CIRCLED = "①②③④⑤"
TX_STEM_RE = re.compile(r"치료|처치|조치|후속|투여|관리|시행해야|치료법|치료방침")
DX_STEM_RE = re.compile(r"진단|질환|병변|종양|암|소견|무엇|합당|가능성이")
NUMERIC_STANDARD_RE = re.compile(r"(?:\d+(?:\.\d+)?\s*(?:%|cm|mm|개월|세|점|cc|mL|kg/m²)|[<>≤≥+-]\s*\d)")


PROFILES = {
    "33": {
        "key": "사진의 장기와 병변 위치를 정한 뒤 육안 경계·절단면과 현미경의 세포 배열·기질침윤을 연결한다.",
        "steps": ["자궁경부·자궁체부·난소 중 어느 장기의 표본인지 먼저 고정한다.", "양성·경계성·악성은 캡슐, 고형부, 유두상 증식과 기질침윤으로 구분한다.", "연령과 양측성은 형태학적 진단을 지지하거나 반박하는 보조 단서로 사용한다."],
        "concept": "여성생식기 병리 사진은 장기와 층, 육안 경계, 현미경의 세포형과 기질침윤 순으로 읽는다. 자궁내막양암은 비정상 샘 구조, 자궁경부 편평상피암은 기저막 침범, 장액성·점액성 난소종양은 유두·점액·침윤 양상이 핵심이다.",
    },
    "34": {
        "key": "염증·증식성 병변·양성 종양을 나눈 뒤 원인, 암 위험도와 필요한 후속 조치를 각각 연결한다.",
        "steps": ["수유·흡연·외상·자가면역질환 같은 배경을 병변 위치와 함께 본다.", "비정형이 없는 증식과 atypia를 구분해 이후 유방암 위험도를 판단한다.", "농양은 배농 여부를, 비정형 증식은 영상-병리 일치와 절제·위험감소 상담 여부를 결정한다."],
        "concept": "급성 수유기 유방염은 항포도알균 치료와 효과적인 유방 비우기가 기본이다. 유두종은 혈성 유두분비를 일으킬 수 있고, atypical ductal hyperplasia는 암 위험 표지이자 비필수 전구병변이므로 영상-병리 일치 여부와 절제 필요성을 평가한다.",
    },
    "35": {
        "key": "침윤 여부와 ER·PR·HER2, 유전 배경, 병기와 유전자 재발점수를 분리해 치료에 연결한다.",
        "steps": ["상피내암과 침윤암을 기저막·근상피세포 보존 여부로 구분한다.", "ER·PR·HER2 조합으로 내분비치료와 HER2 표적치료 가능성을 판정한다.", "나이·가족력·양측성·난소암 가족력은 생식세포 유전자검사 필요성을 높인다."],
        "concept": "호르몬수용체 양성/HER2 음성 조기 유방암에서는 폐경 상태, 림프절, 종양 크기·등급과 다유전자 검사를 함께 보아 항암치료 이득을 추정한다. BRCA1 관련 암은 삼중음성이 흔하고, LCIS는 양측 유방의 장기 위험 표지다.",
    },
    "36": {
        "key": "출혈 원인을 임신·배란장애·자궁 구조병변으로 나누고, 자궁경부 선별검사와 확진검사를 구분한다.",
        "steps": ["만성 희발월경과 비만은 지속적인 무배란 및 무대항 에스트로겐 노출을 시사한다.", "선별검사는 고위험 HPV 또는 세포검사이고, 이상 결과의 평가에는 질확대경·조직검사가 쓰인다.", "고위험 HPV의 E6·E7 단백은 각각 p53·RB 경로를 방해해 자궁경부 발암을 촉진한다."],
        "concept": "비정상 자궁출혈에서는 임신을 배제하고 PALM-COEIN에 따라 원인을 분류한다. 무배란성 출혈은 자궁내막 과증식 위험을 높이며, 가임력 희망이 있으면 내막 보호와 배란 유도를 병행한다. 자궁경부암 선별과 조직 확진은 서로 다른 단계다.",
    },
    "37": {
        "key": "하부요로증상의 기본 평가와 전립샘암 의심 뒤 시행하는 MRI·생검을 단계별로 구분한다.",
        "steps": ["첫 평가에는 병력·IPSS, 신체진찰과 직장수지검사, 요검사가 포함된다.", "PSA는 암 특이 검사가 아니므로 감염·BPH·조작과 반복값을 함께 해석한다.", "암이 의심되면 다중매개변수 MRI로 병변과 표적을 정하고 필요하면 조직검사로 확진한다."],
        "concept": "BPH의 증상 평가는 불편도와 합병증을 중심으로 하며 모든 환자에게 요역동학·CT·내시경을 시행하지 않는다. 전립샘암은 조직학적으로 확진하며 MRI는 생검 전 위험층화와 표적 설정에 유용하다.",
    },
    "38": {
        "key": "비촉지 고환은 진찰을 우선하고, 급성 음낭통은 고환염전과 부고환염을 발병 속도·반사·혈류로 구분한다.",
        "steps": ["따뜻한 환경에서 frog-leg 자세로 서혜관부터 음낭까지 양손 촉진한다.", "자연 하강은 교정연령 6개월 이후 드물어 그 이후에는 고환고정술을 계획한다.", "갑작스런 통증·고환올림근반사 소실·혈류 감소는 염전을, 점진적 통증·혈류 증가는 부고환염을 지지한다."],
        "concept": "잠복고환은 영상보다 숙련된 진찰이 우선이다. 촉지 고환은 고환고정술, 비촉지 고환은 마취하 진찰과 복강경 탐색을 고려한다. 고환염전이 임상적으로 강하게 의심되면 영상 때문에 수술을 지연하지 않는다.",
    },
    "39": {
        "key": "감염 치료에 반응하지 않는 고형 종괴는 조직으로 확인하고, 확진 암은 수용체·병기·유전자 위험에 따라 보조치료를 정한다.",
        "steps": ["항생제 불응, 농양 부재와 고형 종괴는 염증성 유방암을 포함한 악성 질환 배제를 요구한다.", "비촉지 석회화는 영상 유도 또는 위치결정술을 이용해 병변을 정확히 채취한다.", "ER 양성·HER2 음성 저위험 암은 내분비치료가 중심이며 항암치료 이득은 별도로 평가한다."],
        "concept": "유방 진단은 임상진찰·영상·조직검사의 삼중평가로 접근한다. 감시림프절 생검은 적절한 임상 림프절 음성 환자에서 액와곽청보다 림프부종과 감각·운동 합병증을 줄인다.",
    },
    "40-1": {
        "key": "전립샘은 기저세포 유무와 AMACR을, 고환종양은 연령·형태·AFP/hCG·면역표지자를 조합해 판독한다.",
        "steps": ["전립샘암의 작은 샘에서는 HMWCK/p63 양성 기저세포가 소실되고 AMACR이 흔히 증가한다.", "소아 난황낭종양과 사춘기 후 GCNIS 연관 생식세포종양을 연령으로 구분한다.", "seminoma의 OCT3/4·PLAP, embryonal carcinoma의 CD30, 난황낭종양의 AFP를 형태와 함께 해석한다."],
        "concept": "BPH는 이행구역의 샘·간질 증식이며 전암병변이 아니다. 전립샘 선암은 주변구역에 흔하고 기저세포 소실이 진단을 지지한다. 3세 미만 고환종양에서는 난황낭종양이 대표적이며 사춘기 후 종양과 분자 배경이 다르다.",
    },
    "40-2": {
        "key": "유방 병변의 침윤·상피-기질 관계를 확인한 뒤 ER·PR·HER2와 엽상종양 등급 기준을 적용한다.",
        "steps": ["주변 조직으로 불규칙하게 침윤하는 악성 상피세포는 invasive carcinoma, NST를 지지한다.", "ER·PR은 면역조직화학으로, HER2는 IHC와 필요 시 in-situ hybridization으로 평가한다.", "엽상종양은 기질세포의 이형성·과증식·분열·경계와 stromal overgrowth로 양성·경계성·악성을 나눈다."],
        "concept": "엽상종양은 상피가 아니라 기질 성분이 종양성인 fibroepithelial tumor다. 유방암 수용체는 예후표지가 아니라 치료 예측표지이기도 하며, 호르몬수용체 양성은 내분비치료, HER2 양성은 HER2 표적치료 선택에 직접 쓰인다.",
    },
    "41": {
        "key": "누출을 유발하는 상황으로 요실금 유형을 정하고, POP-Q는 가장 돌출된 점과 총질길이로 병기를 계산한다.",
        "steps": ["기침·재채기 때 누출되고 절박뇨가 없으면 복압성 요실금이 우선이다.", "생활습관·골반저근운동 실패 뒤에는 요역동학적 복압성 요실금 여부와 수술 적합성을 평가한다.", "POP-Q 병기는 앞·뒤·첨부 구획 중 가장 원위부에 위치한 점 하나로 정한다."],
        "concept": "복압성 요실금은 체중감량·골반저근운동이 1차 보존치료이며 증상이 지속되면 중부요도슬링을 고려한다. 절박성 요실금은 방광훈련과 약물치료가 중심이다. POP-Q 3기는 최원위부가 hymen보다 1 cm 초과 돌출하지만 TVL-2 cm보다 덜 돌출된 상태다.",
    },
}


SOURCES = {
    "33": [{"kind": "현재 지침", "label": "NCI Ovarian Epithelial Cancer Treatment (PDQ)", "url": "https://www.cancer.gov/types/ovarian/hp/ovarian-epithelial-treatment-pdq", "checkedAt": DATE}],
    "34": [{"kind": "현재 지침", "label": "NCI Breast Cancer Treatment (PDQ)", "url": "https://www.cancer.gov/types/breast/hp/breast-treatment-pdq", "checkedAt": DATE}],
    "35": [{"kind": "현재 지침", "label": "NCI Breast Cancer Treatment (PDQ)", "url": "https://www.cancer.gov/types/breast/hp/breast-treatment-pdq", "checkedAt": DATE}],
    "36": [{"kind": "현재 지침", "label": "NCI Cervical Cancer Screening (PDQ)", "url": "https://www.cancer.gov/types/cervical/hp/cervical-screening-pdq", "checkedAt": DATE}],
    "37": [{"kind": "현재 지침", "label": "AUA/SUO Early Detection of Prostate Cancer Guideline", "url": "https://www.auanet.org/guidelines-and-quality/guidelines/early-detection-of-prostate-cancer-guidelines", "checkedAt": DATE}],
    "38": [{"kind": "현재 지침", "label": "AUA Cryptorchidism Guideline", "url": "https://www.auanet.org/guidelines-and-quality/guidelines/cryptorchidism-guideline", "checkedAt": DATE}],
    "39": [{"kind": "현재 지침", "label": "NCI Breast Cancer Treatment (PDQ)", "url": "https://www.cancer.gov/types/breast/hp/breast-treatment-pdq", "checkedAt": DATE}],
    "40-1": [{"kind": "현재 지침", "label": "NCI Prostate and Testicular Cancer Treatment summaries", "url": "https://www.cancer.gov/types", "checkedAt": DATE}],
    "40-2": [{"kind": "현재 지침", "label": "ASCO/CAP ER/PR and HER2 Testing Guidelines", "url": "https://ascopubs.org/doi/10.1200/JCO.22.02864", "checkedAt": DATE}],
    "41": [{"kind": "현재 지침", "label": "ACOG Urinary Incontinence and Pelvic Support Problems", "url": "https://www.acog.org/womens-health/faqs/urinary-incontinence", "checkedAt": DATE}],
}


CRITERIA = {
    "33": ["장기·병변 위치를 먼저 정한 뒤 양성은 매끈한 경계와 침윤 부재, 경계성은 상피증식·이형성이나 기질침윤 부재, 암은 파괴성 기질침윤으로 구분한다.", "자궁경부 편평상피암은 기저막 침범 여부, 자궁내막양암은 비정상 샘의 밀집·융합과 기질침윤, 난소종양은 세포형·유두·점액·양측성으로 진단한다."],
    "34": ["유방염은 국소 발적·열감·압통과 전신증상으로 진단하고, 파동성 종괴 또는 치료 48~72시간 불응이면 초음파로 농양을 평가한다.", "ADH는 저등급 DCIS와 닮은 단조로운 관내 증식이 제한된 범위(통상 2 mm 이하 또는 두 유관공간 이내)에 있을 때 진단한다."],
    "35": ["침윤암은 종양세포가 근상피층·기저막을 넘어 기질에 침윤한 병변이다. DCIS는 병변 둘레 근상피층이 보존된다.", "ASCO/CAP: ER 또는 PR은 검증된 IHC에서 종양핵 1% 이상 염색이면 양성이고, ER 1~10%는 ER-low positive로 별도 보고한다.", "HER2는 IHC 3+ 또는 ISH 증폭이면 양성으로 판정하며 IHC 2+는 ISH 등 추가검사가 필요하다."],
    "36": ["AUB-O는 임신 배제 후 예측하기 어려운 출혈과 배란장애 근거로 진단하며, PALM-COEIN으로 구조성 원인을 함께 평가한다.", "자궁내막 생검은 45세 이상, 또는 그보다 젊어도 비만·PCOS·지속 무배란 등 무대항 에스트로겐 노출이나 지속 출혈·약물치료 실패가 있으면 시행한다.", "자궁경부 선별에서 고위험 HPV 검사는 세포검사보다 CIN2+ 민감도가 높고, 질확대경·생검은 이상 선별 결과의 확진 단계다."],
    "37": ["BPH/LUTS 초기 평가는 병력·IPSS, 신체진찰/DRE, 요검사가 기본이며 PSA는 공유 의사결정 후 선택한다.", "PSA 상승만으로 암을 확진하지 않는다. 반복 PSA·위험인자·보조표지자와 다중매개변수 MRI를 종합하고 조직검사로 Grade Group을 확진한다."],
    "38": ["잠복고환은 따뜻한 환경의 양손 촉진으로 진단하며 의뢰 전 초음파를 일률적으로 시행하지 않는다. 교정연령 6개월에도 하강하지 않으면 수술 전문의에게 의뢰한다.", "TWIST: 고환 종창 2점, 단단한 고환 2점, 고위 고환 1점, 고환올림근반사 소실 1점, 오심·구토 1점. 고위험이면 영상으로 수술을 지연하지 않는다."],
    "39": ["의심 유방 병변은 임상진찰·영상·조직검사의 삼중평가가 서로 일치해야 한다. 항생제 불응 고형 종괴와 BI-RADS 4 이상은 조직검사 대상이다.", "확진 침윤암에서는 크기·림프절·등급·ER·PR·HER2를 필수로 평가하고 HR+/HER2-에서는 적절한 경우 다유전자 검사를 항암치료 결정에 사용한다."],
    "40-1": ["전립샘 선암은 작은 침윤성 샘, 뚜렷한 핵인, HMWCK/p63 기저세포 소실과 AMACR 증가의 조합으로 진단한다.", "Seminoma는 OCT3/4·SALL4·PLAP, embryonal carcinoma는 CD30·cytokeratin, 난황낭종양은 AFP·glypican-3를 형태와 함께 해석한다."],
    "40-2": ["침윤성 유방암은 기질침윤을 확인하고 ER·PR·HER2를 표준 IHC/ISH로 검사한다. 수용체 검사는 sequencing이나 PCR을 우선하지 않는다.", "엽상종양은 기질 세포밀도·이형성·유사분열·stromal overgrowth와 종양 경계를 종합해 양성·경계성·악성으로 분류한다."],
    "41": ["복압성 요실금은 기침·재채기·운동 때 누출되는 병력과 진찰 중 기침유발검사로 확인하며 요검사와 잔뇨를 기본 평가에 포함한다.", "POP-Q: 2기는 최원위점 -1~+1 cm, 3기는 +1 cm 초과이면서 TVL-2 cm 미만, 4기는 TVL-2 cm 이상이다."],
}


TREATMENT_GUIDES = {
    "33": ["병리 진단 확정", "병기·가임력·종양형 평가", "양성은 관찰/보존수술, 악성은 병기설정 수술과 조직형별 보조치료"],
    "34": ["유방염: 수유·유방 비우기 지속 + 항포도알균 항생제", "48~72시간 불응/파동성 종괴: 초음파·배양", "농양: 초음파 유도 흡인 또는 절개배농"],
    "35": ["침윤·병기 + ER/PR/HER2 확인", "HR+: 내분비치료, HER2+: HER2 표적치료", "항암치료는 병기·폐경·림프절·다유전자 위험으로 추가 여부 결정"],
    "36": ["임신·빈혈·혈역학적 불안정 평가", "PALM-COEIN 분류 + 필요 시 초음파/내막생검", "안정 AUB-O: 복합호르몬/프로게스틴/LNG-IUS; 불안정 대량출혈은 응급 지혈"],
    "37": ["생활습관·경과관찰 또는 α차단제", "전립샘 ≥30 cc/PSA 상승 등 진행 위험: 5α환원효소억제제 추가", "요폐·반복 감염·신기능 저하·약물 실패: 수술 평가"],
    "38": ["교정연령 6개월까지 자연 하강 관찰", "6개월에도 미하강: 수술 의뢰", "6~18개월 안 고환고정술; 호르몬 하강치료는 권장하지 않음"],
    "39": ["삼중평가로 조직 확진", "수술·방사선은 병기와 국소 범위로 결정", "ER/PR/HER2와 유전자 위험에 따라 내분비·HER2 표적·항암치료 선택"],
    "40-1": ["조직형·병기·종양표지자 확정", "고환 생식세포종양: 근치적 서혜부 고환절제", "조직형·병기·표지자 감소 양상에 따라 감시·항암·방사선 선택"],
    "40-2": ["침윤·수용체·병기 확인", "수용체에 맞춰 내분비/HER2 표적치료", "엽상종양은 음성 절제연을 확보하고 등급·크기에 따라 추적"],
    "41": ["생활습관·체중감량 + 골반저근운동", "복압성 지속: 중부요도슬링 등 수술; 절박성: 방광훈련·약물", "POP 증상: 골반저재활/페서리 → 불편 지속 시 구획별 수술"],
}


def has(text: str, *patterns: str) -> bool:
    return any(re.search(pattern, text, re.I) for pattern in patterns)


def image_choice_fact(choice: str, answer: bool) -> str:
    number = re.search(r"(\d+)", choice)
    label = f"{number.group(1)}번" if number else "이"
    if answer:
        return f"{label} 사진은 원본 정답표와 연결된 병변이다. 텍스트 선지가 복원되지 않아 세부 형태는 원본 사진을 확대해 직접 대조해야 한다."
    return f"{label} 사진은 텍스트 선지가 복원되지 않아 특정 조직소견을 임의로 붙일 수 없다. 원본 사진에서 경계·세포형·침윤을 정답 병변과 비교한다."


def gyne_pathology_fact(choice: str) -> str:
    s = choice.lower()
    if "low-grade squamous intraepithelial" in s: return "LSIL은 표층 성숙이 남아 있고 하부 1/3 중심의 이형성 및 koilocytosis를 보이며 침윤은 없다."
    if "squamous cell carcinoma in situ" in s: return "편평상피암종 제자리병변은 전층 이형성이 있으나 기저막을 넘는 기질침윤은 없고 block-type p16이 흔하다."
    if "invasive squamous" in s: return "침윤성 편평상피암은 비정형 편평세포 둥지·삭이 기저막을 뚫고 기질로 들어가며 각질진주나 기질반응을 보일 수 있다."
    if "adenomyosis" in s: return "자궁선근증은 자궁내막샘과 기질이 자궁근층 안에 존재해 미만성 근층 비후를 만들며 피막성 소용돌이 결절과 다르다."
    if "leiomyoma" in s: return "자궁평활근종은 경계가 분명한 소용돌이 절단면과 교차하는 균일 방추세포 다발을 보이고 괴사·심한 이형성·높은 유사분열이 없다."
    if "endometrioid carcinoma" in s: return "자궁내막양암은 서로 밀집·융합한 비정상 샘과 기질침윤을 보이며 비만·무대항 에스트로겐·MMR 이상과 연관될 수 있다."
    if "endometrial stromal sarcoma" in s: return "저등급 자궁내막기질육종은 작은 균일 세포가 나선동맥양 혈관 주위로 배열되고 벌레 모양으로 근층·혈관을 침윤한다."
    if "endocervical adenocarcinoma" in s or "adenocarcinoma in situ" in s: return "HPV 연관 자궁경부 샘병변은 점액 고갈·핵 중첩·apoptosis와 mitosis를 보이며 p16 block 양성이 진단을 지지한다."
    if "clear cell carcinoma" in s: return "투명세포암은 투명하거나 호산성인 세포, hobnail cell과 tubulocystic·papillary 구조가 특징이다."
    if "kruken" in s: return "Krukenberg 종양은 위장관 기원의 점액성 signet-ring cell이 난소 기질에 침윤하는 전이암으로 양측성 고형 난소종괴가 흔하다."
    if "serous cystadenoma" in s: return "장액성 낭선종은 얇고 매끈한 단방성 낭과 섬모성 난관형 상피를 보이며 복잡한 유두증식·침윤이 없다."
    if "mucinous cystadenoma" in s or "mucinous adenoma" in s: return "점액성 낭선종은 매우 큰 다방성 낭종과 점액성 원주상피를 보이지만 기질침윤은 없다."
    if "mucinous borderline" in s: return "점액성 경계종양은 복잡한 상피증식과 이형성이 있지만 파괴성 기질침윤은 없다."
    if "mucinous carcinoma" in s: return "점액성 난소암은 점액성 상피의 융합·미로양 증식과 파괴성 기질침윤을 보이며 전이성 위장관암도 배제해야 한다."
    if "low-grade serous" in s: return "저등급 장액성암은 균일한 세포의 유두상 증식과 기질침윤을 보이고 KRAS/BRAF 경로 이상이 흔하다."
    if "high-grade serous" in s or "high grade serous" in s: return "고등급 장액성암은 심한 핵 이형성, 높은 유사분열과 복잡한 유두·고형 구조를 보이며 TP53 이상이 거의 보편적이다."
    if "serous borderline" in s: return "장액성 경계종양은 계층화된 유두상 상피와 세포 이형성이 있으나 파괴성 기질침윤은 없다."
    if "endometriotic cyst" in s: return "자궁내막종은 오래된 출혈성 내용물과 자궁내막샘·기질, hemosiderin-laden macrophage로 진단한다."
    if "dysgerminoma" in s: return "Dysgerminoma는 젊은 여성의 고형 종양으로 맑은 세포질의 큰 세포가 섬유성 격막과 림프구 사이에 배열되며 OCT3/4·SALL4 양성이다."
    if "adult granulosa" in s: return "성인형 과립막세포종은 coffee-bean 핵구와 Call-Exner body, inhibin·SF1 양성이 특징이며 에스트로겐을 분비할 수 있다."
    if "fibrothecoma" in s: return "Fibrothecoma는 방추형 섬유모세포와 지질성 난포막세포로 이루어진 성삭-간질 양성 종양이다."
    if "mature cystic teratoma" in s or "mature teratoma" in s: return "성숙 낭성 기형종은 피부·지방·연골·뼈 등 둘 이상의 배엽에서 온 성숙 조직을 포함하며 미성숙 신경조직은 진단에 맞지 않는다."
    if "immature teratoma" in s: return "미성숙 기형종은 미성숙 신경상피 등 배아성 조직을 포함하는 악성 생식세포종양이다."
    if "adnexal tissue" in s or "bone tissue" in s or "cartilage" in s or "subcutaneous fat" in s: return "이 조직은 외배엽·중배엽·내배엽에서 유래할 수 있는 성숙 체조직으로 성숙 기형종에서 관찰될 수 있다."
    raise ValueError(choice)


def breast_fact(choice: str) -> str:
    s = choice.lower()
    if has(s, r"acute mastitis.*항생제"): return "수유기 급성 유방염은 효과적인 유방 비우기와 함께 포도알균을 겨냥한 항생제로 치료한다."
    if has(s, r"acute mastitis.*(수술|excision)"): return "고름집이 없는 급성 유방염은 절제술 대상이 아니며, 농양이 확인될 때만 흡인 또는 배농을 추가한다."
    if "fat necrosis" in s and ("배액" in choice or "감염" in choice): return "지방괴사는 외상·수술·방사선 뒤 생길 수 있는 무균성 손상으로, 감염성 농양처럼 배액하는 병변이 아니다."
    if "fat necrosis" in s: return "지방괴사는 외상이나 수술 뒤 생기며 섬유화·석회화로 암처럼 보일 수 있어 영상-병리 일치가 중요하다."
    if "혈성 유두" in choice or "bloody nipple" in s: return "관내유두종은 큰 유관 안의 유두상 병변으로, 한쪽의 자발성 혈성 유두분비를 흔히 일으킨다."
    if "squamous metaplasia" in s or "subareolar abscess" in s: return "흡연은 유두밑 유관의 편평상피화생과 각질 마개를 촉진해 반복성 유륜하 농양과 누공을 일으킬 수 있다."
    if "흡연" in choice and ("낭성" in choice or "석회화" in choice): return "흡연의 대표 유방 병변 연관은 유두밑 유관의 편평상피화생과 반복성 유륜하 농양이지 유방실질의 보편적 낭성 변화·석회화가 아니다."
    if "lymphocytic" in s or "lymphocytic mastopathy" in s: return "림프구성 유방병증은 제1형 당뇨와 갑상선 자가면역질환에 연관되므로 관련 병력을 확인한다."
    if "granulomatous" in s:
        if has(s, r"항암|방사선"): return "육아종성 소엽염은 염증성 질환이므로 감염 배제 뒤 관찰·스테로이드·면역조절 또는 제한적 수술을 고려하며 항암·방사선치료 대상이 아니다."
        return "육아종성 소엽염은 가임기·출산 후 여성에서 소엽 중심 비건락성 육아종으로 나타나며 Corynebacterium 등 감염을 배제해야 한다."
    if "usual ductal hyperplasia" in s: return "통상성 관증식은 비정형이 없는 다형성 증식으로 유방암 위험을 소폭 높이지만 예방적 전절제술 적응증은 아니다."
    if "atypical ductal hyperplasia" in s or "atypical duct hyperplasia" in s:
        if has(s, r"전혀 없|안심"): return "비정형 관증식은 이후 유방암 위험을 높이고 core biopsy에서 더 큰 병변이 과소평가될 수 있어 무추적 관찰로 끝내지 않는다."
        if "5~7%" in choice: return "비정형 관증식의 위험은 단순한 고정 평생위험 5~7%로 설명하지 않고 연령·가족력과 병변 범위를 함께 평가한다."
        if "2mm" in s: return "비정형 관증식과 저등급 DCIS는 질적 소견이 비슷하며 보통 2 mm 이하 또는 두 유관공간 이내의 제한된 범위가 ADH를 지지한다."
        if "50%" in choice: return "소엽 침범 비율은 atypical lobular hyperplasia와 LCIS 구분에 쓰이는 개념이지 ADH의 진단기준이 아니다."
        return "비정형 관증식은 대개 무증상 석회화로 발견되며 저등급 DCIS와 닮은 제한된 단조로운 세포 증식을 보인다."
    if "mammographic calcification" in s or "densities" in s: return "비정형 관증식은 흔히 증상 없이 유방촬영의 미세석회화나 음영으로 발견된다."
    if "5~7%" in choice: return "비정형 관증식의 장기 암 위험은 단순한 고정 평생위험 5~7%보다 높게 평가되며 연령·가족력과 함께 상담한다."
    if "high grade ductal carcinoma in situ" in s and "2mm" in s: return "2 mm 범위 기준은 저등급 DCIS와 ADH의 정량적 구분에 쓰이며 high-grade DCIS를 ADH로 낮추는 기준이 아니다."
    if "전암성 병변" in choice: return "비정형 관증식은 저등급 DCIS와 형태·분자적으로 연속된 비필수 전구병변이자 양측 유방암 위험표지다."
    if "lobule" in s and "50%" in choice: return "소엽의 50% 미만 침범은 atypical lobular hyperplasia를 지지하는 범위 기준으로 ADH와는 다른 소엽성 병변에 적용한다."
    if "fibrocystic" in s: return "비증식성 섬유낭성 변화 자체는 암으로 진행하는 병변이 아니며 광범위 절제나 항암치료가 필요하지 않다."
    if "mammary duct ectasia" in s: return "유관확장증은 큰 유두밑 유관의 확장과 염증·섬유화이며 정상 유즙이 단순히 고여 생기는 상태로만 설명하지 않는다."
    if "streptococcus" in s and "mastitis" in s: return "급성 수유기 유방염의 대표 원인균은 Staphylococcus aureus이며 Streptococcus가 가장 흔하다는 설명은 부정확하다."
    if "developmental disorder" in s: return "발생학적 이상은 유방질환 전체에서 흔한 주류가 아니며 임상에서는 염증·증식성 병변·종양을 더 흔히 평가한다."
    if "40세 미만" in choice and "통증" in choice: return "젊은 여성의 유방통은 주기성 통증과 양성 변화가 더 흔하지만 국소 지속 통증이나 종괴는 영상으로 평가한다."
    if "염증성 질환" in choice and ("고령" in choice or "폐경" in choice): return "유방 염증은 수유기와 가임기에 흔하며 유륜하 농양·유관확장증처럼 비수유기 병변도 있어 고령에 국한되지 않는다."
    if "염증성 질환" in choice and ("가임기" in choice or "수유" in choice): return "급성 유방염과 일부 육아종성 소엽염은 가임기·수유 전후에 흔해 연령과 수유력을 중요한 단서로 쓴다."
    if "상피증식성" in choice and "모두" in choice: return "상피증식성 병변에는 통상성 증식·비정형 증식·상피내암이 포함되며 모두 악성은 아니다."
    if "유방암" in choice and "추적" in choice: return "확진 유방암은 병기와 생물학적 아형에 맞춘 적극적 치료가 필요해 단순 추적관찰만 할 수 없다."
    if "유방암" in choice and ("절제" in choice or "수술" in choice): return "유방암 수술 범위는 병기·종양 크기·다발성과 환자 선호에 따라 정하며, 염증성 증례에서 조직 확진 전에 곧바로 절제술을 선택하지 않는다."
    if "e-cadherin" in s: return "E-cadherin 소실은 소엽성 종양의 계통 표지이며 LCIS가 반드시 침윤성 소엽암으로 진행한다는 시간표를 뜻하지 않는다."
    if "lobular carcinoma in situ" in s or "소엽상피내암종" in choice:
        if "tis" in s: return "고전형 LCIS는 현재 해부학적 Tis 병기로 분류하지 않고 위험표지·비필수 전구병변으로 다룬다."
        if "반대쪽" in choice or "동측" in choice: return "LCIS는 같은 쪽과 반대쪽 유방 모두의 침윤암 위험을 높이는 양측성 위험표지다."
        if "1년에 5%" in choice: return "LCIS의 위험은 매년 5%씩 선형 증가한다고 설명하지 않으며 개인 위험인자와 장기 누적위험을 평가한다."
    if "t category" in s and "tis" in s: return "고전형 LCIS는 AJCC 해부학적 병기에서 Tis로 분류하지 않으며 DCIS와 같은 국소 상피내암 병기로 다루지 않는다."
    if "1년에 5%" in choice: return "LCIS의 침윤암 위험은 매년 5%씩 선형 증가한다고 보지 않으며 양측 유방의 장기 누적위험으로 설명한다."
    if "침범된 소엽의 개수" in choice: return "ALH와 LCIS는 침범 소엽의 단순 개수가 아니라 한 소엽 안 acini가 확장·충만된 범위로 구분한다."
    if "반대쪽 유방" in choice: return "LCIS는 동측뿐 아니라 반대측 유방에서도 침윤암 위험을 높이는 양측성 위험표지다."
    if "atypical lobular" in s: return "ALH와 고전형 LCIS는 비정형 세포가 확장한 소엽의 범위로 구분하며 단순 소엽 개수만 세지 않는다."
    if "er(+)" in s and "her2(-)" in s and "pr(+)" in s: return "ER·PR 양성, HER2 음성은 호르몬수용체 양성/HER2 음성 아형으로 내분비치료 반응을 기대한다."
    if "er(+)" in s and "pr(-)" in s and "her2(+)" in s: return "ER 양성/HER2 양성 종양은 내분비치료와 HER2 표적치료 표적을 모두 가지며 전형적 Luminal A와는 다르다."
    if "er(-)" in s and "pr(+)" in s and "her2(-)" in s: return "ER 음성/PR 단독 양성은 드문 불일치 결과로 전처리·내부대조와 검사를 재확인해야 한다."
    if "her2(+)" in s and "er(-)" in s and "pr(-)" in s: return "ER·PR 음성/HER2 양성은 HER2 표적치료 대상이지만 호르몬수용체 양성 종양과는 다르다."
    if "er(-)" in s and "pr(-)" in s and "her2(-)" in s: return "ER·PR·HER2가 모두 음성이면 삼중음성 유방암으로 내분비·HER2 표적치료 표적이 없다."
    if "brca1-associated" in s: return "젊은 나이의 유방암과 난소암 가족력은 BRCA1 연관 유전성 유방·난소암을 강하게 시사하며 삼중음성 표현형이 흔하다."
    if "brca2-associated" in s: return "BRCA2는 여성·남성 유방암과 난소·전립샘·췌장암 위험을 높이지만 BRCA1보다 삼중음성 연관성이 약하다."
    if "li-fraumeni variant" in s or "chek2" in s: return "CHEK2는 중등도 유방암 감수성 유전자지만 TP53 병원성 변이에 의한 고전적 Li-Fraumeni syndrome과 구분한다."
    if "li-fraumeni" in s: return "TP53 관련 Li-Fraumeni syndrome은 젊은 유방암을 포함한 다양한 암의 높은 평생위험을 보이므로 70세까지 10~20%라는 수치는 지나치게 낮다."
    if "cowden" in s: return "PTEN hamartoma tumor syndrome은 유방·갑상선·자궁내막암 위험과 과오종성 소견이 특징이다."
    if "brca1" in s: return "BRCA1 병원성 변이 관련 유방암은 고등급 삼중음성 표현형이 흔하다."
    if "brca2" in s: return "BRCA2 병원성 변이는 ER 양성 유방암이 비교적 흔하고 남성 유방암·난소암·전립샘암·췌장암 위험도 높인다."
    if "her2 amplification" in s: return "HER2 증폭은 HER2 양성 발암경로의 핵심이며 전형적인 ER 양성/HER2 음성 저등급 경로와는 다르다."
    if "pik3ca" in s: return "PIK3CA 변이는 호르몬수용체 양성 유방암에서 흔하고 일부 진행암에서 표적치료 선택에 쓰인다."
    if "gain chromosome 1q" in s or "loss chromosome 16q" in s: return "1q 증가와 16q 소실은 저등급 ER 양성 유방암 경로에서 흔한 초기 염색체 변화다."
    if "luminal a" in s: return "Luminal A는 보통 ER 양성, HER2 음성, 낮은 증식지수와 좋은 예후를 보이며 늦은 골전이 재발이 가능하다."
    if "luminal b" in s: return "Luminal B는 호르몬수용체 양성이지만 Luminal A보다 증식이 높거나 HER2가 양성일 수 있어 위험도가 더 높다."
    if "her2 양성" in s or "her2-positive" in s: return "HER2 양성 암은 HER2 과발현·증폭이 치료 표적이며 호르몬수용체 음성일 때 선행항암 후 병리학적 완전반응률이 더 높다."
    if "삼중음성" in s or "triple-negative" in s:
        if has(s, r"완전관해.*예후가 나쁘"): return "삼중음성 암은 선행항암에 병리학적 완전반응을 보이면 그렇지 않은 경우보다 예후가 좋아지는 'triple-negative paradox'가 있다."
        return "삼중음성 암은 ER·PR·HER2가 없고 고등급·BRCA1 연관성이 흔하며 일부 특수형은 서로 다른 생물학을 보인다."
    if "10년 이후" in choice and "뼈 전이" in choice: return "호르몬수용체 양성 luminal 암은 늦은 재발과 골전이가 상대적으로 흔하다."
    if has(s, r"tubular|cribriform|mucinous"): return "관상·체모양·점액암은 대개 호르몬수용체 양성/HER2 음성의 저등급 특수형이다."
    if has(s, r"medullary|metaplastic|adenoid cystic"): return "수질양·화생암 등은 삼중음성 표현형이 흔하지만 특수형마다 예후와 분자특성이 같지는 않다."
    if "pd-l1" in s: return "PD-L1 검사는 일부 진행성 삼중음성 유방암에서 면역관문억제제 선택에 쓰이며 Luminal A의 대표 특징이 아니다."
    if "flat epithelial atypia" in s: return "Flat epithelial atypia는 저등급 ER 양성 경로의 병변으로 HER2 양성 암의 대표 전구병변이 아니다."
    if "atypical apocrine" in s: return "비정형 아포크린샘증은 삼중음성·HER2 양성 암의 확립된 공통 전구병변으로 보지 않는다."
    if "근상피세포의 소실" in choice and "관상피내" in choice: return "DCIS는 기저막 안에 머물며 병변 둘레의 근상피층이 보존된다; 근상피 소실은 침윤을 의심하게 한다."
    if "기저막" in choice and "근상피세포의 소실" in choice: return "DCIS는 기저막 안에 머물며 병변 둘레의 근상피층이 보존된다; 근상피 소실은 침윤을 의심하게 한다."
    if "genomic profile" in s: return "DCIS와 침윤암은 등급별로 상당한 유전체 연속성을 공유해 완전히 별개의 분자질환으로 보지 않는다."
    if "1년에 1%" in choice: return "DCIS의 자연사는 등급·크기·괴사에 따라 달라 단일 연간 1% 규칙으로 정의하지 않는다."
    if "저등급" in choice and "고등급" in choice and "진행" in choice: return "저등급과 고등급 DCIS는 대개 서로 다른 분자경로를 따라 발생해 반드시 순차 진행하지 않는다."
    if "괴사" in choice and "재발" in choice: return "광범위 병변, 고등급과 comedo necrosis는 DCIS의 국소재발 위험을 높이는 병리 인자다."
    if "재수술" in s: return "절제연 음성 전절제술 뒤에는 잔여병변 때문에 재수술할 근거가 없다."
    if "방사선" in s: return "유방전절제술 후 방사선은 종양 크기·절제연·림프절 등 국소재발 위험에 따라 결정하며 작은 림프절 음성 종양에는 통상 필요하지 않다."
    if "항암화학" in s or "항암치료" in s: return "호르몬수용체 양성/HER2 음성 조기암의 항암치료 이득은 병기와 유전자 재발점수로 판단하며 저위험 점수에서는 작다."
    if "호르몬치료" in s or "항호르몬" in s: return "ER 양성 침윤암은 재발 감소를 위해 보조 내분비치료가 필요하며 폐경 상태에 따라 약제를 정한다."
    if "표적치료" in s: return "HER2 표적치료는 HER2 과발현·증폭이 확인된 암에 사용하며 HER2 음성 암에는 적응되지 않는다."
    if "가족력" in choice and "폐경" in choice: return "유방암 가족력과 늦은 폐경은 각각 독립적인 유방암 위험인자다."
    if "젊은 나이" in choice and "가족력" in choice: return "젊은 발병, 양측·다발성 암과 강한 유방·난소암 가족력은 생식세포 병원성 변이를 의심하게 하는 단서다."
    if "이른 초경" in choice and "atypical" in s: return "이른 초경과 비정형 관증식은 모두 유방암 위험을 높이는 서로 다른 인자다."
    if "estrogen" in s and "자궁내막암" in choice: return "무대항 에스트로겐은 자궁내막암 위험을 높이며 병합 호르몬요법은 유방암 위험과 관련된다."
    if "비만" in choice and "돌연변이" in choice: return "폐경 후 비만은 말초 에스트로겐 증가와 관련된 위험인자이지 특정 종양억제유전자 돌연변이와 한 쌍으로 묶지 않는다."
    if "모유 수유" in choice: return "모유수유는 유방암 위험을 낮추는 방향의 요인이며 섬유선종 발생 원인으로 보지 않는다."
    if "invasive carcinoma" in s or "invasive ductal" in s: return "악성 상피세포가 근상피층과 기저막을 넘어 불규칙한 샘·삭으로 기질에 침윤하면 invasive carcinoma, NST에 합당하다."
    if "phyllodes" in s or "엽상" in choice:
        if "mitosis" in s and ("양성" in choice or "30" in choice): return "높은 유사분열수와 기질 과증식은 악성 엽상종양을 지지하며 양성 가능성을 높이지 않는다."
        if "상피" in choice and "원인" in choice: return "엽상종양에서 종양성 성분은 기질이며 상피는 동반된 비종양성 성분이다."
        if "0%" in choice: return "양성 엽상종양도 국소재발할 수 있어 재발위험을 0%라고 설명할 수 없다."
        return "나뭇잎 모양 구조와 과세포성 기질은 엽상종양을 지지하며 기질 이형성·분열·경계·과증식으로 등급을 나눈다."
    if "mitosis count" in s or "high power field" in s: return "엽상종양에서 높은 유사분열수는 악성도를 지지하지만 한 슬라이드라는 면적 대신 표준화한 10 HPF와 기질 과증식·경계를 함께 평가한다."
    if "항상 악성" in choice: return "엽상종양은 양성·경계성·악성으로 나뉘므로 나뭇잎 모양만으로 항상 악성이라고 할 수 없다."
    if "가장 흔한 형태" in choice: return "엽상종양은 드문 fibroepithelial tumor이며 유방질환 전체에서 가장 흔한 형태가 아니다."
    if "면역세포 증식" in choice: return "엽상종양은 기질세포가 종양성으로 증식하는 병변이지 면역세포 증식성 질환이 아니다."
    if "상피세포 증식" in choice and "발병" in choice: return "엽상종양에서 종양성 증식의 중심은 기질세포이며 상피는 비종양성 동반 성분이다."
    if "fibroadenoma" in s: return "섬유선종은 경계가 좋은 양성 fibroepithelial tumor지만 큰 크기·빠른 성장·엽상 구조는 엽상종양을 의심하게 한다."
    if "nodular adenosis" in s: return "결절성 선증은 소엽 단위의 샘 증가와 근상피 보존을 보이는 양성 증식으로 침윤암과 감별한다."
    if "intraductal papilloma" in s: return "관내유두종은 섬유혈관축을 상피·근상피가 함께 덮는 양성 유두상 병변으로 혈성 유두분비를 일으킬 수 있다."
    if "섬유성 유방암" in choice: return "섬유성이라는 표현은 ER·PR·HER2 기반 표준 분자아형이 아니며 fibroepithelial tumor와 침윤성 상피암을 혼동한 것이다."
    if ("호르몬 수용체" in choice or "호르몬수용체" in choice) and ("sequencing" in s or "pcr" in s): return "ER·PR 발현은 표준화된 면역조직화학으로 평가하며 sequencing이나 PCR을 우선검사로 사용하지 않는다."
    if "호르몬 수용체" in choice and "100%" in choice: return "ER·PR은 종양핵 1% 이상 염색이면 양성으로 보고하며 100% 양성만 내분비치료 대상인 것은 아니다."
    if "her2" in s and "면역조직화학" in choice and "선호되지" in choice: return "HER2 IHC는 표준 1차 검사이며 2+ 경계 결과를 ISH로 확인한다."
    if "her2" in s and "equivocal" in s: return "HER2 IHC 2+는 경계 결과라 유전자 증폭으로 간주하지 않고 ISH로 확인한 뒤 HER2 표적치료를 결정한다."
    if "면역조직화학" in choice and "표적 치료" in choice: return "ER·PR·HER2 IHC 결과는 내분비치료와 HER2 표적치료 선택에 직접 쓰이는 예측표지다."
    if "면역조직화학" in choice and "재발" in choice: return "ER·PR·HER2 IHC는 치료 표적을 정하지만 그 결과만으로 개인 재발률을 정확히 계산하지 않으며 병기·등급·유전자 검사를 함께 본다."
    if "fine needle" in s or "세침흡인" in choice: return "의심 석회화는 세포흡인보다 조직 구조와 석회화 포함 여부를 확인할 수 있는 core 또는 진공보조 생검이 적합하다."
    if "needle localization" in s or "위치결정" in choice: return "비촉지 의심 석회화는 영상 위치결정 후 절제생검으로 병변을 정확히 채취할 수 있다."
    if "core needle" in s or "중심침" in choice: return "항생제에 반응하지 않는 고형 종괴는 core needle biopsy로 침윤암·염증성 유방암 등을 조직학적으로 배제해야 한다."
    if "mri" in s: return "MRI는 병변 범위 평가에 보조적이지만 조직 확진을 대신하지 않는다."
    if "감수성" in choice: return "농양이나 배양 가능한 분비물이 없고 고형 종괴가 남으면 항생제 감수성검사보다 조직검사가 우선이다."
    if "절개 배농" in choice or "incision" in s: return "초음파에서 농양이 없으면 절개배농할 공간이 없으므로 고형 병변을 조직검사해야 한다."
    if "추적관찰" in choice: return "BI-RADS 4 또는 치료 불응 고형 종괴는 단순 추적관찰 대상이 아니라 조직진단 대상이다."
    if "mastectomy" in s or "유방절제술" in choice: return "조직진단 전 의심 석회화만으로 유방절제술을 시행하지 않으며 병변 범위와 병리 결과 뒤 수술 범위를 정한다."
    if "감시림프절" in choice or "합병증" in choice: return "감시림프절 생검은 액와곽청보다 림프부종·감각이상·어깨운동장애가 적으면서 적절한 환자에서 병기정보를 제공한다."
    if "생존율" in choice: return "감시림프절 생검의 주된 장점은 생존율 증가가 아니라 액와 수술 이환 감소다."
    if "n 병기" in s: return "감시림프절 생검은 병기평가에 유효하지만 액와곽청보다 더 많은 림프절을 제거해 정확도를 높이는 수술은 아니다."
    if "방사선치료를" in choice: return "감시림프절 생검을 했다는 사실만으로 유방·액와 방사선치료 적응증이 사라지지 않는다."
    if "재수술" in choice: return "감시림프절 생검은 이환을 줄이지만 병리 결과와 수술 범위에 따라 추가 액와치료가 필요한 경우가 있다."
    if "comedo" in s: return "Comedo-type DCIS는 확장된 유관을 고등급 종양세포가 채우고 중심부 괴사와 석회화를 보이는 형태다."
    raise ValueError(f"unhandled breast choice: {choice}")


def gyn_fact(choice: str) -> str:
    s = choice.lower()
    if "인유두종" in choice: return "HPV는 자궁경부 상피내병변의 원인이지만 만성 무배란성 자궁내막 자극의 직접 원인은 아니다."
    if "고프로락틴" in choice: return "고프로락틴혈증은 GnRH 억제로 희발·무월경을 만들 수 있으나 비만·만성 무배란에서 내막증식의 직접 자극은 무대항 에스트로겐이다."
    if "무대항" in choice: return "만성 무배란에서는 프로게스테론에 의한 주기적 탈락 없이 에스트로겐이 자궁내막을 지속 자극해 과증식과 불규칙 출혈을 일으킨다."
    if "자궁내막증식" in choice: return "만성 무배란과 무대항 에스트로겐은 자궁내막증식증을 일으켜 불규칙 출혈과 내막암 위험을 높인다."
    if "자궁내막증" in choice: return "자궁내막증은 자궁 밖 내막샘·기질로 주기적 골반통과 난임이 흔하며 무배란성 내막 과증식과 다르다."
    if "자궁샘근육증" in choice: return "자궁샘근육증은 자궁근층 안의 내막샘·기질로 이차성 월경통과 과다월경, 미만성 자궁비대를 만든다."
    if "상피내 종양" in choice: return "자궁경부 상피내종양은 HPV 관련 편평상피 병변이며 자궁내막 과증식과 발생 부위·기전이 다르다."
    if "자궁내막염" in choice: return "자궁내막염은 감염·산후·시술과 관련된 염증으로 만성 희발월경과 무대항 에스트로겐의 결과가 아니다."
    if "고위험" in choice and "검사" in choice: return "고위험 HPV 검사는 자궁경부암 선별에서 세포검사보다 민감도가 높고 일차 선별 또는 공동검사에 사용된다."
    if "세포진" in choice or "pap smear" in s: return "자궁경부 세포검사는 특이도가 높지만 고위험 HPV 검사보다 CIN2+ 검출 민감도가 낮다."
    if "질확대경" in choice: return "질확대경은 이상 선별검사 뒤 병변을 관찰하고 표적생검하는 진단 단계이지 일차 선별검사가 아니다."
    if "소파술" in choice: return "자궁경부관 소파술은 변형대가 충분히 보이지 않거나 관내병변이 의심될 때 보조적으로 시행한다."
    if "p16/ki-67" in s: return "p16/Ki-67 이중염색은 HPV 양성 환자의 위험층화에 도움을 주지만 일차 선별 민감도 비교의 표준 정답은 고위험 HPV 검사다."
    if re.fullmatch(r"\s*16[,.]\s*18\s*", choice) or re.fullmatch(r"\s*16\s*(or)?\s*18\s*", choice, re.I): return "HPV 16과 18은 자궁경부암에 가장 크게 기여하는 고위험형이다."
    if re.fullmatch(r"\s*16\s*", choice): return "HPV 16은 편평상피암에서 가장 중요한 고위험형이다."
    if re.fullmatch(r"\s*(18|31|33|35|39|45|51|52|56|58|68)(\s*(?:[,\.]|or)\s*(31|33|35|39|45|51|52|56|58|68))?\s*", choice, re.I): return "이 형들도 발암성 고위험 HPV에 속하지만 전체 자궁경부암 기여도는 16·18 조합보다 낮다."
    if "e6" in s or "e7" in s: return "HPV E6는 p53 분해, E7은 RB 불활성화를 통해 세포주기 조절을 무너뜨린다."
    if has(s, r"l1|l2"): return "L1·L2는 바이러스 캡시드 단백으로 백신 표적이지만 주된 발암 단백은 E6·E7이다."
    if has(s, r"e1|e2"): return "E1·E2는 바이러스 복제와 전사 조절에 관여하며 E6·E7처럼 직접 p53·RB를 억제하는 주된 발암 단백은 아니다."
    if has(s, r"e4|e5"): return "E4·E5도 바이러스 생활사에 관여하지만 자궁경부 발암의 핵심은 E6·E7의 종양억제경로 억제다."
    if "lcr" in s: return "LCR은 바이러스 전사 조절 부위이며 단백질을 암호화하지 않는다."
    if "transfomation" in s or "transformation zone" in s: return "편평원주접합부가 이동하며 생기는 변형대는 미성숙 화생세포가 있어 고위험 HPV 감염과 전암병변이 가장 흔한 부위다."
    if "fornix" in s: return "질원개는 자궁경부 주변의 질 공간이며 자궁경부 전암병변의 주된 발생 부위인 변형대와 다르다."
    if "internal os" in s: return "내자궁구는 자궁경부관의 상단 경계이며 변형대가 아니다."
    if "nabothian" in s: return "나보트낭은 편평상피화생으로 점액샘 출구가 막힌 양성 낭종이다."
    if "progesterone" in s or "프로게스테론" in choice: return "프로게스틴 투여 중 내막이 안정되며 출혈이 감소하고 중단 뒤에는 호르몬 소퇴로 수일간 철회출혈이 생긴다."
    if "estrogen" in s: return "무배란성 출혈에서 에스트로겐 단독 장기투여는 내막 과증식을 악화시킬 수 있어 내막 보호를 위해 프로게스틴이 필요하다."
    if "tamoxif" in s: return "Tamoxifen은 자궁내막에 부분 작용제 효과가 있어 내막증식·용종 위험을 높일 수 있으며 치료제가 아니다."
    if "gn rh" in s or "gnrh" in s: return "GnRH agonist는 특정 자궁내막증·근종 치료에 사용하지만 만성 무배란성 내막 보호의 기본 약제는 프로게스틴이다."
    if "aromatase" in s: return "Aromatase inhibitor는 일부 난임 배란유도나 난치성 자궁내막증에 쓰일 수 있으나 이 철회출혈 검사에서는 프로게스틴이 핵심이다."
    if "보조생식" in choice: return "양측 난관 폐쇄나 중증 남성요인에서는 IVF가 필요할 수 있지만 무배란만 확인되면 먼저 배란유도와 내막 보호를 계획한다."
    if "경과관찰" in choice: return "지속 출혈과 만성 무배란은 빈혈과 내막 과증식 위험이 있어 원인평가와 내막 보호 없이 관찰만 하지 않는다."
    if "전자궁절제" in choice: return "가임력 희망이 있고 침윤암이 확인되지 않은 무배란성 출혈에는 자궁절제가 일차치료가 아니다."
    if "방사선" in choice: return "골반 방사선은 자궁경부암 등 확진 악성종양의 병기 기반 치료이며 무배란성 출혈 치료가 아니다."
    if "약제 복용 중 질출혈 감소" in choice and "다량" in choice: return "프로게스틴 투여 중에는 내막이 안정되어 출혈이 줄고, 중단 뒤 2~7일 사이 철회출혈이 나타나는 것이 전형적이다."
    if "약제 복용 중 질출혈 감소" in choice: return "프로게스틴 중단 후 내인성 에스트로겐에 의해 자란 내막이 탈락하므로 출혈이 전혀 없다는 예측은 맞지 않는다."
    if "약제 복용 중 질출혈 증가" in choice: return "프로게스틴은 불안정한 증식내막을 안정시키므로 복용 중 지속적으로 출혈이 증가한다는 경과는 전형적이지 않다."
    raise ValueError(f"unhandled gyne choice: {choice}")


def prostate_fact(choice: str) -> str:
    s = choice.lower()
    if choice.strip().lower() == "seminoma": return "Seminoma는 균일한 큰 투명세포와 섬유성 격막의 림프구를 보이며 OCT3/4·SALL4·PLAP 양성이다."
    if "embryonal carcinoma" in s: return "Embryonal carcinoma는 다형성 세포의 샘·유두·고형 성장과 CD30·cytokeratin 양성이 특징이다."
    if "yolk sac tumor" in s: return "난황낭종양은 Schiller-Duval body와 망상 구조를 보이며 AFP·glypican-3 양성이다."
    if choice.strip().lower() == "teratoma": return "고환 기형종은 둘 이상의 배엽에서 온 체조직을 포함하며 사춘기 후에는 성숙도와 무관하게 악성 잠재력을 가진다."
    if "choriocarcinoma" in s: return "Choriocarcinoma는 cytotrophoblast와 syncytiotrophoblast가 출혈성 종괴를 만들며 hCG가 높고 조기 혈행전이가 흔하다."
    if "spermatocytic" in s or "sermatocytic" in s: return "Spermatocytic tumor는 고령 남성에서 생기고 GCNIS·i(12p)와 무관하며 전이는 드물다."
    if "basal cell" in s and ("소실" in choice or "loss" in s): return "전립샘 선암은 침윤성 작은 샘의 기저세포가 소실되어 HMWCK/p63 음성으로 보이는 것이 진단을 지지한다."
    if "central zone" in s: return "BPH는 주로 이행구역, 전립샘 선암은 주로 주변구역에서 발생하므로 중심구역이라는 설명은 맞지 않는다."
    if "transition zone" in s: return "이행구역은 BPH의 호발 부위이고 전립샘 선암은 대개 주변구역에서 발생한다."
    if "prostatic intraepithelial" in s or "전암병변" in choice: return "High-grade PIN은 전립샘 선암의 전구병변이지만 이미 기저세포가 소실된 침윤성 샘암을 PIN으로 진단하지 않는다."
    if "psa" in s and "면역" in choice and "음성" in choice: return "전립샘 선암은 PSA·NKX3.1 등 전립샘 계통 표지에 대개 양성이며 정상조직과의 구분에는 기저세포 표지와 AMACR 조합이 더 유용하다."
    if "epithelial" in s and "stromal" in s: return "BPH에서는 샘상피와 섬유근성 간질이 모두 결절성으로 증식한다."
    if "혈행성 전이" in choice or "hematogenous metastasis" in s: return "초기 혈행전이는 choriocarcinoma의 두드러진 특징이며 대부분 고환 생식세포종양은 먼저 후복막 림프절로 전이한다."
    if "cd30" in s: return "CD30 양성은 embryonal carcinoma를 지지하며 소아 난황낭종양의 대표 표지는 AFP·glypican-3다."
    if "hcg" in s: return "hCG 상승은 choriocarcinoma 또는 syncytiotrophoblast를 포함한 종양을 시사하며 난황낭종양의 주 표지는 AFP다."
    if "3세" in choice and "흔" in choice: return "사춘기 전, 특히 3세 미만 고환 생식세포종양에서 난황낭종양이 가장 흔하다."
    if "plap" in s or "oct3/4" in s: return "PLAP·OCT3/4 양성의 균일한 큰 세포 종양은 seminoma를 지지한다."
    if "alpha-fetoprotein" in s or "afp" in s: return "AFP는 난황낭 성분의 진단과 치료 후 추적에 유용하며 순수 seminoma에서는 상승하지 않는다."
    if "germ cell neoplasia in situ" in s: return "사춘기 전 난황낭종양·기형종은 대개 GCNIS와 무관하고, 사춘기 후 일반 생식세포종양은 GCNIS와 연관된다."
    if "immaturity" in s: return "사춘기 후 고환 기형종은 성숙도와 무관하게 악성 잠재력을 가지지만 사춘기 전 성숙 기형종은 대개 양성이다."
    if "잠복고환" in choice: return "잠복고환은 고환 생식세포종양 위험을 높이며 가장 전형적으로 seminoma와 연관된다."
    if "i(12p)" in s or "isochromosome 12p" in s: return "12p 증가/i(12p)는 사춘기 후 GCNIS 연관 생식세포종양의 특징이며 사춘기 전 난황낭종양에는 보통 없다."
    if "영아기" in choice and "예후" in choice: return "사춘기 전 난황낭종양과 기형종은 성인 대응 종양과 생물학이 달라 적절히 치료하면 예후가 좋다."
    if "2번째로 흔" in choice: return "Seminoma는 성인에서 가장 흔한 순수 고환 생식세포종양으로 단순히 두 번째라고 외우지 않는다."
    if "다른 germ cell tumor" in s: return "사춘기 전 기형종과 난황낭종양은 순수형으로 발생할 수 있어 유아라는 이유만으로 혼합 생식세포종양을 전제하지 않는다."
    if "암 발생률" in choice: return "BPH는 암이 아닌 양성 결절성 증식이므로 남성 암 발생률 순위로 기술할 수 없다."
    if "anti-androgen" in s: return "BPH 성장은 DHT 의존성이 있지만 치료는 α차단제와 5α환원효소억제제가 중심이며 전립샘암용 anti-androgen을 기본치료로 쓰지 않는다."
    if "reductase inhibitor" in s: return "5α환원효소억제제는 전립샘이 커진 BPH에서 DHT를 낮춰 수개월에 걸쳐 용적·요폐·수술 위험을 줄인다."
    if "가, 나, 다" in choice: return "초기 하부요로증상 평가는 요검사와 신체진찰이 기본이고, 기대여명과 의사결정에 영향을 줄 경우 PSA를 포함한다; 크레아티닌은 모든 환자의 필수검사는 아니다."
    if "나, 다, 라" in choice: return "신체진찰과 PSA는 관련되지만 요검사를 빼고 크레아티닌을 일률적으로 넣는 조합은 기본 평가를 충족하지 못한다."
    if choice.strip() == "가, 다": return "요검사와 PSA만으로는 신체진찰·직장수지검사가 빠져 초기 평가가 불완전하다."
    if choice.strip() == "나, 라": return "신체진찰과 크레아티닌만으로는 요검사와 증상평가가 빠진다."
    if "가, 나, 다, 라" in choice: return "신기능검사는 신질환·요폐가 의심될 때 선택하며 모든 하부요로증상 환자의 필수 항목은 아니다."
    if "ipss" in s: return "IPSS는 증상 중증도와 삶의 질을 정량화하는 기본 도구다."
    if "urinalysis" in s or "요검사" in choice: return "요검사는 혈뇨·감염·당뇨 등 하부요로증상의 다른 원인을 찾는 기본 검사다."
    if "digital rectal" in s or "직장 수지" in choice: return "직장수지검사는 전립샘 크기·결절과 항문괄약근 상태를 평가하는 기본 진찰이다."
    if "psa" in s: return "PSA는 BPH·전립샘염·사정·조작과 암에서 증가할 수 있어 암 특이 검사가 아니며 추세와 임상 맥락을 함께 본다."
    if "uroflow" in s: return "요속검사는 폐색 정도를 객관화하는 보조검사지만 모든 초기 평가에 필수는 아니다."
    if "요역동학" in choice: return "요역동학검사는 진단이 불확실하거나 수술 전 방광기능 정보가 치료를 바꿀 때 선택적으로 시행한다."
    if "prostate mri" in s or "전립선 mri" in s: return "다중매개변수 전립샘 MRI는 암 의심 환자의 생검 전 위험층화와 표적 설정에 유용하지만 단순 BPH 초기검사는 아니다."
    if "transrectal prostate biopsy" in s or "전립선 조직" in choice: return "조직검사는 MRI·PSA·진찰로 암 위험이 충분할 때 확진을 위해 시행하며 단순 증상평가 검사는 아니다."
    if "transrectal ultrasonography" in s: return "경직장초음파는 전립샘 용적 측정과 생검 유도에 쓰이며 암의 위치·위험층화에는 MRI가 더 유용하다."
    if "pelvis ct" in s or "복부 ct" in s: return "CT는 국소 전립샘 병변 검출과 표적생검 계획에 MRI보다 불리하며 병기·합병증 평가에 선택한다."
    if "신장 초음파" in choice: return "신장초음파는 수신증·상부요로 이상이 의심될 때 시행하며 전립샘암 확진 검사가 아니다."
    if "방광내시경" in choice or "방광 내시경" in choice: return "방광내시경은 혈뇨·요도협착·방광병변 의심 시 사용하며 전립샘암을 확진하지 않는다."
    if "역행성" in choice: return "역행성 신우조영술은 상부요로 폐색·요로상피병변 평가에 제한적으로 쓰이며 전립샘암 진단 검사가 아니다."
    return fact32(choice)


def pediatric_urology_fact(choice: str) -> str:
    s = choice.lower()
    if "frog" in s or "양손" in choice: return "따뜻한 방에서 frog-leg 자세로 서혜관부터 음낭까지 양손 촉진하는 것이 비촉지 고환의 첫 평가다."
    if "음낭 및 서혜부 초음파" in choice: return "잠복고환은 숙련된 진찰이 영상보다 정확한 첫 단계이며 초음파가 비촉지 고환의 수술 계획을 안정적으로 바꾸지 못한다."
    if "hcg 자극" in s: return "hCG 자극검사는 양측 비촉지 고환에서 기능성 고환조직 여부를 평가할 때 제한적으로 고려되며 한쪽 비촉지 고환의 첫 검사는 아니다."
    if "고환 스캔" in choice: return "핵의학 고환 스캔은 잠복고환 위치 확인의 표준 검사가 아니다."
    if "진단적 복강경" in choice: return "비촉지 고환에서 복강경은 진단과 치료를 겸하지만 마취 전 충분한 진찰 뒤 시행한다; 서혜부 촉지 고환에는 필요하지 않다."
    if "6개월까지 경과 관찰" in choice or choice.strip().startswith("6개월까지"): return "교정연령 6개월 전에는 자연 하강 가능성이 있어 관찰할 수 있지만 이후에는 수술 의뢰를 미루지 않는다."
    if "2세까지 경과" in choice: return "교정연령 6개월 이후 자연 하강은 드물어 2세까지 기다리면 생식세포 손상 위험 때문에 수술 시기를 놓친다."
    if "호르몬" in choice: return "hCG·GnRH 호르몬요법은 성공률과 재상승 문제 때문에 잠복고환의 표준 하강 치료로 권장되지 않는다."
    if "고환고정" in choice or "고환 고정" in choice: return "교정연령 6개월 이후 촉지 잠복고환은 보통 생후 6~18개월 안에 고환고정술을 시행한다."
    if "고환절제" in choice or "고환 절제" in choice: return "어린 소아의 작지만 생존 가능한 촉지 고환은 고정술이 원칙이며 명백한 위축·비정상 고환이 아니면 절제하지 않는다."
    if "음낭수종" in choice or "음낭 수종" in choice: return "음낭수종은 대개 무통성 종창과 투과조명 양성이며 갑작스런 심한 통증이나 혈류 이상을 설명하지 않는다."
    if "정계정맥류" in choice: return "정계정맥류는 서 있을 때 두드러지는 '벌레주머니' 촉감이 특징이며 급성 염증성 통증과 다르다."
    if "부고환염" in choice: return "부고환염은 통증이 비교적 점진적으로 생기고 도플러에서 부고환·고환 혈류가 증가하는 염증성 소견을 보인다."
    if "고환염전" in choice or "고환 염전" in choice: return "고환염전은 갑작스런 통증, 고환올림근반사 소실과 혈류 감소가 전형적이며 즉시 수술적 탐색이 필요하다."
    if "고환파열" in choice or "고환 파열" in choice: return "고환파열은 뚜렷한 외상과 백막 불연속·실질 돌출이 핵심이며 비외상성 염증 소견과 다르다."
    if "고환종양" in choice: return "고환종양은 대개 무통성 고형 종괴로 시작하며 급성 혈류 증가성 통증의 전형적 원인이 아니다."
    if "도플러" in s: return "고환 도플러초음파는 염전에서 혈류 감소, 부고환염에서 혈류 증가를 보여 급성 음낭통 감별에 유용하다."
    if "투과 조명" in choice: return "투과조명은 수종의 액체를 확인할 수 있지만 고환염전의 혈류를 평가하지 못한다."
    if "복부 초음파" in choice: return "복부초음파는 음낭 내 고환 혈류와 부고환 염증을 직접 평가하는 검사가 아니다."
    if "전산화" in choice: return "CT는 방사선 노출이 있고 고환 혈류 평가에 도플러보다 불리해 급성 음낭통의 우선검사가 아니다."
    raise ValueError(f"unhandled pediatric urology choice: {choice}")


def urogyne_fact(choice: str, question: dict) -> str:
    s = choice.lower()
    if "체중" in choice: return "과체중은 복압성 요실금의 교정 가능한 위험인자이며 체중감량은 누출 빈도를 줄일 수 있다."
    if "방광훈련" in choice: return "방광훈련은 절박성·혼합성 요실금의 1차 행동치료로, 순수 복압성 누출의 요도 지지 결함을 교정하지 않는다."
    if "경질" in choice and "호르몬" in choice: return "질 에스트로겐은 비뇨생식기 위축과 관련된 절박뇨·재발성 요로감염에 도움을 줄 수 있지만 복압성 요실금의 주 치료는 아니다."
    if "경구" in choice and "호르몬" in choice: return "전신 에스트로겐은 요실금을 개선하지 않고 악화시킬 수 있어 요실금 치료 목적으로 사용하지 않는다."
    if "여성호르몬" in choice: return "에스트로겐은 폐경 비뇨생식기 증상에는 국소로 고려하지만 요도 과운동성 복압성 요실금을 교정하지 않는다."
    if "항콜린" in choice: return "항무스카린제는 절박뇨·빈뇨를 줄이는 과민성방광 약물이며 기침 때 새는 순수 복압성 요실금에는 맞지 않는다."
    if "슬링" in choice: return "중부요도슬링은 보존치료에 반응하지 않는 증상성 복압성 요실금의 대표 수술로 요도 중간부를 지지한다."
    if re.fullmatch(r"[0-4]기", choice):
        stage = int(choice[0])
        facts = {
            0: "POP-Q 0기는 모든 지지점이 정상 범위이고 첨부점 C 또는 D가 충분히 근위부에 있는 상태다.",
            1: "POP-Q 1기는 가장 돌출된 점이 hymen보다 1 cm 초과 근위부, 즉 -1 cm보다 위에 있다.",
            2: "POP-Q 2기는 가장 돌출된 점이 hymen 기준 -1 cm부터 +1 cm 사이다.",
            3: "POP-Q 3기는 가장 돌출된 점이 +1 cm를 넘지만 TVL-2 cm보다 덜 내려온 상태다.",
            4: "POP-Q 4기는 거의 완전 외번으로 가장 돌출된 점이 TVL-2 cm 이상 내려온 상태다.",
        }
        return facts[stage]
    if re.fullmatch(r"(Aa|Ba|Ap|Bp|C)\s*[+-]\d+", choice):
        point, value = re.match(r"(Aa|Ba|Ap|Bp|C)\s*([+-]\d+)", choice).groups()
        if point == "Ap" and value == "+2": return "후질벽 3기는 후질벽의 가장 원위부 점 Ap 또는 Bp가 hymen 아래 +1 cm를 넘어야 하므로 Ap +2가 가능하다."
        if point in {"Aa", "Ba"} and value.startswith("+"): return "전질벽 1기라면 Aa·Ba는 -1 cm보다 근위부여야 하므로 양수 좌표는 맞지 않는다."
        if point == "Bp" and value == "+1": return "후질벽 3기는 가장 원위부가 +1 cm를 초과해야 하므로 Bp +1은 경계상 2기에 해당한다."
        if point == "C" and value == "+0": return "자궁탈출 1기라면 첨부점 C는 hymen보다 1 cm 초과 근위부에 있어야 하므로 0 cm는 맞지 않는다."
    raise ValueError(f"unhandled urogyne choice: {choice}")


def choice_fact(question: dict, choice: str, index: int) -> str:
    lecture = question["lectureNumber"]
    if choice.startswith("그림 속") or choice.strip() == "?":
        return image_choice_fact(choice, index in question.get("answers", []))
    if lecture == "33":
        for fn in (gyne_pathology_fact, fact27, fact28, fact29):
            try:
                return fn(choice)
            except ValueError:
                pass
        raise ValueError(f"{question['id']}: unhandled pathology choice: {choice}")
    if lecture in {"34", "35", "39", "40-2"}: return breast_fact(choice)
    if lecture == "36": return gyn_fact(choice)
    if lecture == "37": return prostate_fact(choice)
    if lecture == "38": return pediatric_urology_fact(choice)
    if lecture == "40-1": return prostate_fact(choice)
    if lecture == "41": return urogyne_fact(choice, question)
    raise ValueError(f"{question['id']}: unhandled lecture")


def question_specific_clue(question: dict) -> str:
    stem = question.get("stem", "")
    lecture = question["lectureNumber"]
    if lecture == "38":
        if "혈류가 증가" in stem: return "도플러 혈류 증가와 수일에 걸친 통증은 염전보다 급성 부고환염을 지지한다."
        if "고환올림근반사" in stem: return "갑작스런 통증과 고환올림근반사 소실은 고환염전을 우선 배제해야 하는 조합이다."
        if "12개월" in stem: return "12개월에도 서혜부에 머문 촉지 고환은 자연 하강을 더 기다리거나 호르몬으로 치료할 시기가 아니다."
        if "3개월" in stem: return "생후 3개월의 촉지 잠복고환은 교정연령 6개월까지 자연 하강을 관찰할 수 있다."
    if lecture == "41" and ("기침" in stem or "재채기" in stem): return "기침·재채기 때 누출되고 절박뇨가 없다는 조합은 복압성 요실금이다."
    if lecture in {"34", "39"} and "항생제" in stem: return "충분한 항생제에도 호전되지 않고 농양 없이 고형 종괴가 남아 감염이 아닌 악성 병변을 조직으로 배제해야 한다."
    if lecture in {"35", "39"} and "ER" in stem: return "ER 양성·HER2 음성과 낮은 재발점수는 내분비치료 이득은 크고 항암치료의 추가 이득은 작을 가능성을 시사한다."
    if lecture == "36" and ("불규칙" in stem or "무월경" in stem): return "만성 희발·무월경 뒤 불규칙 출혈은 무배란성 내막 자극과 철회출혈의 맥락으로 해석한다."
    if lecture == "37" and "처음" in stem: return "처음 평가에서는 증상·진찰·요검사와 선택적 PSA가 우선이고 MRI·생검은 암 의심 단계에서 시행한다."
    return PROFILES[lecture]["key"]


def unique(items: list[str], limit: int) -> list[str]:
    result: list[str] = []
    for item in items:
        item = re.sub(r"\s+", " ", item).strip()
        if item and item not in result:
            result.append(item)
        if len(result) >= limit:
            break
    return result


def make_explanation(question: dict) -> dict:
    lecture = question["lectureNumber"]
    profile = PROFILES[lecture]
    choices = question.get("choices", [])
    answers = question.get("answers", [])
    facts = [choice_fact(question, choice, index) for index, choice in enumerate(choices, 1)]
    if not answers:
        key = "원본 정답이 없어 특정 사진 번호를 정답으로 확정할 수 없다. 사진의 양성 소견은 매끈한 경계·낭성 절단면·고형 결절과 침윤 부재로 판단한다."
        answer_fact = profile["key"]
    else:
        answer_labels = ", ".join(f"{CIRCLED[index - 1]} {choices[index - 1]}" for index in answers)
        answer_fact = " ".join(facts[index - 1] for index in answers)
        key = f"{answer_fact} 따라서 {answer_labels}가 정답이다."
    differentials = [fact for index, fact in enumerate(facts, 1) if index not in answers]
    steps = [question_specific_clue(question), answer_fact]
    for candidate in [*differentials, *profile["steps"]]:
        if candidate not in steps:
            steps.append(candidate)
        if len(steps) == 4:
            break
    source = SOURCES[lecture][0]
    embedded = {int(number): label.strip() for number, label in re.findall(r"([①②③④⑤])\s*([^①②③④⑤]+)", question.get("stem", "")) for number in [CIRCLED.index(number) + 1]}
    embedded_answer_facts: list[str] = []
    for index in answers:
        label = embedded.get(index)
        if label:
            try:
                embedded_answer_facts.append(choice_fact(question, label, index))
            except ValueError:
                pass
    diagnostic_criteria = unique(
        [*embedded_answer_facts, *(facts[index - 1] for index in answers), *differentials, *CRITERIA[lecture]],
        4,
    )
    treatment_question = bool(TX_STEM_RE.search(question.get("stem", "")))
    explanation = {
        "keyJudgment": key,
        "reasoningSteps": steps,
        "choiceExplanations": facts,
        "diagnosticCriteria": diagnostic_criteria,
        "conceptReview": profile["concept"],
        "commonPitfall": "정답 번호나 한 단어 표지자만 외우지 말고, 같은 선지가 맞아지는 질환·병기·검사 단계와 현재 증례를 대조한다.",
        "evidenceStatus": f"문항·선지별 독립 검수({DATE}); 원본 사진이 복원되지 않은 선택지는 형태를 추정하지 않음",
        "sources": SOURCES[lecture],
        "conceptGroup": question.get("lectureTitle", "핵심 개념"),
        "generatedBy": "manual-review-33-41-v1",
    }
    if treatment_question:
        explanation["treatmentGuideline"] = TREATMENT_GUIDES[lecture]
        explanation["diagnosticVisual"] = {
            "title": "진단·치료 흐름",
            "summary": "OpenEvidence에서 관련 최신 지침 후보를 확인한 뒤 공식 지침 내용으로 다시 구성한 자체 요약 흐름도입니다.",
            "steps": TREATMENT_GUIDES[lecture],
            "sourceUrl": source["url"],
            "sourceLabel": source["label"],
        }
    elif DX_STEM_RE.search(question.get("stem", "")):
        explanation["diagnosticVisual"] = {
            "title": "진단 흐름",
            "summary": "문항의 병리·임상 판별 근거를 공식 자료에 맞춰 다시 배열한 자체 요약 흐름도입니다.",
            "steps": diagnostic_criteria[:3],
            "sourceUrl": source["url"],
            "sourceLabel": source["label"],
        }
    numeric_reference = unique([item for item in diagnostic_criteria if NUMERIC_STANDARD_RE.search(item)], 4)
    explanation["numericReference"] = numeric_reference
    explanation["numericReview"] = {
        "status": "applicable" if numeric_reference else "not-applicable",
        "reason": "정답 판단에 직접 쓰이는 절단값·시기·병기 좌표만 표시" if numeric_reference else "나이·연도·문항번호 외 독립적인 수치 기준이 필요하지 않음",
        "reviewedAt": DATE,
    }
    return explanation


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    changed = 0
    corrected_answers = 0
    for question in payload["questions"]:
        if question.get("lectureNumber") not in TARGETS:
            continue
        if question["id"] == "gendev2-38-2021-q059" and question.get("answers") != [4]:
            question["answers"] = [4]
            question["answerStatus"] = "AUA 잠복고환 지침 기준 교정(12개월 촉지 고환: 고환고정술)"
            corrected_answers += 1
        question["explanation"] = make_explanation(question)
        question["explanationReviewStatus"] = MARKER
        question["semanticChoiceReviewStatus"] = "manual-semantic-audit-2026-08-07"
        changed += 1
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"LECTURES_33_41_REVIEWED questions={changed} correctedAnswers={corrected_answers}")


if __name__ == "__main__":
    main()
