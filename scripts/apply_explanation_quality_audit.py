from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"
CIRCLED = ["①", "②", "③", "④", "⑤"]

ACOG_PB222 = {"kind": "현재 지침", "label": "ACOG Practice Bulletin 222: Gestational Hypertension and Preeclampsia (interim update)", "url": "https://www.acog.org/clinical/clinical-guidance/practice-bulletin/articles/2020/06/gestational-hypertension-and-preeclampsia"}
ACOG_ASPIRIN = {"kind": "현재 지침", "label": "ACOG/SMFM Low-Dose Aspirin Use During Pregnancy (reaffirmed 2023)", "url": "https://www.acog.org/clinical/clinical-guidance/committee-opinion/articles/2018/07/low-dose-aspirin-use-during-pregnancy"}
ACOG_CHAP = {"kind": "출판 후 변경", "label": "ACOG CHAP Integration Guidance (reaffirmed 2025)", "url": "https://www.acog.org/clinical/clinical-guidance/practice-advisory/articles/2022/04/clinical-guidance-for-the-integration-of-the-findings-of-the-chronic-hypertension-and-pregnancy-chap-study"}
SMFM_FGR = {"kind": "현재 지침", "label": "SMFM Consult Series #52: Fetal Growth Restriction", "url": "https://publications.smfm.org/publications/289-society-for-maternal-fetal-medicine-consult-series-52/"}
JACC_PATH = {"kind": "병태생리 근거", "label": "JACC State-of-the-Art Review: Preeclampsia Pathophysiology", "url": "https://pubmed.ncbi.nlm.nih.gov/33004135/"}
WILLIAMS = {"kind": "교과서", "label": "Williams Obstetrics 26e", "url": "https://accessmedicine.mhmedical.com/book.aspx?bookID=2977"}


