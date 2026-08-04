from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"

SOURCES = {
    "w43": {"label": "Williams Obstetrics 26e, Ch. 43 Obstetrical Hemorrhage", "url": "https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=257536897", "kind": "교과서"},
    "pph": {"label": "ACOG Practice Bulletin 183: Postpartum Hemorrhage", "url": "https://www.acog.org/clinical/clinical-guidance/practice-bulletin/articles/2017/10/postpartum-hemorrhage", "kind": "현재 지침"},
    "w41": {"label": "Williams Obstetrics 26e, Ch. 41 Hypertensive Disorders", "url": "https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=263820558", "kind": "교과서"},
    "aspirin": {"label": "ACOG/SMFM: Low-dose aspirin for prevention of preeclampsia", "url": "https://www.acog.org/clinical/clinical-guidance/practice-advisory/articles/2021/12/low-dose-aspirin-use-for-the-prevention-of-preeclampsia-and-related-morbidity-and-mortality", "kind": "현재 지침"},
    "w47": {"label": "Williams Obstetrics 26e, Ch. 47 Fetal-Growth Disorders", "url": "https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=263825314", "kind": "교과서"},
    "fgr": {"label": "SMFM Consult Series 52: Fetal growth restriction", "url": "https://publications.smfm.org/publications/289-society-for-maternal-fetal-medicine-consult-series-52/", "kind": "현재 지침"},
    "ttts": {"label": "SMFM Consult Series 72: TTTS and TAPS", "url": "https://publications.smfm.org/publications/574-society-for-maternal-fetal-medicine-consult-series-72/", "kind": "현재 지침"},
    "w36": {"label": "Williams Obstetrics 26e, Ch. 36 The Puerperium", "url": "https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=249764077", "kind": "교과서"},
    "cdc_mec": {"label": "CDC U.S. Medical Eligibility Criteria for Contraceptive Use, 2024", "url": "https://www.cdc.gov/contraception/hcp/usspr/classifications-mec-contraception.html", "kind": "현재 지침"},
    "epl": {"label": "ACOG Practice Bulletin 200: Early Pregnancy Loss", "url": "https://www.acog.org/clinical/clinical-guidance/practice-bulletin/articles/2018/11/early-pregnancy-loss", "kind": "현재 지침"},
    "ectopic": {"label": "ACOG: Ectopic Pregnancy", "url": "https://www.acog.org/womens-health/faqs/ectopic-pregnancy", "kind": "현재 지침"},
}

