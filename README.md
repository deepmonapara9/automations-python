# 🤖 Automations

A collection of Python automation scripts designed to streamline daily tasks and monitoring processes.

## 📋 Overview

This repository contains various automation tools that help monitor and track different aspects of digital services and news. Each automation is designed to run independently and provides specific functionality for different use cases.

## 🛠 Available Automations

### 📰 News Headlines Tracker

Automated RSS feed monitor that tracks and logs headlines from major Indian news sources on a daily basis.

### 🏥 System Health Check

System monitoring tool that performs regular health checks and reports on system status and performance metrics.

### 🌐 Website Health Check

Website monitoring automation that checks the availability and response times of specified websites.

### 📧 Email Analyzer Streamlit Dashboard

Interactive web dashboard for email analysis featuring:

- Real-time inbox monitoring and unread email tracking
- Top senders visualization with interactive charts
- Email data logging to Google Sheets or local CSV files
- Historical email statistics and trends
- SSL-secured IMAP connection with Gmail integration

### 🧠 AI-Powered Resume Analyzer

Intelligent resume analysis tool powered by local Ollama AI featuring:
- PDF and DOCX resume text extraction
- AI-powered resume analysis and scoring
- Structured data extraction (name, email, skills, experience)
- CSV logging for resume analysis history
- Interactive Streamlit web interface
- Local processing with Ollama (Mistral model)

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Virtual environment (recommended)

### Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```
3. Install dependencies for the specific automation you want to use
4. Navigate to the desired automation folder and run the script

## 📁 Project Structure

```
Automations/
├── News Headlines Tracker/              # RSS feed monitoring
├── System Health Check/                 # System monitoring
├── Website Health Check/                # Website availability monitoring
├── Email Analyzer Streamlit Dashboard/  # Interactive email analysis dashboard
├── AI-Powered Resume Analyzer/          # AI resume analysis with Ollama
├── venv/                               # Virtual environment
└── README.md                           # This file
```

## 🔧 Usage

Each automation script is self-contained within its respective folder. Navigate to the specific automation directory you want to use and follow the instructions in that folder.

### Running the Email Dashboard

For the Streamlit Email Analyzer Dashboard:

```bash
cd "Email Analyzer Streamlit Dashboard"
streamlit run email_dashboard.py
```

The dashboard will open in your web browser at `http://localhost:8501`

### Running the Resume Analyzer

For the AI-Powered Resume Analyzer:

```bash
cd "AI-Powered Resume Analyzer"
streamlit run app.py
```

**Prerequisites:** Ensure Ollama is installed and the Mistral model is available:
```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the Mistral model
ollama pull mistral
```

Most automations are designed to run continuously or on scheduled intervals, making them perfect for:

- Cron jobs
- Background processes
- Scheduled monitoring tasks
- Interactive web dashboards (Streamlit apps)
- AI-powered document analysis

## 📝 Notes

- Each automation maintains its own logs and output files
- Scripts are designed to handle errors gracefully and continue running
- Virtual environment is shared across all automations for consistency

## 🤝 Contributing

Feel free to add new automations or improve existing ones. Each automation should be self-contained in its own directory with clear documentation.

---

_Built with Python for automation and monitoring tasks_
