---
name: image-converter
description: Batch convert a folder of HEIC/HEIF photos (iPhone pictures) to PNG, JPG, WEBP, BMP, TIFF, GIF or PDF into a dedicated output folder. Use when the user wants to convert HEIC photos or change the format of many pictures at once.
---

# Image Converter

Batch converts pictures using `scripts/image_converter.py` (in this skill's base directory).

## Requirements
- `pip install pillow pillow-heif`

## How to run
Pass both the folder and the format, so the script does not stop to ask questions:

```
python "<skill-dir>/scripts/image_converter.py" "<pictures-folder>" <format>
```

- `<format>`: `png`, `jpg`, `webp`, `bmp`, `tiff`, `gif` or `pdf`. Default to `png` if the user didn't say.
- With both arguments, only **HEIC/HEIF** files are converted.
- Results go to a new folder inside the pictures folder named `Converted_<FORMAT>` (e.g. `Converted_JPG`). Originals are never changed.
- Only the folder itself is scanned, not its subfolders.

## Converting other image types too
To also convert JPG/PNG/WEBP/BMP/TIFF/GIF files (not just HEIC), the script must be run with only the folder argument and the user answers `n` to "Only HEIC/HEIF files?". Since that needs typing, ask the user to run it in their terminal (in Claude Code: prefix with `!`):

```
python "<skill-dir>/scripts/image_converter.py" "<pictures-folder>"
```

## Behaviour
- Keeps correct photo rotation and camera EXIF data.
- Transparency becomes a white background in formats that can't store it (JPG, BMP, PDF).
- JPG and WEBP are saved at quality 95.