PROFILES = {
    "previa": ("전치태반과 임신후반기 출혈", ["활력징후와 출혈량, 태아상태를 먼저 안정화한다.", "초음파로 태반 위치를 확인하고 전치태반 전에는 손가락 질검진을 피한다.", "안정적이면 임신주수에 맞춰 관찰하고, 조절되지 않는 출혈이나 모체·태아 불안정이면 분만한다."], "전치태반은 통증 없는 선홍색 출혈이 전형적이다. 안정적 조산기 출혈은 입원 관찰·스테로이드 등을 고려하지만, 대량 출혈이나 태아곤란에서는 제왕절개가 우선이다.", ["w43"]),
    "abruption": ("태반조기박리", ["통증, 자궁긴장, 출혈과 쇼크를 보고 조기박리를 의심한다.", "모체 소생과 태아심박 감시를 동시에 시행한다.", "생존 태아가 위급하면 응급 제왕절개, 태아사망이면 산모가 안정적인 한 질식분만을 우선한다."], "태반조기박리의 외부 출혈량은 실제 박리 정도를 과소평가할 수 있다. 쇼크·DIC를 감시하며, 분만 방법은 태아 생존과 모체·태아 안정성으로 결정한다.", ["w43"]),
    "pph": ("산후출혈과 자궁무력증", ["Tone, Trauma, Tissue, Thrombin의 네 원인을 빠르게 구분한다.", "부드럽고 커진 자궁이면 자궁무력증을 가장 먼저 본다.", "자궁마사지와 oxytocin을 시작하고 반응이 없으면 추가 자궁수축제와 시술로 단계 상승한다."], "산후출혈의 가장 흔한 원인은 자궁무력증이다. 수액·혈액 준비와 원인 교정을 동시에 하며, 자궁수축제 금기는 고혈압(ergot), 천식(carboprost)처럼 환자별로 확인한다.", ["pph"]),
    "preeclampsia": ("전자간증 병태생리와 중증도", ["20주 이후 고혈압과 단백뇨 또는 장기손상 여부를 확인한다.", "중증 혈압, 신경계 증상, 혈소판·간·신장 이상, 폐부종과 태아상태를 평가한다.", "중증 소견과 임신주수에 따라 혈압 조절·MgSO4·분만 시점을 결정한다."], "비정상 영양막 침윤과 나선동맥 재형성 실패가 태반 허혈을 만들고, 항혈관생성 인자가 전신 내피기능장애를 유발한다. 37주 이상 비중증 전자간증은 분만하고, 조절되지 않는 중증 소견은 주수와 무관하게 분만이 필요할 수 있다.", ["w41", "aspirin"]),
    "twins": ("쌍태임신과 융모막성", ["첫삼분기 초음파에서 융모막성과 양막성을 먼저 판정한다.", "단일융모막 이양막 쌍태는 16주부터 적어도 2주마다 TTTS 감시를 한다.", "양수, 방광, 성장과 제대동맥 도플러를 함께 보고 감시 간격·태아치료를 결정한다."], "TTTS는 태반 혈관연결이 있는 단일융모막 임신에서 생긴다. 단일양막에서는 제대 얽힘 위험이, 단일융모막에서는 TTTS·선택적 성장제한 위험이 특히 중요하다.", ["ttts"]),
    "fgr": ("태아성장제한과 도플러 감시", ["EFW 또는 복부둘레가 10백분위 미만인지 확인한다.", "기형·감염·염색체 이상과 태반기능부전을 감별한다.", "제대동맥 도플러와 CTG로 악화를 추적하고 주수와 이완기 혈류에 따라 분만한다."], "FGR 진단 뒤 제대동맥 도플러는 태반 저항과 사산 위험을 반영한다. 정상 도플러는 보통 1–2주 간격, 심한 FGR은 주 1회, AEDV/REDV는 더 잦은 감시와 조기분만이 필요하다.", ["w47", "fgr"]),
    "puerperium": ("산욕기 감염·수유·피임", ["산후 발열은 자궁, 수술상처, 요로와 유방을 차례로 진찰한다.", "감염 부위와 중증도에 맞춰 배농과 항균제를 선택한다.", "수유 지속 가능성과 산후 혈전위험을 함께 고려해 피임법을 정한다."], "제왕절개 후 자궁내막염은 광범위 혐기성·호기성 균을 덮는 clindamycin+gentamicin이 고전적 1차 치료다. 수유성 유방염은 수유·배액을 유지하며 항포도알균제를 쓰고, 산후 초기 복합호르몬 피임은 VTE와 수유 영향을 고려해 피한다.", ["w36", "cdc_mec"]),
    "early": ("초기임신 출혈과 유산", ["활력징후와 파열·대량출혈 위험을 먼저 배제한다.", "질초음파의 임신 위치·배아 심박과 연속 hCG를 함께 해석한다.", "생존 자궁내임신, 유산, 임신위치불명과 자궁외임신으로 나눠 추적 또는 치료한다."], "닫힌 자궁경부와 심박이 있는 자궁내임신은 절박유산이다. 진단이 확실한 초기임신소실은 기대·약물·수술 치료가 가능하며, 불안정·감염·대량출혈이면 수술을 우선한다.", ["epl", "ectopic"]),
    "ectopic": ("임신위치불명과 자궁외임신", ["쇼크와 복강내 출혈 소견이 있으면 즉시 수술 경로로 간다.", "안정적 PUL은 48시간 hCG와 반복 질초음파로 위치와 생존성을 추적한다.", "확진 또는 강한 의심에서 조건에 따라 methotrexate나 수술을 선택한다."], "PUL은 진단명이 아니라 추적 상태다. 안정적이고 파열 소견이 없으며 추적 가능한 환자에서 methotrexate를 고려하고, 혈역학 불안정·파열 의심·추적 불가에서는 수술한다.", ["ectopic", "epl"]),
}


