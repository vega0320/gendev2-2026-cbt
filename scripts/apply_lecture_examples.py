from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"


EXAMPLES = [
    {
        "lectureNumber": "03",
        "lectureTitle": "산전진단/산전태아평가",
        "sourceLectureTitle": "산전진단/산전태아평가",
        "year": "2026",
        "number": 901,
        "displayNumber": "강의 예시 1",
        "sourceKind": "lecture-example",
        "examStatus": "강의에서 제시 · 비출제",
        "answers": [2],
        "answerStatus": "2026 강의 슬라이드 제시 정답",
        "answerRaw": "양수천자",
        "answerNote": "출제 문항이 아닌 강의 예시",
        "professor2026": "김선민",
        "professorAtExam": "김선민",
        "importance": "lecture-demo",
        "classificationStatus": "사용자 지정 3강",
        "yearStatus": "2026 강의 예시",
        "id": "gendev2-03-2026-q901",
        "stem": "임신 15주인 38세 미분만부가 산전상담을 위해 왔다. 2주 전 시행한 태아 DNA 선별검사(cell-free fetal DNA screening)에서 21번 삼염색체증 고위험군, 18번·13번 삼염색체증과 성염색체 이수성은 저위험군이었다. 초음파검사에서 이상은 없다. 처치는?",
        "choices": ["태아 DNA 선별검사 재검", "양수천자", "탯줄천자", "융모막융모생검", "치료유산"],
        "content": [{"type": "text", "text": "2026 강의에서 제시한 비출제 예시"}],
        "choiceStatus": "사용자 제공 슬라이드 수동 대조",
        "assets": [],
        "assetCrops": [{"asset": "gendev2-03-2026-q901-source.png", "x": 48, "y": 147, "width": 441, "height": 248, "sourceWidth": 1495, "sourceHeight": 703, "alt": "태아 DNA 선별검사 결과 표"}],
        "sourcePages": [],
        "explanation": {
            "conceptGroup": "cfDNA 양성 뒤 확진검사",
            "keyJudgment": "cfDNA는 선별검사다. 21번 삼염색체증 고위험 결과는 확진이 아니므로 유전상담 후 진단검사를 권한다. 임신 15주에는 양수천자가 적절하다.",
            "reasoningSteps": ["고위험 cfDNA 결과는 선별 양성이므로 유전상담과 침습적 확진검사가 필요하다.", "정상 초음파는 21번 삼염색체 가능성을 배제하지 못한다.", "임신 15주는 융모막융모검사의 일반적 시기보다 늦고 양수천자가 가능한 시기이므로, 양수 세포의 핵형·염색체검사를 진행한다."],
            "choiceExplanations": ["이미 보고 가능한 양성 결과가 나온 선별검사를 단순 반복하면 확진이 지연된다.", "정답. 임신 15주에 양수를 채취해 태아 염색체를 진단한다.", "탯줄천자는 더 늦은 주수에 특정 적응증으로 고려하며 이 상황의 우선 진단검사가 아니다.", "융모막융모생검도 진단검사지만 일반적으로 더 이른 임신 1삼분기에 시행한다. 15주라는 시점에서는 양수천자가 알맞다.", "선별검사 양성만으로 치료유산을 결정하지 않는다. 진단검사와 상담이 먼저다."],
            "conceptReview": "ACOG가 2026년에 확인한 현재 지침은 cfDNA 양성 뒤 유전상담, 상세 초음파, CVS 또는 양수천자 같은 진단검사를 권한다. 시술 선택은 임신 주수와 환자 선호를 함께 본다.",
            "evidenceStatus": "사용자 제공 슬라이드·ACOG 2026 공식 지침 대조",
            "sources": [{"label": "ACOG: Screening for Fetal Chromosomal Abnormalities (2026)", "url": "https://www.acog.org/clinical/clinical-guidance/practice-advisory/articles/2026/01/screening-for-fetal-chromosomal-abnormalities", "kind": "현재 지침"}, {"label": "Williams Obstetrics 26e", "url": "https://accessmedicine.mhmedical.com/book.aspx?bookid=2977", "kind": "교과서"}],
        },
    },
    {
        "lectureNumber": "03",
        "lectureTitle": "산전진단/산전태아평가",
        "sourceLectureTitle": "산전진단/산전태아평가",
        "year": "2026",
        "number": 902,
        "displayNumber": "강의 예시 2",
        "sourceKind": "lecture-example",
        "examStatus": "강의에서 제시 · 비출제",
        "questionMode": "self-check",
        "answers": [],
        "expectedAnswer": "비수축검사(NST)와 초음파 탯줄동맥 도플러",
        "answerStatus": "2026 강의 슬라이드 제시 정답",
        "answerRaw": "비수축 검사(NST), 초음파 검사(탯줄동맥 도플러)",
        "answerNote": "원본에 객관식 선지가 없는 단답형 강의 예시",
        "professor2026": "김선민",
        "professorAtExam": "김선민",
        "importance": "lecture-demo",
        "classificationStatus": "사용자 지정 3강",
        "yearStatus": "2026 강의 예시",
        "id": "gendev2-03-2026-q902",
        "stem": "임신 35주인 40세 미분만부가 태동이 평소보다 잘 느껴지지 않아 왔다. 혈압 180/70 mmHg, 맥박 90회/분, 호흡 20회/분, 체온 36.5℃이다. 초음파에서 예상태아체중은 1,700 g(5백분위수 1,871 g), 양수지수는 2 cm이다. 필요한 검사는? 두 가지를 쓰시오.",
        "choices": [],
        "content": [{"type": "text", "text": "2026 강의에서 제시한 비출제 단답형 예시"}],
        "choiceStatus": "원본 선택지 없음 · 단답 자기채점",
        "assets": [],
        "sourcePages": [],
        "explanation": {
            "conceptGroup": "태아성장제한 감시",
            "keyJudgment": "태동 감소, 5백분위수 미만의 예상체중, 양수과소는 태반기능 저하와 태아성장제한을 의심하게 한다. 강의 답은 NST와 탯줄동맥 도플러다.",
            "reasoningSteps": ["태동 감소가 있어 현재 태아 상태를 NST로 평가한다.", "성장제한과 양수과소가 있어 태반 저항과 태아 위험을 탯줄동맥 도플러로 평가한다.", "수축기 혈압 180 mmHg는 별도로 즉시 재확인하고 중증 임신고혈압 평가·치료가 필요한 수치다."],
            "choiceExplanations": [],
            "conceptReview": "SMFM은 FGR 진단 뒤 탯줄동맥 도플러를 반복 평가하고, 생존 가능 주수 이후 CTG/NST 감시를 권한다. 빈도와 분만 시점은 도플러의 이완기 혈류, 동반 질환, 임신 주수와 전체 임상상에 따라 달라진다.",
            "evidenceStatus": "사용자 제공 슬라이드·SMFM Consult #52(2024 재확인) 대조",
            "sources": [{"label": "SMFM Consult Series #52: Fetal Growth Restriction", "url": "https://publications.smfm.org/publications/289-society-for-maternal-fetal-medicine-consult-series-52/", "kind": "현재 지침"}, {"label": "ACOG: Preeclampsia and High Blood Pressure During Pregnancy", "url": "https://www.acog.org/womens-health/faqs/preeclampsia-and-high-blood-pressure-during-pregnancy", "kind": "안전 주의"}],
        },
    },
]


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    example_ids = {item["id"] for item in EXAMPLES}
    payload["questions"] = [item for item in payload["questions"] if item.get("id") not in example_ids]
    payload["questions"].extend(EXAMPLES)
    payload["questions"].sort(key=lambda item: (item["lectureNumber"], -int(item["year"]), item["number"], item["id"]))
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"LECTURE_EXAMPLES_APPLIED count={len(EXAMPLES)} total={len(payload['questions'])}")


if __name__ == "__main__":
    main()
