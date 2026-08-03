from __future__ import annotations

import json
from pathlib import Path

from apply_early_lecture_explanations import explanation


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"

SOURCES = {
    "w21": {
        "label": "Williams Obstetrics 26e, Ch. 21 Physiology of Labor",
        "url": "https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=263817742",
        "kind": "교과서",
    },
    "w22": {
        "label": "Williams Obstetrics 26e, Ch. 22 Normal Labor",
        "url": "https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=255633136",
        "kind": "교과서",
    },
    "w24": {
        "label": "Williams Obstetrics 26e, Ch. 24 Intrapartum Assessment",
        "url": "https://accessmedicine.mhmedical.com/content.aspx?bookid=2977&sectionid=257536569",
        "kind": "교과서",
    },
    "acog_labor": {
        "label": "ACOG 2024: First and Second Stage Labor Management",
        "url": "https://www.acog.org/clinical/clinical-guidance/clinical-practice-guideline/articles/2024/01/first-and-second-stage-labor-management",
        "kind": "현재 지침",
    },
    "acog_fhr": {
        "label": "ACOG 2025: Intrapartum Fetal Heart Rate Monitoring",
        "url": "https://www.acog.org/clinical/clinical-guidance/clinical-practice-guideline/articles/2025/10/intrapartum-fetal-heart-rate-monitoring-interpretation-and-management",
        "kind": "현재 지침",
    },
    "acog_oxygen": {
        "label": "ACOG 2022: Oxygen Supplementation for Category II or III FHR Tracings",
        "url": "https://www.acog.org/clinical/clinical-guidance/practice-advisory/articles/2022/01/oxygen-supplementation-in-the-setting-of-category-ii-or-iii-fetal-heart-tracings",
        "kind": "현재 지침",
    },
}


def exp(concept: str, judgment: str, steps: list[str], choices: list[str], review: str, source_ids: list[str], status: str = "Williams 26e·ACOG 공식지침 대조 · 2026-08 현재") -> dict:
    value = explanation(concept, judgment, steps, choices, review, [])
    value["sources"] = [SOURCES[source_id] for source_id in source_ids]
    value["evidenceStatus"] = status
    return value


