---
name: x-video-downloader
description: Download videos from X (Twitter) posts at a chosen resolution from 240p up to 4K. Use when the user shares an x.com or twitter.com link and wants the video saved, or asks to download a tweet's video in a specific quality.
---

# X (Twitter) Video Downloader

Downloads the video from an X/Twitter post using `scripts/x_video_downloader.py` (in this skill's base directory).

## Requirements
- `pip install -U yt-dlp`
- ffmpeg on PATH, or `pip install imageio-ffmpeg` (needed to merge separate video/audio streams for the best quality)

## How to run
Always pass both the URL and the resolution, so the script does not stop to ask questions:

```
python "<skill-dir>/scripts/x_video_downloader.py" "<post-url>" <height>
```

- `<height>`: one of `240`, `360`, `480`, `720`, `1080`, `1440`, `2160` (or `4k`).
- If the user didn't say a quality, use `1080`.
- If the requested quality doesn't exist, the script automatically uses the closest lower one and says so.
- Run it from the folder where the user wants the file; output goes to `X_Downloads/` in the current working directory.

## Notes to tell the user when relevant
- Most X videos top out at 720p or 1080p; real 4K is rare.
- Age-restricted or private posts may fail because no login is used.
- A post with several videos downloads all of them.
