import json
from collectors.youtube_collector import fetch_youtube_workflows
from collectors.forum_collector import fetch_forum_workflows
from collectors.trends_collector import fetch_trends

def run():
    results = []

    yt_queries = [
        "n8n slack automation",
        "n8n gmail workflow",
        "n8n whatsapp automation"
    ]

    for q in yt_queries:
        results.extend(fetch_youtube_workflows(q, "US"))
        results.extend(fetch_youtube_workflows(q, "IN"))

    results.extend(fetch_forum_workflows())

    trends_keywords = [
        "n8n slack integration",
        "n8n google sheets automation"
    ]

    for kw in trends_keywords:
        for country in ["US", "IN"]:
            trend = fetch_trends(kw, country)
            if trend:
                results.append(trend)

    with open("data/workflows.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run()
