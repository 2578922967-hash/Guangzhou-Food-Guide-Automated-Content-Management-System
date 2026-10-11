# Guangzhou Food Guide Automated Content Management System

This repository contains the course group assignment deliverables for `AIDM7360`.

## Included Deliverables

- `Food Auto/` - Full project source code (backend + frontend + database assets)
- `Report.pdf` - Final written report
- `副本Guangzhou Food Guide Automated Content Management System.pptx` - Presentation slides

## Project Overview

`Food Auto` is a full-stack content management system for restaurant data and automated report generation.

- Backend: Python + Flask + SQLite
- Frontend: React + TypeScript + Vite
- Features: restaurant management, filtering/sorting, template management, report generation, statistics dashboard

## Quick Start (Project in `Food Auto`)

### Backend

```bash
cd "Food Auto"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.cli init-db --seed
python -m src.app
```

Backend runs at `http://localhost:8000`.

### Frontend

```bash
cd "Food Auto/frontend"
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

## Notes

- This repository was prepared for course submission and presentation.
- For detailed functional documentation, see `Food Auto/README.md`.
