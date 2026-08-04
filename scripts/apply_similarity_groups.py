from __future__ import annotations

import json
import re
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "questions.json"
REPORT = ROOT / "data" / "similarity_report.json"


MANUAL_GROUPS = {
    "06-placenta-previa": ("전치태반 출혈", [
        "gendev2-06-2025-q087", "gendev2-06-2023-q007",
        "gendev2-06-2022-q056", "gendev2-06-2021-q087",
    ]),
    "06-abruption": ("태반조기박리", [
        "gendev2-06-2025-q088", "gendev2-06-2022-q057", "gendev2-06-2021-q088",
    ]),
    "06-early-pregnancy": ("초기임신 출혈·임신위치불명", [
        "gendev2-06-2020-q019", "gendev2-06-2020-q020",
    ]),
    "07-preeclampsia-mechanism": ("전자간증 병태생리", [
        "gendev2-07-2025-q053", "gendev2-07-2021-q080", "gendev2-07-2020-q014",
    ]),
    "07-preeclampsia-management": ("전자간증 중증도와 분만 시점", [
        "gendev2-07-2025-q054", "gendev2-07-2023-q025", "gendev2-07-2022-q073",
        "gendev2-07-2021-q079", "gendev2-07-2020-q013",
    ]),
    "08-twins": ("쌍태임신·융모막성과 TTTS", [
        "gendev2-08-2025-q035", "gendev2-08-2023-q051", "gendev2-08-2023-q065",
        "gendev2-08-2022-q048", "gendev2-08-2021-q081", "gendev2-08-2020-q009",
    ]),
    "08-fgr": ("태아성장제한과 제대동맥 도플러", [
        "gendev2-08-2025-q036", "gendev2-08-2022-q045",
        "gendev2-08-2021-q082", "gendev2-08-2020-q010",
    ]),
    "09-breastfeeding": ("수유·유방염", [
        "gendev2-09-2025-q061", "gendev2-09-2023-q016", "gendev2-09-2022-q049",
    ]),
    "09-contraception": ("산후 피임과 수유", [
        "gendev2-09-2021-q007", "gendev2-09-2020-q017",
    ]),
    "09-endometritis": ("제왕절개 후 자궁내막염", [
        "gendev2-09-2022-q011", "gendev2-09-2021-q008", "gendev2-09-2020-q018",
    ]),
    "10-pul-ectopic": ("임신위치불명·자궁외임신", [
        "gendev2-10-2025-q003", "gendev2-10-2023-q086",
        "gendev2-10-2022-q004", "gendev2-10-2021-q010",
    ]),
    "10-pregnancy-loss": ("초기임신 출혈·유산", [
        "gendev2-10-2025-q004", "gendev2-10-2023-q066",
        "gendev2-10-2022-q006", "gendev2-10-2021-q009",
    ]),
    "10-antepartum-bleeding": ("임신후반기 출혈(오분류 의심)", [
        "gendev2-10-2020-q015", "gendev2-10-2020-q016",
    ]),
}


def normalized(text: str) -> str:
    text = re.sub(r"\d+(?:[.,/]\d+)*", "#", text.lower())
    return re.sub(r"[^0-9a-z가-힣#]+", "", text)


def similarity(a: dict, b: dict) -> tuple[float, float, float]:
    stem = SequenceMatcher(None, normalized(a.get("stem", "")), normalized(b.get("stem", ""))).ratio()
    choices_a = "|".join(normalized(x) for x in a.get("choices", []))
    choices_b = "|".join(normalized(x) for x in b.get("choices", []))
    choices = SequenceMatcher(None, choices_a, choices_b).ratio() if choices_a and choices_b else 0.0
    score = 0.72 * stem + 0.28 * choices
    return stem, choices, score


def find(parent: dict[str, str], item: str) -> str:
    while parent[item] != item:
        parent[item] = parent[parent[item]]
        item = parent[item]
    return item


