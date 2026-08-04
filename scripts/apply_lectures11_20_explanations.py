from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"

TEXTBOOK = {
    "kind": "교과서",
    "label": "홍창의 소아과학 12판: 성장·발달, 신생아, 유전·대사, 감염, 응급 관련 장",
    "url": "https://snu-primo.hosted.exlibrisgroup.com/primo-explore/fulldisplay?docid=82SNU_INST51922742020002591&vid=82SNU&search_scope=ALL&tab=all&lang=ko_KR&context=L",
}

SOURCES = {
    "aha": {"kind": "현재 지침", "label": "AHA/AAP 2025 Neonatal Resuscitation Algorithm", "url": "https://cpr.heart.org/en/resuscitation-science/cpr-and-ecc-guidelines/algorithms/"},
    "cmv": {"kind": "현재 지침", "label": "CDC Clinical Overview of Congenital CMV", "url": "https://www.cdc.gov/cytomegalovirus/hcp/clinical-overview/index.html"},
    "hie": {"kind": "현재 지침", "label": "AAP 2026 Therapeutic Hypothermia for Neonatal HIE", "url": "https://publications.aap.org/pediatrics/article/157/2/e2025073627/206158/Therapeutic-Hypothermia-for-Neonatal-Hypoxic"},
    "acmg": {"kind": "진단 알고리듬", "label": "ACMG Newborn Screening ACT Sheets and Algorithms", "url": "https://www.acmg.net/act"},
    "cdc_hbv": {"kind": "현재 지침", "label": "CDC Hepatitis B Perinatal Vaccine Information", "url": "https://www.cdc.gov/hepatitis-b/hcp/perinatal-provider-overview/vaccine-administration.html"},
    "cdc_measles": {"kind": "현재 지침", "label": "CDC Interim Infection Prevention and Control Recommendations for Measles", "url": "https://www.cdc.gov/infection-control/hcp/measles/"},
    "who_growth": {"kind": "현재 기준", "label": "WHO Child Growth Standards", "url": "https://www.who.int/tools/child-growth-standards"},
    "cdc_milestone": {"kind": "현재 기준", "label": "CDC Developmental Milestones", "url": "https://www.cdc.gov/ncbddd/actearly/milestones/index.html"},
    "rhc_intuss": {"kind": "진료 알고리듬", "label": "Royal Children's Hospital Clinical Guideline: Intussusception", "url": "https://www.rch.org.au/clinicalguide/guideline_index/intussusception/"},
    "gene_ucd": {"kind": "출판 후 갱신", "label": "GeneReviews Urea Cycle Disorders Overview, updated 2025", "url": "https://www.ncbi.nlm.nih.gov/books/NBK1217/"},
    "aap_adolescent": {"kind": "현재 권고", "label": "AAP Adolescent Health: Confidentiality and Preventive Care", "url": "https://www.aap.org/en/patient-care/adolescent-sexual-health/"},
}

