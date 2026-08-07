# Storm Financial Command Center (SFCC)

A modern desktop personal finance platform built with **Python**, **CustomTkinter**, and **SQLite**.

SFCC is designed to be more than a budgeting app. Its goal is to provide a complete financial command center by combining budgeting, transaction management, receipts, recurring bills, forecasting, investments, and AI-assisted financial insights into one application.

---

# Vision

Most finance applications answer one question:

> Where did my money go?

SFCC is being built to answer four:

- What happened?
- Why did it happen?
- What is coming next?
- What should I do about it?

Financial calculations remain deterministic and transparent, while AI assists with interpretation and recommendations.

---

# Current Features

- Dashboard
- Transaction Management
- Vendor Memory
- Budget Management
- Income Forecasting
- Recurring Transactions
- Receipt Manager
- SQLite Database
- Automatic Database Migrations
- Monthly Financial Summary

---

# Planned Features

- Investment Portfolio Tracking
- Dividend Dashboard
- Retirement Planning
- Net Worth Tracking
- Interactive Financial Calendar
- Cash Flow Forecasting
- OCR Receipt Scanning
- Financial Reports
- Hermes AI Financial Advisor

See `ROADMAP.md` for the complete development roadmap.

---

# Technology Stack

- Python 3.x
- CustomTkinter
- SQLite
- Git
- GitHub

Planned integrations:

- Hermes AI
- OCR
- Banking APIs
- Brokerage APIs

---

# Project Structure

```text
Storm-Financial-Command-Center-SFCC/
│
├── README.md
├── ARCHITECTURE.md
├── ROADMAP.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── .gitignore
│
├── main.py
├── database.py
├── migrations.py
├── config.py
│
├── data/
├── pages/
└── widgets/
```

---

# Getting Started

## Clone the repository

```bash
git clone https://github.com/angusstorm878-cyber/Storm-Financial-Command-Center-SFCC-.git
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run SFCC

```bash
py main.py
```

---

# Documentation

| Document | Purpose |
|----------|---------|
| README.md | Project overview |
| ARCHITECTURE.md | Design philosophy and architecture |
| ROADMAP.md | Planned features and milestones |
| CHANGELOG.md | Version history |
| CONTRIBUTING.md | Development workflow and standards |

---

# Design Philosophy

SFCC follows a few core principles:

- One function = one responsibility
- One calculation = one source of truth
- Pages coordinate
- Widgets display
- Database persists
- Python calculates
- AI interprets

These principles help keep the codebase maintainable as the project grows.

---

# Project Status

Current Status:

```text
Active Development
```

Current Version:

```text
v0.3.x
```

---

# License

This project is intended to be released under the MIT License.

---

Built with Python, curiosity, and a stubborn refusal to accept that personal finance software has to be either ugly or bloated.