L7: dict[str, dict] = {
    "gendev2-07-2025-q053": {
        "answers": [3],
        "key": "2단계 가설의 1단계는 영양막의 불완전한 나선동맥 침윤·재형성으로 생기는 비정상 태반형성이다. 따라서 ③ faulty endovascular trophoblastic remodeling이 정답이다.",
        "steps": ["문제는 임상 증상이 아니라 병태생리의 ‘1단계’를 묻는다.", "1단계는 태반 쪽 사건인 얕은 영양막 침윤과 불완전한 나선동맥 재형성이다.", "항혈관신생인자 증가, 전신 내피세포 활성화, 혈관연축과 고혈압은 이후 산모 증후군을 만드는 2단계에 가깝다."],
        "choices": [
            "혈관신생/항혈관신생 인자의 불균형은 허혈성 태반이 산모 순환으로 방출하는 매개 단계다. 1단계의 원인 병변 자체라기보다 1단계와 산모의 2단계를 연결한다.",
            "전신 내피세포 활성화·손상은 고혈압, 단백뇨, 혈소판 소모 같은 산모 임상 증후군을 만드는 2단계다.",
            "정답. 영양막이 나선동맥을 넓고 저저항인 혈관으로 충분히 바꾸지 못하는 불완전한 혈관내 영양막 재형성이 1단계다.",
            "Angiotensin II 등에 대한 pressor response 증가는 산모 혈관반응이 과장된 2단계 현상이다.",
            "혈관연축과 고혈압은 산모에서 드러나는 최종 임상 표현으로, 태반형성 장애가 일어나는 1단계가 아니다.",
        ],
        "review": "두 단계는 ‘태반형성 장애 → 태반 허혈·항혈관신생인자 방출 → 산모 전신 내피기능장애’로 연결한다. 단계 이름을 묻는 문제에서는 태반 쪽 사건과 산모 쪽 임상 증후군을 먼저 분리한다.",
        "sources": [JACC_PATH],
    },
    "gendev2-07-2025-q054": {
        "answers": [4, 5],
        "key": "34주 미만이라도 조절되지 않는 중증 고혈압과 새로 발생하거나 악화되는 신기능장애는 기대요법을 중단할 산모 적응증이다. 현재 ACOG 기준으로는 ④와 ⑤가 모두 해당해 족보 단일정답 ④는 불완전하다.",
        "steps": ["문제의 핵심은 스테로이드 48시간을 기다릴 수 있는 안정 상태인지 판단하는 것이다.", "조절 불가능한 중증 혈압이나 진행하는 장기손상은 산모 안전 때문에 분만을 미루지 않는다.", "태아 도플러 이상이나 양수감소는 재태주수·감시 결과와 함께 판단하므로 문구만으로 ‘즉시’라고 단정하지 않는다."],
        "choices": [
            "양수과소증만으로 항상 즉시 분만하는 것은 아니다. 태아검사, 양수 정도, 재태주수와 동반 FGR을 함께 판단한다.",
            "조기양막파수나 진통은 감염·진통 진행·태아상태에 따라 분만 시점이 달라진다. 안정적이면 스테로이드 투여 기회를 확보할 수 있어 이 문구만으로 즉시 분만을 고정할 수 없다.",
            "제대동맥 이완기 역류는 고위험 소견이지만 SMFM은 입원, 스테로이드, 강화 감시 후 전체 임상상에 따라 30~32주 분만을 권고한다. 반드시 그 순간 즉시 분만이라는 뜻은 아니다.",
            "정답. 약물로도 조절되지 않는 지속 중증 고혈압은 뇌졸중·박리·심부전 위험 때문에 기대요법 금기이며 분만을 스테로이드 완료 때문에 지연하지 않는다.",
            "정답. ACOG는 새로 생기거나 악화되는 신기능장애도 기대요법을 배제하는 산모 장기손상으로 둔다. 족보에서 ④만 정답으로 제시했다면 현재 지침과 충돌한다.",
        ],
        "review": "34주 미만 중증 자간전증의 기대요법은 산모와 태아가 모두 안정되고 고위험센터에서 촘촘히 감시할 수 있을 때만 고려한다. 조절 불가능한 중증 혈압, 지속 신경증상, HELLP, 악화 신기능, 폐부종, 태반조기박리, 비정상 태아검사 등은 분만 쪽으로 기운다.",
        "sources": [ACOG_PB222, SMFM_FGR],
        "answer_status": "현재 ACOG/SMFM 대조 교정: ④, ⑤",
        "answer_review": "족보 단일정답 ④ 불완전 · 악화 신기능장애 ⑤도 기대요법 중단 조건",
    },
    "gendev2-07-2023-q025": {
        "answers": [5],
        "key": "혈압 150/100에 혈소판 9만/µL이면 혈소판 10만 미만이라는 중증 소견이 있어 외래 통원치료 대상이 아니다. ‘잘못된 것’은 ⑤다.",
        "steps": ["문제 요구가 ‘잘못된 것 1개’임을 먼저 확인한다.", "각 선지를 예방, 중증 소견, 경련 예방, 혈압치료 경계, 외래 가능 여부로 나눠 본다.", "혈소판 9만/µL는 단백뇨 정도와 무관하게 중증 소견이므로 ⑤를 고른다."],
        "choices": [
            "대체로 옳다. 37세와 미산부는 각각 중등도 위험인자이므로 두 개가 함께 있으면 ACOG/SMFM 기준에서 저용량 아스피린 예방을 권고·고려한다. 12~28주, 가능하면 16주 전에 시작해 분만까지 지속한다.",
            "옳다. 약물에 반응하지 않는 새 두통은 중증 소견이다. 27주라도 지속 신경증상은 기대요법을 배제할 수 있어 안정화 후 분만을 평가한다.",
            "옳다. 중증 자간전증의 경련 예방과 자간증 치료에는 magnesium sulfate가 phenytoin보다 효과가 우수하다.",
            "시험 문맥에서는 옳다. 급성으로 지속되는 160/110 mmHg 이상은 신속한 항고혈압치료가 필요한 중증 경계다. 다만 이 문장을 모든 임신 고혈압에 일반화하면 틀리며, 만성 고혈압은 CHAP 이후 140/90부터 시작·증량하는 기준으로 바뀌었다.",
            "정답인 잘못된 선지. 혈소판 90,000/µL는 중증 소견이므로 입원 평가와 재태주수에 따른 분만계획이 필요하고, 집에서 혈압만 재는 통원치료는 부적절하다.",
        ],
        "review": "중증 소견은 혈압 160/110 이상, 혈소판 <100,000/µL, 크레아티닌 >1.1 mg/dL 또는 기저치의 2배, 간효소 2배 이상/지속 우상복부통, 폐부종, 치료 불응 두통·시야장애다. 단백뇨의 양은 중증도를 정하는 기준이 아니다.",
        "sources": [ACOG_PB222, ACOG_ASPIRIN, ACOG_CHAP],
    },
    "gendev2-07-2022-q073": {
        "answers": [4],
        "key": "35주에 단백/크레아티닌비 5.0으로 자간전증은 맞지만, 혈소판 14만, 크레아티닌 0.7, AST 58·ALT 42와 안정적 태아검사에는 명확한 중증 소견이 없다. 37주 유도분만이 가장 적절하다.",
        "steps": ["표에서 단백뇨로 자간전증을 진단한다.", "혈소판·크레아티닌·간효소·증상·태아상태를 중증 기준과 대조한다.", "중증 소견이 없는 35주 자간전증이므로 감시 후 37주 분만을 계획하고, 두정위 자체는 제왕절개 적응증이 아님을 확인한다."],
        "choices": [
            "부적절하다. 자간전증 진단 뒤 아무 계획 없이 자연진통까지 기다리면 37주 이후 질환 악화 위험을 감수하게 된다.",
            "현재 35주이고 중증 소견이나 태아 이상이 없어 즉시 분만의 이득이 조산 위험을 확실히 앞서지 않는다.",
            "제왕절개는 자간전증 진단 자체로 정하지 않는다. 두정위이고 산과적 금기가 없으면 유도분만과 질식분만을 시도할 수 있다.",
            "정답. 중증 소견 없는 임신성 고혈압/자간전증은 37주에 분만을 권고하며, 이 환자는 유도분만이 가능하다.",
            "37주 분만 시점은 맞지만 제왕절개를 미리 정할 이유가 없다. 분만경로는 일반 산과 적응증으로 결정한다.",
        ],
        "review": "단백뇨가 많다고 중증 자간전증은 아니다. 이 문제의 표는 2021년 유사문항의 크레아티닌 1.2와 대비된다. 같은 임상 문장이라도 장기손상 수치 하나가 37주 대기와 즉시 분만을 가른다.",
        "sources": [ACOG_PB222],
    },
    "gendev2-07-2022-q077": {
        "answers": [1],
        "key": "33주 중증 자간전증으로 조산한 과거력은 재발 고위험인자다. 현재 15주이므로 저용량 아스피린을 지금 시작하는 것이 정답이다.",
        "steps": ["과거 조기발병 중증 자간전증을 고위험인자로 분류한다.", "예방약 시작 시기인 12~28주, 최적 16주 이전에 해당하는지 본다.", "혈압이 정상인 지금은 항고혈압제가 아니라 저용량 아스피린을 선택한다."],
        "choices": [
            "정답. ACOG/SMFM은 고위험 임신에서 81 mg/day를 12~28주, 가능하면 16주 이전에 시작해 분만까지 지속하도록 권고한다.",
            "엽산 증량은 신경관결손 고위험군에서 고려하지만 자간전증 재발을 낮추는 표준 예방치료는 아니다.",
            "현재 혈압 120/75 mmHg이며 만성 고혈압도 없다. 정상혈압 환자에게 항고혈압제를 예방 목적으로 투여하지 않는다.",
            "와파린은 자간전증 예방약이 아니며 임신 중 태아 위해가 있다. 항인지질증후군 같은 별도 적응증에서는 heparin과 aspirin 조합을 검토한다.",
            "오메가-3 보충은 자간전증 재발 예방의 표준 권고가 아니다.",
        ],
        "review": "저용량 아스피린 고위험인자는 과거 자간전증, 다태임신, 만성고혈압, 임신 전 당뇨, 신장질환, 자가면역질환 등이다. 과거 34주 이전 중증 자간전증은 전형적인 강한 적응증이다.",
        "sources": [ACOG_ASPIRIN],
    },
    "gendev2-07-2021-q079": {
        "answers": [2],
        "key": "2022년 유사문항과 달리 크레아티닌이 1.2 mg/dL로 1.1을 초과해 중증 소견이다. 이미 35주이므로 산모 안정화 후 즉시 분만하며, 두정위라 유도분만이 적절하다.",
        "steps": ["표에서 크레아티닌 1.2 mg/dL를 놓치지 않는다.", "크레아티닌 >1.1 mg/dL는 다른 신질환이 없다면 중증 자간전증 기준이다.", "34주 이후 중증 자간전증은 분만을 권고하되 제왕절개는 별도 산과 적응증이 있을 때 선택한다."],
        "choices": [
            "부적절하다. 중증 소견이 확인되어 퇴원·대기관찰 대상이 아니다.",
            "정답. 35주 중증 자간전증이고 태아가 두정위이므로 안정화와 MgSO4 등 처치 뒤 유도분만을 시행할 수 있다.",
            "자간전증만으로 즉시 제왕절개를 정하지 않는다. 태아곤란, 유도 실패, 분만 금기 등이 없으면 질식분만을 시도한다.",
            "크레아티닌 1.2라는 중증 신기능 기준 때문에 37주까지 기다리지 않는다.",
            "분만 시점과 경로가 모두 부적절하다. 즉시 분만이 필요하지만 제왕절개를 자동 선택하지 않는다.",
        ],
        "review": "이 문항은 2022년 73번과 거의 같지만 크레아티닌만 0.7에서 1.2로 바뀌었다. 숫자를 표에서 직접 읽어 중증 여부를 다시 판정해야 하며, 유사문항의 결론을 그대로 가져오면 틀린다.",
        "sources": [ACOG_PB222],
    },
    "gendev2-07-2021-q080": {
        "answers": [2],
        "key": "부종·단백뇨·혈전·용혈을 하나로 가장 직접 설명하는 공통 기전은 전신 혈관내피 손상이다. 따라서 ②가 정답이다.",
        "steps": ["여러 장기의 증상을 동시에 만드는 공통 병변을 찾는다.", "내피 손상은 모세혈관 누출, 신장 사구체 내피증, 혈소판 활성·미세혈전과 용혈을 연결한다.", "혈관연축과 항혈관신생인자 증가는 상위 또는 동반 기전이지만 네 증상을 가장 직접 묶는 답은 내피 손상이다."],
        "choices": [
            "혈관연축은 고혈압과 장기 관류 저하에 중요하지만 부종·단백뇨·혈전·용혈을 모두 가장 직접 설명하는 조직 수준 병변은 아니다.",
            "정답. 전신 내피 손상은 혈관 투과성 증가로 부종, 사구체 내피증으로 단백뇨, 혈소판·응고 활성로 혈전과 미세혈관병성 용혈을 만든다.",
            "압력물질 반응 증가는 고혈압 경향을 설명하지만 단백뇨와 미세혈관병성 용혈의 직접 기전은 아니다.",
            "sFlt-1·soluble endoglin 같은 항혈관신생인자 증가는 내피기능장애를 유발하는 상위 매개기전이다. 임상 병변을 직접 묻는 답은 내피 손상이다.",
            "면역관용 이상이 병태생리에 관여할 수 있으나 자간전증을 급성 이식편 거부반응으로 동일시하지 않는다.",
        ],
        "review": "병태생리 문제에서는 원인 사슬의 층을 구분한다. 비정상 태반형성은 시작점, 항혈관신생인자 증가는 순환 매개자, 전신 내피기능장애는 산모 장기손상의 직접 공통기전이다.",
        "sources": [JACC_PATH],
    },
    "gendev2-07-2020-q013": {
        "answers": [5],
        "key": "25주라도 혈압 160/110, 시야증상, 혈소판 7.8만과 심한 FGR은 중증 자간전증이다. 중증 혈압은 치료하고 MgSO4를 투여하며, 혈관내 용적이 감소해 있어 폐부종이 없는 한 이뇨제를 피한다. 현재 기준의 옳은 선지는 ⑤다.",
        "steps": ["중증 혈압, 시야증상, 혈소판 감소와 태아상태를 모두 확인한다.", "산모 안정화가 먼저이므로 급성 중증 혈압치료와 경련 예방을 시작한다.", "혈관내 용적 수축 때문에 루틴 이뇨는 해로울 수 있고 폐부종 같은 명확한 적응증에서만 사용한다."],
        "choices": [
            "혈소판 7.8만은 중증 소견이지만 혈소판 수혈을 자동으로 시행하지 않는다. 활동성 출혈, 매우 낮은 수치 또는 수술·분만을 위한 지혈 목표에 따라 결정한다.",
            "족보 정답이지만 현재 기준상 틀리다. 지속 혈압 160/110 mmHg는 뇌졸중 예방을 위해 labetalol, hydralazine 또는 nifedipine 등으로 신속히 치료한다.",
            "시야증상과 혈소판 7.8만은 기대요법을 어렵게 하는 산모 중증 소견이고 태아도 심한 FGR이다. 단순 집중관찰만으로 임신을 유지한다는 표현은 부적절하다.",
            "중증 소견과 시야증상이 있어 MgSO4 경련 예방 적응증이다. ‘아직 이르다’는 설명은 틀리다.",
            "정답. 자간전증은 전신부종이 있어도 혈관내 유효용적은 감소할 수 있어 루틴 이뇨제를 피한다. 다만 폐부종이 있으면 산소·혈압관리와 함께 이뇨제를 사용할 수 있다.",
        ],
        "review": "중증 자간전증은 ‘부어 있으니 이뇨’가 아니다. 내피 누출로 간질액은 늘지만 혈관내 용적은 줄 수 있다. 치료 우선순위는 산모 안정화, 중증 혈압치료, MgSO4, 분만 시점 결정이며 과도한 수액과 루틴 이뇨를 모두 피한다.",
        "sources": [ACOG_PB222],
        "answer_status": "현재 ACOG 대조 교정: ⑤",
        "answer_review": "족보 정답 ② 오류 · 중증 혈압은 치료해야 하며 현재 근거상 ⑤",
    },
    "gendev2-07-2020-q014": {
        "answers": [3, 5],
        "key": "현재 근거로 옳은 것은 soluble endoglin 증가 ③과 다태임신 고위험군의 저용량 아스피린 ⑤ 두 개다. 문항은 세 가지를 요구하지만 제시된 선지에는 세 번째 옳은 답이 없어 문항 오류로 보아야 한다.",
        "steps": ["문제 요구가 ‘옳은 것 세 가지’임을 먼저 확인한다.", "각 선지를 분만 적응증, 역학, 항혈관신생인자, 영양막 침윤, 예방으로 나눈다.", "현재 지침과 병태생리에 맞는 ③·⑤만 남으므로 저장 답 개수와 요구 개수가 충돌한다고 표시한다."],
        "choices": [
            "FGR이 있다는 이유만으로 언제나 즉시 분만하지 않는다. 태아검사, 제대동맥 도플러, 재태주수, 성장속도와 산모 중증도를 함께 판단한다.",
            "흡연은 산모·태아에 해롭지만 역학적으로 자간전증 위험은 역설적으로 낮게 관찰돼 왔다. 따라서 ‘발생 가능성이 높다’는 문장은 옳지 않다.",
            "정답. 자간전증에서는 항혈관신생성 soluble endoglin이 증가해 TGF-β 신호와 내피기능을 방해할 수 있다.",
            "반대다. 자간전증의 1단계는 영양막의 나선동맥 침윤과 재형성이 지나친 것이 아니라 얕고 불완전한 것이다.",
            "정답. 다태임신은 자간전증 고위험인자이며 ACOG/SMFM은 저용량 아스피린을 12~28주, 가능하면 16주 전에 시작하도록 권고한다.",
        ],
        "review": "이 문항은 정답 내용보다 정답 개수 오류가 핵심 검수사항이다. 현재 근거상 ③·⑤만 옳다. FGR 단독 즉시분만, 흡연 위험 증가, 과도한 영양막 침윤은 모두 현재 설명과 맞지 않는다.",
        "sources": [ACOG_PB222, ACOG_ASPIRIN, SMFM_FGR, JACC_PATH],
        "answer_status": "현재 근거상 ③, ⑤ · 문항은 3개 요구",
        "answer_review": "정답 개수 불일치 · 제시 선지에서 옳은 것은 ③,⑤ 두 개뿐",
    },
}


