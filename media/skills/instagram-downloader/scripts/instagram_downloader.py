"""
Instagram downloader - stories, highlights, posts, reels, photos, carousels,
profile pictures.

Usage:
    python instagram_downloader.py              # interactive menu
    python instagram_downloader.py <url>        # post / reel / story link

Requires:  pip install -U instaloader

Stories and highlights need you to log in with your own Instagram account
(Instagram's rule). Your session is saved, so you only log in once.
Only download content you are allowed to; private accounts must follow you.
"""
import re
import sys
from getpass import getpass
from pathlib import Path

try:
    import instaloader
    from instaloader import Post, Profile
    from instaloader.exceptions import (
        BadCredentialsException,
        TwoFactorAuthRequiredException,
    )
except ImportError:
    print("instaloader is not installed. Run:  pip install -U instaloader")
    sys.exit(1)

# Save downloads in the current working directory
output_dir = Path.cwd() / "Instagram_Downloads"

L = instaloader.Instaloader(
    dirname_pattern=str(output_dir / "{target}"),
    filename_pattern="{date_utc:%Y-%m-%d_%H-%M-%S}_{shortcode}",
    download_video_thumbnails=False,
    save_metadata=False,
    compress_json=False,
    post_metadata_txt_pattern="",
    storyitem_metadata_txt_pattern="",
)
logged_in = False


def login():
    global logged_in
    if logged_in:
        return True

    username = input("Instagram username (for login): ").strip().lstrip("@")
    if not username:
        return False

    # Reuse a saved session if there is one
    try:
        L.load_session_from_file(username)
        logged_in = True
        print(f"OK - Logged in as {username} (saved session)")
        return True
    except FileNotFoundError:
        pass

    password = getpass("Password (hidden): ")
    try:
        L.login(username, password)
    except TwoFactorAuthRequiredException:
        code = input("2FA code: ").strip()
        L.two_factor_login(code)
    except BadCredentialsException:
        print("Wrong username or password.")
        return False
    except Exception as e:
        print(f"Login failed: {e}")
        return False

    L.save_session_to_file()
    logged_in = True
    print(f"OK - Logged in as {username} (session saved)")
    return True


def get_profile(username):
    return Profile.from_username(L.context, username.strip().lstrip("@"))


def download_post_url(url):
    match = re.search(r"instagram\.com/(?:[^/]+/)?(?:p|reel|reels|tv)/([^/?#]+)", url)
    if not match:
        print("Could not find a post/reel code in that link.")
        return
    post = Post.from_shortcode(L.context, match.group(1))
    print(f"Downloading post by @{post.owner_username} "
          f"({post.mediacount} item{'s' if post.mediacount > 1 else ''})...")
    L.download_post(post, target=post.owner_username)


def download_stories(username):
    if not login():
        return
    profile = get_profile(username)
    print(f"Downloading current stories of @{profile.username}...")
    L.download_stories(
        userids=[profile.userid],
        filename_target=f"{profile.username}_stories",
    )


def download_highlights(username):
    if not login():
        return
    profile = get_profile(username)
    print(f"Downloading highlights of @{profile.username}...")
    L.download_highlights(profile, filename_target=f"{profile.username}_highlights")


def download_all_posts(username, limit=None):
    profile = get_profile(username)
    if profile.is_private and not logged_in:
        print("This account is private - log in with an account that follows it.")
        if not login():
            return
        profile = get_profile(username)

    total = limit or profile.mediacount
    print(f"Downloading {total} posts from @{profile.username}...")
    for i, post in enumerate(profile.get_posts(), start=1):
        if limit and i > limit:
            break
        print(f"[{i}/{total}]", end=" ")
        try:
            L.download_post(post, target=profile.username)
        except Exception as e:
            print(f"skipped: {e}")


def download_profile_pic(username):
    profile = get_profile(username)
    L.download_profilepic(profile)


def handle_url(url):
    story = re.search(r"instagram\.com/stories/([^/?#]+)", url)
    if story and story.group(1) != "highlights":
        download_stories(story.group(1))
    else:
        download_post_url(url)


def menu():
    while True:
        print("\n=== Instagram Downloader ===")
        print("  1) Post / Reel / Carousel (by link)")
        print("  2) Stories of a user           [login]")
        print("  3) Highlights of a user        [login]")
        print("  4) All posts of a profile")
        print("  5) Profile picture (HD)")
        print("  6) Log in")
        print("  0) Exit")
        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                handle_url(input("Paste link: ").strip())
            elif choice == "2":
                download_stories(input("Username: "))
            elif choice == "3":
                download_highlights(input("Username: "))
            elif choice == "4":
                username = input("Username: ")
                n = input("How many posts? (Enter = all): ").strip()
                download_all_posts(username, int(n) if n.isdigit() else None)
            elif choice == "5":
                download_profile_pic(input("Username: "))
            elif choice == "6":
                login()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
                continue
            print(f"\nDone! Saved to: {output_dir}")
        except KeyboardInterrupt:
            print("\nCancelled.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            handle_url(sys.argv[1])
            print(f"\nDone! Saved to: {output_dir}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        menu()
