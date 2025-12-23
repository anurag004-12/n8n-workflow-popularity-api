import requests

DISCOURSE_BASE_URL = "https://community.n8n.io"

def fetch_forum_workflows(limit=50):
    response = requests.get(f"{DISCOURSE_BASE_URL}/latest.json")
    data = response.json()

    results = []

    for topic in data["topic_list"]["topics"][:limit]:
        results.append({
            "workflow": topic["title"],
            "platform": "Forum",
            "country": "Global",
            "popularity_metrics": {
                "replies": topic["reply_count"],
                "likes": topic.get("like_count", 0),
                "contributors": topic.get("participant_count", 0),
                "views": topic["views"]
            },
            "popularity_score": (
                topic["views"] * 0.3 +
                topic["reply_count"] * 4 +
                topic.get("like_count", 0) * 5
            ),
            "evidence_source": "Discourse API (n8n Forum)"
        })

    return results
