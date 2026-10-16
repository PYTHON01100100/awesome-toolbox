---
name: audio-extractor
description: Extract the audio track from a video file or every video in a folder, saving as MP3, M4A, WAV, FLAC, OGG or OPUS. Use when the user wants audio, music or sound taken out of videos, or wants to convert a video to MP3.
---

# Audio Extractor

Extracts audio from videos using `scripts/audio_extractor.py` (in this skill's base directory).

## Requirements
- ffmpeg on PATH, or `pip install imageio-ffmpeg`

## How to run
Always pass both the source and the format, so the script does not stop to ask questions:

```
python "<skill-dir>/scripts/audio_extractor.py" "<video-file-or-folder>" <format>
```

- `<video-file-or-folder>`: one video, or a folder (searched including its subfolders). Supported inputs: mp4, mkv, mov, avi, webm, flv, wmv, m4v, 3gp, ts, mpeg, mpg.
- `<format>`: `mp3` (320k), `m4a` (AAC 256k), `wav`, `flac`, `ogg` or `opus`. Default to `mp3` if the user didn't say.
- Output goes to `Extracted_Audio/` in the current working directory, so run it from where the user wants the files. Existing files with the same name are overwritten.
- Videos with no audio track are reported as failed; the rest continue.
