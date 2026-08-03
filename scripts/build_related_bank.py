from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[1]
DATA_PATH = ROOT / "data" / "questions.json"
IMCHU_PATH = WORKSPACE / "2023_임추2_족보_GitHub_Pages" / "questions.js"
GUKSI_PATH = WORKSPACE / "2023_임추2_족보_GitHub_Pages" / "guksi_questions.js"
OUTPUT = ROOT / "work" / "related_bank_report.json"

CURATED_OVERRIDES = {
    "gendev2-01-2025-q051": ["kme-90-s2-q010", "kme-88-s3-q067", "kme-89-s4-q020"],
    "gendev2-01-2025-q052": ["kme-88-s4-q015", "kme-88-s1-q030", "kme-88-s2-q043"],
    "gendev2-01-2023-q053": ["kme-90-s2-q010"],
}

DOMAIN = re.compile(r"임신|산모|태아|태반|분만|산후|자궁|난소|난관|질\b|월경|폐경|유방|신생아|소아|사춘기|선천|유전|염색체|산부인과|여성의학|embry|pregnan|fetal|placent|obstet|gyne", re.I)
TOKEN_RE = re.compile(r"[가-힣]{2,}|[A-Za-z]{3,}")
STOP = {"환자","여자","남자","다음","대한","관한","설명","정상","검사","치료","진단","문항","고르시오","있다","한다","이다","보기","가장","문제","혈액","임신"}


def load_js_array(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    start = text.index("[")
    end = text.rfind("]") + 1
    return json.loads(text[start:end])


def text_of(item: dict, source: str) -> str:
    if source == "임추":
        fields = [item.get("specialty"), item.get("topic"), item.get("prompt"), *item.get("tags", []), *item.get("keyConcepts", [])]
    else:
        fields = [item.get("subject"), item.get("specialty"), item.get("diagnosis"), item.get("stemText"), item.get("summary"), *item.get("keyConcepts", [])]
    return " ".join(str(value or "") for value in fields)


def tokens(text: str) -> Counter:
    found = [token.lower() for token in TOKEN_RE.findall(text) if token.lower() not in STOP]
    expanded = []
    for token in found:
        expanded.append(token)
        if "철분" in token or token == "철" or "빈혈" in token: expanded.append("iron")
        if "갑상" in token or token in {"tsh", "hcg", "thyroid"}: expanded.append("thyroid")
        if "태아" in token or "태반" in token: expanded.append("fetal")
        if "고혈압" in token or "전자간" in token: expanded.append("preeclampsia")
        if "요당" in token or "당뇨" in token or "포도당" in token: expanded.append("glucose")
        if "콜레스테롤" in token or "지질" in token: expanded.append("lipid")
        if "심박" in token or "심박출" in token: expanded.append("cardiac")
    return Counter(expanded)


def compact(item: dict, source: str) -> dict:
    if source == "임추":
        return {
            "id": f"imchu-q{int(item['number']):03d}", "source": source,
            "title": item.get("topic") or item.get("specialty") or "임추 문항",
            "stem": item.get("prompt", ""), "choices": item.get("choices", []),
            "answer": item.get("answer"), "explanation": item.get("explanation", ""),
            "choiceExplanations": item.get("choiceExplanations", []),
        }
    return {
        "id": item.get("id"), "source": source,
        "title": item.get("diagnosis") or item.get("specialty") or "국시 문항",
        "stem": item.get("stemText") or item.get("summary") or "",
        "choices": item.get("choices", []), "answer": item.get("answer"),
        "explanation": item.get("explanation", ""), "choiceExplanations": item.get("choiceExplanations", []),
    }


def main() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    candidates = []
    for source, path in [("임추", IMCHU_PATH), ("국시", GUKSI_PATH)]:
        for item in load_js_array(path):
            haystack = text_of(item, source)
            if len(item.get("choices", [])) == 5:
                candidates.append((compact(item, source), tokens(haystack)))
    bank: dict[str, dict] = {}
    candidate_by_id = {item["id"]: item for item, _ in candidates}
    matched = 0
    for question in payload["questions"]:
        query = tokens(" ".join([question.get("lectureTitle", ""), question.get("stem", ""), *question.get("choices", [])]))
        scored = []
        concept_tokens = {"iron", "thyroid", "preeclampsia", "glucose", "lipid", "cardiac", "fetal"}
        required_concepts = query.keys() & concept_tokens
        primary_concepts = ({"iron"} if "iron" in required_concepts else
                            {"thyroid"} if "thyroid" in required_concepts else
                            {"glucose"} if "glucose" in required_concepts else
                            {"lipid"} if "lipid" in required_concepts else
                            {"preeclampsia"} if "preeclampsia" in required_concepts else
                            {"cardiac"} if "cardiac" in required_concepts else
                            required_concepts)
        for item, candidate_tokens in candidates:
            if primary_concepts and not (primary_concepts & candidate_tokens.keys()):
                continue
            if not required_concepts and not DOMAIN.search(item["stem"] + " " + item["title"]):
                continue
            shared = query.keys() & candidate_tokens.keys()
            score = sum(min(query[token], candidate_tokens[token]) for token in shared)
            score += 5 * len(shared & concept_tokens)
            if score >= 3:
                scored.append((score, item))
        scored.sort(key=lambda pair: (-pair[0], pair[1]["source"], pair[1]["id"]))
        chosen = []
        for score, item in scored:
            if item["id"] in chosen:
                continue
            bank[item["id"]] = item
            chosen.append(item["id"])
            if len(chosen) == 3:
                break
        question["relatedExternalIds"] = chosen
        if question["id"] in CURATED_OVERRIDES:
            chosen = [item_id for item_id in CURATED_OVERRIDES[question["id"]] if item_id in candidate_by_id]
            question["relatedExternalIds"] = chosen
            for item_id in chosen:
                bank[item_id] = candidate_by_id[item_id]
        if chosen:
            matched += 1
    payload["relatedBank"] = list(bank.values())
    DATA_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    report = {"imchuCount": len(load_js_array(IMCHU_PATH)), "guksiCount": len(load_js_array(GUKSI_PATH)), "domainCandidates": len(candidates), "matchedGenerationQuestions": matched, "relatedBankItems": len(bank), "pilotMatches": {q["id"]: q["relatedExternalIds"] for q in payload["questions"][:3]}}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
