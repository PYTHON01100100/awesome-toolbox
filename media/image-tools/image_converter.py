"""
Batch convert HEIC/HEIF pictures (and other images) to PNG, JPG, WEBP, etc.

Usage:
    python image_converter.py                        # asks everything
    python image_converter.py <folder>               # asks format
    python image_converter.py <folder> jpg           # no prompts

Requires:  pip install pillow pillow-heif
"""
import sys
from pathlib import Path

from PIL import Image, ImageOps
import pillow_heif

# Enable HEIC support
pillow_heif.register_heif_opener()

INPUT_EXTS = {".heic", ".heif", ".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif", ".gif"}

# choice -> (extension, Pillow format name)
FORMATS = {
    "1": ("png", "PNG"),
    "2": ("jpg", "JPEG"),
    "3": ("webp", "WEBP"),
    "4": ("bmp", "BMP"),
    "5": ("tiff", "TIFF"),
    "6": ("gif", "GIF"),
    "7": ("pdf", "PDF"),
}

# Formats that can't store transparency
NO_ALPHA = {"JPEG", "BMP", "PDF"}


def choose_format(arg=None):
    if arg:
        arg = arg.lower().lstrip(".").replace("jpeg", "jpg")
        for key, (ext, _) in FORMATS.items():
            if ext == arg:
                return FORMATS[key]
        print(f"Unknown format '{arg}'.")

    print("\nConvert to:")
    for key, (ext, _) in FORMATS.items():
        print(f"  {key}) {ext.upper()}")
    while True:
        choice = input("Enter number (1-7): ").strip()
        if choice in FORMATS:
            return FORMATS[choice]
        print("Invalid choice, try again.")


def main():
    raw = sys.argv[1] if len(sys.argv) > 1 else input("Pictures folder (Enter = this folder): ")
    source = Path(raw.strip().strip('"')) if raw.strip() else Path(__file__).parent
    if not source.is_dir():
        print(f"Folder not found: {source}")
        return

    ext, pil_format = choose_format(sys.argv[2] if len(sys.argv) > 2 else None)

    if len(sys.argv) > 2:
        only_heic = True
    else:
        only_heic = input("Only HEIC/HEIF files? (Y/n): ").strip().lower() != "n"

    allowed = {".heic", ".heif"} if only_heic else INPUT_EXTS
    files = sorted(
        p for p in source.iterdir()
        if p.is_file() and p.suffix.lower() in allowed and p.suffix.lower() != f".{ext}"
    )
    if not files:
        print("No matching pictures found.")
        return

    # Dedicated output folder inside the pictures folder
    output_dir = source / f"Converted_{ext.upper()}"
    output_dir.mkdir(exist_ok=True)

    total = len(files)
    done = 0
    for i, file in enumerate(files, start=1):
        out_file = output_dir / f"{file.stem}.{ext}"
        print(f"[{i}/{total}] {file.name} -> {out_file.name}")
        try:
            with Image.open(file) as img:
                img = ImageOps.exif_transpose(img)  # keep correct rotation

                if pil_format in NO_ALPHA and img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGBA")
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                elif img.mode not in ("RGB", "RGBA", "L"):
                    img = img.convert("RGB")

                options = {}
                if pil_format in ("JPEG", "WEBP"):
                    options["quality"] = 95
                if "exif" in img.info and pil_format in ("JPEG", "WEBP", "PNG", "TIFF"):
                    options["exif"] = img.info["exif"]

                img.save(out_file, format=pil_format, **options)
            print("  OK")
            done += 1
        except Exception as e:
            print(f"  Failed: {e}")

    print(f"\nDone! {done}/{total} converted to: {output_dir}")


if __name__ == "__main__":
    main()