# id: (profile, 핵심 판단, 정답 선지의 이유)
SPECS = {
    "gendev2-06-2025-q087": ("previa", "31주 출혈이지만 산모와 태아가 안정적이고 초음파상 전치태반이 의심된다. 즉시 질검진이나 분만보다 관찰이 우선이다.", "안정적 조산기 전치태반 출혈에서는 입원 감시와 기대요법이 맞다."),
    "gendev2-06-2025-q088": ("abruption", "복통·대량출혈·쇼크와 비정상 태아심박은 중증 태반조기박리이다. 소생과 동시에 응급 제왕절개가 필요하다.", "생존 태아가 위급하고 산모도 불안정하므로 가장 빠른 분만이 필요하다."),
    "gendev2-06-2023-q007": ("previa", "통증 없는 반복 출혈과 자궁경부를 덮는 태반 영상은 전치태반을 가리킨다.", "임상 양상과 초음파 위치가 전치태반에 일치한다."),
    "gendev2-06-2023-q029": ("pph", "열상·잔류태반이 보이지 않고 이완된 자궁에서 출혈하므로 자궁무력증이다. 첫 약은 oxytocin이다.", "자궁마사지와 함께 사용하는 1차 자궁수축제이다."),
    "gendev2-06-2022-q056": ("previa", "질초음파에서 태반이 내자궁구를 덮고 태아는 사망했다. 전치태반 때문에 일반 유도분만보다 출혈을 통제할 수 있는 수술 분만을 택한다.", "전치태반이 산도를 막아 질식분만의 대량출혈 위험이 크다."),
    "gendev2-06-2022-q057": ("abruption", "중증 고혈압 환자의 갑작스런 통증·출혈과 태아곤란은 조기박리이다. 응급 제왕절개가 답이다.", "지연하면 태아저산소증과 모체 출혈이 악화한다."),
    "gendev2-06-2021-q087": ("previa", "초음파상 전치태반과 태아사망이 함께 있다. 산도를 막는 태반 때문에 수술 분만이 필요하다.", "태아사망만으로 항상 질식분만하는 것은 아니며 전치태반은 분만경로를 바꾼다."),
    "gendev2-06-2021-q088": ("abruption", "통증성 출혈과 태아사망은 태반조기박리에 합당하다. 산모가 안정적이면 질식 유도분만이 수술보다 출혈 부담이 적다.", "태아사망 후 산모가 안정적이고 질식분만이 가능하면 유도분만을 우선한다."),
    "gendev2-06-2020-q019": ("early", "CRL 7 mm 이상인데 심박이 없으면 초기임신소실 진단 기준에 부합한다. 내용상 10강에 더 가깝다.", "배아가 보이지만 심박이 없어 계류유산에 해당한다."),
    "gendev2-06-2020-q020": ("ectopic", "hCG가 판별구역 부근인데 48시간 상승이 불충분하고 자궁내 임신이 보이지 않는다. 안정적이고 추적 가능해 methotrexate를 선택한다.", "비파열 자궁외임신 가능성이 높고 약물치료 조건에 맞는다."),
    "gendev2-07-2025-q053": ("preeclampsia", "전자간증 2단계 모델의 첫 단계는 영양막 침윤과 나선동맥 재형성 실패이다.", "얕은 영양막 침윤이 태반 관류부전을 시작한다."),
    "gendev2-07-2025-q054": ("preeclampsia", "34주 미만 기대요법 중 약물로도 조절되지 않는 중증 고혈압은 지연하지 말고 분만해야 한다.", "지속되는 조절 불가 중증 혈압은 즉시 분만 적응증이다."),
    "gendev2-07-2023-q025": ("preeclampsia", "150/100과 혈소판 9만은 중증 소견이다. 외래관찰 대상으로 보는 설명이 틀렸다.", "혈소판 10만 미만은 중증 소견이므로 입원 평가와 분만계획이 필요하다."),
    "gendev2-07-2022-q073": ("preeclampsia", "35주 단백뇨는 크지만 중증 혈압·혈소판감소·신기능장애가 없다. 안정적으로 감시해 37주 분만한다.", "단백뇨 양 자체는 중증 기준이 아니며 비중증이면 37주 분만이 원칙이다."),
    "gendev2-07-2022-q077": ("preeclampsia", "과거 34주 이전 중증 전자간증 분만은 고위험 병력이다. 12–28주, 가능하면 16주 전에 저용량 aspirin을 시작한다.", "고위험 환자의 전자간증 재발 예방 표준이다."),
    "gendev2-07-2021-q079": ("preeclampsia", "35주에 creatinine 1.2 mg/dL은 신장 중증 소견이다. 34주 이후 중증 전자간증이므로 분만한다.", "중증 신기능장애가 있어 37주까지 기다리지 않는다."),
    "gendev2-07-2021-q080": ("preeclampsia", "부종·단백뇨·혈전·용혈을 하나로 설명하는 핵심은 전신 내피기능장애이다.", "혈관 투과성, 혈소판 활성과 미세혈관병성 용혈을 연결한다."),
    "gendev2-07-2020-q013": ("preeclampsia", "25주라도 160/110, 시각증상, 혈소판 7.8만과 심한 FGR은 중증이다. 족보 정답 ②는 현재 기준과 충돌해 선지·정답 오류가 의심된다.", "족보 표기 정답이나, 지속 중증 고혈압에서 치료를 피하라는 설명은 현재 표준과 맞지 않는다."),
    "gendev2-07-2020-q014": ("preeclampsia", "전자간증에서는 soluble endoglin이 증가하고 다태임신은 저용량 aspirin 고위험 적응증이다. 따라서 ③, ⑤가 맞다.", "두 진술 모두 현재 병태생리와 예방지침에 부합한다."),
    "gendev2-08-2025-q035": ("twins", "24주 쌍태에서 즉시 태아치료 기준이 없고 추적이 필요하다. 단일융모막이면 짧은 간격 감시가 핵심이다.", "현재 중증 TTTS 소견이 없어 2주 내 재평가가 적절하다."),
    "gendev2-08-2025-q036": ("fgr", "25주 조기 중증 FGR에서 입원 판단을 바꾸는 핵심은 제대동맥 이완기 혈류 이상이다.", "AEDV/REDV는 악화 위험이 높아 집중감시가 필요하다."),
    "gendev2-08-2023-q051": ("twins", "TTTS는 단일융모막이면 양막성에 관계없이 생길 수 있다. 단일양막에서는 생기지 않는다는 문장이 틀렸다.", "단일융모막 단일양막 쌍태도 태반 혈관연결이 있어 TTTS가 가능하다."),
    "gendev2-08-2023-q065": ("twins", "단일융모막 이양막 쌍태는 TTTS·성장불일치 때문에 짧은 간격 초음파 감시가 필요하다.", "이상 소견이 의심되어 1주 추적이 안전하다."),
    "gendev2-08-2022-q045": ("fgr", "태반기능부전은 후기 비대가 주로 영향을 받아 전형적으로 비대칭 FGR을 만든다. 대칭형이라는 설명이 틀렸다.", "자궁태반기능부전이 대칭형을 만든다는 문장이 오답이다."),
    "gendev2-08-2022-q048": ("twins", "첫삼분기 초음파의 융모막성이 이융모막임을 시사한다. TTTS는 공통 태반 혈관연결이 없어 예상되지 않는다.", "TTTS는 단일융모막 쌍태의 고유 합병증이다."),
    "gendev2-08-2021-q081": ("twins", "영상은 단일융모막 이양막 쌍태에 합당하다. 제대 얽힘은 같은 양막강을 쓰는 단일양막에서 주로 생긴다.", "양막이 분리되어 있어 제대 얽힘은 직접 관련이 가장 적다."),
    "gendev2-08-2021-q082": ("fgr", "성장곡선상 FGR의 예후와 분만시점을 가장 잘 바꾸는 감시는 제대동맥 도플러이다.", "태반 저항과 이완기 혈류 소실·역전을 직접 평가한다."),
    "gendev2-08-2020-q009": ("twins", "단일융모막 이양막 쌍태에서는 TTTS와 성장불일치가 중요하지만 제대 얽힘은 덜 관련된다.", "제대 얽힘은 주로 단일양막 쌍태의 위험이다."),
    "gendev2-08-2020-q010": ("fgr", "33주 중증 FGR이라도 NST와 제대동맥 도플러가 정상이면 즉시 분만보다 촘촘한 감시를 한다.", "1주 후 제대동맥 도플러와 양수량 재평가가 적절하다."),
    "gendev2-09-2025-q061": ("puerperium", "현재 세포독성 항암치료는 약물 노출과 면역억제 때문에 수유의 절대적 금기에 해당한다.", "항암제 치료 중에는 모유수유를 중단한다."),
    "gendev2-09-2025-q062": ("puerperium", "수술상처 감염과 벌어짐은 항균제만으로 부족하다. 상처를 열어 배농하고 괴사조직을 제거한다.", "감염원 배액과 항균치료를 함께 해야 한다."),
    "gendev2-09-2023-q016": ("puerperium", "산후 2–3주 복합호르몬 피임은 VTE 위험이 높고 수유에도 불리할 수 있어 잘못된 설명이다.", "수유 중 산후 초기 estrogen 포함 피임을 시작하라는 문장이 틀렸다."),
    "gendev2-09-2023-q085": ("pph", "산후 10일의 출혈과 자궁내 혼합에코는 잔류조직·혈괴를 시사한다. 안정적이면 맹목적 소파술부터 하는 것은 피한다.", "소파술은 천공·유착 위험이 있어 영상과 임상평가 뒤 선택한다."),
    "gendev2-09-2022-q011": ("puerperium", "제왕절개 4일 뒤 발열·우측 통증과 CT 소견은 산후 골반감염에 합당하다. clindamycin+gentamicin이 표준 경험치료다.", "혐기성균과 그람음성균을 함께 덮는 조합이다."),
    "gendev2-09-2022-q049": ("puerperium", "수유 중 국소 유방통·홍반·발열은 수유성 유방염이다. 수유를 지속하며 dicloxacillin을 사용한다.", "MSSA를 겨냥하는 고전적 1차 경구 항균제이다."),
    "gendev2-09-2021-q007": ("puerperium", "estrogen 포함 복합피임약은 산후 초기 유즙량을 줄일 수 있다.", "복합 estrogen-progestin 제제가 수유 감소와 가장 관련된다."),
    "gendev2-09-2021-q008": ("puerperium", "제왕절개 후 발열과 골반 CT 소견은 산후 자궁내막염이다. clindamycin+gentamicin을 쓴다.", "광범위 복합균 감염을 경험적으로 치료한다."),
    "gendev2-09-2020-q017": ("puerperium", "estrogen 포함 복합피임약은 수유량을 감소시킬 수 있다.", "복합호르몬 피임이 수유에 가장 불리하다."),
    "gendev2-09-2020-q018": ("puerperium", "제왕절개 후 발열과 골반통은 자궁내막염을 우선한다. clindamycin+gentamicin이 답이다.", "혐기성균을 포함한 다균성 감염을 덮는다."),
    "gendev2-10-2025-q003": ("ectopic", "자궁내 임신이 없고 부속기 종괴와 복강내 액체가 보이면 자궁외임신 가능성이 높다. 출혈 의심 때문에 수술을 택한다.", "복강내 출혈을 동반한 자궁외임신은 수술 평가가 안전하다."),
    "gendev2-10-2025-q004": ("early", "자궁내 배아 심박이 있고 자궁경부가 닫힌 상태의 출혈은 절박유산이다.", "생존 자궁내임신에 출혈이 있으나 배출은 진행되지 않았다."),
    "gendev2-10-2023-q066": ("early", "배아가 보이지만 심박이 없는 영상은 계류유산에 합당하다.", "임신산물이 자궁 안에 남은 초기임신소실이다."),
    "gendev2-10-2023-q086": ("ectopic", "hCG 1,000이고 자궁·부속기·복강이 정상인 안정적 PUL은 즉시 치료하지 말고 48시간 hCG를 반복한다.", "아직 위치와 생존성을 확정할 수 없어 연속 측정이 우선이다."),
    "gendev2-10-2022-q004": ("ectopic", "안정적 임신위치불명에서 단일 hCG만으로 유산이나 자궁외임신을 확정하면 안 된다. 48시간 후 재검한다.", "연속 hCG 변화가 다음 초음파와 치료 시점을 정한다."),
    "gendev2-10-2022-q006": ("early", "이전에 확인된 심박이 소실되고 유산이 확진되었다. 보기 중 자궁내용 제거가 적절하다.", "확진된 임신소실의 수술적 치료이다."),
    "gendev2-10-2021-q009": ("early", "초음파로 심박 없는 초기임신소실이 확진되었다. 보기 중 D&C가 치료 선택지이다.", "수술적 자궁내용 제거로 치료한다."),
    "gendev2-10-2021-q010": ("ectopic", "자궁내 임신이 없고 hCG 상승이 비정상이며 종괴가 보이지 않는 안정적 환자는 지속 PUL/자궁외임신을 의심해 methotrexate를 고려한다.", "비파열·안정·추적 가능 조건의 약물치료이다."),
    "gendev2-10-2020-q015": ("previa", "38주 출혈이지만 현재 산모와 태아가 안정적이고 제시 영상상 즉시 응급분만 소견이 없다. 우선 관찰한다. 내용상 6강 오분류가 의심된다.", "안정성을 확인하며 원인을 평가하는 선택이다."),
    "gendev2-10-2020-q016": ("abruption", "통증성 대량출혈·쇼크와 태아심박 이상은 중증 태반조기박리이다. 응급 제왕절개가 필요하다. 내용상 6강 오분류가 의심된다.", "모체 소생과 동시에 태아를 신속히 분만해야 한다."),
}


