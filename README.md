# n8n Automation Project - AI-Powered Workflow Automation System

This project is an automation system inspired by n8n-style workflow automation. It integrates multiple APIs and data sources to automatically collect, process, score, and deliver relevant workflow popularity data.

It uses the YouTube Data API, the n8n Community Forum API, Google Trends, Python, and FastAPI to automate data extraction, filtering, analysis, and API delivery without manual effort.

## Objectives

- Automate repetitive digital data collection tasks
- Integrate multiple APIs into a single workflow
- Build scalable automation pipelines
- Reduce manual research work using intelligent collectors
- Demonstrate real-world automation engineering
- Store and expose processed workflow popularity data

## Features

- API integration with YouTube Data API, n8n Forum, and Google Trends
- Automated workflow data collection
- Scheduled background execution
- Data extraction and processing
- Smart popularity scoring logic
- JSON-based storage output
- FastAPI endpoint for accessing collected data
- Secure API key handling through `.env`
- GitHub-safe environment variable setup
- Cloud-ready project structure

## System Architecture

```text
Trigger -> API Request -> Data Processing -> Filtering/Scoring -> Storage -> API Output
```

## Core Components

- n8n-style automation logic
- Python collectors
- REST API integrations
- FastAPI backend
- APScheduler background jobs
- JSON storage
- Environment variable security
- Git and GitHub version control

## Tech Stack

| Area | Technology |
| --- | --- |
| Automation Logic | Python |
| API Backend | FastAPI |
| Scheduler | APScheduler |
| APIs | YouTube Data API v3, n8n Community Forum API, Google Trends |
| Storage | JSON file |
| Security | `.env`, API key management |
| Version Control | Git, GitHub |

## Project Structure

```text
api/
  main.py
collectors/
  youtube_collector.py
  forum_collector.py
  trends_collector.py
data/
  workflows.json
scheduler/
  run_collectors.py
.env.example
requirements.txt
README.md
```

## Setup

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a local `.env` file from `.env.example`, then replace the placeholder with your YouTube Data API v3 key:

```env
YOUTUBE_API_KEY=your-youtube-api-key-here
```

## Run the API

```powershell
uvicorn api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## API Endpoints

```text
GET /
GET /workflows
GET /workflows?platform=YouTube
GET /workflows?platform=Forum
GET /workflows?country=IN
```

## Run Without Startup Refresh

Use this when you only want to browse existing data:

```powershell
$env:SKIP_INITIAL_UPDATE = "1"
uvicorn api.main:app --reload
```

## Refresh Data Manually

```powershell
python -m scheduler.run_collectors
```

## Security Notes

- Do not commit `.env`
- Keep API keys in environment variables
- Use `.env.example` only as a template
- Rotate your API key if it is accidentally exposed

## Use Case

This project helps identify which n8n automation ideas are gaining attention online by collecting signals from videos, community discussions, and trend data. It can be extended into a dashboard, notification system, or automated recommendation engine.
