---
name: instagram-downloader
description: Download Instagram content - posts, reels, photos, carousels, stories, highlights, all posts of a profile, and HD profile pictures. Use when the user shares an instagram.com link or asks to save someone's Instagram stories, reels, photos or posts.
---

# Instagram Downloader

Downloads Instagram media using `scripts/instagram_downloader.py` (in this skill's base directory). Output goes to `Instagram_Downloads/<username>/` in the current working directory.

## Requirements
- `pip install -U instaloader`

## Post, reel or carousel links (no login needed) - run it yourself
```
python "<skill-dir>/scripts/instagram_downloader.py" "<post-or-reel-url>"
```
Works for `/p/...`, `/reel/...`, `/reels/...` and `/tv/...` links on public accounts. Carousels download every photo and video in the post.

## Stories, highlights, whole profiles, profile pictures - the user runs it
These use an interactive menu, and stories/highlights require logging in with the user's own Instagram account (password is typed hidden). You cannot answer those prompts, so tell the user to run this in their own terminal (in Claude Code they can type it with a leading `!`):

```
python "<skill-dir>/scripts/instagram_downloader.py"
```

Menu options:
1. Post / Reel / Carousel (by link)
2. Stories of a user - login required
3. Highlights of a user - login required
4. All posts of a profile (can limit how many)
5. Profile picture (HD)
6. Log in

A story link (`instagram.com/stories/<user>/...`) passed as an argument also triggers the login prompt, so hand that case to the user as well.

## Notes to tell the user when relevant
- Instagram only serves stories to logged-in users; there is no way around that. The login is saved after the first time.
- Private accounts only work if the logged-in account follows them.
- Downloading a lot quickly can get the account rate-limited or temporarily blocked.
- Only download content the user has the right to save.