def union(parent: dict[str, str], a: str, b: str) -> None:
    ra, rb = find(parent, a), find(parent, b)
    if ra != rb:
        parent[rb] = ra


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    questions = payload["questions"]
    by_id = {q["id"]: q for q in questions}
    parent = {q["id"]: q["id"] for q in questions}
    candidates = []

    by_lecture: dict[str, list[dict]] = defaultdict(list)
    for q in questions:
        by_lecture[q["lectureNumber"]].append(q)

    # 전체 강의를 훑되, 실제 순서 변경은 오탐이 적은 높은 문장 유사도만 사용한다.
    for lecture, items in by_lecture.items():
        for i, a in enumerate(items):
            for b in items[i + 1:]:
                stem, choices, score = similarity(a, b)
                if stem >= 0.64 or score >= 0.62:
                    candidates.append({
                        "lecture": lecture, "a": a["id"], "b": b["id"],
                        "stem": round(stem, 3), "choices": round(choices, 3), "score": round(score, 3),
                    })
                if stem >= 0.90 or (stem >= 0.76 and choices >= 0.58 and score >= 0.72):
                    union(parent, a["id"], b["id"])

    manual_meta: dict[frozenset[str], tuple[str, str]] = {}
    for group_id, (label, ids) in MANUAL_GROUPS.items():
        missing = [qid for qid in ids if qid not in by_id]
        if missing:
            raise SystemExit(f"manual similarity ID missing: {missing}")
        for qid in ids[1:]:
            union(parent, ids[0], qid)
        manual_meta[frozenset(ids)] = (group_id, label)

    components: dict[str, list[str]] = defaultdict(list)
    for qid in parent:
        components[find(parent, qid)].append(qid)

    for q in questions:
        for key in ("similarGroupId", "similarGroupLabel", "similarGroupPosition", "similarGroupSize", "studyOrder"):
            q.pop(key, None)

    groups = []
    for lecture, items in by_lecture.items():
        original_index = {q["id"]: i for i, q in enumerate(items)}
        lecture_components = [sorted(ids, key=original_index.get) for ids in components.values()
                              if len(ids) >= 2 and by_id[ids[0]]["lectureNumber"] == lecture]
        for n, ids in enumerate(sorted(lecture_components, key=lambda x: original_index[x[0]]), 1):
            manual = next((value for ids_key, value in manual_meta.items() if ids_key.issubset(set(ids))), None)
            group_id = manual[0] if manual else f"{lecture}-auto-{n:02d}"
            label = manual[1] if manual else "문장·선지가 매우 비슷한 반복 문항"
            for pos, qid in enumerate(ids, 1):
                q = by_id[qid]
                q["similarGroupId"] = group_id
                q["similarGroupLabel"] = label
                q["similarGroupPosition"] = pos
                q["similarGroupSize"] = len(ids)
                peers = [other for other in ids if other != qid]
                q["relatedIds"] = list(dict.fromkeys(peers + q.get("relatedIds", [])))
            groups.append({"id": group_id, "label": label, "lecture": lecture, "members": ids})

        # 기존 순서를 최대한 보존하면서 첫 문항이 나오면 같은 묶음을 바로 이어 붙인다.
        ordered, seen = [], set()
        component_by_id = {qid: ids for ids in lecture_components for qid in ids}
        for q in items:
            if q["id"] in seen:
                continue
            block = component_by_id.get(q["id"], [q["id"]])
            ordered.extend(block)
            seen.update(block)
        for order, qid in enumerate(ordered, 1):
            by_id[qid]["studyOrder"] = order

    candidates.sort(key=lambda x: (-x["score"], x["lecture"], x["a"], x["b"]))
    REPORT.write_text(json.dumps({"groups": groups, "candidates": candidates}, ensure_ascii=False, indent=2), encoding="utf-8")
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"SIMILARITY_GROUPS_APPLIED lectures={len(by_lecture)} groups={len(groups)} grouped_questions={sum(len(g['members']) for g in groups)} candidates={len(candidates)}")


if __name__ == "__main__":
    main()
