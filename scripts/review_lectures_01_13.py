from __future__ import annotations

"""1~13강 선지 해설을 짧고 선지 독립적으로 다시 작성한다."""

import json
import re
from pathlib import Path

from review_lectures_01_10 import fact_for, is_negative_stem, profile_for


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"
REVIEW_DATE = "2026-08-06"


EXTRA_FACTS = [
    (r"기관 삽관", "기관삽관은 마스크 양압환기가 효과적이지 않거나 장기 환기가 필요할 때 대체 기도로 고려한다."),
    (r"흉부 압박", "흉부압박은 효과적인 양압환기를 30초 시행한 뒤에도 심박수가 60회/분 미만일 때 시작한다."),
    (r"체온 유지.*관찰", "무호흡 또는 심박수 100회/분 미만인 신생아는 관찰만 하지 말고 양압환기를 시작한다."),
    (r"다시 호흡 자극", "초기 자극 뒤에도 무호흡이고 심박수가 100회/분 미만이면 자극을 반복하기보다 환기를 제공한다."),
    (r"마스크.?백.*양압|양압환기", "무호흡·헐떡호흡 또는 심박수 100회/분 미만이면 마스크 양압환기가 첫 교정 처치다."),
    (r"양수에서 바이러스", "양수 CMV 검출은 산전 태아감염을 평가하지만 출생 후 선천 CMV 확진 검체 기준은 아니다."),
    (r"모유에서 바이러스", "모유 CMV 검출은 산후 노출을 반영할 수 있어 선천감염을 확진하지 못한다."),
    (r"소변이나 침", "생후 21일 이내 소변 또는 침 PCR에서 CMV를 검출하면 선천감염으로 확진할 수 있다."),
    (r"피부 조직", "피부조직 검사는 선천 CMV의 표준 선별·확진 검체가 아니다."),
    (r"비만증.*고혈당", "모체 비만은 거대아 위험을 높이지만 신생아 고혈당보다 저혈당과 대사 합병증을 주의한다."),
    (r"자간증.*혈소판 과다", "중증 자간전증은 태반기능부전과 태아성장제한, 모체 혈소판감소와 연관되며 혈소판과다증이 전형적이지 않다."),
    (r"중증.*당뇨병.*성장", "혈관병증이 진행된 중증 당뇨병은 태반관류 저하로 태아성장제한을 일으킬 수 있다."),
    (r"청색증형.*과체중", "청색증형 심질환은 모체 저산소혈증 때문에 태아성장제한 위험을 높이지 과체중아를 만들지 않는다."),
    (r"근육.*퇴행위축.*괴사성", "모체 신경근육질환은 신생아 저긴장 등과 연관될 수 있으나 괴사성 장염의 직접 짝은 아니다."),
    (r"만곡족|태아압박", "장기간 양수과소는 자궁 내 압박을 높여 만곡족 같은 자세 변형을 만들 수 있다."),
    (r"척추갈림", "척추갈림증은 신경관 결손이며 NSAID로 인한 후기 양수과소의 압박 변형이 아니다."),
    (r"신경근육질환", "신경근육질환은 태동 감소로 관절구축을 만들 수 있지만 이 증례의 NSAID-양수과소 경로와 다르다."),
    (r"낭종샘모양|폐기형", "선천성 폐기도기형은 폐 발생 이상으로 양수과소 압박 때문에 새로 생기지 않는다."),
    (r"태아의 발열", "태아 발열은 기저선 빈맥의 원인이며 수축과 거울상인 조기감속의 원인이 아니다."),
    (r"태아의 머리압박", "태아 머리압박에 따른 미주신경 반응은 수축과 동시에 완만히 내려갔다 회복되는 조기감속을 만든다."),
    (r"진정제.*태반", "진정제의 태반 통과는 변이도와 반응성을 낮출 수 있지만 조기감속의 전형적 기전은 아니다."),
    (r"폐정맥 환류 증가", "첫 호흡으로 폐혈관저항이 떨어지면 폐혈류와 폐정맥의 좌심방 환류가 증가한다."),
    (r"폐혈관 저항.*증가", "출생 후 폐가 팽창하고 산소분압이 오르면 폐혈관저항은 급격히 감소한다."),
    (r"제대 정맥 혈류 증가", "제대 결찰 뒤 태반에서 오는 제대정맥 혈류는 소실된다."),
    (r"전신 혈관 저항.*감소", "저저항 태반순환이 제거되므로 출생 직후 전신혈관저항은 증가한다."),
    (r"동맥관.*우좌", "출생 후 폐혈관저항이 떨어지면 동맥관 단락은 일시적으로 좌우 방향이 된 뒤 닫힌다."),
    (r"20초.*무호흡", "만삭아의 20초 이상 무호흡은 병적 무호흡 기준에 해당해 즉시 원인을 평가한다."),
    (r"독성 홍반", "신생아 독성홍반은 활력징후가 정상인 신생아에서 흔한 양성 발진으로 검사가 필요하지 않다."),
    (r"두정골.*두개로", "두정골의 국소적 craniotabes는 일부 정상 신생아에서도 일시적으로 보일 수 있다."),
    (r"머리둘레.*-1", "머리둘레 Z점수 -1.0은 소두증 기준인 약 -2 SD 미만에 해당하지 않는다."),
    (r"간이 1cm", "신생아에서 간이 오른쪽 갈비뼈 아래 약 1~2 cm 촉지되는 것은 정상일 수 있다."),
    (r"분유수유만", "적절한 출생 직후 면역예방을 받은 B형간염 산모의 신생아는 분유만 먹일 필요가 없다."),
    (r"처음부터.*모유", "HBV 백신과 HBIG를 출생 직후 투여했다면 처음부터 직접 모유수유할 수 있다."),
    (r"유축.*냉동", "모유를 냉동·해동하는 과정은 B형간염 전파 예방에 필요하지 않다."),
    (r"면역글로불린.*2주", "HBIG 투여 뒤 2주를 기다려야 한다는 근거는 없으며 면역예방 직후 수유할 수 있다."),
    (r"초유.*검사", "초유의 HBV 검사는 모유수유 허용 여부를 정하는 표준 검사가 아니다."),
    (r"비대칭적 모로", "비대칭 모로반사는 쇄골골절·상완신경총 손상·편측 신경학적 이상을 시사해 비정상이다."),
    (r"굽힘 근육 우위", "만삭 신생아는 사지 굴곡근 긴장이 우세한 자세가 정상이다."),
    (r"tonic neck|강직 목", "비대칭 긴장성 목반사는 초기 영아기에 나타날 수 있는 원시반사다."),
    (r"턱.*근간대", "잠깐의 턱 떨림이나 자극성은 신생아에서 보일 수 있지만 지속·자발성·눈 편위가 있으면 발작을 평가한다."),
    (r"3회.*clonus|3회의.*간대", "발목에서 몇 차례의 소진성 clonus는 어린 영아에서 보일 수 있으나 지속성 clonus는 비정상이다."),
    (r"병렬 순환", "태아순환은 두 심실의 혈류가 난원공·동맥관을 통해 병렬로 연결된다."),
    (r"폐혈관 저항이 낮", "태아 폐는 액체로 차 있고 저산소성 혈관수축이 있어 폐혈관저항이 높다."),
    (r"상지 산소분압.*하지", "태아에서는 상지·뇌로 가는 상행대동맥 혈액이 하행대동맥 혈액보다 산소포화도가 높다."),
    (r"동맥관.*좌우", "태아 동맥관에서는 폐동맥에서 하행대동맥으로 우좌단락이 일어난다."),
    (r"50%.*태아폐", "태아 우심실 혈류 대부분은 동맥관을 지나며 폐로 가는 혈류는 약 10% 수준이다."),
    (r"말단청색증", "생후 초기의 대칭적 말단청색증은 중심부가 분홍색이면 정상적인 혈관운동 반응일 수 있다."),
    (r"이마 주름.*비대칭", "울 때 이마 주름이 비대칭이면 안면신경 손상 등 국소 신경학적 이상을 평가한다."),
    (r"심박수 110", "편안히 자는 만삭 신생아의 심박수 110회/분은 정상 범위에 들어간다."),
    (r"빨간색 동공", "양측 적색반사는 정상이며 비대칭·백색반사·소실이면 백내장이나 망막질환을 평가한다."),
    (r"secretory IgA", "분비형 IgA는 점막 면역을 제공하지만 장상피 성장 촉진을 묻는 선지의 핵심 성장인자는 아니다."),
    (r"glutathione peroxidase", "glutathione peroxidase는 항산화 방어에 관여한다."),
    (r"oligosaccharide", "모유 올리고당은 유익균 증식과 병원체 부착 억제를 돕는 프리바이오틱 성분이다."),
    (r"k-casein", "κ-casein은 단백질 응고와 소화 특성에 관여하지만 대표 장상피 성장인자는 아니다."),
    (r"Transforming growth factor", "모유의 TGF는 장상피 발달과 면역 관용·장 장벽 성숙을 촉진한다."),
    (r"Mupirocin", "세균성 농가진 소견이 없는 양성 신생아 발진에는 mupirocin이 필요하지 않다."),
    (r"Epinephrine", "활력징후가 안정된 양성 발진은 아나필락시스가 아니므로 epinephrine 적응증이 아니다."),
    (r"hydrocortisone", "신생아 독성홍반은 염증성 피부질환 치료용 스테로이드가 필요하지 않다."),
    (r"amoxicillin", "전신감염이나 세균성 피부감염 소견이 없는 독성홍반에는 경구 항생제가 필요하지 않다."),
    (r"임신 초기에 시작", "대칭성 성장제한은 임신 초기에 시작해 머리와 몸통이 함께 작아지는 경우가 많다."),
    (r"임신 후기에 시작", "비대칭성 성장제한은 후기 태반기능부전으로 시작하는 경우가 많다."),
    (r"Ponderal index.*정상", "대칭성 성장제한은 체중과 길이가 비례해 ponderal index가 비교적 정상일 수 있다."),
    (r"Ponderal index.*감소", "비대칭성 성장제한은 체중이 길이보다 더 감소해 ponderal index가 낮아진다."),
    (r"성장 잠재능", "염색체·감염 같은 초기 원인의 대칭성 성장제한에서는 세포 수와 성장 잠재능이 감소할 수 있다."),
    (r"머리가 상대적으로 크", "태반기능부전성 비대칭 성장제한은 brain-sparing 때문에 몸통보다 머리가 상대적으로 보존된다."),
    (r"유전", "염색체·유전 이상은 임신 초기부터 나타나는 대칭성 성장제한의 대표 원인이다."),
    (r"선천성 감염", "선천감염은 세포 증식에 영향을 주어 대칭성 성장제한을 일으킬 수 있다."),
    (r"임신성 고혈압", "임신성 고혈압·자간전증은 후기 태반관류 저하로 비대칭성 성장제한과 연관된다."),
    (r"출생 후 나이|Postnatal day", "출생 뒤 피부가 성숙하면서 조산아의 불감수분손실은 날짜가 지날수록 감소한다."),
    (r"광선 치료", "광선치료는 피부와 주변 공기 흐름을 통해 불감수분손실을 증가시킬 수 있다."),
    (r"복사 온열|Radiant warmer", "개방형 복사온열기는 습도 장벽이 없어 불감수분손실을 증가시킨다."),
    (r"미숙성", "재태주령이 낮을수록 각질층이 미성숙해 경피 수분손실이 커진다."),
    (r"발열", "체온 상승은 증발성 수분손실을 증가시킨다."),
    (r"High ambient humidity", "높은 보육기 습도는 피부와 환경의 수증기압 차이를 줄여 불감수분손실을 감소시킨다."),
    (r"Double-walled incubator", "이중벽 보육기는 복사열 손실과 필요한 환경열을 줄여 수분손실 관리에 유리하다."),
    (r"Plastic bag wrapping", "출생 직후 비닐 포장은 극소미숙아의 증발성 열·수분손실을 줄인다."),
    (r"피부가 매끄럽고.*세정맥", "26주 전후 미숙아는 피부가 얇고 매끄러우며 혈관이 잘 비치는 소견이 맞다."),
    (r"고환이 음낭", "고환 하강과 음낭 주름의 발달은 더 성숙한 재태주령을 시사한다."),
    (r"발바닥 전체.*주름", "발바닥 전체의 깊은 주름은 만삭에 가까운 신체 성숙 소견이다."),
    (r"젖꼭지.*10mm", "큰 유방결절과 뚜렷한 유륜은 26주보다 더 성숙한 재태주령 소견이다."),
    (r"귀를 접으면 즉시", "연골이 충분해 접은 귀가 즉시 펴지는 것은 더 성숙한 신생아 소견이다."),
]


