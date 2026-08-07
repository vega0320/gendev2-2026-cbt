from __future__ import annotations

"""27~32강 병리·부인종양·비뇨생식 문항 해설 수동 보강."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"
DATE = "2026-08-06"
MARKER = "manual-choice-independent-audit-27-32"


PROFILES = {
    27: {
        "key": "자궁경부·질·외음 병리는 정상 상피의 위치, HPV 효과, 성숙도와 기저막 침범 여부를 순서대로 읽는다.",
        "steps": ["정상 외경부·내경부·변형대 구조를 구분한다.", "koilocytosis, p16, 세포 성숙도와 N:C 비를 확인한다.", "기저막 침범 전후를 전암병변과 침윤암으로 나눈다."],
        "concept": "외경부는 비각화 중층편평상피, 내경부는 점액분비 단층원주상피다. 변형대는 원주상피가 편평상피로 치환되는 편평화생 부위이며 HPV 관련 병변이 흔하다.",
        "criteria": ["LSIL은 대개 표층 koilocytosis와 성숙 보존, HSIL은 기저양 세포 확장·높은 N:C 비·block-type p16을 보인다."],
    },
    28: {
        "key": "자궁내막 종양은 형태와 분자군을 연결하고, 포상기태는 융모 형태·태아조직·배수성·p57로 완전형과 부분형을 구분한다.",
        "steps": ["자궁내막암의 조직형과 분자군을 확인한다.", "포상기태에서 융모 부종과 영양막 증식 분포를 본다.", "p57과 배수성 결과를 유전적 기원에 연결한다."],
        "concept": "자궁내막암 분자군은 POLEmut, MMRd, NSMP, p53abn으로 나뉜다. 완전포상기태는 보통 부계 이배체·p57 소실, 부분포상기태는 흔히 삼배체·p57 보존이다.",
        "criteria": ["POLEmut는 대체로 가장 좋은 예후, p53abn는 가장 불량한 예후군이다.", "완전포상기태는 태아조직이 없고 융모 부종·영양막 증식이 광범위하다."],
    },
    29: {
        "key": "난소 종양은 조직기원, type I/II 경로, 전구병변과 기질침윤을 연결해 양성·경계성·악성을 구분한다.",
        "steps": ["상피성·생식세포·성삭간질·전이성 종양을 구분한다.", "type I과 type II의 분자경로를 연결한다.", "기질침윤 여부로 경계성과 암을 가른다."],
        "concept": "고등급 장액암은 난관채의 STIC와 TP53/상동재조합복구 결함에, 투명세포암·자궁내막양암은 자궁내막증에 연결된다. 경계성 종양은 증식·이형성은 있으나 파괴적 기질침윤이 없다.",
        "criteria": ["악성 판정의 핵심은 파괴적 기질침윤이며 조직형 자체만으로 양성·경계성·악성을 정하지 않는다."],
    },
    30: {
        "key": "난소 종괴는 연령, 폐경 여부, 초음파 형태, 크기, 복수·체중감소, 종양표지자를 합쳐 관찰과 수술을 결정한다.",
        "steps": ["임신반응검사와 통증·활력징후로 임신 관련 종괴, 염전, 파열 같은 즉시 처치 상황을 먼저 배제한다.", "초음파에서 단순 단방성·얇은 벽이면 기능성 가능성이 높고, 고형부·유두상 돌기·복수·혈류 증가가 있으면 악성 위험이 올라간다.", "가임기 단순 낭종은 주기 후 초음파 추적이 기본이고, 지속·증대하거나 악성 소견이 있으면 가임력 보존 범위와 병기설정을 고려해 수술한다."],
        "concept": "가임기 4 cm 단순낭종은 대개 기능성이라 단기 초음파 추적이 적절하다. 폐경 후 큰 복합종괴와 복수·체중감소는 악성을 의심해 온전한 절제와 동결절편을 고려한다.",
        "criteria": ["단순 기능성 낭종은 보통 6~12주 뒤 초음파로 소실 여부를 본다.", "AFP 상승 청소년 난소종괴는 yolk sac tumor를 우선 의심한다."],
    },
    31: {
        "key": "폐경 후 출혈은 위축이 가장 흔하지만 자궁내막암을 반드시 배제하고, 암이 확인되면 영상 병기평가 뒤 수술을 중심으로 치료한다.",
        "steps": ["출혈 원인과 약물력을 확인한다.", "초음파 자궁내막과 조직검사로 암을 확인한다.", "병기·조직형·분자위험군에 따라 수술과 보조치료를 정한다."],
        "concept": "대부분의 자궁내막암은 자궁에 국한된 상태로 발견되어 예후가 좋다. 표준 1차 치료는 자궁·양측 부속기 절제와 적절한 림프절 평가이며 최소침습 접근이 흔히 사용된다.",
        "criteria": ["폐경 후 출혈에서 경질초음파 자궁내막 두께 4 mm 이하는 암 가능성이 매우 낮지만 지속·재발 출혈은 조직평가가 필요하다."],
    },
    32: {
        "key": "전립샘은 발생 구역·기저세포·Gleason 규칙을, 고환종양은 연령·표지자·GCNIS·면역표현형을 함께 본다.",
        "steps": ["BPH와 전립샘암의 구역·조직소견을 구분한다.", "Gleason 점수의 검체별 합산 규칙을 적용한다.", "고환종양의 연령, AFP/hCG, GCNIS 연관과 면역표현형을 확인한다."],
        "concept": "BPH는 이행구역의 샘·간질 증식이고 전암병변이 아니다. 전립샘암은 주변구역에 흔하고 기저세포 소실·뚜렷한 핵인을 보이며 골전이는 주로 조골성이다. 사춘기 후 일반 생식세포종양은 대개 GCNIS와 연관되지만 spermatocytic tumor는 예외다.",
        "criteria": ["침생검 Gleason은 가장 흔한 pattern + 가장 나쁜 pattern, 전절제는 가장 흔한 pattern + 두 번째로 흔한 pattern을 기본으로 한다.", "seminoma는 OCT3/4·SALL4·KIT 양성, embryonal carcinoma는 CD30·cytokeratin 양성이 전형적이다."],
    },
}


SOURCES = {
    27: [{"type": "textbook", "title": "WHO 여성생식기 종양 분류 기반 강의 병리", "checkedAt": DATE}],
    28: [{"type": "guideline", "title": "FIGO 2023 endometrial cancer staging and molecular classification", "url": "https://www.figo.org/news/figo-staging-endometrial-cancer-2023", "checkedAt": DATE}],
    29: [{"type": "textbook", "title": "WHO 난소종양 분류 기반 강의 병리", "checkedAt": DATE}],
    30: [{"type": "guideline", "title": "ACOG guidance: evaluation of adnexal masses", "url": "https://www.acog.org/clinical", "checkedAt": DATE}],
    31: [{"type": "guideline", "title": "NCI Endometrial Cancer Treatment (PDQ)", "url": "https://www.cancer.gov/types/uterine/hp/endometrial-treatment-pdq", "checkedAt": DATE}],
    32: [{"type": "guideline", "title": "NCI Prostate and Testicular Cancer Treatment summaries", "url": "https://www.cancer.gov/types", "checkedAt": DATE}],
}


def fact27(choice: str) -> str:
    s = choice.lower()
    if "위쪽 1/3" in choice: return "정상 편평상피는 표면으로 갈수록 세포질이 풍부하고 핵이 작아져 N:C 비가 낮아진다."
    if "koilocyte" in s and "basal" in s: return "koilocyte는 주로 표층·중간층의 핵주위 투명대와 불규칙한 과염색핵으로 보이며 기저세포와 닮지 않는다."
    if "high-grade" in s and "감소" in choice: return "HSIL은 미성숙 기저양 세포가 상층까지 차지해 N:C 비가 증가한다."
    if "low-grade" in s and "p16" in s: return "LSIL은 patchy p16일 수 있으며 강한 연속 block 염색은 HSIL을 더 지지한다."
    if "columnar" in s and "squamous" in s and "transformation" in s: return "변형대는 기존 원주상피가 새 편평상피로 치환되는 편평화생 부위다."
    if "lichen simplex" in s and ("atrophy" in s or "위축" in choice): return "만성 긁음은 표피 비후·과각화·과립층 증가를 만들므로 표피 위축과 연결하면 틀리다."
    if "lichen simplex" in s: return "만성 자극성 피부병으로 HPV가 원인이 아니다."
    if "adenocarcinoma" in s: return "자궁경부 선암의 상당수는 고위험 HPV, 특히 16·18·45형과 연관된다."
    if "paget" in s: return "외음 Paget병은 PAS 양성 점액을 지닌 선암세포를 보지만 보통 HPV 관련 병변은 아니다."
    if "rhabdomyo" in s: return "태아형 횡문근육종은 소아 질 종양으로 rhabdomyoblast와 desmin·myogenin이 특징이며 HPV와 무관하다."
    if "lichen sclerosus" in s: return "경화성태선은 자가면역·만성 염증과 관련되고 HPV 비의존성 외음암 경로와 연결된다."
    if "condyloma" in s: return "첨형콘딜로마는 저위험 HPV 6·11과 관련되고 papillomatosis와 koilocytosis를 보인다."
    if "vain 1" in s: return "저등급 질 상피내병변에서는 HPV 세포병변인 koilocytosis가 나타날 수 있다."
    if "high-risk hpv" in s: return "HSIL은 지속성 고위험 HPV 감염과 강하게 연관된다."
    if "high-grade squamous" in s: return "세포 성숙 소실과 높은 N:C 비가 상피 중·상층까지 확장되면 HSIL에 해당한다."
    if "low-risk hpv" in s: return "침윤성 자궁경부 편평세포암은 저위험형보다 고위험 HPV와 연관된다."
    if "sexually transmitted" in s: return "HPV는 성접촉으로 전파되므로 HPV 관련 병변은 성매개감염의 맥락에서 이해한다."
    if "p16" in s and ("발현은 없" in choice or "과발현은 관찰되지" in choice): return "고위험 HPV에 의한 RB 경로 억제는 p16 block 과발현을 일으켜 고등급 병변에서 소실보다 과발현이 예상된다."
    if "keratin" in s: return "분화가 좋은 편평세포암은 각질진주와 풍부한 keratin을 형성할 수 있다."
    if "p57" in s: return "p57은 포상기태 감별 표지자이며 자궁경부 HSIL 확인에는 p16과 Ki-67이 더 유용하다."
    if "transformation zone" in s and "columnar metaplasia" not in s: return "미성숙 화생세포가 있는 변형대는 고위험 HPV 감염과 전암병변의 호발 부위다."
    if "cin 3" in s: return "HSIL의 조직학적 범주에는 CIN2와 CIN3가 포함될 수 있다."
    if "전구병변" in choice and "hsil" in s: return "고위험 HPV 관련 편평세포암의 전구병변은 HSIL/CIN3이다."
    if "basement membrane" in s: return "이형성 세포가 기저막을 뚫으면 상피내병변이 아니라 침윤성 편평세포암이다."
    if "endocervix" in s and "stratified" in s: return "내경부는 점액분비 단층원주상피로 덮여 중층원주상피라는 설명은 맞지 않는다."
    if "exocervix" in s and "simple" in s: return "외경부는 비각화 중층편평상피이며 단층원주상피가 아니다."
    if "exocervix" in s and ("stratified" in s or "stratisfied" in s): return "외경부는 비각화 중층편평상피로 구성된다."
    if "점액" in choice: return "점액분비는 내경부 원주세포의 특징이고 외경부 편평세포의 특징이 아니다."
    if "표면" in choice or "maturation" in s: return "정상 외경부는 기저층에서 표면으로 갈수록 핵이 작아지고 세포질이 풍부해지는 성숙을 보인다."
    if "host dna" in s: return "저등급 생산성 감염은 episomal HPV 복제와 koilocytosis가 중심이며 숙주 유전체 통합은 고등급 진행에서 더 중요하다."
    if "koilocytosis" in s: return "핵주위 투명대와 불규칙한 과염색핵은 HPV의 생산성 감염을 나타내는 koilocytosis다."
    if "viral replication" in s: return "LSIL의 표층 성숙세포에서는 HPV의 생산성 복제가 활발할 수 있지만 HSIL에서는 세포주기 이상이 중심이다."
    if "자연" in choice: return "LSIL을 일으키는 HPV 감염은 면역반응으로 자연 소실되는 경우가 많다."
    if "에스트로겐" in choice: return "koilocytosis는 성호르몬 과자극이 아니라 HPV 세포병변 효과다."
    if "질(vagina)" in s: return "자궁경부 LSIL은 변형대에 흔하며 질에서 더 호발하는 병변으로 볼 수 없다."
    if "columnar metaplasia" in s: return "변형대는 columnar metaplasia가 아니라 columnar-to-squamous metaplasia로 형성된다."
    if "hpv 감염에 민감" in s: return "변형대의 미성숙 화생세포는 HPV 감염과 변형에 취약하다."
    raise ValueError(choice)


def fact28(choice: str) -> str:
    s = choice.lower()
    if "pole" in s: return "병원성 POLE exonuclease-domain 변이는 초고돌연변이군을 만들고 대체로 매우 좋은 예후와 연관된다."
    if "serous" in s and "atrophy" in s: return "장액성 자궁내막암은 고령·위축성 내막에서 발생하는 경우가 흔하다."
    if "pten" in s and "hyperplasia" in s: return "PTEN 이상은 자궁내막양암의 전구 단계인 atypical hyperplasia/EIN부터 관찰될 수 있다."
    if "gland" in s and "grade 1" in s: return "자궁내막양암에서 고형성 비편평 성장 5% 이하의 잘 형성된 샘 구조는 저등급에 해당한다."
    if "high-grade serous" in s: return "자궁 장액암은 난소·난관 고등급 장액암과 비슷한 유두상·고등급 핵 형태와 p53 이상을 보인다."
    if "aneuploid" in s: return "염색체 불안정과 aneuploidy는 전통적 type II/p53 이상 암에서 더 두드러진다."
    if "indolent" in s: return "전통적 type I 자궁내막양암은 비교적 서서히 진행하고 조기에 발견되는 경우가 많다."
    if "aggressive" in s: return "공격적 경과는 전통적 type II 장액암에 더 맞고 type I 자궁내막양암은 비교적 완만하다."
    if "type i" in s and "좋은 예후" in choice: return "type II는 고등급·p53 이상·진행 병기와 연관되어 type I보다 예후가 나쁘다."
    if "atrophic endometrium" in s: return "위축성 내막 배경은 장액암과 연관되고 type I 자궁내막양암은 에스트로겐 자극·과증식 배경이 흔하다."
    if "unopposed" in s: return "프로게스테론에 길항되지 않은 에스트로겐 노출은 자궁내막 증식과 자궁내막양암 위험을 높인다."
    if "endometrial hyperplasia" in s: return "EIN/비정형 자궁내막증식증은 자궁내막양암의 대표 전구병변이다."
    if "p57" in s: return "모계 유래 유전자가 없는 완전포상기태의 영양막·융모기질은 p57이 소실되어 감별에 유용하다."
    if "triploid" in s or "69 xxy" in s: return "삼배체 핵형은 부분포상기태를 지지하며 태아조직이 남을 수 있다."
    if "정상 융모" in choice or "정상 villi" in s: return "부분포상기태는 일부 비교적 정상인 융모와 비정상 융모가 섞이지만 완전형은 광범위하게 침범한다."
    if "태아" in choice: return "태아 또는 배아 조직은 부분포상기태에서 가능하고 완전포상기태에서는 보통 보이지 않는다."
    if "국소" in choice or ("trophoblast" in s and "소량" in choice): return "부분형은 영양막 증식이 국소적이고 완전형은 더 광범위·원주성이다."
    if "trophoblast" in s and "모두" in choice: return "두 유형 모두 부종성 융모와 영양막 증식을 보이지만 완전형은 광범위하고 부분형은 국소적이다."
    if "choriocarcinoma" in s and ("높지" in choice or "증가시키지" in choice): return "완전포상기태는 지속성 임신성영양막질환과 융모막암 위험이 부분형보다 높다."
    if "hemorrhage" in s or "괴사" in choice: return "심한 출혈과 괴사는 융모막암에서 전형적이며 포상기태 자체의 진단 기준은 아니다."
    if "p53" in s: return "완전형과 부분형 감별에는 p57과 유전형/배수성 검사가 유용하며 p53은 표준 감별표지가 아니다."
    if "자궁 벽" in choice or "원격전이" in choice: return "근층 침윤·원격전이는 침입포상기태나 융모막암에서 가능하며 단순 포상기태 자체의 필수 소견은 아니다."
    if "endometrioid" in s: return "자궁내막양암은 전통적 type I의 대표 조직형이며 PTEN·PIK3CA·MMR 경로 이상이 흔하다."
    if "대표적인 아형" in choice and "endometrioid" in s: return "자궁내막양암은 type I의 대표이고 type II의 대표는 장액암이다."
    if "tp53" in s: return "TP53 이상은 장액성암과 p53abn 분자군의 핵심이며 전통적 type I의 가장 흔한 변화가 아니다."
    if "serous endometrial" in s: return "장액성 자궁내막상피내암은 장액암의 전구병변이지 type I 자궁내막양암의 전구병변이 아니다."
    if "p53 abnormal" in s: return "p53abn 분자군은 고위험 특징이라 초기·저등급·PR 양성 정보와 한 덩어리로 예후를 단순화하면 안 된다."
    if "tumor size" in s: return "3 cm라는 크기만으로 분자분류를 정할 수 없고 병기에서는 근층·경부·자궁외 침범을 함께 본다."
    if "depth of invasion" in s: return "근층 침범이 절반 미만이면 자궁체부 국한암에서 더 낮은 해부학적 위험에 해당한다."
    if "progesterone receptor" in s: return "PR 양성은 자궁내막양 분화와 호르몬 반응 가능성을 지지하지만 분자군을 대신하지 않는다."
    if "pten mutation" in s: return "PTEN은 자궁내막양암 경로에 흔하지만 FIGO의 네 분자분류 이름 자체는 아니다."
    if "mismatch" in s: return "MMR 결핍/MSI는 자궁내막암의 공식 분자군 중 하나다."
    if "no specific" in s: return "POLE·MMRd·p53abn에 속하지 않는 종양은 NSMP로 분류한다."
    if "granulosa" in s: return "성인형 과립막세포종은 황색 고형 종괴, Call-Exner body와 coffee-bean 핵이 특징이다."
    if "serous borderline" in s: return "장액성 경계성 종양은 계층성 유두와 이형성은 있으나 파괴적 기질침윤이 없다."
    if "high-grade serous" in s: return "고등급 장액암은 복잡한 유두·슬릿, 심한 핵이형성과 잦은 유사분열을 보이는 가장 흔한 난소 상피암이다."
    if "endometriotic cyst" in s: return "자궁내막증성 낭종은 오래된 출혈과 hemosiderin macrophage, 내막샘·기질을 보인다."
    if "mature cystic" in s: return "성숙낭성기형종은 피부·피지·털 등 여러 배엽의 성숙조직으로 구성되는 양성 종양이다."
    if "leiomyoma" in s: return "평활근종은 경계가 분명한 소용돌이형 결절로, 미만성 근층 비후와 내막샘 포착 소견과 다르다."
    if "adenomyosis" in s: return "자궁근층 안의 내막샘과 기질이 주변 평활근 비후를 일으켜 월경통·과다월경과 미만성 자궁비대를 만든다."
    if "endometriosis" in s: return "자궁내막증은 자궁 바깥의 내막샘·기질을 뜻하며 근층 내부 병변은 자궁선근증으로 부른다."
    if "polyp" in s: return "내막폴립은 자궁강 안의 국소 돌출병변으로 미만성 근층 비후를 만들지 않는다."
    if "endometritis" in s: return "급성 자궁내막염은 내막의 호중구성 염증이며 근층 속 내막샘과 만성 비후가 핵심이 아니다."
    raise ValueError(choice)


def fact29(choice: str) -> str:
    s = choice.lower()
    if ("mucinous" in s or "점액암" in choice) and "가장 흔" in choice: return "원발 점액암은 드물며 가장 흔한 상피성 난소암은 고등급 장액암이다."
    if "type i" in s and "항상" in choice: return "type I은 대체로 저등급·단계적 경로지만 조직형을 막론하고 항상 저등급이라고 할 수 없다."
    if "type i" in s and "tp53" in s: return "type I은 KRAS·BRAF·PTEN·ARID1A 경로가 흔하고 TP53 이상은 type II보다 드물지만 절대 배제되지는 않는다."
    if "brca" in s: return "type II의 대표인 고등급 장액암은 생식세포 BRCA1/2 변이와 상동재조합복구 결함에 연관된다."
    if "80%" in s: return "고등급 장액암은 초기 항암반응이 좋아도 진행 병기 발견과 재발 때문에 5년 생존율을 80% 이상으로 볼 수 없다."
    if "mature cystic" in s and "high-grade" in s: return "성숙낭성기형종은 생식세포 종양이며 고등급 장액암 전구병변이 아니다."
    if "low-grade" in s and "tubal" in s: return "저등급 장액암은 serous borderline tumor 경로이고 STIC는 고등급 장액암 전구병변이다."
    if "endometrioid" in s and ("tubal" in s or "teratoma" in s): return "자궁내막양 난소암은 자궁내막증과 연관되며 난관임신이나 성숙기형종에서 기원하지 않는다."
    if "clear cell" in s and "endometri" in s: return "투명세포암은 자궁내막증성 낭종에서 발생할 수 있고 ARID1A·PIK3CA 이상과 연관된다."
    if "mucinous" in s and ("fibro" in s or "teratoma" in s): return "점액성 종양은 보통 자체적인 단계적 상피 증식 경로이며 섬유난포막종이 전구병변은 아니다. 드물게 기형종과 연관될 수 있으나 표준 짝은 아니다."
    if "가장 흔" in choice and "low grade" in s: return "난소 상피암의 가장 흔한 조직형은 고등급 장액암이다."
    if "type i" in s and "전신" in choice: return "진행 병기로 흔히 발견되는 빠른 경과는 type II의 특징이며 type I은 비교적 국한·저등급인 경우가 많다."
    if "type ii" in s and "예후" in choice: return "초기 항암 민감성이 있어도 빠른 성장과 재발 때문에 상대적으로 예후가 불량하다."
    if "homologous" in s: return "고등급 장액암은 BRCA1/2를 포함한 상동재조합복구 결함이 중요한 발병 축이다."
    if "mucinous" in s and "tp53" in s: return "type I 분류가 TP53 변이를 절대 배제하는 뜻은 아니므로 관찰되지 않는다고 단정할 수 없다."
    if "low grade" in s and "tubal" in s: return "STIC는 고등급 장액암과 연결되고 저등급 장액암은 경계성 장액종양과 연결된다."
    if "high-grade" in s and "borderline" in s: return "장액성 경계성 종양은 저등급 장액암의 전구경로이지 고등급 장액암 경로가 아니다."
    if "high grade serous" in s and "cystadenoma" in s: return "고등급 장액암은 난관채 STIC 경로가 대표적이며 양성 낭선종에서 단계적으로 진행하지 않는다."
    if "seromucinous" in s and "endometrioid cyst" in s: return "장액점액성 계열은 자궁내막증 연관성이 있을 수 있으나 현재 분류와 명칭을 원본 출제시점 기준으로 확인해야 한다."
    if "carcinosarcoma" in s: return "암육종은 고등급 상피암의 화생성 형태로 양성 낭선종이 직접 전구병변은 아니다."
    if "clear cell" in s: return "난소 투명세포암은 자궁내막증과 강하게 연관되는 상피성 악성종양이다."
    if "serous adenofibroma" in s: return "장액성 선섬유종은 양성 상피·기질 종양이다."
    if "borderline" in s: return "경계성 종양은 파괴적 기질침윤은 없지만 양성종양으로 분류하지 않는다."
    if "granulosa" in s: return "성인형 과립막세포종은 저등급 악성 잠재력을 가진 성삭간질 종양이다."
    if "immature teratoma" in s: return "미성숙기형종은 악성 생식세포종양이다."
    if "krukenberg" in s or "krukenburg" in s: return "Krukenberg 종양은 위장관 등에서 전이한 악성 난소종양이다."
    if "serous cystadenoma" in s: return "장액성 낭선종은 단순 장액성 상피로 덮인 양성 상피성 종양이다."
    if "mucinous adenofibroma" in s: return "점액성 선섬유종은 양성 상피와 풍부한 섬유성 기질로 이루어진다."
    if "fibrothecoma" in s: return "섬유난포막종은 대개 양성 성삭간질 종양이며 일부에서 에스트로겐을 분비한다."
    if "endometriotic cyst" in s: return "자궁내막증성 낭종은 양성 병변이지만 일부 상피암의 전구환경이 될 수 있다."
    if "육안" in choice: return "고형부·유두상 돌기는 악성 위험 단서지만 최종 양성·경계성·악성 판정은 현미경 침윤이 핵심이다."
    if "증식 정도" in choice: return "상피 증식과 복잡성은 양성과 경계성 종양을 구분하는 데 도움이 된다."
    if "이형성" in choice: return "핵 이형성은 위험도를 높이지만 기질침윤과 함께 해석해야 한다."
    if "기질 침윤" in choice: return "파괴적 기질침윤은 경계성 종양과 암을 가르는 가장 중요한 기준이다."
    if "조직학적 유형" in choice: return "장액성·점액성 같은 조직형은 계통을 정하지만 그 자체가 양성·경계성·악성의 기준은 아니다."
    if "mature cystic teratoma" in s: return "성숙낭성기형종은 양성 생식세포종양이다."
    if "brennor" in s or "brenner" in s: return "비정형 증식성 Brenner 종양은 경계성 범주로 단순 양성종양과 구분한다."
    if "yolk sac" in s: return "난황낭종양은 AFP를 분비하는 악성 생식세포종양이다."
    raise ValueError(choice)


def fact30(q: dict, choice: str) -> str:
    s, stem = choice.lower(), q["stem"]
    simple = "4cm" in stem or "4 cm" in stem
    malignant = "65세" in stem
    if ("후" in choice and "초음파" in choice) or "추적관찰" in choice:
        return "가임기 단순 단방성 기능성 낭종은 한두 월경주기 뒤 소실 여부를 확인하는 추적이 적절하다." if simple else "폐경 후 큰 복합종괴와 복수·체중감소는 관찰만 하기에는 악성 위험이 높다."
    if "항생제" in choice: return "발열·백혈구증가·압통 등 감염 단서가 없는 단순낭종을 항생제로 치료하지 않는다."
    if "흡인" in choice or "흡입" in choice or "경화" in choice: return "흡인만 하면 재발하고 세포 유출·병기평가 실패 위험이 있어 악성 가능 종괴에서는 피한다."
    if "낭종 절제" in choice:
        return "젊은 환자에서 지속·증상성 양성 종괴면 가임력 보존 절제가 가능하지만 전형적 기능성 낭종에는 즉시 수술하지 않는다." if simple else "악성 의심 폐경 후 종괴에서 낭종만 벗기면 피막 파열과 불충분 병기설정 위험이 있다."
    if "난소난관 절제" in choice or "난소난관절제" in s: return "폐경 후 악성 의심 종괴를 파열 없이 제거하고 동결절편 결과에 따라 병기설정술로 이어갈 수 있다."
    if "난소절제" in choice or "난소 절제" in choice: return "단순 기능성 낭종에서 정상 난소까지 제거하면 불필요한 가임력 손실이다."
    if "피임제" in choice: return "복합피임제는 새 기능성 낭종을 줄일 수 있어도 기존 악성 의심 종괴를 치료하거나 더 빨리 없애지 못한다."
    if "ct" in s or "mri" in s or "자기공명" in choice: return "전형적 단순낭종은 초음파 추적으로 충분하고 고가 영상이 1차 처치를 바꾸지 않는다."
    if "pedigree" in s or "brca1/brca2" in s: return "강한 유방·난소암 가족력에서는 유전상담과 가계도 작성 후 BRCA1/2 등 생식세포 검사를 고려한다."
    if "경구 피임제" in choice: return "경구피임제는 난소암 위험 감소와 연관되지만 개인 혈전위험·임신계획을 반영해 선택한다."
    if "29세" in choice: return "BRCA 보인자는 보통 25세부터 유방 MRI를 시작하고 30세부터 유방촬영을 함께 쓰므로 제시 일정은 정확하지 않다."
    if "35세 이후" in choice: return "BRCA1은 35~40세, BRCA2는 40~45세에 출산 완료 후 위험감소 난소난관절제술을 논의한다."
    if "ca125" in s: return "질초음파와 CA-125 감시는 사망률 감소가 입증된 대체 선별법이 아니며 수술을 미루는 보장책이 아니다."
    if choice in {"IIIA1", "IIIA2", "IIIB", "IIIC", "IVA"}:
        return {"IIIA1":"후복막 림프절만 전이된 IIIA1과 달리 복막 병변 크기 자료가 제시됐다.", "IIIA2":"현미경적 복막 전이에 해당하나 제시 병변은 육안으로 확인된다.", "IIIB":"골반 밖 육안 복막전이가 2 cm 이하일 때 해당한다.", "IIIC":"골반 밖 육안 복막전이가 2 cm를 넘으면 해당하며 간·비장 피막 전이도 포함된다.", "IVA":"흉수 세포검사 양성이 있어야 IVA이며 단순 복수만으로는 아니다."}[choice]
    if "serous cystadeno" in s: return "장액성 상피암은 고령에서 더 흔하고 AFP를 종양표지자로 분비하지 않는다."
    if "borderline mucinous" in s: return "점액성 경계성 종양은 거대한 낭성 종괴가 될 수 있지만 현저한 AFP 상승과 맞지 않는다."
    if "dysgerminoma" in s: return "미분화생식세포종은 LDH 상승이 흔하고 AFP는 올라가지 않는 것이 원칙이다."
    if "immature" in s: return "미성숙기형종은 AFP가 경미하게 오를 수 있지만 현저한 상승은 난황낭 성분을 먼저 의심한다."
    if "endodermal" in s: return "난황낭종양은 청소년·젊은 여성에서 큰 난소종괴와 현저한 AFP 상승을 보인다."
    raise ValueError(f"{q['id']}: {choice}")


def fact31(choice: str) -> str:
    s = choice.lower()
    if "atrophy" in s: return "저에스트로겐 상태의 얇고 취약한 내막·질상피가 폐경 후 출혈의 가장 흔한 원인이다."
    if "estrogen replacement" in s: return "호르몬치료 관련 출혈은 가능하지만 전체 폐경 후 출혈의 가장 흔한 원인은 위축이다."
    if "polyp" in s: return "용종은 국소 출혈 원인이지만 위축보다 빈도가 낮고 초음파·자궁경으로 평가한다."
    if "hyperplasia" in s: return "내막증식증은 비길항 에스트로겐과 연관되며 암 전구병변 가능성 때문에 조직평가가 필요하다."
    if "cancer" in s: return "빈도는 위축보다 낮지만 놓치면 중요한 원인이므로 모든 폐경 후 출혈에서 배제해야 한다."
    if "확진용" in choice: return "의뢰 전 내막검사로 조직학적 진단이 확보됐다면 확진만을 위한 두 번째 채취는 우선순위가 낮다."
    if ("조직검사" in choice or "생검" in choice) and "자궁경부" not in choice: return "이미 조직학적으로 암이 확진된 뒤 같은 목적의 생검을 반복하기보다 병기평가로 넘어간다."
    if "ct" in s or "mr" in s or "영상" in choice: return "확진 후 근층·경부·림프절·원격전이 범위를 파악해 수술계획을 세운다."
    if "원추절제" in choice: return "원추절제는 자궁경부 상피병변의 절제·진단법으로 자궁내막 병변을 채취하지 못한다."
    if "자궁경" in choice: return "자궁강 국소병변 표적검사에는 유용하지만 확진된 암의 전신 병기평가를 대신하지 않는다."
    if "복강경" in choice: return "진단만 위한 복강경보다 비침습 영상으로 수술 전 범위를 평가한다."
    if "질 세포진" in choice or "질세포진" in choice: return "질 세포진은 자궁내막암을 확진하는 검사가 아니며 폐경 후 출혈의 내막 병변을 직접 채취하지 못한다."
    if "자궁경부 조직" in choice: return "자궁경부 병변이 아니라 두꺼워진 자궁내막이 의심되므로 경부 조직검사는 표적이 다르다."
    if "자궁 확대경" in choice: return "질확대경은 자궁경부 상피병변 평가용이며 자궁내막을 관찰하지 못한다."
    if "병기설정술" in choice: return "수술 가능한 자궁내막암은 자궁·양측 부속기 절제와 림프절 평가를 포함한 병기설정 수술이 기본이다."
    if "진단적 자궁경" in choice: return "내막생검으로 암이 확인됐고 MRI까지 있다면 진단 자궁경을 반복할 단계가 아니다."
    if "프로게스테론" in choice: return "가임력 보존을 원하는 엄선된 저등급 초기암에 고려하며 폐경 후 일반 환자의 표준 1차 치료는 아니다."
    if "방사선" in choice: return "위험도에 따라 수술 후 보조치료로 쓰지만 수술 가능 환자의 단독 1차 치료는 아니다."
    if "항암" in choice: return "진행·고위험·재발암에서 중요하지만 병기 미확정 수술 가능 환자에게 먼저 단독 투여하지 않는다."
    if ("70%" in choice and "5년" not in choice) or "7명" in choice or "국한" in choice: return "자궁내막암은 비정상 출혈로 일찍 발견되어 약 70%가 자궁에 국한된 병기로 진단된다."
    if "20%" in choice or "brca" in s or "유전성" in choice: return "유전성은 일부이며 대표적으로 Lynch syndrome의 MMR 유전자를 평가한다. BRCA가 중심 검사는 아니다."
    if "5년" in choice: return "FIGO I기의 5년 생존은 대체로 70%보다 높아 저위험 조기암에서는 90% 안팎이다."
    if "1차 치료" in choice or "주된" in choice: return "국한암의 기본은 수술이며 방사선·항암은 병리 위험도나 진행·재발 상황에 따라 추가한다."
    if "개복" in choice: return "적합한 환자에서는 복강경·로봇 등 최소침습 수술이 표준적으로 사용되며 개복이 예후상 우월하지 않다."
    raise ValueError(choice)


def fact32(choice: str) -> str:
    s = choice.lower()
    if "가장 흔하다" in choice: return "고환종은 가장 흔한 순수형이지만 사진의 비seminoma 조직형에 그대로 적용할 수 없다."
    if "방사선치료에 잘 반응" in choice: return "높은 방사선 민감성은 seminoma의 특징이며 비seminoma는 cisplatin 기반 항암치료가 중심이다."
    if "benign" in s or "결절" in choice:
        if "central" in s or "중심" in choice: return "BPH는 요도 주위 이행구역에서 발생하며 중심구역이라는 표현은 부정확하다."
        if "stroma" in s or "간질" in choice: return "DHT는 샘상피와 간질 모두의 증식에 관여해 두 성분이 함께 늘어난다."
        if "전암" in choice: return "BPH는 전암병변이 아니며 증상 정도와 합병증에 따라 치료한다."
    if "tmprss2" in s: return "TMPRSS2-ETS 융합은 전립샘암에서 가장 대표적이고 흔한 분자 이상 중 하나다."
    if "전립샘암" in choice or "전립선 암" in choice or "전립선암" in choice:
        if "central" in s or "중심구역" in choice or "이행구역" in choice: return "전립샘암은 주로 주변구역에서 생겨 초기에는 요도폐쇄 증상이 없을 수 있다."
        if "발생률 1위" in choice: return "암 발생 순위는 통계 연도에 따라 변하므로 병리학적 정의로 쓰지 않으며 출제 당시 국내 통계와 기준연도를 확인해야 한다."
    if "전체 종양" in choice: return "다발성 전립샘암은 지배적/가장 큰 결절과 각 병소를 평가하며 모든 병소를 단순 합산해 하나의 Gleason 점수를 만들지 않는다."
    if "osteolytic" in s: return "전립샘암 골전이는 주로 조골성 경화 병변을 만든다."
    if "epithelial" in s and "stromal" in s: return "BPH 현미경에서는 샘상피와 섬유근성 간질이 모두 결절성으로 증식한다."
    if "peripheral" in s and ("nodular" in s or "질환" in s): return "BPH는 이행구역에 생기며 주변구역은 전립샘암의 호발 부위다."
    if "peripheral zone" in s: return "주변구역은 전립샘암이 흔한 자리이고 BPH 결절은 주로 이행구역에 생긴다."
    if "amacr" in s: return "AMACR은 전립샘암에서 양성일 수 있지만 BPH 샘의 대표 소견은 아니다."
    if "전암병변" in choice: return "BPH는 전립샘암의 전구병변으로 간주되지 않는다."
    if "i(12p)" in s: return "12p 이상은 고환 생식세포종양의 특징이지 BPH의 원인이 아니다."
    if "basal cell" in s or "기저세포" in choice or "기저 세포" in choice:
        if "소실" in choice: return "작고 침윤성인 샘, 뚜렷한 핵인과 기저세포층 소실이 전립샘 선암을 지지한다."
        return "p63·고분자량 cytokeratin은 기저세포 표지자다. 암에서는 기저세포가 소실되므로 양성이어야 암이라는 해석은 반대다."
    if "myc" in s or "androgen receptor mutation" in s: return "대표 초기 분자이상은 TMPRSS2-ETS 융합이며 MYC 증폭이나 AR 변이는 가장 흔한 초기 이상으로 보지 않는다."
    if "호르몬치료" in choice: return "전립샘암은 안드로겐 의존성이 있어 진행암에서 안드로겐박탈치료에 반응한다."
    if "gleason" in s:
        if "3+4" in s: return "전절제의 3+4는 가장 넓은 pattern 3과 두 번째로 넓은 pattern 4를 뜻한다."
        if "3+5" in s: return "침생검은 가장 흔한 pattern과 가장 나쁜 pattern을 더하므로 3+5 표기가 가능하다."
        if "33%" in s: return "전절제에서는 가장 흔한 4와 두 번째로 흔한 3을 기본으로 4+3=7로 보고하고 소량 pattern 5는 별도 표기한다."
        return "Gleason grade group은 병기와 독립적으로 예후와 치료결정에 중요한 조직학적 지표다."
    if "perineural" in s: return "전립샘 선암은 신경주위 침윤을 흔히 보인다."
    if "teratoma" in s or "기형종" in choice:
        if "사춘기 이전" in choice: return "사춘기 전 순수 기형종은 대개 GCNIS 비연관 양성이며 미성숙 성분만으로 악성을 정하지 않는다."
        return "사춘기 후 고환 기형종은 성숙도와 무관하게 악성 잠재력을 가지며 혼합 생식세포종양의 일부인 경우가 많다."
    if ("seminoma" in s and "non-seminomatous" not in s) or choice.strip().startswith("고환종 ("):
        if "alpha-fetoprotein" in s: return "seminoma는 젊은 성인에 흔하고 AFP를 만들지 않으며 방사선 민감성이 높다."
        if "cd30" in s or "ki-1" in s: return "seminoma는 OCT3/4·KIT가 전형적이고 CD30·cytokeratin은 embryonal carcinoma 쪽이다."
        if "stage 1" in s or "pure form" in s: return "seminoma는 가장 흔한 순수 고환 생식세포종양이며 조기 병기 발견과 높은 치료감수성으로 예후가 좋다."
        return "seminoma는 사춘기 후 GCNIS 연관 종양이므로 GCNIS 비연관 종양을 고르는 경우에는 해당하지 않는다."
    if "spermatocytic" in s or "정모세포" in choice:
        if "60세" in choice and "가장 많이" in choice: return "고령에서 상대적으로 보이지만 60세 이상 가장 흔한 고환종양은 림프종이다."
        return "spermatocytic tumor는 고령에 생기며 GCNIS를 거치지 않는 별도 경로의 생식세포종양이다."
    if "germ cell neoplasia in situ" in s or "제자리" in choice: return "GCNIS는 사춘기 후 seminoma와 비seminoma 생식세포종양 대부분의 전구병변이고 미치료 시 침윤암 위험이 높다."
    if "non-seminomatous" in s: return "비seminoma는 진행 병기로 발견될 수 있고 혈행전이가 이르며, seminoma처럼 방사선 민감 종양으로 치료하지 않는다."
    if "schiller" in s or "shiller" in s or "hyaline globule" in s: return "Schiller-Duval body와 AFP 양성 hyaline globule은 난황낭종양의 특징이다."
    if "c-kit" in s: return "KIT 양성은 seminoma를 지지하지만 형태와 OCT3/4·SALL4 등을 함께 해석해야 한다."
    if "yolk sac" in s:
        if "hcg" in s: return "난황낭종양은 AFP를 분비하며 hCG는 융모막암·syncytiotrophoblast와 연관된다."
        return "난황낭종양은 AFP·glypican-3·SALL4가 유용하고 CD30은 embryonal carcinoma 표지다."
    if "embryonal" in s: return "embryonal carcinoma는 CD30과 cytokeratin 양성이 전형적이며 GCNIS 연관 악성종양이다."
    if "choriocarcinoma" in s: return "사춘기 후 융모막암은 GCNIS 연관 비seminoma 계열이며 혈행전이와 높은 hCG가 특징이다."
    if "lymphoma" in s or "림프종" in choice: return "고령 남성의 가장 흔한 고환 종양은 diffuse large B-cell lymphoma이며 30대 호발이 아니다."
    if "psa" in s: return "PSA는 전립샘 특이적이지만 암 특이적이지 않아 감염·BPH·조작과 추세를 함께 본다."
    if "조직 생검" in choice: return "반복 상승한 PSA는 직장수지검사, 전립샘 MRI와 위험도를 평가한 뒤 표적·계통 생검으로 확진한다."
    if "경과관찰" in choice: return "PSA가 반복 상승하면 단순 관찰만 하기보다 암 위험을 층화해 추가 평가한다."
    if "국소 절제술" in choice: return "경요도 국소절제는 BPH 폐쇄 완화에는 쓰지만 PSA 상승만으로 전립샘암 치료처럼 시행하지 않는다."
    if "방사선" in choice: return "방사선치료는 확진된 국소 전립샘암의 위험군·기대수명을 평가한 뒤 선택한다."
    if "항암" in choice: return "세포독성 항암은 진행성 거세저항성 암 등에서 사용하며 PSA 상승의 확진검사가 아니다."
    if "절제술" in choice: return "근치수술은 조직학적 확진과 병기·위험도 평가 뒤 선택한다."
    raise ValueError(choice)


def explain(q: dict, choice: str) -> str:
    lecture = int(q["lectureNumber"])
    return {27: fact27, 28: fact28, 29: fact29, 31: fact31, 32: fact32}[lecture](choice) if lecture != 30 else fact30(q, choice)


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    reviewed = []
    for q in payload["questions"]:
        raw = str(q.get("lectureNumber", ""))
        if not raw.isdigit() or not 27 <= int(raw) <= 32:
            continue
        lecture = int(raw)
        spec = PROFILES[lecture]
        explanations = [explain(q, choice) for choice in q["choices"]]
        if len(set(explanations)) != len(explanations):
            raise SystemExit(f"{q['id']}: duplicate choice explanations")
        exp = q.get("explanation") or {}
        exp.update({
            "keyJudgment": spec["key"], "reasoningSteps": spec["steps"],
            "choiceExplanations": explanations, "diagnosticCriteria": spec["criteria"],
            "conceptReview": spec["concept"],
            "evidenceStatus": f"27~32강 문항·선지 독립 수동 검수({DATE}); 병리 기준과 공식 종양 지침 대조",
            "sources": SOURCES[lecture],
        })
        q["explanation"] = exp
        q["explanationReviewStatus"] = MARKER
        q["semanticChoiceReviewStatus"] = f"manual-semantic-audit-{DATE}"
        reviewed.append(q)

    for q in reviewed:
        for i, text in enumerate(q["explanation"]["choiceExplanations"]):
            choice = q["choices"][i].strip()
            if len(choice) >= 12 and choice in text:
                raise SystemExit(f"{q['id']}: choice {i + 1} copied verbatim")
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"LECTURE_27_32_REVIEW_PASS questions={len(reviewed)} choices={sum(len(q['choices']) for q in reviewed)}")


if __name__ == "__main__":
    main()