VISUALS = {
    "resuscitation": {
        "title": "진단·처치 흐름 참고: 2025 신생아 소생술",
        "summary": "OpenEvidence에서 후보를 찾은 뒤 AHA/AAP 원문으로 재확인한 자체 요약 흐름입니다.",
        "steps": ["출생 직후 만삭·근긴장·호흡/울음 평가", "무호흡/헐떡임 또는 심박수 <100회/분이면 효과적인 양압환기", "환기 교정 뒤에도 심박수 <60회/분이면 기도 확보와 3:1 흉부압박", "계속 <60회/분이면 혈관 확보 후 에피네프린, 저혈량·기흉 평가"],
        "sourceLabel": "AHA/AAP 2025 Neonatal Resuscitation Algorithm",
        "sourceUrl": SOURCES["aha"]["url"],
    },
    "cmv": {
        "title": "진단 흐름 참고: 선천 CMV",
        "summary": "검체와 채취 시점이 선천감염 여부를 가릅니다.",
        "steps": ["선천 CMV 의심 또는 표적 선별 양성", "생후 2~3주 이내 타액 PCR", "양성이면 소변 PCR로 확인", "3주가 지나면 출생 후 감염과 구분이 어려움"],
        "sourceLabel": "CDC Congenital CMV testing",
        "sourceUrl": SOURCES["cmv"]["url"],
    },
    "hie": {
        "title": "치료 적응 흐름 참고: HIE 저체온치료",
        "summary": "OpenEvidence가 제시한 2026 AAP Figure 1을 공식 원문에서 확인해 글로 다시 그린 흐름입니다.",
        "steps": ["재태주수와 출생 후 경과시간 확인(표준: ≥36주, 6시간 이내)", "주산기 저산소를 뒷받침하는 혈액가스·Apgar·지속 소생 여부 확인", "중등도~중증 뇌병증 또는 경련 확인", "적응 시 33.5~34.5℃로 72시간 치료하며 뇌파·체온·장기기능 감시"],
        "sourceLabel": "AAP 2026 Therapeutic Hypothermia Clinical Report",
        "sourceUrl": SOURCES["hie"]["url"],
    },
    "nbs": {
        "title": "진단 흐름 참고: 신생아 선별검사 양성",
        "summary": "ACMG ACT Sheet와 Algorithm의 공통 구조를 시험용으로 단순화했습니다.",
        "steps": ["선별검사 이상 결과와 응급성 확인", "ACT Sheet에 따라 즉시 대사전문의 연락·증상 평가", "질환별 확진검사 시행(혈장 아미노산, 효소, 유전자 등)", "확진 전에도 위기 위험이 크면 이화작용 차단·원인 영양소 중단 등 선제 처치"],
        "sourceLabel": "ACMG ACT Sheets and Algorithms",
        "sourceUrl": SOURCES["acmg"]["url"],
    },
    "intussusception": {
        "title": "진단·치료 흐름 참고: 장중첩증",
        "summary": "안정 여부와 복막자극징후가 공기정복과 수술의 갈림길입니다.",
        "steps": ["간헐적 복통·구토·기면이 있으면 장중첩증 의심", "소생과 정맥로 확보 후 초음파로 확인", "안정적이고 천공/복막염이 없으면 영상유도 공기 또는 조영 정복", "불안정·천공·복막염 또는 비수술 정복 실패면 수술"],
        "sourceLabel": "RCH Intussusception Clinical Guideline",
        "sourceUrl": SOURCES["rhc_intuss"]["url"],
    },
}


def ids(lecture: int, entries: str) -> list[str]:
    return [f"gendev2-{lecture:02d}-{item}" for item in entries.split()]


