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
    expected = 3 if args.pilot else 450
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
        if q.get("lectureNumber") in {"01", "02", "03", "04"}:
            if not exp or not exp.get("keyJudgment") or not exp.get("reasoningSteps") or not exp.get("conceptReview"):
                fail(f"{qid}: 1~4강 상세 해설 누락", errors)
            if q.get("questionMode") != "self-check" and len((exp or {}).get("choiceExplanations", [])) != 5:
                fail(f"{qid}: 1~4강 선지별 해설 5개 누락", errors)
            if not (exp or {}).get("sources"):
                fail(f"{qid}: 1~4강 해설 출처 누락", errors)
    html = (SITE / "index.html").read_text(encoding="utf-8")
    html_ids = set(re.findall(r'id="([^"]+)"', html))
    required_ids = {"login", "attendance", "lecture-list", "question-card", "discussion-list", "review-view", "review-list", "concept-view", "concept-list"}
    missing_ids = sorted(required_ids - html_ids)
    if missing_ids:
        fail(f"HTML 필수 대상 누락: {missing_ids}", errors)
    table_images = list((SITE / "assets" / "questions").glob("*-table-*.png"))
    print(f"VALIDATION_COUNTS questions={len(questions)} assets={sum(len(q.get('assets', [])) for q in questions)} tableImagesOnDisk={len(table_images)}")
    if errors:
        print("VALIDATION_FAIL")
        print("\n".join(f"- {error}" for error in errors))
        sys.exit(1)
    print("PILOT_VALIDATION_PASS" if args.pilot else "FULL_VALIDATION_PASS")


if __name__ == "__main__":
    main()
