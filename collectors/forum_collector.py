import requests

DISCOURSE_BASE_URL = "https://community.n8n.io"
REQUEST_TIMEOUT_SECONDS = 15


def fetch_forum_workflows(limit=50):
    response = requests.get(
        f"{DISCOURSE_BASE_URL}/latest.json",
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    data = response.json()

    results = []
    topics = data.get("topic_list", {}).get("topics", [])

    for topic in topics[:limit]:
        views = int(topic.get("views", 0))
        replies = int(topic.get("reply_count", 0))
        likes = int(topic.get("like_count", 0))
        contributors = int(topic.get("participant_count", 0))

        results.append({
            "workflow": topic.get("title", "Untitled forum topic"),
            "platform": "Forum",
            "country": "Global",
            "popularity_metrics": {
                "replies": replies,
                "likes": likes,
                "contributors": contributors,
                "views": views,
            },
            "popularity_score": views * 0.3 + replies * 4 + likes * 5,
            "evidence_source": "Discourse API (n8n Forum)",
        })

    return results