PROFILES: dict[str, dict] = {
    "resuscitation": {"concept": "신생아 소생술", "judgment": "무호흡 또는 헐떡임과 심박수 100회/분 미만은 양압환기의 적응이다. 심박수 60회/분 미만이라도 먼저 효과적인 환기를 확보한다.", "steps": ["호흡과 심박수를 먼저 분류한다.", "무호흡/헐떡임 또는 심박수 <100이면 마스크 양압환기를 시작한다.", "가슴 상승과 심박수 반응으로 환기 효과를 확인하고 다음 단계로 간다."], "review": "신생아 서맥의 가장 흔한 원인은 불충분한 폐환기다. 따라서 약물이나 흉부압박보다 환기 확보가 먼저이며, 30초간 효과적인 환기 뒤에도 심박수 <60회/분일 때 압박을 더한다.", "sources": ["aha"], "visual": "resuscitation"},
    "cmv": {"concept": "선천 CMV 진단", "judgment": "선천 CMV는 생후 2~3주 이내 타액 또는 소변 PCR로 확인해야 출생 후 감염과 구분할 수 있다.", "steps": ["선천감염을 의심한다.", "항체가 아니라 바이러스 DNA 검사를 고른다.", "생후 3주 이내 검체라는 시간 조건을 확인한다."], "review": "타액 PCR이 편리하지만 모유 오염 가능성 때문에 양성이면 소변 PCR로 확인한다. 3주 이후 양성은 선천감염인지 산후감염인지 판별하기 어렵다.", "sources": ["cmv"], "visual": "cmv"},
    "fgr": {"concept": "태아성장제한 유형", "judgment": "초기·유전적 손상은 대칭형, 임신 후기 태반기능부전은 머리가 상대적으로 보존되는 비대칭형 성장제한을 만든다.", "steps": ["원인이 시작된 시기를 본다.", "머리둘레와 복부둘레의 상대적 보존 여부를 본다.", "후기 태반기능부전이면 비대칭형을 고른다."], "review": "모체 혈관합병증이 심한 당뇨병은 태반기능부전으로 성장제한을 만들 수 있다. 반대로 혈당 과다 공급이 주된 경우에는 거대아가 흔하다.", "sources": []},
    "oligo": {"concept": "양수과소증과 태아 변형", "judgment": "프로스타글란딘 억제 NSAID는 태아 신혈류와 소변 생성을 줄여 양수과소증을 일으킬 수 있고, 지속 압박은 사지 변형을 만든다.", "steps": ["약물이 태아 소변량을 줄이는지 본다.", "양수 감소가 자궁 내 압박을 높인다고 연결한다.", "폐형성저하와 자세성 사지 변형을 합병증으로 고른다."], "review": "중기 이후 양수는 주로 태아 소변에서 온다. 심한 양수과소증은 폐형성저하, 제대압박, 관절 구축과 만곡족 같은 변형을 유발한다.", "sources": []},
    "fhr": {"concept": "태아심박수 감속", "judgment": "자궁수축과 거의 동시에 시작하고 최저점도 수축 정점과 일치하는 완만한 조기감속은 태아 머리 압박에 의한 미주신경 반응이다.", "steps": ["감속의 모양이 점진적인지 급격한지 본다.", "수축과 감속의 시작·최저점·회복 시점을 비교한다.", "수축을 거울처럼 따라가면 조기감속으로 판단한다."], "review": "조기감속은 머리 압박, 후기감속은 자궁태반기능부전, 변이감속은 제대압박을 시사한다. 반복 후기감속이나 지속 서맥은 즉각적인 원인 교정과 분만 평가가 필요하다.", "sources": []},
    "transition": {"concept": "출생 후 순환 전환", "judgment": "첫 호흡으로 폐혈관저항이 감소하면 폐혈류와 폐정맥 환류가 증가하고, 좌심방압 상승이 난원공의 기능적 폐쇄를 돕는다.", "steps": ["제대 결찰과 폐 팽창을 구분한다.", "폐 팽창은 폐혈관저항을 낮춘다.", "증가한 폐정맥 환류가 좌심방압을 올린다."], "review": "태아순환은 병렬이고 출생 후 직렬로 바뀐다. 제대 결찰은 전신혈관저항을 올리고, 폐 팽창은 폐혈관저항을 내려 좌→우 압력관계를 역전시킨다.", "sources": []},
    "apnea": {"concept": "영아 무호흡 평가", "judgment": "20초 이상 무호흡이나 청색증·서맥이 동반된 짧은 무호흡은 병적 사건으로 보고 즉시 원인을 평가한다.", "steps": ["시간과 동반 증상을 확인한다.", "정상 주기호흡과 병적 무호흡을 나눈다.", "병적이면 감염·호흡·신경·대사 원인을 평가한다."], "review": "주기호흡은 짧은 호흡중지가 반복되지만 청색증이나 서맥이 없다. 병적 무호흡은 자극과 기도·호흡 보조가 필요할 수 있다.", "sources": []},
    "hbv": {"concept": "B형간염 산모와 모유수유", "judgment": "출생 직후 적절한 HBIG와 B형간염 백신을 맞으면 처음부터 직접 모유수유할 수 있다.", "steps": ["신생아 면역예방이 완료됐는지 확인한다.", "모유를 통한 추가 전파 위험은 매우 낮다고 판단한다.", "젖꼭지 출혈 등 혈액 노출 상황만 별도 주의한다."], "review": "HBsAg 양성 산모의 신생아는 출생 12시간 이내 백신과 HBIG를 서로 다른 부위에 투여한다. 예방조치 때문에 모유수유를 미룰 이유는 없다.", "sources": ["cdc_hbv"]},
    "development": {"concept": "영유아 발달 이정표", "judgment": "운동·언어·인지·사회성 발달은 각 영역의 정상 순서를 기준으로 판단하며, 비대칭 소견은 단순 지연보다 신경학적 이상을 시사한다.", "steps": ["문항의 행동을 발달 영역으로 분류한다.", "대략적인 획득 연령과 순서를 확인한다.", "비대칭 또는 이미 사라져야 할 원시반사가 있는지 본다."], "review": "발달은 범위가 있지만 순서가 중요하다. 한 영역의 뚜렷한 지연, 기술의 소실, 지속적 비대칭은 조기 평가 대상이다.", "sources": ["cdc_milestone"]},
    "newborn_normal": {"concept": "정상 신생아 소견", "judgment": "독성홍반처럼 전신상태가 좋은 신생아의 일과성 피부 병변은 관찰과 안심이 원칙이다.", "steps": ["전신상태와 발병 시기를 본다.", "생리적·일과성 소견인지 감염성 병변인지 구분한다.", "정상 변이면 불필요한 검사와 치료를 피한다."], "review": "독성홍반은 생후 수일 내 홍반성 바탕의 구진·농포로 나타나며 자연 소실한다. 출생 시부터 있는 수포, 점막 침범, 아픈 모습은 감염을 배제해야 한다.", "sources": []},
    "breastmilk": {"concept": "모유의 생물학적 기능", "judgment": "모유의 면역·성장인자는 장장벽 성숙과 면역조절을 돕는다.", "steps": ["단순 열량 공급을 넘어선 모유 성분을 떠올린다.", "TGF-β 등 성장인자가 장 상피와 면역계에 미치는 영향을 연결한다.", "장 성숙을 촉진하는 설명을 고른다."], "review": "모유에는 분비형 IgA, lactoferrin, oligosaccharide, 성장인자와 살아있는 세포가 포함되어 감염 방어와 장내미생물·점막 성숙을 돕는다.", "sources": []},
    "preterm_exam": {"concept": "재태연령 신체평가", "judgment": "미숙할수록 피부가 얇고 투명하며 피하지방·발바닥 주름·유방결절·귀연골과 생식기 성숙이 적다.", "steps": ["사진의 피부와 발바닥 주름을 본다.", "귀 연골과 생식기 성숙도를 함께 본다.", "여러 신체 소견을 묶어 재태연령을 추정한다."], "review": "New Ballard Score는 신경근육 성숙과 신체 성숙을 함께 평가한다. 단일 사진보다 여러 항목의 일관성이 중요하다.", "sources": []},
    "iwl": {"concept": "미숙아 불감수분손실", "judgment": "재태연령이 낮고 출생 직후일수록 피부장벽이 미숙해 불감수분손실이 크며, 방사보온기는 이를 증가시킨다.", "steps": ["피부 성숙도와 환경을 본다.", "습도·보온 방식이 증발량에 미치는 영향을 연결한다.", "시간이 지나 피부가 성숙하면 손실이 감소한다고 판단한다."], "review": "미숙아는 높은 습도와 보육기 관리가 증발성 손실을 줄인다. 수액은 체중·소변량·나트륨·혈당을 반복 측정해 조절한다.", "sources": []},
    "fluid": {"concept": "신생아 수액 계산", "judgment": "신생아 수액은 체중당 일일 요구량을 계산한 뒤 임상 상태와 소변·전해질에 따라 조절한다.", "steps": ["현재 생후일과 체중을 확인한다.", "mL/kg/day에 체중을 곱한다.", "광선치료·방사보온·미숙도 등 추가 손실을 보정한다."], "review": "고정 수치만 외우지 말고 체중 변화, 소변량, 혈청 나트륨으로 적정성을 재평가한다.", "sources": []},
    "hie": {"concept": "저산소허혈뇌병증 저체온치료", "judgment": "중등도~중증 HIE는 가능한 출생 6시간 이내 치료적 저체온요법을 시작하는 것이 핵심이다.", "steps": ["재태주수와 출생 후 시간을 확인한다.", "주산기 저산소 근거와 뇌병증 중증도를 평가한다.", "적응이면 신속히 냉각센터와 연계한다."], "review": "2026 AAP는 표준군을 ≥36주, 출생 6시간 이내 중등도~중증 HIE로 둔다. 목표체온 33.5~34.5℃에서 72시간 시행하며 지속 뇌파·장기기능 감시가 필요하다.", "sources": ["hie"], "visual": "hie"},
    "abuse": {"concept": "영아 두부손상과 학대", "judgment": "출생 외상으로 설명하기 어려운 경막하출혈, 망막출혈, 병력과 맞지 않는 손상은 아동학대를 우선 고려한다.", "steps": ["출생 직후 손상인지 이후 손상인지 본다.", "손상 양상과 보호자 병력의 일치성을 본다.", "의심 시 안전 확보와 체계적 추가 평가를 시행한다."], "review": "학대 의심은 단정이 아니라 보호를 위한 진단 과정이다. 골격조사, 안과검사, 뇌영상과 다학제 평가가 필요할 수 있다.", "sources": []},
    "cephalohematoma": {"concept": "신생아 두피 종괴", "judgment": "두혈종은 골막 아래 출혈이므로 봉합선을 넘지 않는다.", "steps": ["종괴가 출생 직후인지 본다.", "봉합선을 넘는지 확인한다.", "골막하 병변이면 두혈종을 고른다."], "review": "산류는 봉합선을 넘고, 두혈종은 한 두개골에 국한된다. 광범위하고 진행하는 모상건막하출혈은 쇼크 위험이 있어 응급이다.", "sources": []},
    "pvl": {"concept": "미숙아 뇌실주위백질연화", "judgment": "미숙아의 뇌실주위 백질 손상은 하지를 지배하는 피질척수로를 잘 침범해 경직성 양하지마비를 남긴다.", "steps": ["미숙아라는 위험요인을 확인한다.", "영상의 뇌실주위 백질 병변을 읽는다.", "경직성 운동장애와 연결한다."], "review": "PVL은 미숙아 뇌성마비의 중요한 원인이다. 하지가 상지보다 더 심한 경직성 양하지마비가 전형적이다.", "sources": []},
    "nbs": {"concept": "신생아 선별검사", "judgment": "선별검사는 증상 전 치료 이득이 큰 질환을 대상으로 하며, 적절한 시점·채혈·건조·운송이 정확도를 좌우한다.", "steps": ["선별 대상 질환인지 확인한다.", "발뒤꿈치 안전 부위에서 여과지를 충분히 적신다.", "완전 건조 후 오염·열·습기를 피해 운송한다."], "review": "선별 양성은 진단이 아니다. 질환별 확진검사와 ACT Sheet에 따른 긴급도를 확인한다. 채혈지를 젖은 채 비닐에 밀봉하면 검체가 손상될 수 있다.", "sources": ["acmg"], "visual": "nbs"},
    "metabolic_treatment": {"concept": "선천대사질환 표적치료", "judgment": "결핍 효소·보조인자·축적 물질의 기전을 확인해 식이제한, 효소대체, 킬레이션 또는 호르몬대체를 연결한다.", "steps": ["결핍된 효소나 축적 물질을 찾는다.", "가역적 보조인자 반응 여부를 확인한다.", "질환 기전에 맞는 장기 치료를 고른다."], "review": "Gaucher병은 효소대체, Wilson병은 구리 킬레이션/흡수억제, 선천갑상샘저하증과 CAH는 결핍 호르몬 보충이 치료의 중심이다.", "sources": ["acmg"]},
    "bh4": {"concept": "고페닐알라닌혈증과 BH4", "judgment": "BH4 반응성 PKU는 페닐알라닌 제한에 sapropterin을 병용할 수 있고, 중추 BH4 결핍은 신경전달물질 전구체 보충이 추가된다.", "steps": ["고페닐알라닌혈증을 확인한다.", "BH4 부하 반응과 pterin/DHPR 결과를 구분한다.", "말초 PKU와 중추 BH4 결핍의 치료 차이를 고른다."], "review": "모든 고페닐알라닌혈증을 같은 방식으로 치료하지 않는다. 중추 BH4 결핍은 dopamine·serotonin 합성도 떨어져 L-dopa와 5-HTP가 필요할 수 있다.", "sources": ["acmg"], "visual": "nbs"},
    "hyperammonemia": {"concept": "고암모니아혈증 응급처치", "judgment": "비케톤성 고암모니아혈증과 호흡성 알칼리증은 요소회로 이상을 시사하며, 단백질을 중단하고 고농도 포도당으로 이화를 막은 뒤 심하면 투석한다.", "steps": ["암모니아를 즉시 재확인하고 채혈 오류를 배제한다.", "단백질 중단과 포도당/지질로 이화작용을 차단한다.", "질소제거제·arginine/citrulline을 투여하고 중증이면 혈액투석한다."], "review": "고암모니아혈증은 수치보다 신경학적 악화 속도가 중요하다. 신속한 대사전문의 협진과 체외제거가 뇌손상을 줄인다.", "sources": ["acmg", "gene_ucd"], "visual": "nbs"},
    "galactosemia": {"concept": "갈락토스혈증", "judgment": "신생아 황달·간부전·패혈증 양상에서 갈락토스혈증을 의심하면 즉시 유당/갈락토스를 중단하고 확진검사를 진행한다.", "steps": ["수유 뒤 악화되는 간질환을 인지한다.", "갈락토스 또는 GALT 이상을 확인한다.", "확진 전이라도 lactose-free formula로 바꾼다."], "review": "고전 갈락토스혈증은 E. coli 패혈증 위험이 있다. 최근 수혈은 적혈구 GALT 효소검사를 거짓 정상으로 만들 수 있어 유전자검사를 고려한다.", "sources": ["acmg"], "visual": "nbs"},
    "growth": {"concept": "소아 성장 평가", "judgment": "성장은 한 번의 수치보다 표준 성장곡선에서의 위치와 시간에 따른 성장속도로 판단한다.", "steps": ["정확한 방법으로 키·체중·머리둘레를 잰다.", "연령·성별 성장곡선에 표시한다.", "백분위수 교차와 신체 비율을 본다."], "review": "2세 미만은 누운키를 재고, 이후 선키를 사용한다. 영아기는 체중 변화가 빠르므로 출생체중 배수와 성장곡선을 함께 본다.", "sources": ["who_growth"]},
    "intussusception": {"concept": "장중첩증", "judgment": "안정적인 장중첩증은 초음파로 진단하고 천공·복막염이 없으면 공기정복이 진단과 치료를 겸한다.", "steps": ["간헐적 복통·구토·기면을 인지한다.", "초음파의 표적징후로 확인한다.", "불안정·천공·복막염이 없으면 비수술 정복을 시행한다."], "review": "혈변이나 복부 종괴의 고전적 삼징후가 모두 나타나지 않아도 된다. 정복 실패, 천공, 복막염 또는 쇼크면 수술이 필요하다.", "sources": ["rhc_intuss"], "visual": "intussusception"},
    "pediatric_ed": {"concept": "소아 응급진료", "judgment": "소아 응급은 연령별 정상범위와 해부·생리 차이를 아는 팀이 중증도에 따라 신속히 안정화해야 한다.", "steps": ["ABCDE로 즉시 위험을 찾는다.", "연령에 맞는 활력징후와 장비를 적용한다.", "감염격리·관찰·입원 동선을 중증도에 맞춘다."], "review": "소아는 보상 후 급격히 악화할 수 있다. 진료구역은 전방 응급처치와 후방 관찰·입원대기 기능을 분리할 수 있다.", "sources": []},
    "meningitis": {"concept": "소아 뇌수막염", "judgment": "영아는 경부강직 같은 수막자극징후가 없다고 뇌수막염을 배제할 수 없으며, CSF 세포·당·단백과 임상상으로 세균성과 바이러스성을 구분한다.", "steps": ["연령별 비특이 증상을 인지한다.", "안정화와 혈액배양 후 요추천자 가능 여부를 판단한다.", "CSF 양상과 배양/PCR로 원인을 좁힌다."], "review": "세균성은 대개 호중구 증가, 저당, 고단백이 뚜렷하지만 초기에는 전형적이지 않을 수 있다. 치료 지연 위험이 있으면 요추천자보다 경험적 항균제가 먼저다.", "sources": []},
    "measles": {"concept": "홍역 감염관리", "judgment": "홍역 의심 환자는 즉시 공기주의 음압격리하고 검사와 신고를 진행한다.", "steps": ["발열·기침/콧물/결막염과 발진을 인지한다.", "대기실 노출 전에 마스크와 공기주의 격리를 시행한다.", "보건당국과 감염관리팀에 연락한다."], "review": "홍역은 공기전파력이 매우 높다. 표준주의나 비말주의만으로 부족하며, 면역이 확인된 인력이 적절한 호흡보호구를 착용한다.", "sources": ["cdc_measles"]},
    "pediatric_difference": {"concept": "소아 해부·생리 특성", "judgment": "소아는 성인보다 흉벽 순응도가 크고 기도 직경이 작으며 장기별 질환 스펙트럼이 다르다.", "steps": ["연령에 따라 변하는 구조를 찾는다.", "작은 기도 반경 변화가 저항을 크게 올린다고 연결한다.", "성인 기준을 그대로 적용한 선지를 피한다."], "review": "영아 갈비뼈는 더 수평이고 흉벽은 유연하다. 고전 시험에서는 윤상연골을 가장 좁은 부위로 배우지만, 현대 영상은 성문 부위를 기능적으로 중요한 협착점으로 본다.", "sources": []},
    "adolescent": {"concept": "청소년 성장과 면담", "judgment": "사춘기 성장급증의 시기와 HEEADSSS 비밀보장 면담을 함께 이해해야 청소년 위험행동과 순응 문제를 평가할 수 있다.", "steps": ["성별 Tanner 단계와 성장급증 시기를 확인한다.", "보호자와 분리된 비밀보장 면담을 마련한다.", "Home·Education/Employment·Activities·Drugs·Sexuality·Suicide/Safety를 체계적으로 묻는다."], "review": "여아 성장급증은 비교적 이른 Tanner 2~3, 남아는 고환용적 증가 뒤 Tanner 3~4 무렵이 두드러진다. 자살위험은 직접 묻는 것이 위험을 높이지 않으며 계획·수단·과거시도를 확인한다.", "sources": ["aap_adolescent"]},
}