GENERIC_MARKERS = (
    "이 상황의 우선순위 또는 진단 기준과 맞지 않는다",
    "이 문항의 결정 단서와 맞지 않는다",
    "다른 적응증·안정도·임신주수에서 고려한다",
)


def clean_focus(stem: str, limit: int = 105) -> str:
    text = re.sub(r"\s+", " ", stem).strip()
    text = re.sub(r"(다음 중|고르시오|선택하시오).*$", "", text).strip(" .")
    return text if len(text) <= limit else text[:limit].rstrip() + "…"


def direction_for(question: dict) -> tuple[str, int | None]:
    stem = question.get("stem", "")
    if question.get("questionMode") == "self-check":
        return "직접 답을 쓰고 자기채점", None
    negative = any(token in stem for token in ("잘못된", "옳지 않은", "아닌 것", "틀린 것", "적절하지 않은", "거리가 먼"))
    if negative:
        direction = "옳지 않은 선지"
    else:
        direction = "옳은 선지"
    count = len(question.get("answers", [])) or 1
    return direction, count


def answer_text(question: dict) -> str:
    parts = []
    for answer in question.get("answers", []):
        choice = question.get("choices", [])[answer - 1]
        parts.append(f"{CIRCLED[answer - 1]} ‘{choice}’")
    return ", ".join(parts)


