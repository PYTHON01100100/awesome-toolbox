"""
Extract audio from videos (one file or a whole folder).

Usage:
    python audio_extractor.py                         # asks everything
    python audio_extractor.py <file-or-folder>        # asks format
    python audio_extractor.py <file-or-folder> mp3    # no prompts

Requires:  ffmpeg on PATH, or:  pip install imageio-ffmpeg
"""
import shutil
import subprocess
import sys
from pathlib import Path

VIDEO_EXTS = {".mp4", ".mkv", ".mov", ".avi", ".webm", ".flv", ".wmv", ".m4v", ".3gp", ".ts", ".mpeg", ".mpg"}

# format -> (extension, ffmpeg codec args)
FORMATS = {
    "1": ("mp3",  ["-c:a", "libmp3lame", "-b:a", "320k"]),
    "2": ("m4a",  ["-c:a", "aac", "-b:a", "256k"]),
    "3": ("wav",  ["-c:a", "pcm_s16le"]),
    "4": ("flac", ["-c:a", "flac"]),
    "5": ("ogg",  ["-c:a", "libvorbis", "-q:a", "8"]),
    "6": ("opus", ["-c:a", "libopus", "-b:a", "192k"]),
}

# Save next to this script
output_dir = Path(__file__).parent / "Extracted_Audio"


def find_ffmpeg():
    path = shutil.which("ffmpeg")
    if path:
        return path
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return None


def collect_videos(source):
    if source.is_file():
        return [source]
    return sorted(p for p in source.rglob("*") if p.suffix.lower() in VIDEO_EXTS)


def choose_format(arg=None):
    if arg:
        for key, (ext, _) in FORMATS.items():
            if ext == arg.lower().lstrip("."):
                return FORMATS[key]
        print(f"Unknown format '{arg}'.")

    print("\nChoose audio format:")
    for key, (ext, _) in FORMATS.items():
        print(f"  {key}) {ext}")
    while True:
        choice = input("Enter number (1-6): ").strip()
        if choice in FORMATS:
            return FORMATS[choice]
        print("Invalid choice, try again.")


def main():
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        print("ffmpeg not found. Run:  pip install imageio-ffmpeg")
        return

    raw = sys.argv[1] if len(sys.argv) > 1 else input("Video file or folder (Enter = this folder): ")
    source = Path(raw.strip().strip('"')) if raw.strip() else Path(__file__).parent
    if not source.exists():
        print(f"Not found: {source}")
        return

    videos = collect_videos(source)
    if not videos:
        print("No video files found.")
        return

    ext, codec_args = choose_format(sys.argv[2] if len(sys.argv) > 2 else None)
    output_dir.mkdir(exist_ok=True)

    total = len(videos)
    done = 0
    for i, video in enumerate(videos, start=1):
        out_file = output_dir / f"{video.stem}.{ext}"
        print(f"[{i}/{total}] {video.name} -> {out_file.name}")

        cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
               "-i", str(video), "-vn", *codec_args, str(out_file)]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")

        if result.returncode == 0:
            print("  OK")
            done += 1
        else:
            print(f"  Failed: {result.stderr.strip().splitlines()[-1] if result.stderr.strip() else 'no audio track?'}")

    print(f"\nDone! {done}/{total} extracted to: {output_dir}")


if __name__ == "__main__":
    main()