def extra_fact(choice: str, question: dict) -> str:
    text = re.sub(r"\s+", " ", choice).strip()
    qid = question["id"]
    if qid == "gendev2-12-2023-q076":
        candidate_notes = {
            "A-B-C-D": "이 배열은 기기/서기 관련 동작보다 네발기기를 먼저 두지 않아 발달의 머리-꼬리 및 근위-원위 순서와 맞지 않는다.",
            "A-B-D-C": "이 배열은 안정된 앉기보다 선 자세 동작을 먼저 두어 운동발달 순서가 뒤바뀐다.",
            "A-C-B-D": "이 배열은 그림에서 더 이른 자세반응보다 네발기기를 앞에 두어 순서가 맞지 않는다.",
            "B-C-A-D": "그림의 자세반응에서 앉기, 네발기기, 서기 단계로 이어지는 발달 순서에 맞는다.",
            "B-A-C-D": "이 배열은 네발기기를 안정된 앉기보다 먼저 두므로 일반적인 대근육 발달 순서와 맞지 않는다.",
        }
        return candidate_notes[text]
    if qid in {"gendev2-13-2025-q038", "gendev2-13-2021-q016"}:
        notes = {
            "그림 속 1번 선지": "그림 1의 자세 소견은 24주 미숙아의 대표 신경근육 성숙 점수와 일치하지 않는다.",
            "그림 속 2번 선지": "그림 2의 90도 미만 굴곡·반동은 24주보다 성숙한 신경근육 소견이다.",
            "그림 속 3번 선지": "그림 3의 약 90도 각도는 24주보다 성숙한 관절 저항을 뜻한다.",
            "그림 속 4번 선지": "그림 4의 낮은 굴곡긴장과 적은 저항은 24주 극소미숙아의 신경근육 성숙도에 맞는다.",
            "그림 속 5번 선지": "그림 5의 굴곡 저항은 24주에서 기대하는 매우 낮은 근긴장과 맞지 않는다.",
        }
        return notes[text]
    if qid == "gendev2-13-2020-q026":
        volume = int(re.search(r"\d+", text).group())
        if volume == 100:
            return "소변 100 mL+IWL 22.5 mL에서 허용할 생리적 체중감소 15 g을 빼면 약 107.5 mL이므로 보기 중 100 mL가 맞다."
        if volume == 125:
            return "125 mL는 소변과 IWL만 합산하고 허용할 생리적 체중감소 15 g을 빼지 않은 값이다."
        return f"{volume} mL는 소변 100 mL+IWL 22.5 mL-허용 체중감소 15 mL로 계산한 약 107.5 mL와 맞지 않는다."
    for pattern, explanation in EXTRA_FACTS:
        if re.search(pattern, text, re.IGNORECASE):
            return explanation
    return fact_for(text, question).rstrip(".") + "."


