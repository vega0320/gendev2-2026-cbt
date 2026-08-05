from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "site" / "data" / "questions.json"


def main() -> None:
    questions = json.loads(DATA.read_text(encoding="utf-8"))["questions"]
    errors: list[str] = []
    numeric = []
    for question in questions:
        qid = question["id"]
        exp = question.get("explanation") or {}
        required_fields = ["keyJudgment", "reasoningSteps", "conceptReview", "sources"]
        if question.get("questionMode") != "self-check":
            required_fields.append("choiceExplanations")
        for field in required_fields:
            if not exp.get(field):
                errors.append(f"{qid}: {field} missing")
        if question.get("questionMode") != "self-check" and len(exp.get("choiceExplanations", [])) != 5:
            errors.append(f"{qid}: choice explanations != 5")
        text = question.get("stem", "") + " " + " ".join(question.get("choices", []))
        lecture = question.get("lectureNumber", "")
        audited_01_10 = lecture.isdigit() and 1 <= int(lecture) <= 10
        if audited_01_10:
            review = exp.get("numericReview") or {}
            if review.get("status") not in {"applicable", "not-applicable"}:
                errors.append(f"{qid}: numeric review status missing")
            if review.get("status") == "applicable":
                numeric.append(question)
                if not exp.get("numericReference"):
                    errors.append(f"{qid}: applicable numeric reference missing")
            elif exp.get("numericReference"):
                errors.append(f"{qid}: non-applicable question has numeric reference")
            if question.get("explanationReviewStatus") != "manual-lecture-choice-numeric-audit":
                errors.append(f"{qid}: lecture 1-10 manual review marker missing")
        elif any(char.isdigit() for char in text):
            numeric.append(question)
            if not exp.get("numericReference"):
                errors.append(f"{qid}: numeric reference missing")
        if question.get("sourceKind") == "2026-predicted":
            for field in ("predictionBasis", "difficulty", "predictionReviewDate"):
                if not question.get(field):
                    errors.append(f"{qid}: {field} missing")
            if not exp.get("commonPitfall"):
                errors.append(f"{qid}: predicted pitfall missing")
            if not audited_01_10 and sum(step.startswith("최종 재확인:") for step in exp.get("reasoningSteps", [])) != 1:
                errors.append(f"{qid}: predicted final-check step duplicated or missing")
            if not audited_01_10 and exp.get("conceptReview", "").count("재출제 포인트:") != 1:
                errors.append(f"{qid}: predicted review point duplicated or missing")
    all_explanations = [text for q in questions for text in q.get("explanation", {}).get("choiceExplanations", [])]
    banned = ("적어도 하나가 정답 조건과 맞지", "옳은 선지은", "원문과 비교하세요")
    for phrase in banned:
        if any(phrase in text for text in all_explanations):
            errors.append(f"banned generic phrase remains: {phrase}")
    reviewed_choices = [
        text for q in questions
        if q.get("lectureNumber", "").isdigit() and 1 <= int(q["lectureNumber"]) <= 10
        for text in q.get("explanation", {}).get("choiceExplanations", [])
    ]
    for phrase in ("결정 단서와 맞지 않는다", "관련되지 않는다", "구분해야 한다", "사례를 그 원칙에 대입해", "정답 조건과 맞지"):
        if any(phrase in text for text in reviewed_choices):
            errors.append(f"lecture 1-10 banned choice phrase remains: {phrase}")
    predicted = [q for q in questions if q.get("sourceKind") == "2026-predicted"]
    judgments = [q.get("explanation", {}).get("keyJudgment", "") for q in questions]
    print(
        "EVIDENCE_AUDIT_COUNTS "
        f"questions={len(questions)} explanations={sum(bool(q.get('explanation')) for q in questions)} "
        f"numeric={len(numeric)} numericCovered={sum(bool(q.get('explanation', {}).get('numericReference')) for q in numeric)} "
        f"predicted={len(predicted)} duplicateJudgments={sum(count > 1 for count in Counter(judgments).values())}"
    )
    if errors:
        print("EVIDENCE_CONTENT_AUDIT_FAIL")
        print("\n".join(f"- {error}" for error in errors))
        raise SystemExit(1)
    print("EVIDENCE_CONTENT_AUDIT_PASS")


if __name__ == "__main__":
    main()
