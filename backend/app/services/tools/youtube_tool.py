import os
import requests

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def search_youtube_video(query: str) -> str | None:
    if not YOUTUBE_API_KEY:
        return None

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": query,
        "maxResults": 1,
        "type": "video",
        "key": YOUTUBE_API_KEY,
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        items = data.get("items")
        if not items:
            return None

        video_id = items[0]["id"]["videoId"]
        return f"https://www.youtube.com/watch?v={video_id}"

    except Exception:
        return None