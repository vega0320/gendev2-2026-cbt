#!/usr/bin/env python3
"""Extract page-scoped text and a compact manifest from private 2026 lecture PDFs."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "data" / "lecture_notes_2026"
INDEX_DIR = SOURCE_DIR / "index"

KEYWORDS = {
    "case": re.compile(r"\bcase\b|증례", re.IGNORECASE),
    "question": re.compile(r"문제|연습|quiz|question", re.IGNORECASE),
    "past_year": re.compile(r"(?:19|20)\d{2}\s*년?"),
    "emphasis": re.compile(r"중요|강조|시험|족보|출제", re.IGNORECASE),
}


def normalized_name(path: Path) -> str:
    return unicodedata.normalize("NFC", path.name)


def slug_for(path: Path) -> str:
    match = re.match(r"\[(\d{6}_\d{2})\]", normalized_name(path))
    if not match:
        raise ValueError(f"강의 파일 접두사를 읽을 수 없습니다: {path.name}")
    return match.group(1)


def main() -> None:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(SOURCE_DIR.glob("*.pdf"), key=lambda p: normalized_name(p))
    if len(pdfs) != 10:
        raise SystemExit(f"필기 PDF 10개가 필요하지만 {len(pdfs)}개입니다.")

    manifest: list[dict[str, object]] = []
    for pdf_path in pdfs:
        reader = PdfReader(pdf_path)
        page_records: list[dict[str, object]] = []
        markdown: list[str] = [f"# {normalized_name(pdf_path)}", ""]
        for page_number, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").replace("\x00", "").strip()
            flags = [name for name, pattern in KEYWORDS.items() if pattern.search(text)]
            years = sorted(set(KEYWORDS["past_year"].findall(text)))
            page_records.append(
                {
                    "page": page_number,
                    "characters": len(text),
                    "flags": flags,
                    "years": years,
                }
            )
            markdown.extend(
                [
                    f"## p.{page_number}",
                    f"<!-- source: p.{page_number}; flags: {', '.join(flags) or '-'} -->",
                    "",
                    text or "[텍스트층 없음 - 원본 이미지 확인 필요]",
                    "",
                ]
            )

        slug = slug_for(pdf_path)
        md_path = INDEX_DIR / f"{slug}.md"
        md_path.write_text("\n".join(markdown), encoding="utf-8")
        manifest.append(
            {
                "slug": slug,
                "file": normalized_name(pdf_path),
                "bytes": pdf_path.stat().st_size,
                "pages": len(reader.pages),
                "textCharacters": sum(int(row["characters"]) for row in page_records),
                "pagesWithoutText": [row["page"] for row in page_records if row["characters"] == 0],
                "flaggedPages": [row for row in page_records if row["flags"]],
                "markdown": str(md_path.relative_to(ROOT)).replace("\\", "/"),
            }
        )

    manifest_path = INDEX_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"files": len(manifest), "pages": sum(int(row["pages"]) for row in manifest), "manifest": str(manifest_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
