from pathlib import Path
from PIL import Image
import pillow_heif

# Enable HEIC support
pillow_heif.register_heif_opener()

# Current folder where script is located
root_dir = Path(__file__).parent

# Find all HEIC files
heic_files = list(root_dir.glob("*.heic")) + list(root_dir.glob("*.HEIC"))

if not heic_files:
    print("No HEIC files found.")
    exit()

total = len(heic_files)

for i, heic_file in enumerate(heic_files, start=1):
    print(f"[{i}/{total}] Converting {heic_file.name}")
    try:
        img = Image.open(heic_file)

        output_file = heic_file.with_suffix(".png")

        img.save(output_file, format="PNG")
        print(f"  ✓ {output_file.name}")

    except Exception as e:
        print(f"Failed: {heic_file.name}")
        print(e)

print("\nDone!")