from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source_render" / "lecture_notes_2026" / "260804_03" / "p041.jpg"
OUTPUT = ROOT / "site" / "assets" / "questions"

CROPS = {
    "gendev2-05-2026-practice-q001-01.jpg": (45, 410, 360, 575),
    "gendev2-05-2026-practice-q001-02.jpg": (360, 400, 620, 650),
    "gendev2-05-2026-practice-q002-01.jpg": (740, 440, 1015, 725),
}


def main() -> None:
    image = Image.open(SOURCE)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for filename, box in CROPS.items():
        crop = image.crop(box)
        crop.save(OUTPUT / filename, "JPEG", quality=92, optimize=True)
    print(f"LECTURE_PRACTICE_ASSETS_CREATED count={len(CROPS)} source={image.size}")


if __name__ == "__main__":
    main()
