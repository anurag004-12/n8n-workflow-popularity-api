import json
import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from config import DATA_DIR, DATA_FILE
from collectors.forum_collector import fetch_forum_workflows
from collectors.trends_collector import fetch_trends
from collectors.youtube_collector import fetch_youtube_workflows

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="n8n Workflow Popularity API")
scheduler = BackgroundScheduler()


def update_workflows():
    logger.info("Starting workflow update...")
    results = []

    yt_queries = [
        "n8n slack automation",
        "n8n gmail workflow",
        "n8n whatsapp automation",
    ]

    for query in yt_queries:
        try:
            results.extend(fetch_youtube_workflows(query, "US", 25))
            results.extend(fetch_youtube_workflows(query, "IN", 25))
        except Exception as e:
            logger.warning(f"YouTube fetch skipped for '{query}': {e}")

    try:
        results.extend(fetch_forum_workflows(limit=50))
    except Exception as e:
        logger.warning(f"Forum fetch skipped: {e}")

    trends_keywords = [
        "n8n slack integration",
        "n8n google sheets automation",
    ]

    for keyword in trends_keywords:
        for country in ["US", "IN"]:
            try:
                trend = fetch_trends(keyword, country)
                if trend:
                    results.append(trend)
            except Exception as e:
                logger.warning(
                    f"Google Trends fetch skipped for '{keyword}' ({country}): {e}"
                )

    DATA_DIR.mkdir(exist_ok=True)
    if not results:
        logger.warning("Workflow update produced no results; keeping existing data file.")
        return

    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    logger.info(f"Workflow update complete. Total workflows: {len(results)}")


@app.on_event("startup")
def startup_event():
    logger.info("API startup - scheduler starting")

    scheduler.add_job(
        update_workflows,
        "interval",
        hours=24,
        id="workflow-update-interval",
        replace_existing=True,
    )
    scheduler.start()

    if os.getenv("SKIP_INITIAL_UPDATE", "").lower() in {"1", "true", "yes"}:
        logger.info("Initial workflow update skipped by SKIP_INITIAL_UPDATE")
    else:
        scheduler.add_job(
            update_workflows,
            "date",
            id="initial-workflow-update",
            replace_existing=True,
        )


@app.on_event("shutdown")
def shutdown_event():
    logger.info("API shutdown - scheduler stopping")
    if scheduler.running:
        scheduler.shutdown()


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "n8n Workflow Popularity API is live",
    }


@app.get("/workflows")
def get_workflows(platform: str = None, country: str = None):
    if not DATA_FILE.exists():
        return {"count": 0, "workflows": []}

    with DATA_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if platform:
        data = [
            item for item in data
            if item.get("platform", "").lower() == platform.lower()
        ]

    if country:
        data = [
            item for item in data
            if item.get("country", "").lower() == country.lower()
        ]

    return {"count": len(data), "workflows": data}