GROUPS = {
    "resuscitation": ids(11, "2025-q041 2023-q059 2021-q012"),
    "cmv": ids(11, "2025-q042"),
    "fgr": ids(11, "2023-q012 2022-q066 2021-q011 2020-q022") + ids(13, "2025-q037 2023-q041 2022-q058 2021-q015"),
    "oligo": ids(11, "2022-q067"),
    "fhr": ids(11, "2020-q021"),
    "transition": ids(12, "2025-q025 2021-q013"),
    "apnea": ids(12, "2025-q026"),
    "hbv": ids(12, "2023-q044"),
    "development": ids(12, "2023-q076 2022-q007 2021-q014") + ids(17, "2025-q018 2022-q018 2021-q020 2020-q030"),
    "newborn_normal": ids(12, "2020-q024"),
    "breastmilk": ids(12, "2020-q023"),
    "preterm_exam": ids(13, "2025-q038 2021-q016 2020-q025"),
    "iwl": ids(13, "2023-q084 2022-q033"),
    "fluid": ids(13, "2020-q026"),
    "hie": ids(14, "2025-q027 2021-q018 2020-q028"),
    "abuse": ids(14, "2025-q028 2023-q055 2022-q009"),
    "cephalohematoma": ids(14, "2023-q042"),
    "pvl": ids(14, "2023-q063 2022-q016 2021-q017 2020-q027"),
    "nbs": ids(15, "2025-q083 2023-q062 2022-q060 2021-q022 2020-q033"),
    "metabolic_treatment": ids(15, "2025-q084 2023-q082 2022-q021 2021-q021 2020-q034"),
    "bh4": ids(16, "2025-q085 2023-q060 2021-q023 2020-q031"),
    "hyperammonemia": ids(16, "2025-q086 2023-q038 2022-q061 2021-q024"),
    "galactosemia": ids(16, "2022-q017 2020-q032"),
    "growth": ids(17, "2025-q017 2022-q089 2021-q019 2020-q029"),
    "intussusception": ids(18, "2025-q067 2023-q064 2022-q008"),
    "pediatric_ed": ids(18, "2025-q068 2023-q026 2022-q030"),
    "meningitis": ids(18, "2021-q025 2020-q035 2020-q036"),
    "measles": ids(18, "2021-q026"),
    "pediatric_difference": ids(19, "2025-q019 2025-q020 2023-q024 2023-q037 2022-q029 2022-q090 2021-q027 2021-q028 2020-q037 2020-q038"),
    "adolescent": ids(20, "2025-q005 2025-q006 2023-q057 2023-q083 2022-q019 2022-q071 2021-q029 2021-q030 2020-q039 2020-q040"),
}