def numeric_profile(question: dict) -> tuple[list[str], list[str]]:
    lecture = int(question["lectureNumber"])
    if lecture <= 10:
        return profile_for(question)
    concept = (question.get("explanation") or {}).get("conceptGroup", "")
    if lecture == 11:
        if "소생술" in concept:
            return ["초기 안정화 뒤 호흡과 심박수로 환기·압박 단계를 정한다."], ["무호흡/헐떡호흡 또는 HR <100/분: PPV", "효과적 PPV 30초 뒤 HR <60/분: 흉부압박"]
        if "CMV" in concept:
            return ["산후 획득 감염과 구분하려면 생후 초기 검체로 바이러스를 확인한다."], ["선천 CMV 확진 검체: 생후 21일 이내 소변 또는 침 PCR"]
        if "양수과소" in concept:
            return ["약물 노출 뒤 태아 소변 감소와 압박 변형을 연결한다."], ["양수과소: AFI ≤5 cm 또는 단일최대수직포켓 <2 cm"]
        return [], []
    if lecture == 12:
        if "무호흡" in concept:
            return ["무호흡 지속시간과 서맥·청색증 동반 여부를 확인한다."], ["병적 무호흡: 호흡정지 ≥20초 또는 더 짧아도 서맥·청색증 동반"]
        if "발달" in concept:
            return ["각 그림의 대근육 동작을 확인하고 일반적인 획득 순서로 배열한다."], ["혼자 앉기 약 6개월, 네발기기 약 9개월, 혼자 서기 약 12개월은 참고 범위"]
        if "B형간염" in concept:
            return ["출생 직후 능동·수동면역을 완료했는지 확인한다."], ["HBV 백신+HBIG는 가능하면 출생 12시간 이내 투여"]
        return [], []
    if lecture == 13:
        if "수액 계산" in concept:
            return ["측정된 소변량과 체중당 불감수분손실을 합하고 허용할 생리적 체중감소량을 뺀다."], ["100+22.5-15=107.5 mL/일; 보기 중 100 mL"]
        if "불감수분" in concept:
            return ["피부 성숙도, 환경 습도, 개방형 열원과 광선치료 여부로 증발 손실 방향을 판단한다."], []
        return [], []
    return [], []


