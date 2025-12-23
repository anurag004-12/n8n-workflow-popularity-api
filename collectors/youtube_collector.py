import os
import logging
from googleapiclient.discovery import build

def get_youtube_client():
    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        raise RuntimeError(
            "YOUTUBE_API_KEY not set. Please set it as an environment variable."
        )

    return build(
        "youtube",
        "v3",
        developerKey=api_key,
        cache_discovery=False
    )

def fetch_youtube_workflows(query, country, max_results=25):
    youtube = get_youtube_client()
    results = []

    search_response = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=max_results,
        regionCode=country,
        type="video"
    ).execute()

    video_ids = [
        item["id"]["videoId"]
        for item in search_response.get("items", [])
    ]

    if not video_ids:
        return results

    stats_response = youtube.videos().list(
        part="statistics,snippet",
        id=",".join(video_ids)
    ).execute()

    for item in stats_response.get("items", []):
        stats = item.get("statistics", {})

        views = int(stats.get("viewCount", 0))
        likes = int(stats.get("likeCount", 0))
        comments = int(stats.get("commentCount", 0))

        results.append({
            "workflow": item["snippet"]["title"],
            "platform": "YouTube",
            "country": country,
            "popularity_metrics": {
                "views": views,
                "likes": likes,
                "comments": comments,
                "like_to_view_ratio": round(likes / views, 4) if views else 0,
                "comment_to_view_ratio": round(comments / views, 4) if views else 0
            },
            "popularity_score": views + (likes * 2) + (comments * 3),
            "evidence_source": "YouTube Data API v3"
        })

    return results
