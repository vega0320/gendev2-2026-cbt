from __future__ import annotations

"""14~20강의 모든 객관식 선지를 자기 문장만 설명하도록 다시 검수한다."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"
REVIEW_DATE = "2026-08-06"
MARKER = "manual-choice-independent-audit-14-20"


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def has(text: str, *patterns: str) -> bool:
    return any(re.search(pattern, text, re.I) for pattern in patterns)


def fact_hie(choice: str) -> str:
    if has(choice, "뇌실.*복강", "ventriculo"):
        return "뇌실-복강 단락술은 진행성 수두증에서 뇌척수액을 복강으로 배액하는 수술이며, 저산소허혈뇌병증 자체의 신경보호 치료가 아니다."
    if has(choice, "덱사메타손", "부신피질"):
        return "전신 스테로이드는 이 사례의 저산소성 뇌손상을 줄이는 표준 신경보호요법이 아니다."
    if has(choice, "면역글로불린"):
        return "정맥 면역글로불린은 특정 면역·염증성 질환의 치료이며 주산기 질식 뒤 HIE의 치료가 아니다."
    if has(choice, "저체온"):
        return "재태주수 기준을 충족하는 중등도~중증 HIE는 출생 6시간 이내 전신 저체온치료를 시작해 33.5~34.5℃를 72시간 유지하면 사망·중증 신경발달장애를 줄일 수 있다."
    if has(choice, "카페인"):
        return "카페인은 주로 미숙아 무호흡의 호흡자극제로 사용하며 HIE의 재관류성 뇌손상을 줄이지 않는다."
    if has(choice, "고빈도"):
        return "고빈도진동환기는 중증 호흡부전의 환기 전략이지 HIE의 장기 신경학적 예후를 개선하는 치료는 아니다."
    if has(choice, "항생제"):
        return "감염이 의심되면 항생제가 필요하지만, 주산기 질식과 중증 산증으로 생긴 HIE의 신경보호 효과는 없다."
    if has(choice, "일산화질소"):
        return "흡입 일산화질소는 지속성 폐고혈압의 산소화를 개선하며 HIE의 표준 신경보호 치료가 아니다."
    if has(choice, "항경련"):
        return "임상·뇌파 경련은 치료하지만 예방적 항경련제만으로 HIE의 신경발달 예후가 좋아지지는 않는다."
    if has(choice, "고탄산"):
        return "관용적 고탄산혈증은 일부 환기 전략일 뿐이며 중증 HIE의 검증된 신경보호 치료가 아니다."
    if has(choice, "교환수혈"):
        return "교환수혈은 중증 비포합 고빌리루빈혈증이나 일부 혈액학적 적응증에 사용하며 HIE 치료가 아니다."
    raise ValueError(choice)


def fact_abuse(choice: str) -> str:
    if has(choice, "거미막"):
        return "거미막밑출혈은 저산소증·응고장애·출생 손상 등 여러 원인으로 생길 수 있어 이 보기들 중 학대에 가장 특이적인 형태는 아니다."
    if has(choice, "경질막", "경막 밑"):
        return "분만 손상으로 설명되지 않는 영아 경막하출혈은 가속-감속 손상과 연관될 수 있어 망막출혈·골절·병력 불일치와 함께 학대를 평가해야 한다."
    if has(choice, "배기질", "뇌실막하", "뇌실내", "뇌실 내"):
        return "배아기질-뇌실내출혈은 뇌혈관이 미숙한 조산아에서 흔한 합병증으로, 그 자체가 학대를 대표하지 않는다."
    if has(choice, "소뇌"):
        return "소뇌출혈은 극소미숙아, 출생 손상, 저산소·응고 이상과 관련될 수 있으며 단독으로 학대의 전형적 지표는 아니다."
    if has(choice, "모상건막"):
        return "모상건막하출혈은 진공흡입 등 출생 손상 뒤 광범위한 실혈을 일으킬 수 있는 신생아 응급질환이다."
    if has(choice, "출산 후 부종", "caput"):
        return "산류는 분만 압력으로 생기는 두피 피하부종으로 봉합선을 넘을 수 있고 수일 안에 호전한다."
    raise ValueError(choice)


def fact_scalp(choice: str) -> str:
    if has(choice, "머리혈종", "cephal"):
        return "두혈종은 골막하 출혈이어서 봉합선을 넘지 않고, 석회화되면 수주~수개월 단단하게 만져질 수 있다."
    if has(choice, "출산머리", "caput"):
        return "산류는 피하부종이라 봉합선을 넘고 대개 생후 수일 내 사라지므로 2개월까지 단단한 융기로 남는 양상과 다르다."
    if has(choice, "경막"):
        return "경막하출혈은 두개강 안 병변이므로 봉합선에 국한된 외부 두피 융기로 진단하지 않는다."
    if has(choice, "수막탈출"):
        return "뇌수막류는 두개골 결손을 통해 수막이 돌출하는 선천기형인데, 이 사례에는 뼈결손이 없다."
    if has(choice, "모상건막"):
        return "모상건막하출혈은 봉합선을 넘어 퍼지고 창백·빈맥·머리둘레 증가와 쇼크를 일으킬 수 있어 안정적으로 작아지는 국한 종괴와 다르다."
    raise ValueError(choice)


def fact_pvl(choice: str, stem: str) -> str:
    if has(choice, "강직성", "뇌성마비"):
        return "뇌실주위 백질의 피질척수로 손상은 하지에 더 두드러진 경직성 양하지마비 형태의 뇌성마비를 흔히 남긴다."
    if has(choice, "뇌실주위"):
        return "극소미숙아에서 운동발달 지연과 양측 하지 경직은 뇌실주위백질연화증의 전형적인 임상 결과다."
    if has(choice, "감각신경성 난청"):
        return "감각신경성 난청은 선천감염·이독성 약물·심한 고빌리루빈혈증 등과 연관되며 PVL의 대표 후유증은 운동장애다."
    if has(choice, "소뇌성", "소뇌출혈"):
        return "소뇌 손상은 운동실조·협응장애를 만들 수 있지만 뇌실주위 백질 병변의 주된 해부학적 결과와 다르다."
    if has(choice, "안면마비"):
        return "말초성 안면마비는 얼굴신경 손상으로 생기며 양측 하지 피질척수로를 침범하는 PVL과 위치가 다르다."
    if has(choice, "자폐"):
        return "미숙아에서 자폐 위험이 증가할 수는 있어도 이 뇌실주위 병변이 가장 직접적으로 예측하는 것은 경직성 운동장애다."
    if has(choice, "뇌전증"):
        return "뇌전증도 뇌손상 뒤 동반될 수 있지만 뇌실주위 백질 손상의 가장 전형적 후유증은 경직성 뇌성마비다."
    if has(choice, "중추성 무호흡"):
        return "중추성 무호흡은 뇌간 호흡중추·미숙한 호흡조절과 관련되며 PVL의 대표 장기 후유증이 아니다."
    if has(choice, "뇌량무형성"):
        return "뇌량무형성은 선천적 구조 이상으로, 극소미숙과 연관된 후천적 뇌실주위 백질 손상을 설명하지 않는다."
    if has(choice, "배아질"):
        return "배아기질출혈은 조산아의 급성 출혈 병변이지만 하지 경직이 진행하는 전형적 백질 손상은 PVL이다."
    if has(choice, "핵황달"):
        return "핵황달은 기저핵·뇌간 손상으로 무정위형 운동장애와 청각신경병증을 만들며 경직성 양하지마비와 다르다."
    raise ValueError(choice)


def fact_nbs(choice: str, qid: str) -> str:
    if qid.endswith("2025-q083"):
        if has(choice, "테이"):
            return "테이-삭스병은 hexosaminidase A 결핍 질환이지만 이 문항이 전제한 국내 2024년 6종 추가 선별 목록에는 포함되지 않는다."
        if has(choice, "고셔"):
            return "고셔병은 glucocerebrosidase 결핍 리소좀축적질환으로 해당 확대 선별 항목에 포함된다."
        if has(choice, "니만") and has(choice, "파브리"):
            return "선지에 함께 적힌 니만-픽 A/B병과 파브리병은 모두 이 문항이 전제한 확대 선별 항목에 포함된다."
        if has(choice, "니만"):
            return "산성 sphingomyelinase 결핍 니만-픽 A/B병은 해당 확대 선별 항목에 포함된다."
        if has(choice, "크라베"):
            return "크라베병은 GALC 결핍 질환으로 증상 전 발견이 중요한 확대 선별 항목이다."
        if has(choice, "파브리"):
            return "파브리병은 α-galactosidase A 결핍 리소좀축적질환으로 해당 확대 선별 항목에 포함된다."
    if qid.endswith("2022-q060"):
        hour = int(re.search(r"\d+", choice).group())
        if hour == 60:
            return "생후 60시간은 수유가 시작되고 출생 직후 대사 전환의 영향이 줄어드는 권장 채혈 창(대개 48~72시간)에 해당한다."
        if hour in (12, 24):
            return f"생후 {hour}시간은 너무 이르면 일부 질환의 대사물질·호르몬 변화가 충분하지 않아 위음성이 늘 수 있다."
        return f"생후 {hour}일은 일상 선별검사로는 늦어 조기 치료 기회를 놓칠 수 있다."
    if qid.endswith("2021-q022"):
        step = int(re.search(r"\d+", choice).group()) if re.search(r"\d+", choice) else 0
        return {
            1: "발을 따뜻하게 하는 1과정은 말초혈류를 늘려 과도한 압착 없이 채혈하도록 돕는다.",
            2: "알코올 소독 뒤 완전히 말리는 2과정은 오염과 용혈·검체 희석을 줄이는 올바른 준비다.",
            3: "사진 설명처럼 첫 혈액방울부터 묻힌 3과정이 잘못이다. 첫 방울은 닦고 다음 방울을 자연스럽게 여과지에 스며들게 한다.",
            4: "원을 충분히 채운 뒤 약 4시간 수평 자연건조한 4과정은 적절하다. 젖은 채 겹치거나 밀봉하지 않는다.",
            5: "첫 방울 사용이라는 명확한 오류가 있으므로 ‘잘못된 부분 없음’으로 판단할 수 없다.",
        }[step or 5]
    if qid.endswith("2020-q033"):
        spot = int(re.search(r"\d+", choice).group())
        return {
            1: "1번의 발가락 부위는 뼈·연골 손상 위험이 있어 표준 발뒤꿈치 채혈점이 아니다.",
            2: "2번의 발바닥 중간 부위는 신경·건 손상 위험 때문에 신생아 선별검사 천자점으로 권하지 않는다.",
            3: "3번은 그림에서 표시한 발뒤꿈치 발바닥의 안전 구역으로, 종골 중앙을 피하며 채혈할 수 있다.",
            4: "4번처럼 발뒤꿈치 뒤쪽 곡면에 너무 가까운 부위는 종골 손상 위험 때문에 피한다.",
            5: "5번의 가쪽 앞발·발가락 인접 부위는 표준 heel-stick 위치가 아니다.",
        }[spot]
    raise ValueError(f"{qid}: {choice}")


def fact_nbs_by_index(qid: str, index: int, choice: str) -> str:
    if qid.endswith("2023-q062"):
        return [
            "생후 48시간은 일반적인 신생아 건조혈반 선별검사의 적절한 채혈 시점에 들어간다.",
            "발꿈치 정중앙·뒤쪽 곡면은 종골 손상 위험 때문에 피하고 안쪽 또는 가쪽 발바닥 면을 사용한다.",
            "발을 따뜻하게 하고 소독한 뒤 알코올이 완전히 마른 후 천자하면 혈류와 검체 품질이 좋아진다.",
            "첫 방울은 닦아내고 자연스럽게 맺힌 다음 방울로 여과지 한쪽에서 원을 충분히 적신다.",
            "젖은 채 바로 비닐에 밀봉하면 습기·곰팡이·검체 변성이 생기므로 평평하게 충분히 자연건조한 뒤 포장한다.",
        ][index]
    return fact_nbs(choice, qid)


def fact_metabolic(choice: str, qid: str) -> str:
    if has(choice, "A와 B의 제한", "기질 A"):
        return "기질 제한은 독성 기질의 유입을 줄이는 전략으로 PKU·갈락토스혈증·단풍당뇨증 같은 식이치료에 해당한다."
    if has(choice, "AB의 억제", "효소 AB"):
        return "상류 효소 억제는 독성 대사물 생성을 줄이는 기질감소 전략이며, 결핍 산물이나 호르몬을 직접 보충하는 방법과 다르다."
    if has(choice, "BC의 주기", "효소 BC"):
        if has(choice, "주기적 투여") and qid.endswith(("2022-q021", "2021-q021")):
            return "고셔병은 결핍된 glucocerebrosidase를 정기적으로 정주하는 효소대체요법의 대표 질환이다."
        return "결핍 효소를 반복 공급하는 효소대체요법으로 고셔병 등 일부 리소좀축적질환에 적용한다."
    if has(choice, "C의 보충", "최종 산물 E"):
        if qid.endswith("2023-q082"):
            return "선천부신과형성증은 부족한 cortisol을 glucocorticoid로 보충하고 필요하면 mineralocorticoid도 보충한다."
        if qid.endswith("2020-q034"):
            return "갑상선무발생증은 부족한 갑상선호르몬을 levothyroxine으로 조기에 보충하는 질환이다."
        return "결핍된 최종 산물·호르몬을 보충하는 전략으로 선천갑상선저하증이나 선천부신과형성증에 해당한다."
    if has(choice, "대체 경로", "chelation"):
        if qid.endswith("2025-q084"):
            return "Penicillamine은 구리를 결합해 소변 배설을 늘리므로 축적 물질을 대체 배설경로로 제거하는 전략이다."
        return "킬레이션은 축적된 금속을 결합해 체외 배설을 촉진하는 전략이며 Wilson병의 구리 제거가 대표적이다."
    disease = clean(choice)
    facts = {
        "갈락토즈 혈증": "갈락토스혈증은 유당·갈락토스를 즉시 제한하는 기질 제한 치료가 핵심이지 효소를 정맥 주입하지 않는다.",
        "고셔병": "고셔병은 결핍 lysosomal enzyme을 주기적으로 공급하는 효소대체요법의 대표 질환이다.",
        "단풍당뇨증": "단풍당뇨증은 분지사슬아미노산 제한과 급성기 이화 차단이 핵심이며 표준 효소대체질환은 아니다.",
        "선천성 부신 과형성증": "선천부신과형성증은 결핍된 cortisol±aldosterone을 보충하는 호르몬대체 치료를 한다.",
        "요소회로 대사 이상증": "요소회로 이상은 질소부하 제한·질소제거제·경로별 아미노산과 위기 시 투석을 사용하며 효소대체가 표준은 아니다.",
        "레쉬-니한병": "Lesch-Nyhan병은 요산 생성을 줄이는 치료와 지지요법을 쓰지만 결핍 산물 C를 단순 보충해 교정하지 못한다.",
        "갑상선 무발생증": "갑상선무발생증은 결핍된 갑상선호르몬을 levothyroxine으로 보충하는 치료가 핵심이다.",
    }
    if has(disease, "요소회로.*이상"):
        return "요소회로 이상은 질소부하 제한·질소제거제·경로별 아미노산과 위기 시 투석을 사용하며 결핍 호르몬 C를 보충하는 질환은 아니다."
    if disease in facts:
        return facts[disease]
    raise ValueError(f"{qid}: {choice}")


def fact_bh4(choice: str, qid: str) -> str:
    if has(choice, "수산화 효소의 주기적"):
        return "PAH 효소를 정기 정주하는 치료는 임상 표준이 아니다. 식이·sapropterin 반응성·원인별 치료를 선택한다."
    if has(choice, "제한.*타이로신"):
        return "페닐알라닌 제한과 tyrosine 보충은 고전적 PAH 결핍의 기본 식이치료지만 BH4 반응 또는 중추 신경전달물질 결핍을 따로 반영해야 한다."
    if has(choice, "제한 식이.*tetra"):
        return "BH4 부하 뒤 phenylalanine이 의미 있게 감소한 PAH 결핍은 제한식에 sapropterin(BH4)을 병용해 조절할 수 있다."
    if has(choice, "tetra.*dopamin"):
        return "BH4 합성·재생 결함은 phenylalanine 조절뿐 아니라 dopamine·serotonin 합성도 부족하므로 BH4와 L-dopa 계열·5-HTP 보충이 필요하다."
    if has(choice, "dopamin"):
        return "신경전달물질 전구체만 주면 고페닐알라닌혈증과 BH4 자체 결핍이 교정되지 않아 불완전하다."
    if has(choice, "PAH 유전자"):
        return "PAH 유전자검사는 원인 확정에 도움이 되지만 즉시 BH4 반응성과 중추 BH4 결핍을 모두 기능적으로 구분하지는 못한다."
    if has(choice, "소변 아미노산"):
        return "24시간 소변 아미노산은 지속 고페닐알라닌혈증의 다음 단계에서 원인·치료반응을 가르는 핵심 검사가 아니다."
    if has(choice, "pterin"):
        return "소변 pterin 분석은 BH4 대사이상 감별에 중요하지만 ‘24시간 소변’보다 적절히 채취·보존한 검체와 DHPR 평가를 함께 해석한다."
    if has(choice, "부하검사"):
        return "BH4 부하검사는 phenylalanine 감소 양상으로 sapropterin 반응성을 평가하고 치료 방침을 나누는 데 유용하다."
    if has(choice, "1회 더"):
        return "두 차례 고페닐알라닌혈증이 확인됐으므로 선별검사만 반복하기보다 원인 감별과 치료평가 단계로 넘어가야 한다."
    if has(choice, "제한 식이$"):
        return "페닐알라닌 제한만으로는 BH4 반응성이나 중추 BH4 결핍의 추가 치료 필요성을 반영하지 못한다."
    raise ValueError(f"{qid}: {choice}")


def fact_hyperammonemia(choice: str, qid: str) -> str:
    if has(choice, "10% dextrose"):
        return "10% 포도당 수액은 충분한 포도당 투입으로 단백질 이화를 빠르게 억제하는 초기 치료다. 전해질은 검사·소변량에 맞춰 조절한다."
    if has(choice, "5% dextrose"):
        return "5% 포도당은 중증 대사 위기에서 이화를 억제하기 위한 열량 공급이 부족할 수 있어 고농도 포도당이 우선된다."
    if has(choice, "Hartmann?", "Ringer"):
        return "젖산 포함 균형질 수액은 순환 보충에는 쓸 수 있지만 포도당 열량이 없어 고암모니아 위기의 이화 차단 수액으로 충분하지 않다."
    if has(choice, "Normal saline"):
        return "생리식염수는 저혈량 교정에는 유용하지만 열량을 제공하지 않아 단독으로 단백질 이화를 막지 못한다."
    if has(choice, "금식.*지방과 단백질"):
        return "급성 고암모니아혈증에서는 단백질을 일시 중단해야 하므로 단백질이 포함된 수액은 질소부하를 악화시킬 수 있다."
    if has(choice, "락툴"):
        return "Lactulose는 간성뇌증에서 장내 암모니아 흡수를 줄이지만 신생아 요소회로 위기의 1차 신속 제거법이 아니다."
    if has(choice, "비위관"):
        return "의식저하·경련과 중증 고암모니아혈증에서 단백질 수유를 계속하면 질소부하와 흡인 위험이 커진다."
    if has(choice, "복막 투석"):
        return "복막투석은 암모니아 제거 속도가 느려 수치가 매우 높고 신경증상이 있는 위기에서는 혈액투석보다 불리하다."
    if has(choice, "혈액 투석"):
        return "중증 신경증상과 극심한 고암모니아혈증에서는 혈액투석/지속적 신대체요법이 가장 빠르게 암모니아를 제거한다."
    diseases = {
        "단풍당뇨증": "단풍당뇨증은 케톤산증과 단풍 냄새, 분지사슬아미노산 상승이 특징이며 비케톤성 호흡성 알칼리증과 다르다.",
        "요소회로 대사이상증": "요소회로 이상은 암모니아가 요소로 전환되지 않아 고암모니아혈증, 과호흡성 호흡알칼리증, 대개 무케톤·정상혈당 양상을 보인다.",
        "유기산뇨증": "유기산뇨증은 대개 고음이온차 대사산증과 케톤뇨가 뚜렷해 이 사례와 구분된다.",
        "지방산대사이상증": "지방산산화장애는 금식 뒤 저케톤성 저혈당이 핵심이며 이 사례의 정상혈당·호흡알칼리증과 다르다.",
        "페닐케톤뇨증": "PKU는 치료하지 않으면 신경발달장애를 일으키지만 신생아 급성 고암모니아 위기의 전형적 원인은 아니다.",
    }
    if clean(choice) in diseases:
        return diseases[clean(choice)]
    raise ValueError(f"{qid}: {choice}")


def fact_galactosemia(choice: str) -> str:
    if has(choice, "광선"):
        return "광선치료는 비포합 빌리루빈을 낮출 뿐 galactose-1-phosphate 축적과 간부전·패혈증의 원인을 제거하지 못한다."
    if has(choice, "교환수혈"):
        return "교환수혈은 중증 고빌리루빈혈증의 제한적 적응증이며 갈락토스혈증의 기본 원인치료가 아니다."
    if has(choice, "무유당"):
        return "모유·일반분유를 중단하고 lactose/galactose가 없는 분유로 바꾸는 것이 의심 즉시 해야 할 핵심 치료다."
    if has(choice, "저단백"):
        return "저단백식은 일부 아미노산·요소회로 질환에서 고려하며 갈락토스 제거를 대신하지 못한다."
    if has(choice, "저지방"):
        return "지방 제한은 galactose 대사 결함의 독성 기질을 줄이지 못한다."
    markers = {
        "galactose": "고전 갈락토스혈증에서는 total galactose/galactose-1-phosphate가 상승하며 황달·간비대·출혈·E. coli 패혈증과 연결된다.",
        "homocysteine": "Homocysteine 상승은 homocystinuria 선별 소견으로 수정체 탈구·혈전 위험과 관련된다.",
        "17-hydroxyprogesterone": "17-hydroxyprogesterone 상승은 주로 21-hydroxylase 결핍 선천부신과형성증 선별 소견이다.",
        "leucine": "Leucine/alloisoleucine 상승은 단풍당뇨증을 시사한다.",
        "thyroid stimulating hormone": "TSH 상승은 일차성 선천갑상선저하증의 선별 소견이다.",
    }
    for marker, fact in markers.items():
        if marker.lower() in choice.lower():
            return fact
    raise ValueError(choice)


def fact_growth(choice: str, qid: str) -> str:
    if qid.endswith("2025-q017"):
        if has(choice, "키가"):
            return "키가 출생 시의 2배가 되는 것은 신체 크기의 양적 증가이므로 성장에 해당한다."
        if has(choice, "블록"):
            return "블록 쌓기는 손의 미세운동·시각운동 통합 발달을 보여준다."
        if has(choice, "컵"):
            return "한 손으로 컵을 들어 마시는 행동은 미세운동과 적응행동 발달을 보여준다."
        if has(choice, "깡충"):
            return "양발 모아 뛰기는 대근육 운동 발달 이정표다."
        if has(choice, "큰 것"):
            return "크기 비교는 인지·개념 발달을 보여주며 신체 크기 증가인 성장과 다르다."
    if qid.endswith("2021-q019"):
        months = int(re.search(r"\d+", choice).group())
        if months == 24:
            return "표준 성장측정은 만 24개월 미만에서 누운키, 24개월부터 선키를 사용한다."
        if months < 24:
            return f"{months}개월에 선키로 전환하면 아직 협조가 어려운 영아의 표준 누운키 기간을 너무 짧게 잡는다."
        return "36개월까지 일률적으로 누운키만 재면 24개월 이후 성장차트의 선키 기준과 맞지 않는다."
    if qid.endswith("2020-q029"):
        facts = {
            "키 성장이 저조하다.": "출생 49 cm에서 12개월 74 cm는 약 1.5배로 1세의 일반적인 길이 증가와 맞는다.",
            "키 성장이 과도하다.": "12개월 74 cm는 과도한 선형성장으로 볼 수 없다.",
            "체중 성장이 저조하다.": "출생 3.4 kg이면 12개월 무렵 약 3배가 기대되는데 7.2 kg은 약 2.1배라 체중 증가가 저조하다.",
            "체중 성장이 과도하다.": "7.2 kg은 출생체중 대비 기대 증가보다 작아 과도한 체중 증가가 아니다.",
            "체중, 키 성장이 다 양호하다.": "키 증가는 대체로 맞지만 체중이 출생체중의 약 3배에 미치지 않아 둘 다 양호하다고 할 수 없다.",
        }
        return facts[choice]
    raise ValueError(f"{qid}: {choice}")


def fact_growth_by_index(qid: str, index: int, choice: str) -> str:
    if qid.endswith("2022-q089"):
        return [
            "누운키 측정에서 머리 꼭대기는 고정된 headboard에 밀착시킨다.",
            "만 2세 미만은 표준적으로 길이판에서 누운키를 측정한다.",
            "한 명이 머리와 몸통을 정렬하고 다른 한 명이 무릎을 펴 footboard를 대면 오차가 줄어 두 사람이 권장된다.",
            "Frankfort plane은 외이도와 안와의 ‘아래쪽 가장자리’를 잇는 선이다. 선지의 ‘안와 중심’은 기준점을 잘못 적었다.",
            "골반을 비틀지 않고 좌우 고관절선이 몸통 장축과 직각이 되도록 정렬한다.",
        ][index]
    return fact_growth(choice, qid)


def fact_development(choice: str, qid: str) -> str:
    if qid.endswith("2025-q018"):
        domains = {
            "인지 영역": "익숙한 소리에 대한 관심이 줄었다가 새로운 소리에 다시 주의를 돌리는 습관화·탈습관화는 기억과 변별이라는 인지 발달을 보여준다.",
            "언어 영역": "소리에 반응하지만 옹알이·단어 이해·표현을 평가한 행동은 아니므로 주된 언어영역 과제는 아니다.",
            "운동 영역": "고개를 돌리는 움직임이 포함되어도 핵심은 새 자극을 알아차리는 정보처리이며 대근육 기술 평가가 아니다.",
            "사회성 영역": "사람과의 상호작용·공동주의·사회적 미소를 본 상황이 아니므로 사회성 영역이 중심이 아니다.",
            "적응행동 영역": "도구 사용이나 일상생활 문제해결보다 새 소리를 구분하고 기억하는 인지 과정이 핵심이다.",
        }
        return domains[choice]
    if qid.endswith("2022-q018"):
        if has(choice, "앞숫구멍"):
            return "앞숫구멍 폐쇄는 해부학적 성숙·성장 소견이지 기능 획득인 발달영역 행동이 아니다."
        if has(choice, "체중"):
            return "체중 배수는 신체 크기의 양적 성장 지표다."
        if has(choice, "또래"):
            return "또래와 어울려 노는 능력은 사회성 발달을 나타낸다."
        if has(choice, "체질량"):
            return "BMI 분류는 영양·성장 상태를 나타내며 발달 기능이 아니다."
        if has(choice, "두위"):
            return "머리둘레 백분위수는 뇌·두개 성장 지표이지 행동 발달영역은 아니다."
    if qid.endswith("2021-q020"):
        if has(choice, "뒤집"):
            return "뒤집기는 보통 4~6개월경 획득하므로 7개월 영아에서 기대할 수 있다."
        if has(choice, "배밀이"):
            return "배밀이나 기기 전 이동은 개인차가 있지만 7개월 무렵 나타날 수 있다."
        if has(choice, "붙잡고 일어"):
            return "붙잡고 일어서기는 대개 9~10개월 이후 기술이라 7개월의 기대 운동발달로는 이르다."
        if has(choice, "혼자 앉"):
            return "앉혀 놓으면 지지 없이 앉는 능력은 약 6~8개월에 나타나 7개월에 기대할 수 있다."
        if has(choice, "몸을 지탱"):
            return "세웠을 때 다리에 체중을 싣는 반응은 7개월에 관찰될 수 있다."
    if qid.endswith("2020-q030"):
        seq = clean(choice)
        if seq == "U→P→D":
            return "잡기는 새끼손가락 쪽 손바닥(ulnar-palmar)에서 엄지 쪽 손바닥(radial-palmar), 엄지·손가락(radial-digital) 순으로 정교해진다."
        return f"{seq}는 손 전체의 척측 잡기에서 요측 손가락 잡기로 진행하는 정상 근위-원위·척측-요측 발달 순서를 거스른다."
    raise ValueError(f"{qid}: {choice}")


def fact_intussusception(choice: str, qid: str) -> str:
    if has(choice, "공기 정복"):
        return "안정적이고 천공·복막염이 없는 장중첩증은 영상 유도 공기정복이 빠르고 효과적인 1차 비수술 치료다."
    if has(choice, "바륨관장"):
        return "바륨관장도 정복이 가능하지만 천공 시 바륨복막염 위험이 있어 현재는 공기 또는 수용성/생리식염수 정복을 더 흔히 쓴다."
    if has(choice, "초음파 유도 수기"):
        return "초음파 유도 hydrostatic enema는 가능하지만 복벽을 손으로 눌러 정복하는 단순 수기정복이 표준은 아니다."
    if has(choice, "복강경"):
        return "복강경 정복은 비수술 정복 실패나 병적 선두점이 의심될 때 고려하며 안정적인 첫 치료가 아니다."
    if has(choice, "개복"):
        return "개복 정복·장절제는 천공, 괴사, 복막염, 쇼크 또는 관장정복 실패 때 필요하다."
    if has(choice, "잠혈"):
        return "대변잠혈은 장점막 손상을 보일 수 있지만 장중첩의 위치와 표적징후를 확인하지 못한다."
    if has(choice, "세균배양"):
        return "대변배양은 감염성 장염 감별검사이며 간헐적 복통과 딸기잼변의 장중첩을 진단하지 못한다."
    if has(choice, "단순 X"):
        return "단순 복부촬영은 폐색·천공을 찾는 보조검사지만 정상이어도 장중첩을 배제하지 못한다."
    if has(choice, "복부초음파", "복부 초음파"):
        return "복부초음파는 방사선 노출 없이 target/doughnut sign을 확인하는 장중첩증의 우선 진단검사다."
    if has(choice, "복부 CT"):
        return "CT도 병변을 보지만 방사선량이 크고 전형적 소아 장중첩의 1차 검사로 초음파보다 뒤선다."
    if has(choice, "대장내시경"):
        return "대장내시경은 급성 장중첩의 표준 진단·정복 검사가 아니며 천공 위험과 진정 부담이 있다."
    if has(choice, "바륨관장술"):
        return "관장술은 진단과 치료를 겸할 수 있지만 진단만 묻는 단계에서는 비침습적 초음파가 우선이다."
    raise ValueError(f"{qid}: {choice}")


def fact_ed(choice: str, qid: str) -> str:
    if qid.endswith("2023-q026"):
        if has(choice, "Triage"):
            return "환자분류실은 도착 직후 중증도와 격리 필요성을 정하는 전방(front-end) 기능이다."
        if has(choice, "소생실"):
            return "소생실은 불안정 환자를 즉시 처치하는 전방 급성진료 구역이다."
        if has(choice, "격리실"):
            return "격리실은 전파 위험 환자를 초기 동선에서 분리하는 전방 기능이다."
        if has(choice, "입원대기"):
            return "입원 결정 뒤 병상을 기다리며 관찰·치료를 지속하는 구역은 후방(back-end) 흐름에 해당한다."
        if has(choice, "의사"):
            return "응급의학과 의사는 전후방을 모두 담당하는 인력이지 특정 후방 공간 구성요소로만 분류하지 않는다."
    raise ValueError(f"{qid}: {choice}")


def fact_ed_by_index(qid: str, index: int, choice: str) -> str:
    if qid.endswith("2025-q068"):
        return [
            "응급실은 연령·중증도·질환이 매우 다양한 비선택 환자군을 진료한다.",
            "응급실에서는 장기 추적보다 제한된 정보로 즉시 위험을 찾아 안정화·처분을 결정해야 한다.",
            "중증도와 환자 유입이 예측되지 않아 진료 시간이 여유롭지 않다.",
            "응급환자는 예약 없이 내원하므로 정해진 외래 일정에 맞춘 진료와 다르다.",
            "소아 응급은 연령별 정상범위, 소생술, 감염·외상·내외과 응급을 함께 다루는 폭넓은 지식과 술기가 필요하다.",
        ][index]
    if qid.endswith("2022-q030"):
        return [
            "소아 응급실 방문량은 특정 3~5세군만 가장 높다고 단정할 수 없고 어린 연령군의 방문 부담이 크다.",
            "0~1세 영아는 감염·호흡·수유 문제의 중증화 위험이 커 응급실 방문 뒤 입원 건수가 가장 높은 연령군으로 제시된다.",
            "10~14세의 흔한 응급 주소는 손상·복통·발열 등이며 두통이 단일 최다 주소라는 설명은 맞지 않는다.",
            "질병이 손상보다 많아도 5:3이라는 고정 비율은 해당 강의의 국내 연령별 통계와 일치하지 않는다.",
            "소아청소년의 응급실 이용은 연령별 위험과 보호자의 접근행태 영향을 받아 인구비율보다 일률적으로 낮다고 할 수 없다.",
        ][index]
    return fact_ed(choice, qid)


def fact_meningitis(choice: str, qid: str) -> str:
    if qid.endswith("2020-q035"):
        diagnoses = {
            "정상": "CSF 백혈구 750/μL는 정상 범위를 크게 넘으므로 정상 뇌척수액이 아니다.",
            "viral meningitis": "림프구 우세 백혈구 증가, 경도 단백 상승, 보존된 CSF/혈청 포도당 비는 바이러스수막염에 맞는다.",
            "acute bacterial meningitis": "급성 세균수막염은 보통 호중구 우세, 더 높은 단백, 낮은 CSF 포도당 비를 보이므로 이 결과와 다르다.",
            "partially treated meningitis": "항생제 선행 병력이 없고 포도당이 잘 보존되어 부분치료 세균수막염보다 바이러스 양상이 뚜렷하다.",
            "tuberculous meningitis": "결핵수막염은 림프구 우세라도 포도당 저하와 현저한 단백 상승이 흔하며 아급성 임상경과가 보통이다.",
        }
        return diagnoses[choice]
    if has(choice, "A의 방법"):
        return "Kernig·Brudzinski 등 고전 수막자극징후는 어느 하나가 항상 더 정확하다고 할 만큼 민감도가 높지 않다."
    if has(choice, "시행해서는"):
        return "영아에서도 수막자극징후를 볼 수는 있지만 음성 결과의 민감도가 낮다는 점을 알고 해석해야 한다."
    if has(choice, "음성이더라도"):
        return "어린 영아는 경부강직·Kernig·Brudzinski 징후가 나타나지 않을 수 있어 음성이라도 수막염을 배제할 수 없다."
    if has(choice, "음성이면.*뇌척수액"):
        return "검사 음성만으로 요추천자 필요성을 없앨 수 없고 연령·전신상태·발열 원인과 치료 지연 위험을 함께 판단한다."
    if has(choice, "양성이면.*확진"):
        return "수막자극징후 양성은 의심도를 높이지만 다른 뇌막자극 원인도 있어 CSF 검사 없이 확진하지 못한다."
    if has(choice, "나이 어릴수록"):
        return "어릴수록 고전 수막자극징후의 민감도가 낮아져 양성 비율이 감소한다."
    if has(choice, "약 50%"):
        return "수막자극징후의 민감도는 징후·연령·원인에 따라 크게 달라 ‘전체의 약 50%’로 고정하기 어렵다."
    if has(choice, "숙달"):
        return "검사법에 따른 차이는 있어도 수막염 진단의 핵심 한계는 낮은 민감도이며, 숙련도만으로 진단력을 확보하지 못한다."
    if has(choice, "무균성보다 세균성"):
        return "세균수막염은 염증이 더 강해 고전 수막자극징후가 무균성 수막염보다 양성일 가능성이 높다."
    if has(choice, "어떤 경우에도"):
        return "수막자극징후 음성은 특히 영유아에서 수막염을 배제하지 못한다."
    raise ValueError(f"{qid}: {choice}")


def fact_measles(choice: str) -> str:
    if has(choice, "호흡 격리"):
        return "홍역 의심 환자는 즉시 마스크를 씌우고 공기주의가 가능한 음압격리실(AIIR)에 배정한다."
    if has(choice, "비말 격리"):
        return "홍역은 비말주의만으로 부족한 공기전파 감염이며 역격리는 면역저하 환자를 외부 병원체에서 보호하는 개념이다."
    if has(choice, "KTAS level 1"):
        return "홍역 의심 자체가 즉시 소생이 필요한 KTAS 1을 뜻하지 않으며 생리적 불안정 여부로 중증도를 정한다."
    if has(choice, "Level D"):
        return "일반진료실과 Level D 보호복보다 노출 최소화, 음압실, 적합한 호흡보호구가 핵심이다."
    if has(choice, "타병원"):
        return "응급실 진입을 막고 무조건 전원하면 치료가 지연되고 이동 중 노출이 생길 수 있어 먼저 안전하게 격리·평가한다."
    raise ValueError(choice)


def fact_pediatric_difference(choice: str, qid: str) -> str:
    if has(choice, "뇌혈관"):
        return "뇌혈관질환은 소아에서도 생기지만 죽상경화성 뇌졸중은 성인에서 훨씬 흔하다."
    if has(choice, "폐쇄성 폐질환"):
        return "세기관지염·천식처럼 하기도 폐쇄를 일으키는 질환은 소아에서 흔하므로 매우 드물지 않다."
    if has(choice, "감염성 폐질환"):
        return "바이러스성 하기도감염과 폐렴은 소아의 흔한 질병부담이다."
    if has(choice, "허혈성 심장"):
        return "죽상경화성 허혈심장질환은 성인에서 흔하고 소아에서는 선천심장병·심근염 등이 상대적으로 중요하다."
    if has(choice, "간 질환"):
        return "소아 간질환은 선천 대사·유전질환의 비중이 성인보다 커 연령별 원인 구성이 다르다."
    if has(choice, "패혈증"):
        return "신생아·영아도 중증 세균감염과 패혈증 위험이 있어 매우 드문 질환이 아니다."
    if has(choice, "복벽근"):
        return "영아 호흡은 횡격막 의존도가 높으며 복벽근 수축이 주된 정상 흡기 기전은 아니다."
    if has(choice, "갈비뼈"):
        if has(choice, "평행"):
            return "영아 갈비뼈는 성인보다 더 수평이어서 몸의 세로축에는 더 직각에 가깝다. ‘세로축과 평행’은 반대 설명이다."
        return "영아 갈비뼈는 성인보다 수평이라 몸의 세로축에 더 직각인 방향이고 흉곽 확장 효율이 낮다."
    if has(choice, "입으로 호흡"):
        return "어린 영아는 주로 코로 호흡하므로 비강폐쇄가 호흡곤란을 쉽게 일으킨다."
    if has(choice, r"상부\s*기도.*넓"):
        return "소아 기도는 절대직경이 작아 같은 부종도 저항을 크게 증가시킨다."
    if has(choice, "가장 좁은.*성[문분]", r"성문\("):
        return "고전 소아 기도 시험에서는 윤상연골의 고정된 성문하부를 가장 좁다고 배운다. 현대 영상은 성문부 형태도 강조하므로 문맥을 구분한다."
    if has(choice, "가장 좁은.*반지", "반지연골"):
        return "고전 교과서 기준에서 영유아 기도의 가장 좁고 고정된 부위는 윤상연골 성문하부로 설명한다."
    if has(choice, "유순도"):
        if has(choice, "크다", "더 크"):
            return "영아 흉벽은 연골성이고 유연해 순응도가 성인보다 크며, 쉽게 함몰되어 호흡근 효율이 떨어진다."
        return "영아 흉벽 순응도는 성인보다 큰 것이 원칙이다. ‘작다’는 족보 정답 ④와도 충돌해 원문 선지·정답 재확인이 필요하다."
    if has(choice, "횡격막의 중요성이 매우 낮"):
        return "영아는 늑간근이 미숙하고 갈비뼈가 수평이라 오히려 횡격막 의존도가 높다."
    raise ValueError(f"{qid}: {choice}")


def fact_adolescent(choice: str, qid: str) -> str:
    if has(choice, "Home.*Employment.*Activities.*Drugs.*Sexuality.*Suicide"):
        return "HEEADSSS의 핵심 영역인 가정, 교육/고용, 활동, 약물, 성, 자살·우울/안전을 체계적으로 포함한다."
    if has(choice, "Home.*Employment.*Activities.*Drugs.*Sexuality.*Sleep"):
        return "수면도 중요하지만 이 조합은 청소년 비밀면담의 필수 자살·우울/안전 평가가 빠져 있다."
    if has(choice, "Home.*Education.*Activities.*Drinking.*Sexuality.*Suicide"):
        return "음주는 Drugs 영역의 일부지만 표준 약물 문진 전체를 좁히고, 상황에 따라 employment·safety까지 빠질 수 있다."
    if has(choice, "Home.*Employment.*Activities.*Drinking.*Safety.*Sleep"):
        return "이 조합은 성건강과 자살·우울 평가가 빠져 비순응의 심리사회적 원인을 충분히 찾지 못한다."
    if has(choice, "Home.*Employment.*Activities.*Drinking.*Sexuality.*Sleep"):
        return "음주와 수면은 포함하지만 약물 전반과 자살·우울/안전 평가가 빠져 표준 HEEADSSS 문진으로 불완전하다."
    if has(choice, "Home.*Education.*Activities.*Drinking.*Sexuality.*Depression"):
        return "우울은 묻지만 약물 전체와 자살사고·안전을 직접 확인하지 않아 표준 위험평가를 완전히 포함하지 못한다."
    if has(choice, "Home.*Escape"):
        return "Escape는 HEEADSSS의 표준 영역명이 아니며 교육/고용·약물·안전 문진이 빠져 있다."
    if has(choice, "Home, Education, Drug, Sexuality"):
        return "가정·학교·약물·성생활은 만성질환 청소년의 순응을 흔히 흔드는 핵심 비밀면담 영역이다."
    if has(choice, "Home E-cigarettes"):
        return "전자담배·음주·수면만 묻는 조합은 학교, 성건강, 우울·자살과 안전을 빠뜨린다."
    if has(choice, "Health, Egocentrism"):
        return "Health와 Egocentrism은 표준 HEEADSSS 영역명이 아니며 가정·교육과 안전 평가가 빠진다."
    if has(choice, "Home, Education, Drinking, Sleep"):
        return "가정·교육은 포함하지만 약물 전반, 성건강, 자살·안전 평가가 불완전하다."
    if has(choice, "Health, E-cigarettes"):
        return "전자담배 질문은 유용해도 가정·교육·우울/자살·안전을 포함한 전체 심리사회 평가를 대신하지 못한다."
    if has(choice, "여아.*2-3"):
        return "여아의 성장속도 정점은 비교적 이른 사춘기인 Tanner 유방 2~3단계 무렵에 나타난다."
    if has(choice, "편도선염"):
        return "아데노이드·편도와 이관 구조 문제가 큰 어린 연령에서 삼출중이염이 흔하며 사춘기에 증가하는 현상은 아니다."
    if has(choice, "여자가.*체지방.*느리"):
        return "사춘기 여아는 estrogen 영향으로 체지방률이 남아보다 더 증가한다."
    if has(choice, "고환.*2 mL", "고환.*2mL"):
        return "남아 사춘기 시작은 고환용적이 약 4 mL 이상으로 증가할 때로 보며 2 mL는 사춘기 전 범위다."
    if has(choice, "척추가 다리보다"):
        return "사춘기 초기는 다리가 몸통보다 먼저 길어져 일시적으로 팔다리가 길어 보인다."
    if has(choice, "고환.*10.*15"):
        return "남아 성장속도 정점은 사춘기 중후반, 대략 고환용적 10~15 mL 무렵에 나타난다."
    if has(choice, "성호르몬.*지연"):
        return "성호르몬 증가는 성장판 성숙과 골연령을 촉진하므로 골격 성숙을 지연시키지 않는다."
    if has(choice, "성호르몬.*촉진"):
        return "성호르몬, 특히 estrogen 작용은 골연령과 성장판 성숙을 촉진한다."
    if has(choice, r"고환.*4\s*[-~]\s*8"):
        return "고환 4~8 mL는 사춘기 시작 단계이며 남아의 최대 성장속도는 보통 더 뒤인 10~15 mL 무렵이다."
    if has(choice, "척추보다 다리가"):
        return "사춘기 초기에는 다리의 성장이 몸통보다 먼저 빨라져 일시적으로 신체 비율이 어색해 보일 수 있다."
    if has(choice, "여아보다 남아"):
        return "사춘기는 평균적으로 여아가 남아보다 약 1~2년 먼저 시작한다."
    if has(choice, "교육은 흡연 시작"):
        return "발달단계에 맞는 예방교육은 흡연 시작을 늦추는 데 도움이 된다."
    if has(choice, "급성 손상"):
        return "흡연·음주 예방과 위해감소 교육은 중독, 사고, 폭력 같은 급성 위해를 줄이는 목표가 있다."
    if has(choice, "비용.*건강"):
        return "효과적인 예방체계는 질병·사고 비용을 줄여 장기적인 건강·경제 편익이 구축비용을 웃돌 수 있다."
    if has(choice, "발달 상태"):
        return "추상적 훈계보다 청소년의 인지·사회정서 발달에 맞춘 프로그램이 행동변화 가능성이 높다."
    if has(choice, "흡연율이 매년"):
        return "청소년 흡연율이 사회정서적 미숙 때문에 매년 필연적으로 증가한다는 설명은 사실이 아니며 예방정책과 사회환경에 따라 변한다."
    adherence = {
        "친구와의 관계": "또래 압력·낙인·일상 공개 문제는 인슐린 누락과 직접 연결될 수 있어 중요한 질문이다.",
        "여가활동": "여가 일정도 참고할 수 있지만 가족·학교 관계와 질병에 대한 정서보다 지속적인 중증 비순응 원인을 설명하는 우선순위가 낮다.",
        "부모와의 관계": "보호자 갈등과 치료 책임의 전환은 청소년 만성질환 순응에 큰 영향을 준다.",
        "선생님과의 관계": "학교에서 투약할 공간·지원·낙인이 순응을 방해하는지 확인할 가치가 있다.",
        "당뇨에 대한 정서적 반응": "치료소진, 부정, 우울, 체중 걱정과 의도적 인슐린 생략을 직접 확인해야 한다.",
        "흡연여부": "흡연은 건강위험 문진에는 필요하지만 자살계획의 즉각적 위험도를 가르는 질문들보다 직접성은 낮다.",
        "가족 내의 상황": "가족 갈등·지지 상실·학대는 자살위험과 보호요인을 평가하는 핵심 정보다.",
        "죽음에 대한 인식변화": "죽음에 대한 집착·인식 변화는 자살사고의 심화와 직접 관련될 수 있다.",
        "친구관계의 변화": "고립·괴롭힘·관계 단절은 최근 자살위험 변화를 설명할 수 있다.",
        "주변환경의 변화": "이사·상실·폭력·학교 변화 같은 최근 스트레스 사건은 자살위험 평가에 중요하다.",
    }
    if choice in adherence:
        return adherence[choice]
    raise ValueError(f"{qid}: {choice}")


def choice_fact(question: dict, index: int) -> str:
    choice = clean(question["choices"][index])
    group = question["explanation"]["conceptGroup"]
    qid = question["id"]
    if group == "저산소허혈뇌병증 저체온치료": return fact_hie(choice)
    if group == "영아 두부손상과 학대": return fact_abuse(choice)
    if group == "신생아 두피 종괴": return fact_scalp(choice)
    if group == "미숙아 뇌실주위백질연화": return fact_pvl(choice, question["stem"])
    if group == "신생아 선별검사": return fact_nbs_by_index(qid, index, choice)
    if group == "선천대사질환 표적치료": return fact_metabolic(choice, qid)
    if group == "고페닐알라닌혈증과 BH4": return fact_bh4(choice, qid)
    if group == "고암모니아혈증 응급처치": return fact_hyperammonemia(choice, qid)
    if group == "갈락토스혈증": return fact_galactosemia(choice)
    if group == "소아 성장 평가": return fact_growth_by_index(qid, index, choice)
    if group == "영유아 발달 이정표": return fact_development(choice, qid)
    if group == "장중첩증": return fact_intussusception(choice, qid)
    if group == "소아 응급진료": return fact_ed_by_index(qid, index, choice)
    if group == "소아 뇌수막염": return fact_meningitis(choice, qid)
    if group == "홍역 감염관리": return fact_measles(choice)
    if group == "소아 해부·생리 특성": return fact_pediatric_difference(choice, qid)
    if group == "청소년 성장과 면담": return fact_adolescent(choice, qid)
    raise ValueError(f"{qid}: unhandled group {group}")


def is_negative_stem(stem: str) -> bool:
    return bool(re.search(r"옳지 않은|틀린|않는|않은|아닌|잘못|가치가 적은|관련성이 적은", stem))


def numeric_profile(question: dict) -> tuple[list[str], list[str]]:
    qid = question["id"]
    group = question["explanation"]["conceptGroup"]
    if group == "저산소허혈뇌병증 저체온치료":
        return ["표준 치료 대상: 재태주수 ≥36주, 출생 6시간 이내, 중등도~중증 신생아뇌병증과 주산기 저산소 근거"], ["목표 중심체온 33.5~34.5℃, 72시간 냉각 후 서서히 재가온"]
    if group == "신생아 선별검사":
        if qid.endswith(("2023-q062", "2022-q060", "2021-q022")):
            return ["건조혈반 채혈은 일반적으로 생후 48~72시간에 시행"], ["첫 방울은 닦고 원을 완전히 적신 뒤 최소 3시간 이상 수평 자연건조"]
        return [], []
    if group == "고페닐알라닌혈증과 BH4":
        return ["지속 고페닐알라닌혈증은 PAH 결핍과 BH4 합성·재생 결함을 구분"], ["문항 정상치 <100 또는 <120 μmol/L; 연속 상승이면 선별 반복보다 확진·BH4 감별로 진행"]
    if group == "고암모니아혈증 응급처치":
        return ["과호흡성 호흡알칼리증+고암모니아혈증+무케톤은 요소회로 이상을 강하게 시사"], ["암모니아는 μmol/L 또는 μg/dL 단위를 확인; 중증 신경증상·급격한 상승은 수치와 함께 즉시 체외제거 판단"]
    if group == "소아 성장 평가":
        if qid.endswith("2020-q029"):
            return ["출생체중은 약 4~6개월에 2배, 12개월에 3배; 출생길이는 약 12개월에 1.5배"], ["3.4→7.2 kg은 약 2.1배, 49→74 cm는 약 1.51배"]
        if qid.endswith(("2021-q019", "2022-q089")):
            return ["만 2세 미만은 누운키, 24개월부터 선키를 표준 성장차트와 맞춰 사용"], []
    if group == "소아 뇌수막염" and qid.endswith("2020-q035"):
        return ["바이러스성: 림프구 우세, 당 보존, 단백 경도 상승; 세균성: 호중구 우세, 당 감소, 단백 상승"], ["이 문항 CSF/혈청 glucose 비=81/107≈0.76로 보존됨"]
    if group == "청소년 성장과 면담":
        return ["남아 사춘기 시작: 고환용적 ≥4 mL; 성장속도 정점은 대략 10~15 mL 무렵", "여아 성장속도 정점: Tanner 유방 2~3단계 무렵"], []
    return [], []


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    reviewed = []
    for question in payload["questions"]:
        lecture = question.get("lectureNumber", "")
        if not lecture.isdigit() or not 14 <= int(lecture) <= 20:
            continue
        explanation = question.get("explanation") or {}
        if len(question.get("choices", [])) != 5 or len(question.get("answers", [])) == 0:
            raise SystemExit(f"{question['id']}: objective structure missing")
        negative = is_negative_stem(question["stem"])
        answers = set(question["answers"])
        choice_explanations = []
        for index, choice in enumerate(question["choices"]):
            number = index + 1
            if question["id"] == "gendev2-19-2022-q029" and number == 4:
                verdict = "족보 정답·오류 의심"
            elif question["id"] == "gendev2-19-2022-q029" and number == 5:
                verdict = "의학적으로 옳음·정답 재검토"
            elif number in answers:
                verdict = "정답(틀린 진술)" if negative else "정답"
            else:
                verdict = "제외(옳은 진술)" if negative else "오답"
            choice_explanations.append(f"‘{clean(choice)}’ — {verdict}. {choice_fact(question, index)}")
        explanation["choiceExplanations"] = choice_explanations
        criteria, numeric = numeric_profile(question)
        explanation["diagnosticCriteria"] = criteria
        explanation["numericReference"] = numeric
        explanation["numericReview"] = {
            "status": "applicable" if numeric else "not-applicable",
            "reason": "이 문항의 판단에 직접 필요한 수치만 기재" if numeric else "별도 수치 경계가 정답을 가르지 않음",
            "reviewedAt": REVIEW_DATE,
        }
        explanation["evidenceStatus"] = f"14~20강 문항·정답·이미지·각 선지 독립 재검수 ({REVIEW_DATE})"
        question["explanationReviewStatus"] = MARKER
        question["explanation"] = explanation
        reviewed.append(question)

    by_id = {question["id"]: question for question in reviewed}
    by_id["gendev2-16-2023-q060"]["stem"] = (
        "신생아 대사이상 선별검사에서 페닐알라닌 수치 이상으로 병원을 방문하여 "
        "tetrahydrobiopterin 부하검사를 시행한 신생아 4명의 검사 결과이다. "
        "A 환자의 치료방침은? (정상치 <100 μmol/L)"
    )
    by_id["gendev2-16-2023-q038"]["answerReviewStatus"] = "암모니아 1020 mg/dL 표기 단위 오류 의심 · 원본 재확인 필요"

    for question in reviewed:
        explanations = question["explanation"]["choiceExplanations"]
        if len(explanations) != 5 or len(set(explanations)) != 5:
            raise SystemExit(f"{question['id']}: missing or duplicate choice explanation")
        for index, text in enumerate(explanations):
            if len(text) > 430:
                raise SystemExit(f"{question['id']}: choice {index + 1} too long ({len(text)})")
            body = text.split(". ", 1)[-1]
            for other_index, other in enumerate(question["choices"]):
                other = clean(other)
                if other_index != index and len(other) >= 12 and other in body:
                    raise SystemExit(f"{question['id']}: choice {index + 1} contains choice {other_index + 1}")

    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    total = sum(len(q["explanation"]["choiceExplanations"]) for q in reviewed)
    average = sum(len(text) for q in reviewed for text in q["explanation"]["choiceExplanations"]) / total
    print(f"LECTURE_14_20_CHOICE_AUDIT_PASS questions={len(reviewed)} choices={total} average_chars={average:.1f}")


if __name__ == "__main__":
    main()
