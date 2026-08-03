from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in payload["questions"]}
    corrected = by_id["gendev2-01-2020-q002"]
    corrected["originalAnswers"] = corrected["answers"]
    corrected["answers"] = [3]
    corrected["answerStatus"] = "족보 ① 오류 의심 · Williams 대조 정답 ③"
    corrected["answerNote"] = "정상 임신은 말초 인슐린 저항으로 포도당 흡수가 감소한다. 공복 유리지방산은 감소가 아니라 증가한다."
    corrected["answerReviewStatus"] = "Williams Obstetrics 26e Chapter 4 수동 대조"
    ambiguous = by_id["gendev2-01-2023-q053"]
    ambiguous["answerNote"] = "족보 정답 ① 유지. 다만 ②는 현재 WHO 예방 보충 지침의 '가능한 한 이르게 시작'과 겹쳐 문항 표현이 모호함."
    ambiguous["answerReviewStatus"] = "② 선지 현재 지침과 충돌 · 오류토의 권장"
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("EVIDENCE_CORRECTIONS_APPLIED corrected=1 ambiguous=1")


if __name__ == "__main__":
    main()