def choice_explanations(q: dict, correct_note: str) -> list[str]:
    answers = set(q.get("answers", []))
    result = []
    for i, choice in enumerate(q.get("choices", []), 1):
        if i in answers:
            result.append(f"정답 선지. {correct_note}")
        else:
            result.append(f"이 상황의 우선순위 또는 진단 기준과 맞지 않는다. ‘{choice}’는 다른 적응증·안정도·임신주수에서 고려한다.")
    return result


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    by_id = {q["id"]: q for q in payload["questions"]}
    missing = sorted(set(SPECS) - set(by_id))
    if missing:
        raise SystemExit(f"question IDs missing: {missing}")

    # 원문 표기는 보존하되 현재 기준과 명백히 충돌하는 문항은 따로 표시한다.
    by_id["gendev2-07-2020-q013"]["answerReviewStatus"] = "족보 정답 ②와 현재 기준 충돌 · 선지/정답 오류 의심"
    by_id["gendev2-07-2020-q014"]["answers"] = [3, 5]
    by_id["gendev2-07-2020-q014"]["answerStatus"] = "교과서·현재 지침 대조 교정: ③, ⑤"
    by_id["gendev2-07-2020-q014"]["answerReviewStatus"] = "족보 ①,③에서 ③,⑤로 교정"
    for qid in ("gendev2-06-2020-q019", "gendev2-06-2020-q020"):
        by_id[qid]["classificationStatus"] = "강의 오분류 의심: 내용상 10강 초기임신 출혈·자궁외임신"
    for qid in ("gendev2-10-2020-q015", "gendev2-10-2020-q016"):
        by_id[qid]["classificationStatus"] = "강의 오분류 의심: 내용상 06강 임신후반기 출혈"

    for qid, (profile_id, judgment, correct_note) in SPECS.items():
        q = by_id[qid]
        concept, steps, review, source_ids = PROFILES[profile_id]
        exp = {
            "conceptGroup": concept,
            "keyJudgment": judgment,
            "reasoningSteps": steps,
            "choiceExplanations": choice_explanations(q, correct_note),
            "conceptReview": review,
            "evidenceStatus": "Williams Obstetrics 26e·현재 공식 지침 대조 · 2026-08",
            "sources": [SOURCES[source_id] for source_id in source_ids],
        }
        q["explanation"] = exp
        q["explanationReviewStatus"] = exp["evidenceStatus"]
        q["keyConcepts"] = list(dict.fromkeys([concept, q.get("lectureTitle", "")]))[:3]

    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"LECTURES6_10_EXPLANATIONS_APPLIED count={len(SPECS)}")


if __name__ == "__main__":
    main()
