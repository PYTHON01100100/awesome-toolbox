from pathlib import Path
from yt_dlp import YoutubeDL

APP_NAME = "Pyutube Downloader"
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)


QUALITY_MAP = {
    "1": ("2160p / 4K", "bestvideo[height<=2160]+bestaudio/best"),
    "2": ("1440p / 2K", "bestvideo[height<=1440]+bestaudio/best"),
    "3": ("1080p / Full HD", "bestvideo[height<=1080]+bestaudio/best"),
    "4": ("720p / HD", "bestvideo[height<=720]+bestaudio/best"),
    "5": ("480p", "bestvideo[height<=480]+bestaudio/best"),
    "6": ("Best available", "bestvideo+bestaudio/best"),
}


def choose_quality():
    print("\nChoose video quality:")
    for key, value in QUALITY_MAP.items():
        print(f"{key}. {value[0]}")

    choice = input("\nQuality: ").strip()
    return QUALITY_MAP.get(choice, QUALITY_MAP["6"])


def get_common_options(output_template, playlist=True):
    return {
        "outtmpl": str(output_template),
        "noplaylist": not playlist,
        "ignoreerrors": True,
        "quiet": False,
        "no_warnings": False,
        "restrictfilenames": False,
        "windowsfilenames": True,
        "merge_output_format": "mp4",
    }


def download_video(url, playlist=False):
    quality_name, quality_format = choose_quality()

    if playlist:
        output_template = DOWNLOAD_DIR / "%(playlist_title)s" / "%(playlist_index)03d - %(title)s.%(ext)s"
    else:
        output_template = DOWNLOAD_DIR / "%(title)s.%(ext)s"

    options = get_common_options(output_template, playlist=playlist)
    options.update({
        "format": quality_format,
    })

    print(f"\nDownloading video: {quality_name}")
    print("Video and audio will be merged automatically using FFmpeg.")

    with YoutubeDL(options) as ydl:
        ydl.download([url])


def download_audio(url, playlist=False):
    if playlist:
        output_template = DOWNLOAD_DIR / "%(playlist_title)s" / "%(playlist_index)03d - %(title)s.%(ext)s"
    else:
        output_template = DOWNLOAD_DIR / "%(title)s.%(ext)s"

    options = get_common_options(output_template, playlist=playlist)
    options.update({
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ],
    })

    print("\nDownloading audio as MP3 320kbps...")

    with YoutubeDL(options) as ydl:
        ydl.download([url])


def download_thumbnail(url, playlist=False):
    if playlist:
        output_template = DOWNLOAD_DIR / "%(playlist_title)s" / "%(playlist_index)03d - %(title)s.%(ext)s"
    else:
        output_template = DOWNLOAD_DIR / "%(title)s.%(ext)s"

    options = get_common_options(output_template, playlist=playlist)
    options.update({
        "skip_download": True,
        "writethumbnail": True,
    })

    print("\nDownloading thumbnail...")

    with YoutubeDL(options) as ydl:
        ydl.download([url])


def download_subtitles(url, playlist=False):
    if playlist:
        output_template = DOWNLOAD_DIR / "%(playlist_title)s" / "%(playlist_index)03d - %(title)s.%(ext)s"
    else:
        output_template = DOWNLOAD_DIR / "%(title)s.%(ext)s"

    options = get_common_options(output_template, playlist=playlist)
    options.update({
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en", "ar"],
        "subtitlesformat": "srt/best",
    })

    print("\nDownloading subtitles if available...")

    with YoutubeDL(options) as ydl:
        ydl.download([url])


def show_menu():
    print("\n" + "=" * 50)
    print(APP_NAME)
    print("=" * 50)
    print("1. Download single video")
    print("2. Download single audio MP3")
    print("3. Download playlist videos")
    print("4. Download playlist audios MP3")
    print("5. Download thumbnail")
    print("6. Download subtitles")
    print("7. Exit")


def main():
    while True:
        show_menu()

        choice = input("\nChoose option: ").strip()

        if choice == "7":
            print("Goodbye!")
            break

        url = input("\nEnter YouTube URL: ").strip()

        if not url:
            print("Invalid URL.")
            continue

        try:
            if choice == "1":
                download_video(url, playlist=False)

            elif choice == "2":
                download_audio(url, playlist=False)

            elif choice == "3":
                download_video(url, playlist=True)

            elif choice == "4":
                download_audio(url, playlist=True)

            elif choice == "5":
                playlist_choice = input("Is this a playlist? y/n: ").strip().lower()
                download_thumbnail(url, playlist=playlist_choice == "y")

            elif choice == "6":
                playlist_choice = input("Is this a playlist? y/n: ").strip().lower()
                download_subtitles(url, playlist=playlist_choice == "y")

            else:
                print("Invalid option.")
                continue

            print("\n✅ Done!")
            print(f"Saved in: {DOWNLOAD_DIR.resolve()}")

        except Exception as error:
            print("\n❌ Error happened:")
            print(error)


if __name__ == "__main__":
    main()