EXPLANATIONS = {
    "gendev2-04-2025-q079": exp(
        "분만곡선과 분만 단계",
        "족보 그림의 D는 자궁목 개대가 거의 끝나고 태아 하강이 가속되는 pelvic division 진입부로 해석된다. 이 구간부터 굴곡·내회전·신전 등 분만기전(cardinal movements)이 임상적으로 두드러진다는 ④가 족보 정답이다.",
        [
            "빨간 곡선은 자궁목 개대, 검은 곡선은 선진부 하강을 나타낸다.",
            "첫째 단계는 진통 시작부터 완전개대까지이고, 둘째 단계는 완전개대부터 태아 만출까지, 셋째 단계는 태아 만출부터 태반 만출까지다.",
            "Friedman의 고전 곡선은 4 cm 전후를 활성기 시작으로 보았지만, 현재 ACOG는 활성기 기준을 6 cm로 잡는다.",
            "현재 추출 그림에는 문제에서 지칭한 A–E 문자가 보이지 않으므로 위치 표지는 원본 강의자료 재확인이 필요하다.",
        ],
        [
            "A의 정확한 위치 표지가 현재 이미지에서 누락되어 있고, 고전 Friedman 곡선과 현재 기준의 활성기 시작점도 다르므로 A를 곧바로 활성기 시작점으로 단정할 수 없다.",
            "둘째 단계는 B부터 E 같은 넓은 구간이 아니라 자궁목 완전개대부터 태아 만출까지다.",
            "C 역시 현재 이미지에서 표지가 보이지 않는다. 현재 ACOG 기준 활성기는 약 6 cm부터이므로 단순 분할선 하나를 활성기 시작으로 암기하지 않는다.",
            "정답. D는 태아 하강이 가속되는 pelvic division 쪽으로, 내회전·신전 등 cardinal movements가 본격화되는 구간으로 제시됐다.",
            "셋째 단계는 태아가 나온 뒤부터 태반이 나올 때까지다. 분만곡선 안의 E 지점 자체가 태아 만출 뒤를 뜻한다는 근거가 없다.",
        ],
        "분만 단계와 자궁 활성 단계를 구분한다. 고전 Friedman 곡선은 시험 개념으로 남아 있지만, 현대 진료에서는 정상 진행의 개인차가 크며 활성기 정체 기준을 6 cm 이전에 적용하지 않는다.",
        ["w22", "acog_labor"],
        "족보 정답·교과서 대조 완료 / A–E 표지 누락으로 그림 위치 재검수 필요 · 2026-08",
    ),
    "gendev2-04-2025-q080": exp(
        "비정상 태아심박동과 자궁내 소생술",
        "그림은 수축과 연관된 반복 감속으로 태아 산소공급 저하 가능성을 먼저 교정해야 하는 상황이다. 족보는 ① 산소와 ② 좌측위를 정답으로 제시하지만, 현재 ACOG는 산모 저산소증이 없다면 일률적 산소 투여를 권하지 않는다.",
        [
            "기준선·변이도·감속의 시작과 최저점·회복을 수축과 함께 읽는다.",
            "즉시 산모를 옆으로 돌리고, 옥시토신 사용 중이면 중단하며, 저혈압·빈맥·탈수 여부를 확인해 원인을 교정한다.",
            "지속되는 비정상 소견은 신속히 재평가하고 호전되지 않으면 분만을 서두를지 판단한다.",
            "시험 정답과 2022년 이후 산소 권고가 충돌하므로 ‘족보 정답’과 ‘현재 진료’를 따로 기억한다.",
        ],
        [
            "족보 정답. 과거 자궁내 소생술 묶음에는 산소가 포함됐지만, 현재는 산모 산소포화도가 정상이라면 태아 소생만을 위한 일률적 산소 투여를 권하지 않는다.",
            "정답. 좌측위 등 측와위는 대정맥 압박을 줄이고 자궁태반 관류를 개선하는 첫 조치다.",
            "저혈압이나 저혈량이 있으면 정맥수액이 도움이 된다. 이 문항은 혈압이 정상이라 족보 정답에서 제외됐지만 임상에서는 원인과 활력징후에 따라 선택한다.",
            "비정상 감속 중 옥시토신을 새로 투여하면 자궁수축을 늘려 산소공급을 더 악화시킬 수 있다. 이미 주입 중이라면 중단한다.",
            "인공양막파수는 이 감속의 즉각적인 교정책이 아니며 탯줄압박·감염 위험을 추가할 수 있다.",
        ],
        "자궁내 소생술의 핵심은 산소 자체가 아니라 원인 교정이다. 체위 변경, 자궁수축촉진제 중단, 저혈압 교정, 빈수축 치료 후에도 Category III 또는 고위험 Category II가 지속되면 신속 분만을 고려한다.",
        ["w24", "acog_fhr", "acog_oxygen"],
        "족보 정답과 현재 산소 권고 일부 충돌 표시 · 2026-08",
    ),
    "gendev2-04-2023-q032": exp(
        "인간 분만의 4단계 생리",
        "인간은 혈중 progesterone 농도가 분만 전에 뚜렷이 떨어지는 고전적(classic) withdrawal이 아니라 수용체·공조절인자 변화에 따른 기능적 progesterone withdrawal을 보인다. 따라서 실제 옳지 않은 문장은 ③이며, 족보의 ①은 오류로 판단된다.",
        [
            "Phase 1은 자궁 정지와 자궁목 연화, Phase 2는 분만 준비와 자궁목 숙성이다.",
            "Phase 3은 규칙적 자궁수축, 개대, 태아 만출이며 prostaglandin과 oxytocin 체계가 활성화된다.",
            "사람에서는 progesterone 혈중 농도가 분만 직전 급락하지 않으므로 classic withdrawal이라는 표현이 틀렸다.",
            "동일 문장을 ②로 둔 2021년 6번 문항의 정답과도 일치하므로 이 문항은 ③으로 교정한다.",
        ],
        [
            "Phase 1에는 chorion의 prostaglandin dehydrogenase가 prostaglandin을 불활성화해 자궁근층 도달을 제한하는 장벽 역할을 한다는 설명으로 볼 수 있다.",
            "Phase 2의 자궁목 숙성에서는 collagen 배열과 결합이 느슨해지고 수분·glycosaminoglycan 구성이 변한다.",
            "교정 정답. 인간 분만은 혈중 progesterone 감소에 의한 classic withdrawal이 아니라 기능적 withdrawal이 핵심이다.",
            "Phase 3에서 prostaglandin과 oxytocin 및 수용체 증가는 자궁수축을 강화하므로 맞다.",
            "Phase 3은 임상적 진통의 잠복기·활성기와 태아 만출을 포함하므로 맞다.",
        ],
        "Phase 1 정지 → Phase 2 활성화 준비 → Phase 3 진통·만출 → Phase 4 산욕기 회복 순서로 연결한다. 사람과 다른 동물의 progesterone 변화가 다르다는 점이 반복 출제된다.",
        ["w21"],
        "동일문항·Williams 26e 대조로 족보 ①을 ③으로 교정 · 2026-08",
    ),
    "gendev2-04-2023-q046": exp(
        "태아심박동 감속의 초기 처치",
        "반복되는 비정상 감속에서는 자궁태반 관류를 개선해야 한다. 앙와위는 임신 자궁이 하대정맥을 눌러 정맥환류와 자궁태반 혈류를 떨어뜨릴 수 있으므로 ‘우선 처치로 옳지 않은 것’은 ④다.",
        [
            "수축과 감속의 시간 관계, 변이도, 반복성을 확인한다.",
            "산모를 측와위로 바꾸고 옥시토신을 중단하며 활력징후와 자궁 빈수축을 평가한다.",
            "저혈압·저혈량이 의심되면 수액으로 교정하고 지속 모니터링한다.",
            "호전되지 않는 Category III 또는 악화되는 Category II는 분만을 지연하지 않는다.",
        ],
        [
            "옥시토신은 수축 빈도를 늘려 태반 재관류 시간을 줄일 수 있으므로 비정상 감속 때 중단하는 것이 맞다.",
            "과거 시험에서는 산소가 초기 처치에 포함됐다. 현재는 산모 저산소증이 없는 경우 일률적 산소 투여는 권하지 않는다.",
            "저혈압이나 상대적 저혈량이 있으면 빠른 정맥수액으로 자궁태반 관류를 회복시킬 수 있다.",
            "정답. 앙와위는 대정맥 압박으로 정맥환류와 심박출량을 낮출 수 있어 피하고 좌·우 측와위를 사용한다.",
            "지속 전자태아심박동 감시로 조치에 대한 반응을 확인해야 한다.",
        ],
        "감속 처치는 ‘모니터만 보기’가 아니라 모체 저혈압, 빈수축, 탯줄압박, 태반관류 저하 같은 가역 원인을 동시에 찾고 교정하는 과정이다.",
        ["w24", "acog_fhr", "acog_oxygen"],
    ),
    "gendev2-04-2022-q013": exp(
        "조기감속과 태아 머리 압박",
        "그림은 30초 이상에 걸쳐 서서히 감소하고 감속 최저점이 수축 정점과 거의 일치하는 조기감속이다. 태아 머리 압박이 미주신경을 활성화해 발생하므로 ②가 맞다.",
        [
            "감속이 급격한지(시작부터 최저점까지 30초 미만) 서서히인지 먼저 본다.",
            "서서히 시작해 수축과 거울상으로 겹치면 조기감속이다.",
            "조기감속은 보통 정상 분만 진행 중 머리 압박을 반영하며 단독으로 태아 산증을 뜻하지 않는다.",
        ],
        [
            "태동은 주로 acceleration과 관련되고, 조기감속의 대표 원인은 아니다.",
            "정답. 머리 압박으로 미주신경이 활성화되면 수축과 동시에 완만한 감속이 나타난다.",
            "자궁태반 혈류 부족에 의한 저산소증은 수축보다 늦게 최저점이 오는 late deceleration을 만든다.",
            "탯줄압박은 시작과 회복이 급격하고 모양·시점이 변하는 variable deceleration의 원인이다.",
            "중추신경 억제제나 황산마그네슘은 주로 baseline variability 감소와 연관된다.",
        ],
        "Early는 head, variable은 cord, late는 placenta로 연결하되, 실제 판독은 시작-최저점 시간과 수축에 대한 시차를 함께 본다.",
        ["w24", "acog_fhr"],
    ),
    "gendev2-04-2021-q005": exp(
        "비정상 태아심박동과 모체 체위",
        "그림의 반복 감속을 교정할 때 앙와위는 자궁태반 관류를 악화시킬 수 있다. 따라서 우선 처치로 옳지 않은 것은 ③ supine position이다.",
        [
            "감속의 반복성과 수축과의 관계를 확인한다.",
            "측와위로 전환하고 옥시토신을 중단하며 산모 저혈압·빈수축을 교정한다.",
            "계속 감시하면서 회복되지 않으면 신속 분만 가능성을 평가한다.",
        ],
        [
            "옥시토신 중단은 자궁 빈수축과 태반 관류 저하를 줄이는 적절한 초기 조치다.",
            "과거 족보 처치에는 산소가 포함됐으나, 현재는 산모 저산소증이 없다면 일률적 산소 투여를 권하지 않는다.",
            "정답. 앙와위는 하대정맥 압박을 늘릴 수 있으므로 피하고 측와위를 취한다.",
            "저혈압·저혈량이 있으면 빠른 정맥수액이 도움이 된다.",
            "지속 감시로 처치 후 변이도와 감속의 회복 여부를 평가한다.",
        ],
        "양수과소증에서는 탯줄압박과 variable deceleration 가능성도 높다. 반복 variable deceleration이 지속되면 원인 평가와 함께 상황에 따라 양수주입을 고려할 수 있다.",
        ["w24", "acog_fhr", "acog_oxygen"],
    ),
    "gendev2-04-2021-q006": exp(
        "기능적 progesterone withdrawal",
        "사람에서는 분만 직전 혈중 progesterone 분비가 뚜렷하게 감소하는 classic withdrawal이 일어나지 않는다. 수용체와 공조절인자 변화에 따른 기능적 withdrawal이므로 ②가 옳지 않다.",
        [
            "Phase 1의 자궁 정지, Phase 2의 분만 준비, Phase 3의 진통·만출을 구분한다.",
            "Phase 2에는 자궁목 숙성과 자궁근의 수축 준비가 진행된다.",
            "혈중 progesterone 농도 저하가 아니라 작용 변화가 핵심임을 확인해 ②를 고른다.",
        ],
        [
            "Phase 1에는 prostaglandin 대사 장벽이 자궁 정지 유지에 기여한다는 설명으로 맞다.",
            "정답. 사람에서는 classic progesterone withdrawal보다 functional withdrawal이 일어난다.",
            "Collagen 결합 약화와 기질 재편에 의한 cervical ripening은 Phase 2의 핵심이다.",
            "Prostaglandin·oxytocin과 그 수용체는 Phase 3의 수축을 강화한다.",
            "Phase 3은 임상 진통과 태아 만출을 포함한다.",
        ],
        "이 문항은 2023년 32번과 사실상 같은 문제다. 두 문항을 함께 보면 2023년 정답표의 ①이 오류이고 classic progesterone withdrawal 문장이 정답임을 확인할 수 있다.",
        ["w21"],
    ),
    "gendev2-04-2020-q007": exp(
        "태아심박동 3단계 분류",
        "Category I은 기준선 110–160회/분, moderate variability, late·variable deceleration 없음이 모두 필요하다. Variable deceleration이 있으면 Category I이 아니므로 ③이 정답이다.",
        [
            "기준선이 110–160인지 확인한다.",
            "변이도가 moderate인지 확인한다.",
            "late 또는 variable deceleration이 하나라도 있으면 Category I에서 제외한다.",
            "early deceleration과 acceleration은 있거나 없어도 Category I일 수 있다.",
        ],
        [
            "115회/분은 정상 기준선 110–160 안에 든다.",
            "Moderate variability는 Category I의 필수 조건이다.",
            "정답. Variable deceleration은 Category I에서 반드시 없어야 한다.",
            "Early deceleration은 있거나 없어도 Category I일 수 있다.",
            "Acceleration은 없어도 Category I 분류가 가능하다.",
        ],
        "Category I은 현재 정상 산-염기 상태를 강하게 시사한다. Category III은 variability 소실과 반복 late/variable, 서맥 중 하나의 조합 또는 sinusoidal pattern이며, 나머지 대부분은 Category II다.",
        ["w24", "acog_fhr"],
    ),
    "gendev2-04-2020-q008": exp(
        "둔위의 태향",
        "그림은 엉덩이가 선진부인 둔위이며 태아 천골이 산모의 왼쪽 뒤를 향한다. 태향은 선진부 기준점과 모체 골반의 관계로 이름 붙이므로 left sacro-posterior인 ⑤가 정답이다.",
        [
            "먼저 태아 장축이 모체 장축과 나란한 longitudinal lie인지 본다.",
            "선진부가 엉덩이이므로 breech presentation이다.",
            "둔위의 기준점은 sacrum이며, 그림에서 산모의 왼쪽 뒤를 향하므로 LSP로 명명한다.",
        ],
        [
            "Longitudinal은 태위(lie)를 말할 뿐 그림이 묻는 구체적 태향(position)은 아니다.",
            "Breech는 태세가 아니라 선진부를 나타내는 presentation으로, 구체적 방향까지 답하지 못한다.",
            "Compound presentation은 주 선진부 옆에 손·팔 같은 사지가 함께 내려온 상태다.",
            "Mento-anterior는 얼굴 선진에서 턱(mentum)을 기준점으로 쓰는 명칭이며 이 그림은 둔위다.",
            "정답. 둔위의 기준점 sacrum이 산모 왼쪽 뒤에 있어 left sacro-posterior다.",
        ],
        "명명 순서는 lie → presentation → attitude → position이다. 두정위는 occiput, 안면위는 mentum, 둔위는 sacrum, 견갑위는 acromion을 기준점으로 사용한다.",
        ["w22"],
    ),
}


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    by_id = {question["id"]: question for question in payload["questions"]}
    missing = sorted(set(EXPLANATIONS) - set(by_id))
    if missing:
        raise SystemExit(f"문항 ID 없음: {missing}")
    for qid, value in EXPLANATIONS.items():
        question = by_id[qid]
        question["explanation"] = value
        question["explanationReviewStatus"] = value["evidenceStatus"]
    corrected = by_id["gendev2-04-2023-q032"]
    corrected["answers"] = [3]
    corrected["answerStatus"] = "교과서·동일문항 대조 교정"
    corrected["answerNote"] = "원본 족보 ①. Williams 26e와 2021년 동일문항을 대조해 ③으로 교정."
    corrected["answerReviewStatus"] = "족보 정답 오류 교정: ① → ③"
    by_id["gendev2-04-2025-q079"]["answerReviewStatus"] = "그림 A–E 표지 원본 대조 필요"
    by_id["gendev2-04-2025-q080"]["answerReviewStatus"] = "족보 정답과 현재 산소 권고 일부 충돌"
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"LECTURE4_EXPLANATIONS_APPLIED count={len(EXPLANATIONS)} corrected=gendev2-04-2023-q032")


if __name__ == "__main__":
    main()