def explicit_requested_count(stem: str) -> int | None:
    patterns = ((r"두\s*가지.{0,20}(고르|선택)", 2), (r"세\s*가지.{0,20}(고르|선택)", 3), (r"3\s*개.{0,20}(고르|선택)", 3))
    for pattern, count in patterns:
        if re.search(pattern, stem):
            return count
    return None


def question_check(question: dict) -> str:
    direction, count = direction_for(question)
    if count is None:
        return "문제 요구 확인: 단답형이며 강의 제시 답과 비교해 직접 채점한다."
    stored = len(question.get("answers", []))
    requested = explicit_requested_count(question.get("stem", ""))
    mismatch = requested is not None and requested != stored
    suffix = f" 문항 문구는 {requested}개를 요구하지만 현재 근거로 확인된 답은 {stored}개이므로 정답 개수 오류를 함께 검토해야 한다." if mismatch else ""
    return f"문제 요구 확인: {direction} {stored}개를 고른다. 저장 정답은 {', '.join(CIRCLED[a-1] for a in question.get('answers', []))}다.{suffix}"


def generic_choice_explanations(question: dict, explanation: dict) -> list[str]:
    existing = explanation.get("choiceExplanations", [])
    answers = set(question.get("answers", []))
    negative = any(token in question.get("stem", "") for token in ("잘못된", "옳지 않은", "아닌 것", "틀린 것", "적절하지 않은"))
    correct_summary = answer_text(question)
    result = []
    for index, choice in enumerate(question.get("choices", []), 1):
        old = existing[index - 1].strip() if index <= len(existing) else ""
        is_generic = not old or len(old) < 45 or any(marker in old for marker in GENERIC_MARKERS)
        if not is_generic:
            result.append(old)
            continue
        if index in answers:
            prefix = "정답 선지(문제에서 요구한 잘못된 설명)." if negative else "정답 선지."
            result.append(f"{prefix} {explanation.get('keyJudgment', '')} 이 사례에서 선택해야 할 문장은 ‘{choice}’다.")
        elif negative:
            result.append(f"옳은 설명이므로 이 문제의 정답이 아니다. ‘{choice}’를 {explanation.get('conceptGroup', question.get('lectureTitle', '핵심 개념'))}의 원칙과 대조하면 유지되는 설명이며, 잘못된 선지는 {correct_summary}다.")
        else:
            result.append(f"오답 선지. ‘{choice}’는 이 사례의 결정 단서와 맞지 않는다. {explanation.get('keyJudgment', '')} 따라서 이 문항에서는 {correct_summary}와 구분해야 한다.")
    return result


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    questions = payload["questions"]
    target = [q for q in questions if q.get("lectureNumber", "").isdigit() and 1 <= int(q["lectureNumber"]) <= 20]
    by_id = {q["id"]: q for q in questions}

    diagnostic_by_lecture = {
        "05": ["조산: 임신 37+0주 이전 출생", "조기진통은 규칙 자궁수축과 자궁목 변화로 진단하며 수축만으로 확정하지 않는다."],
        "06": ["산후출혈: 출산 과정 24시간 이내 누적 실혈 ≥1,000 mL 또는 실혈량과 무관한 저혈량 징후", "원인 4T: Tone·Trauma·Tissue·Thrombin"],
        "07": ["고혈압: ≥140/90 mmHg; 중증 혈압: ≥160/110 mmHg", "중증 소견: 혈소판 <100,000, Cr >1.1 mg/dL 또는 2배, 간효소 ≥2배, 폐부종, 지속 신경증상 등", "단백뇨가 없어도 새 고혈압과 말단장기 기능장애가 있으면 자간전증을 진단할 수 있다."],
        "08": ["FGR: EFW 또는 복부둘레 <10백분위수; severe FGR: EFW <3백분위수", "도플러 단계와 태아감시·동반질환이 분만시기를 결정한다."],
        "09": ["산후 발열은 자궁압통·오로, 상처, 유방, 소변·호흡기 증상과 혈전 위험을 함께 평가한다.", "제왕절개와 장시간 막파수는 산후 자궁내막염의 주요 위험인자다."],
        "10": ["초기임신소실 확진 초음파 기준에는 CRL ≥7 mm인데 심박동 없음, MSD ≥25 mm인데 배아 없음이 포함된다.", "위치불명임신은 최종 진단이 아니며 위치가 확인될 때까지 hCG·질초음파·증상을 추적한다."],
    }

    for qid, spec in L7.items():
        q = by_id[qid]
        q["answers"] = spec["answers"]
        if spec.get("answer_status"):
            q["answerStatus"] = spec["answer_status"]
        if spec.get("answer_review"):
            q["answerReviewStatus"] = spec["answer_review"]
        exp = q.setdefault("explanation", {})
        exp.update({
            "conceptGroup": "임신 중 고혈압성 질환",
            "keyJudgment": spec["key"],
            "reasoningSteps": spec["steps"],
            "choiceExplanations": spec["choices"],
            "conceptReview": spec["review"],
            "evidenceStatus": "문항·표·족보 정답 재대조 + OpenEvidence 탐색 후 ACOG/SMFM 공식 원문 검증 · 2026-08-05",
            "sources": spec["sources"],
        })
        q["explanationReviewStatus"] = exp["evidenceStatus"]
        q["keyConcepts"] = ["임신 중 고혈압성 질환", exp["conceptGroup"]]

    key_counts = Counter(q.get("explanation", {}).get("keyJudgment", "") for q in target)
    step_counts = Counter(tuple(q.get("explanation", {}).get("reasoningSteps", [])) for q in target)
    review_counts = Counter(q.get("explanation", {}).get("conceptReview", "") for q in target)
    for q in target:
        exp = q.setdefault("explanation", {})
        if not exp.get("diagnosticCriteria") and q.get("lectureNumber") in diagnostic_by_lecture:
            exp["diagnosticCriteria"] = diagnostic_by_lecture[q["lectureNumber"]]
        q["questionCheck"] = question_check(q)
        exp["questionCheck"] = q["questionCheck"]
        if q["id"] in L7:
            continue
        # 반복 출제된 같은 개념은 판단문과 알고리듬이 같을 수 있다. 중복을 없애겠다고
        # 문제·정답 문장을 덧붙이면 해설이 길어질 뿐 의학적 정보는 늘지 않는다.
        # 따라서 이 감사 단계에서는 내용을 자동 재작성하지 않는다.
        # 선지 해설은 앞선 문항별 검수 결과를 보존한다. 감사 단계에서 공통 fallback으로
        # 덮어쓰면 서로 다른 선지에 같은 설명이 들어가는 회귀가 생긴다.
        if not exp.get("sources"):
            exp["sources"] = [WILLIAMS]
        # 개념 복습에는 선지 원문을 다시 붙이지 않는다.
        audit_label = "문항 방향/정답 개수/중복 해설 품질감사 2026-08-05"
        if audit_label not in exp.get("evidenceStatus", ""):
            exp["evidenceStatus"] = (exp.get("evidenceStatus", "") + " · " + audit_label).strip(" ·")
        q["explanationReviewStatus"] = exp["evidenceStatus"]

    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    unique_keys = len({q["explanation"]["keyJudgment"] for q in target})
    print(f"EXPLANATION_QUALITY_AUDIT_APPLIED questions={len(target)} uniqueKeyJudgments={unique_keys} lecture7={len(L7)}")


if __name__ == "__main__":
    main()
