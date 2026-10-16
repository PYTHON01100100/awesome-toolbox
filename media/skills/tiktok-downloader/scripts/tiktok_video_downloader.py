"""
TikTok video downloader with resolution choice (240p - 4K).

Works with a single video link or a whole profile (https://www.tiktok.com/@user).

Usage:
    python tiktok_video_downloader.py                     # asks for URL and quality
    python tiktok_video_downloader.py <url>               # asks for quality
    python tiktok_video_downloader.py <url> 1080          # no prompts

Requires:  pip install -U yt-dlp
Optional:  ffmpeg on PATH (or: pip install imageio-ffmpeg)
"""
import re
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

# Save downloads in the current working directory
output_dir = Path.cwd() / "TikTok_Downloads"


def find_ffmpeg():
    path = shutil.which("ffmpeg")
    if path:
        return path
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return None


def is_profile_url(url):
    # https://www.tiktok.com/@user  (no /video/ part)
    return bool(re.search(r"tiktok\.com/@[^/?]+/?(\?|$)", url))


def get_available_heights(url):
    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
        info = ydl.extract_info(url, download=False)

    heights = {
        f["height"]
        for f in info.get("formats", [])
        if f.get("height") and f.get("vcodec") != "none"
    }
    title = info.get("title") or info.get("description") or "video"
    return title[:80], sorted(heights)


def choose_resolution(available):
    print("\nChoose resolution:")
    for key, (label, height) in RESOLUTIONS.items():
        mark = "  [available]" if height in available else ""
        print(f"  {key}) {label}{mark}")

    while True:
        choice = input("Enter number (1-7): ").strip()
        if choice in RESOLUTIONS:
            return RESOLUTIONS[choice][1]
        print("Invalid choice, try again.")


def download(url, height, ffmpeg):
    output_dir.mkdir(exist_ok=True)

    # TikTok usually serves video+audio in one file; the merge option is a fallback
    if ffmpeg:
        fmt = (
            f"best[height<={height}][acodec!=none]/"
            f"bestvideo[height<={height}]+bestaudio/"
            f"best[height<={height}]/best"
        )
    else:
        fmt = f"best[height<={height}][acodec!=none]/best[height<={height}]/best"

    opts = {
        "format": fmt,
        "outtmpl": str(output_dir / "%(uploader)s" / "%(id)s_%(height)sp.%(ext)s"),
        "merge_output_format": "mp4",
        "ignoreerrors": True,  # keep going if one video of a profile fails
        "download_archive": str(output_dir / "downloaded.txt"),  # skip already-downloaded videos
    }
    if ffmpeg:
        opts["ffmpeg_location"] = ffmpeg

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else input("Paste TikTok URL (video or profile): ").strip()
    if not url:
        print("No URL given.")
        return

    ffmpeg = find_ffmpeg()
    profile = is_profile_url(url)
    available = []

    if profile:
        print("\nProfile link detected -> all videos will be downloaded.")
    else:
        print("\nFetching video info...")
        try:
            title, available = get_available_heights(url)
        except Exception as e:
            print(f"Failed to read video info: {e}")
            print("(Photo slideshows are not supported - use a video link.)")
            return
        print(f"Title: {title}")
        print(f"Available heights: {', '.join(f'{h}p' for h in available) or 'unknown'}")

    if len(sys.argv) > 2:
        height = int(sys.argv[2].lower().replace("4k", "2160").rstrip("p"))
    else:
        height = choose_resolution(available)

    # If chosen quality doesn't exist, fall back to the closest lower one
    if available and height not in available:
        lower = [h for h in available if h <= height]
        actual = max(lower) if lower else min(available)
        print(f"\n{height}p not available for this video -> using {actual}p")
        height = actual

    print(f"\nDownloading at up to {height}p ...\n")
    try:
        download(url, height, ffmpeg)
    except Exception as e:
        print(f"Download failed: {e}")
        return

    print(f"\nDone! Saved to: {output_dir}")


if __name__ == "__main__":
    main()
