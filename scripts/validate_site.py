from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    payload = json.loads((SITE / "data" / "questions.json").read_text(encoding="utf-8"))
    questions = payload.get("questions", [])
    expected = 3 if args.pilot else 499
    if len(questions) != expected:
        fail(f"문항 수: expected={expected}, actual={len(questions)}", errors)
    ids = [q.get("id") for q in questions]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        fail(f"중복 ID: {duplicates}", errors)
    for q in questions:
        qid = q.get("id", "(no id)")
        if not q.get("stem"):
            fail(f"{qid}: 빈 문제", errors)
        if q.get("questionMode") != "self-check" and (len(q.get("choices", [])) != 5 or any(not choice for choice in q.get("choices", []))):
            fail(f"{qid}: 선택지 5개 아님/빈 선택지", errors)
        answers = q.get("answers", [])
        if q.get("questionMode") != "self-check" and not answers and q.get("answerStatus") != "정답 불명":
            fail(f"{qid}: 정답 누락", errors)
        if any(answer not in range(1, 6) for answer in answers):
            fail(f"{qid}: 정답 누락/범위 오류", errors)
        if not q.get("lectureNumber") or not q.get("lectureTitle"):
            fail(f"{qid}: 강의 분류 누락", errors)
        if not q.get("keyConcepts") or any(not concept.strip() for concept in q.get("keyConcepts", [])):
            fail(f"{qid}: 복습 개념 누락", errors)
        for asset in q.get("assets", []):
            asset_path = SITE / asset if asset.startswith("assets/") else SITE / "assets" / "questions" / asset
            if not asset_path.is_file():
                fail(f"{qid}: 이미지 없음 {asset}", errors)
        for crop in q.get("assetCrops", []):
            if not (SITE / "assets" / "lecture-examples" / crop["asset"]).is_file():
                fail(f"{qid}: 강의 예시 이미지 없음 {crop['asset']}", errors)
        exp = q.get("explanation")
        if args.pilot and (not exp or len(exp.get("choiceExplanations", [])) != 5):
            fail(f"{qid}: 시험판 선지별 해설 누락", errors)
        if q.get("lectureNumber") in {f"{number:02d}" for number in range(1, 21)}:
            if not exp or not exp.get("keyJudgment") or not exp.get("reasoningSteps") or not exp.get("conceptReview"):
                fail(f"{qid}: 1~20강 상세 해설 누락", errors)
            if q.get("questionMode") != "self-check" and len((exp or {}).get("choiceExplanations", [])) != 5:
                fail(f"{qid}: 1~20강 선지별 해설 5개 누락", errors)
            if not (exp or {}).get("sources"):
                fail(f"{qid}: 1~20강 해설 출처 누락", errors)
            if not (exp or {}).get("questionCheck"):
                fail(f"{qid}: 문제 요구·정답 개수 확인 문구 누락", errors)
    if not args.pilot:
        for lecture in [f"{number:02d}" for number in range(1, 11)]:
            predicted = [q for q in questions if q.get("lectureNumber") == lecture and q.get("sourceKind") == "2026-predicted"]
            if len(predicted) < 3:
                fail(f"{lecture}강: 2026 예상문제 3개 미만", errors)
            for q in predicted:
                if not q.get("explanation", {}).get("diagnosticCriteria"):
                    fail(f"{q['id']}: 진단 기준·분류 누락", errors)
    # 2026-08-05부터 일부 강의가 아니라 전체 문항에 같은 해설 품질 문턱을 적용한다.
    numeric_questions = []
    for q in questions:
        qid = q.get("id", "(no id)")
        exp = q.get("explanation") or {}
        if not exp.get("keyJudgment") or not exp.get("reasoningSteps") or not exp.get("conceptReview"):
            fail(f"{qid}: 전체 문항 핵심·단계·개념 해설 누락", errors)
        if q.get("questionMode") != "self-check" and len(exp.get("choiceExplanations", [])) != 5:
            fail(f"{qid}: 전체 문항 선지별 해설 5개 누락", errors)
        if not exp.get("sources"):
            fail(f"{qid}: 전체 문항 출처 누락", errors)
        numeric_text = q.get("stem", "") + " " + " ".join(q.get("choices", []))
        if any(char.isdigit() for char in numeric_text):
            numeric_questions.append(q)
            if not exp.get("numericReference"):
                fail(f"{qid}: 수치 문항 정상치·진단 기준 누락", errors)
    html = (SITE / "index.html").read_text(encoding="utf-8")
    app_js = (SITE / "app.js").read_text(encoding="utf-8")
    if "예상문제 · 비출제" not in app_js or "pill prediction" not in app_js:
        fail("예상문제 전용 배지 누락", errors)
    if "evidence.css" not in html:
        fail("예상문제·수치 기준 스타일시트 누락", errors)
    audited = [q for q in questions if q.get("lectureNumber", "").isdigit() and 1 <= int(q["lectureNumber"]) <= 20]
    judgments = [q.get("explanation", {}).get("keyJudgment", "") for q in audited]
    duplicate_judgments = sorted({text for text in judgments if text and judgments.count(text) > 1})
    if duplicate_judgments:
        fail(f"1~20강 동일 핵심해설 재사용 {len(duplicate_judgments)}개", errors)
    concept_reviews = [q.get("explanation", {}).get("conceptReview", "") for q in audited]
    duplicate_reviews = sorted({text for text in concept_reviews if text and concept_reviews.count(text) > 1})
    if duplicate_reviews:
        fail(f"1~20강 동일 개념복습 재사용 {len(duplicate_reviews)}개", errors)
    choice_explanations = [text for q in audited for text in q.get("explanation", {}).get("choiceExplanations", [])]
    duplicate_choice_explanations = sorted({text for text in choice_explanations if text and choice_explanations.count(text) > 1})
    if duplicate_choice_explanations:
        fail(f"1~20강 동일 선지해설 재사용 {len(duplicate_choice_explanations)}개", errors)
    html_ids = set(re.findall(r'id="([^"]+)"', html))
    grouped = [q for q in questions if q.get("similarGroupId")]
    groups: dict[str, list[dict]] = {}
    for q in grouped:
        groups.setdefault(q["similarGroupId"], []).append(q)
    for group_id, members in groups.items():
        if len(members) < 2:
            fail(f"{group_id}: 유사문항 묶음에 문항이 1개뿐", errors)
        if len({q["lectureNumber"] for q in members}) != 1:
            fail(f"{group_id}: 서로 다른 강의가 한 묶음에 포함", errors)
        expected_positions = list(range(1, len(members) + 1))
        if sorted(q.get("similarGroupPosition", 0) for q in members) != expected_positions:
            fail(f"{group_id}: 유사문항 위치 번호 오류", errors)
        member_ids = {q["id"] for q in members}
        for q in members:
            if not member_ids.difference({q["id"]}).issubset(set(q.get("relatedIds", []))):
                fail(f"{q['id']}: 같은 묶음 문항 relatedIds 누락", errors)
    for lecture in {q["lectureNumber"] for q in questions}:
        orders = [q.get("studyOrder") for q in questions if q["lectureNumber"] == lecture]
        if sorted(orders) != list(range(1, len(orders) + 1)):
            fail(f"{lecture}강: studyOrder 중복/누락", errors)

    required_ids = {"login", "attendance", "lecture-list", "question-card", "discussion-list", "review-view", "review-list", "concept-view", "concept-list", "sync-status", "progress-view", "progress-summary", "progress-list", "professors-view", "professors-table"}
    missing_ids = sorted(required_ids - html_ids)
    if missing_ids:
        fail(f"HTML 필수 대상 누락: {missing_ids}", errors)
    table_images = list((SITE / "assets" / "questions").glob("*-table-*.png"))
    print(f"VALIDATION_COUNTS questions={len(questions)} numericQuestions={len(numeric_questions)} assets={sum(len(q.get('assets', [])) for q in questions)} tableImagesOnDisk={len(table_images)}")
    if errors:
        print("VALIDATION_FAIL")
        print("\n".join(f"- {error}" for error in errors))
        sys.exit(1)
    print("PILOT_VALIDATION_PASS" if args.pilot else "FULL_VALIDATION_PASS")


if __name__ == "__main__":
    main()
