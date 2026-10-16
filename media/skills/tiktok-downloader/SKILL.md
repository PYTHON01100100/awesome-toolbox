---
name: tiktok-downloader
description: Download TikTok videos at a chosen resolution (240p to 4K), either a single video or every video on a profile. Use when the user shares a tiktok.com link or asks to save TikTok videos or a TikTok account's videos.
---

# TikTok Video Downloader

Downloads TikTok videos using `scripts/tiktok_video_downloader.py` (in this skill's base directory).

## Requirements
- `pip install -U yt-dlp`
- Optional: ffmpeg on PATH, or `pip install imageio-ffmpeg`

## How to run
Always pass both the URL and the resolution, so the script does not stop to ask questions:

```
python "<skill-dir>/scripts/tiktok_video_downloader.py" "<url>" <height>
```

- `<url>`: a video link (`https://www.tiktok.com/@user/video/123...`) or a profile link (`https://www.tiktok.com/@user`) to download all of that account's videos.
- `<height>`: `240`, `360`, `480`, `720`, `1080`, `1440`, `2160` (or `4k`). Default to `1080` if the user didn't say.
- Run it from the folder where the user wants the files; output goes to `TikTok_Downloads/<uploader>/` in the current working directory.
- Already-downloaded videos are recorded in `TikTok_Downloads/downloaded.txt` and skipped next time, so re-running on a profile only fetches new videos.

## Limits
- Photo slideshow posts are not supported, only videos.
- Most TikTok videos max out at 1080p.
- Downloading a large profile can take a long time; for a profile, run the command in the background.