def build_choice_explanations(question: dict) -> list[str]:
    negative = is_negative_stem(question.get("stem", ""))
    answers = set(question.get("answers", []))
    output = []
    for index, choice in enumerate(question.get("choices", []), 1):
        fact = extra_fact(choice, question)
        if index in answers:
            verdict = "정답(틀린 진술)" if negative else "정답"
        else:
            verdict = "제외(옳은 진술)" if negative else "오답"
        output.append(f"‘{choice}’ — {verdict}. {fact}")
    return output


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    reviewed = []
    for question in payload["questions"]:
        lecture = question.get("lectureNumber", "")
        if not lecture.isdigit() or not 1 <= int(lecture) <= 13:
            continue
        exp = question.get("explanation") or {}
        if not exp:
            raise SystemExit(f"{question['id']}: explanation missing")
        if question.get("questionMode") != "self-check":
            exp["choiceExplanations"] = build_choice_explanations(question)
        criteria, numeric = numeric_profile(question)
        exp["diagnosticCriteria"] = criteria
        exp["numericReference"] = numeric
        exp["numericReview"] = {
            "status": "applicable" if numeric else "not-applicable",
            "reason": "정답 판단에 직접 쓰이는 수치만 표시" if numeric else "별도 수치 절단값이 필요하지 않음",
            "reviewedAt": REVIEW_DATE,
        }
        exp["evidenceStatus"] = f"1~13강 문항·선지 독립 재검수({REVIEW_DATE}); 각 선지는 해당 주장만 설명"
        question["explanationReviewStatus"] = "manual-choice-independent-audit-01-13"
        question["explanation"] = exp
        reviewed.append(question)

    for question in reviewed:
        explanations = question["explanation"].get("choiceExplanations", [])
        if question.get("questionMode") != "self-check" and len(explanations) != 5:
            raise SystemExit(f"{question['id']}: choice explanation count")
        if len(set(explanations)) != len(explanations):
            raise SystemExit(f"{question['id']}: duplicate explanations within question")
        key = question["explanation"].get("keyJudgment", "").strip()
        if len(key) >= 80 and any(key in text for text in explanations):
            raise SystemExit(f"{question['id']}: key judgment copied into choices")
        for index, text in enumerate(explanations):
            if len(text) > 430:
                raise SystemExit(f"{question['id']}: choice {index + 1} too long")
            for other_index, other in enumerate(question.get("choices", [])):
                if other_index != index and len(other.strip()) >= 12 and other.strip() in text:
                    raise SystemExit(f"{question['id']}: choice {index + 1} explains choice {other_index + 1}")

    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"LECTURE_01_13_CHOICE_AUDIT_PASS questions={len(reviewed)} choices={sum(len(q['explanation'].get('choiceExplanations', [])) for q in reviewed)}")


if __name__ == "__main__":
    main()
