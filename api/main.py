from fastapi import FastAPI, BackgroundTasks
from apscheduler.schedulers.background import BackgroundScheduler
import json
import os
import logging

from collectors.youtube_collector import fetch_youtube_workflows
from collectors.forum_collector import fetch_forum_workflows
from collectors.trends_collector import fetch_trends

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_FILE = "data/workflows.json"

app = FastAPI(title="n8n Workflow Popularity API")

# -----------------------------
# Workflow updater
# -----------------------------
def update_workflows():
    logger.info("Starting workflow update...")
    results = []

    # YouTube queries
    yt_queries = [
        "n8n slack automation",
        "n8n gmail workflow",
        "n8n whatsapp automation"
        ]

    for q in yt_queries:
        try:
            results.extend(fetch_youtube_workflows(q, "US", 25))
            results.extend(fetch_youtube_workflows(q, "IN", 25))
        except Exception as e:
            logging.warning(f"YouTube fetch skipped for '{q}': {e}")

    results.extend(fetch_forum_workflows(limit=50))

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
                logging.warning(
                    f"Google Trends fetch skipped for '{kw}' ({country}): {e}"
                )

    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    logger.info(f"Workflow update complete. Total workflows: {len(results)}")

# -----------------------------
# Scheduler
# -----------------------------
scheduler = BackgroundScheduler()

@app.on_event("startup")
def startup_event():
    logger.info("API startup - scheduler starting")

    scheduler.add_job(update_workflows, "interval", hours=24)
    scheduler.start()

    # Run first update in background (non-blocking)
    update_workflows()

@app.on_event("shutdown")
def shutdown_event():
    logger.info("API shutdown - scheduler stopping")
    scheduler.shutdown()

# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def home():
    return {
        "status": "running",
        "message": "n8n Workflow Popularity API is live 🚀"
    }

@app.get("/workflows")
def get_workflows(platform: str = None, country: str = None):
    if not os.path.exists(DATA_FILE):
        return {"workflows": []}

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if platform:
        data = [
            d for d in data
            if d.get("platform", "").lower() == platform.lower()
        ]

    if country:
        data = [
            d for d in data
            if d.get("country", "").lower() == country.lower()
        ]

    return {"count": len(data), "workflows": data}
