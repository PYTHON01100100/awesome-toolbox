"""
X (Twitter) video downloader with resolution choice (240p - 4K).

Usage:
    python x_video_downloader.py                      # asks for URL and quality
    python x_video_downloader.py <url>                # asks for quality
    python x_video_downloader.py <url> 1080           # no prompts

Requires:  pip install -U yt-dlp
Optional:  ffmpeg on PATH (or: pip install imageio-ffmpeg) to merge
           separate video/audio streams for the best quality.
"""
import shutil
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("yt-dlp is not installed. Run:  pip install -U yt-dlp")
    sys.exit(1)

RESOLUTIONS = {
    "1": ("240p", 240),
    "2": ("360p", 360),
    "3": ("480p", 480),
    "4": ("720p (HD)", 720),
    "5": ("1080p (Full HD)", 1080),
    "6": ("1440p (2K)", 1440),
    "7": ("2160p (4K)", 2160),
}

# Save downloads next to this script
output_dir = Path(__file__).parent / "X_Downloads"


def find_ffmpeg():
    path = shutil.which("ffmpeg")
    if path:
        return path
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return None


def get_available_heights(url):
    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
        info = ydl.extract_info(url, download=False)

    # A post can hold several videos; check the first one
    if info.get("_type") == "playlist" and info.get("entries"):
        info = info["entries"][0]

    heights = {
        f["height"]
        for f in info.get("formats", [])
        if f.get("height") and f.get("vcodec") != "none"
    }
    return info.get("title", "video"), sorted(heights)


def choose_resolution(available):
    print("\nChoose resolution:")
    for key, (label, height) in RESOLUTIONS.items():
        mark = "  ✓ available" if height in available else ""
        print(f"  {key}) {label}{mark}")

    while True:
        choice = input("Enter number (1-7): ").strip()
        if choice in RESOLUTIONS:
            return RESOLUTIONS[choice][1]
        print("Invalid choice, try again.")


def download(url, height, ffmpeg):
    output_dir.mkdir(exist_ok=True)

    if ffmpeg:
        # Best video up to chosen height + best audio, merged to mp4
        fmt = (
            f"bestvideo[height<={height}]+bestaudio/"
            f"best[height<={height}]/best"
        )
    else:
        # No ffmpeg: only formats that already contain video + audio
        fmt = f"best[height<={height}][acodec!=none]/best[height<={height}]/best"

    opts = {
        "format": fmt,
        "outtmpl": str(output_dir / "%(uploader_id)s_%(id)s_%(height)sp.%(ext)s"),
        "merge_output_format": "mp4",
        "noplaylist": False,
    }
    if ffmpeg:
        opts["ffmpeg_location"] = ffmpeg

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else input("Paste X/Twitter video URL: ").strip()
    if not url:
        print("No URL given.")
        return

    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        print("Note: ffmpeg not found - quality may be limited. "
              "Fix with:  pip install imageio-ffmpeg")

    print("\nFetching video info...")
    try:
        title, available = get_available_heights(url)
    except Exception as e:
        print(f"Failed to read video info: {e}")
        return

    print(f"Title: {title}")
    print(f"Available heights: {', '.join(f'{h}p' for h in available) or 'unknown'}")

    if len(sys.argv) > 2:
        height = int(sys.argv[2].lower().rstrip("p").replace("4k", "2160"))
    else:
        height = choose_resolution(available)

    # If chosen quality doesn't exist, fall back to the closest lower one
    if available and height not in available:
        lower = [h for h in available if h <= height]
        actual = max(lower) if lower else min(available)
        print(f"\n{height}p not available for this video -> using {actual}p")
        height = actual

    print(f"\nDownloading at {height}p ...\n")
    try:
        download(url, height, ffmpeg)
    except Exception as e:
        print(f"Download failed: {e}")
        return

    print(f"\nDone! Saved to: {output_dir}")


if __name__ == "__main__":
    main()