def choice_explanations(question: dict, profile: dict) -> list[str]:
    answers = set(question.get("answers", []))
    result = []
    for number, choice in enumerate(question.get("choices", []), 1):
        if number in answers:
            result.append(f"정답 선지. {profile['judgment']}")
        else:
            result.append(f"이 문항의 결정 단서와 맞지 않는다. ‘{choice}’는 다른 시기·상태·적응증에서는 가능할 수 있으므로, 정답 개념인 {profile['concept']}과 구분한다.")
    return result


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    by_id = {q["id"]: q for q in payload["questions"]}
    assigned = {qid for group in GROUPS.values() for qid in group}
    targets = {q["id"] for q in payload["questions"] if q["lectureNumber"].isdigit() and 11 <= int(q["lectureNumber"]) <= 20}
    if assigned != targets:
        raise SystemExit(f"mapping mismatch missing={sorted(targets-assigned)} extra={sorted(assigned-targets)}")

    for profile_id, question_ids in GROUPS.items():
        profile = PROFILES[profile_id]
        for qid in question_ids:
            q = by_id[qid]
            source_ids = profile.get("sources", [])
            explanation = {
                "conceptGroup": profile["concept"],
                "keyJudgment": profile["judgment"],
                "reasoningSteps": profile["steps"],
                "choiceExplanations": choice_explanations(q, profile),
                "conceptReview": profile["review"],
                "evidenceStatus": "홍창의 소아과학 12판·현재 공식 지침 대조 · 2026-08",
                "sources": [TEXTBOOK] + [SOURCES[source_id] for source_id in source_ids],
            }
            if profile.get("visual"):
                explanation["diagnosticVisual"] = VISUALS[profile["visual"]]
            q["explanation"] = explanation
            q["explanationReviewStatus"] = explanation["evidenceStatus"]
            q["keyConcepts"] = list(dict.fromkeys([profile["concept"], q.get("lectureTitle", "")]))[:3]

    by_id["gendev2-19-2022-q029"]["answerReviewStatus"] = "족보 정답 ④와 현재 소아 흉벽 설명 충돌 · 선지/정답 오류 의심"
    for qid in ("gendev2-19-2021-q028", "gendev2-19-2020-q037"):
        by_id[qid]["answerReviewStatus"] = "고전 교과서 정답(윤상연골) · 현대 영상해부학에서는 성문부 강조"

    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"LECTURES11_20_EXPLANATIONS_APPLIED count={len(targets)} visuals={sum(bool(by_id[qid]['explanation'].get('diagnosticVisual')) for qid in targets)}")


if __name__ == "__main__":
    main()
