import json
import logging

from config import DATA_DIR, DATA_FILE
from collectors.youtube_collector import fetch_youtube_workflows
from collectors.forum_collector import fetch_forum_workflows
from collectors.trends_collector import fetch_trends

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run():
    results = []

    yt_queries = [
        "n8n slack automation",
        "n8n gmail workflow",
        "n8n whatsapp automation"
    ]

    for q in yt_queries:
        try:
            results.extend(fetch_youtube_workflows(q, "US"))
            results.extend(fetch_youtube_workflows(q, "IN"))
        except Exception as e:
            logger.warning(f"YouTube fetch skipped for '{q}': {e}")

    try:
        results.extend(fetch_forum_workflows())
    except Exception as e:
        logger.warning(f"Forum fetch skipped: {e}")

    trends_keywords = [
        "n8n slack integration",
        "n8n google sheets automation"
    ]

    for kw in trends_keywords:
        for country in ["US", "IN"]:
            try:
                trend = fetch_trends(kw, country)
                if trend:
                    results.append(trend)
            except Exception as e:
                logger.warning(f"Google Trends fetch skipped for '{kw}' ({country}): {e}")

    DATA_DIR.mkdir(exist_ok=True)
    if not results:
        logger.warning("Workflow update produced no results; keeping existing data file.")
        return

    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run()
