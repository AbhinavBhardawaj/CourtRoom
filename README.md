# CourtRoom

#Overview
A small web utility to fetch and display case metadata and latest orders/judgments from the Delhi High Court public site. The MVP uses a manual CAPTCHA flow: the app fetches the search form and CAPTCHA image, you enter the CAPTCHA, and it returns parsed case details.

#Key features

Inputs: Case Type, Case Number, Filing Year

Parses: Petitioner, Respondent, Case Status, Filing Date, Next Hearing Date (best-effort), Order/Judgment PDF links

Storage: Logs each query and saves raw HTML responses in SQLite

Error handling: Clear messages for invalid CAPTCHA, case not found, and other failures

Court chosen

Delhi High Court: https://delhihighcourt.nic.in/

#Project structure

scraper.py: Core scraper with manual CAPTCHA two-step flow

requirements.txt: Python dependencies

app.py (optional): Minimal Flask API/UI if included

templates/ (optional): HTML templates for simple UI

static/ (optional): Placeholder for assets

README.md: This file

.gitignore: Python cache, .env, database files

scraper_logs.db: SQLite database (auto-created)

Setup

Prerequisites

Python 3.10+ recommended

pip

Install dependencies

pip install -r requirements.txt

Windows note (only if you try optional OCR later)

If you experiment with OCR, you’ll need Tesseract installed and pytesseract configured. For this MVP, OCR is not required.

Environment variables

None required for the manual CAPTCHA flow.

Do not commit secrets; if you later add a CAPTCHA solver or proxies, store keys in a .env and add .env to .gitignore.

