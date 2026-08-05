#!/usr/bin/env python3
"""Render selected private lecture-note PDF pages to JPEG for visual verification."""

from __future__ import annotations

import argparse
from pathlib import Path

import pypdfium2 as pdfium


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "data" / "lecture_notes_2026"
RENDER_DIR = ROOT / "source_render" / "lecture_notes_2026"


def parse_pages(spec: str) -> list[int]:
    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = (int(value) for value in part.split("-", 1))
            pages.update(range(start, end + 1))
        else:
            pages.add(int(part))
    return sorted(pages)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("slug", help="Filename prefix such as 260803_03")
    parser.add_argument("pages", help="1-based pages, e.g. 4,19-20,32")
    parser.add_argument("--scale", type=float, default=1.6)
    args = parser.parse_args()

    matches = list(SOURCE_DIR.glob(f"*{args.slug}*.pdf"))
    if len(matches) != 1:
        raise SystemExit(f"{args.slug}: PDF 1개가 필요하지만 {len(matches)}개입니다.")
    document = pdfium.PdfDocument(matches[0])
    output_dir = RENDER_DIR / args.slug
    output_dir.mkdir(parents=True, exist_ok=True)

    rendered: list[str] = []
    for page_number in parse_pages(args.pages):
        if not 1 <= page_number <= len(document):
            raise SystemExit(f"범위를 벗어난 페이지: {page_number}/{len(document)}")
        bitmap = document[page_number - 1].render(scale=args.scale)
        image = bitmap.to_pil()
        output_path = output_dir / f"p{page_number:03d}.jpg"
        image.save(output_path, "JPEG", quality=90, optimize=True)
        rendered.append(str(output_path.relative_to(ROOT)).replace("\\", "/"))
    print(f"RENDERED {len(rendered)} pages: {', '.join(rendered)}")


if __name__ == "__main__":
    main()
