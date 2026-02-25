# 📧 Receipt Automation Pipeline

An automated system that reads receipt emails from Outlook,
extracts transaction data using regex parsing, and stores it
in Google Sheets for tracking and visualization.

Built as a portfolio project to demonstrate end-to-end
automation pipeline skills.

---

## ✨ Features

- Automatically fetches receipt emails from Outlook (Hotmail)
- Extracts key fields: date, store, amount, currency, approval number
- Saves data to Google Sheets 
- Interactive dashboard with spending charts (Streamlit)
- Runs daily via GitHub Actions — fully automated

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Email Access | Microsoft Graph API |
| Parsing | Python regex |
| Storage | Google Sheets (gspread) |
| Dashboard | Streamlit |
| Automation | GitHub Actions |

---

## 📁 Project Structure

receipt-automation-pipeline/
├── .github/
│   └── workflows/
│       └── daily_run.yml
├── src/
│   ├── email_fetcher.py
│   ├── parser.py
│   └── sheets_writer.py
├── dashboard/
│   └── app.py
├── .env.example
├── requirements.txt
└── README.md

---

## 🚀 How It Works

1. GitHub Actions triggers the script every morning
2. Script connects to Outlook via Microsoft Graph API
3. Filters emails from @jp-post.jp (Yucho Bank debit receipts)
4. Regex extracts transaction fields from email body
5. New rows appended to Google Sheets (duplicates skipped)
6. Streamlit dashboard reads Sheets and displays charts

---

## ⚙️ Setup

(You will fill this in during Week 3 when everything works)

---

## 📊 Dashboard Preview

(Add screenshot here in Week 3)

---

