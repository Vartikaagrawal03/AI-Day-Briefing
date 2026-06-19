# 🧠 AI Day-Briefing Agent

An intelligent personal assistant that integrates Gmail and Google Calendar, applies NLP-based email prioritization, and uses a generative AI agent to deliver natural-language daily briefings via email.

## 🎯 Problem Statement

Professionals spend significant time manually scanning emails and calendars each morning to figure out what matters. This project automates that process — combining real-time data from multiple sources, prioritizing it using NLP, and summarizing it conversationally using an LLM.

## 🏗️ Architecture

Gmail API ─┐
           ├─→ Data Pipeline → NLP Processing → SQLite Storage → LLM Agent → Email Notification
Calendar───┘
   API

## ⚙️ Tech Stack

- **APIs:** Gmail API, Google Calendar API, Google OAuth 2.0
- **NLP:** spaCy (Named Entity Recognition), rule-based urgency classification
- **LLM:** Google Gemini 2.5 Flash (agentic briefing generation)
- **Storage:** SQLite
- **Data Analysis:** pandas, matplotlib, seaborn
- **Notification:** SMTP email delivery
- **Language:** Python 3.11

## ✨ Features

- 🔐 Secure OAuth 2.0 authentication with Gmail and Calendar
- 📧 Automated email fetching with real-time inbox scanning
- 🧠 NLP pipeline extracting people, dates, and organizations via Named Entity Recognition
- ⚡ Rule-based urgency scoring system (validated against test cases — see EDA notebook)
- 🗂️ Automatic email categorization (meeting-related, action-needed, promotional, automated, informational)
- 🤖 LLM-powered natural language briefing generation
- 📬 Automated email notification delivery
- 📊 Exploratory data analysis notebook with validated insights

## 📈 Key Results

From EDA analysis on real inbox data:
- Urgency classifier shows strong validity: meeting-related emails averaged **6.0/10** urgency vs **0.0/10** for automated/promotional emails
- Successfully validated scoring logic against engineered test cases (10/10 score achieved on deliberately urgent test email)
- NLP pipeline extracts structured entities (people, dates, organizations) from unstructured email text

## 🚀 How It Works

1. **Authentication** — OAuth flow connects securely to Gmail and Calendar
2. **Data Fetching** — Pulls last 24 hours of emails and upcoming calendar events
3. **NLP Processing** — Runs NER and rule-based urgency scoring on each email
4. **Storage** — Persists structured data to SQLite for analysis and historical tracking
5. **LLM Synthesis** — Gemini generates a natural-language briefing from structured context
6. **Delivery** — Briefing is emailed to the user automatically

## 📁 Project Structure

AI-Day-Briefing/
├── auth.py                  # OAuth authentication
├── fetch_data.py             # Gmail + Calendar data fetching
├── nlp_processor.py           # NLP pipeline (NER + urgency scoring)
├── database.py                # SQLite storage layer
├── run_pipeline.py            # Orchestrates full pipeline
├── briefing_agent.py          # LLM agent for briefing generation
├── notifier.py                 # Email notification delivery
├── eda_analysis.ipynb           # Exploratory data analysis notebook
└── README.md

## 🔮 Future Improvements

- Fine-tune a custom NER model on email-specific text to reduce false positives
- Add Outlook integration for broader email provider support
- Build a Streamlit dashboard for live interaction
- Collect multi-day data to enable behavioral pattern analysis (response time trends, sender prioritization learning)
- Replace rule-based urgency scoring with a trained ML classifier using engagement data as labels

## 🛠️ Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Google Cloud OAuth credentials (Gmail + Calendar API)
4. Add `credentials.json` to project root
5. Create `.env` file with `GEMINI_API_KEY`, `GMAIL_SENDER`, `GMAIL_APP_PASSWORD`
6. Run: `python briefing_agent.py`

---

*Built as a personal project exploring agentic AI systems, NLP, and multi-API integration.*
