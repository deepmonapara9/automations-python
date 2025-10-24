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
├── News Headlines Tracker/    # RSS feed monitoring
├── System Health Check/       # System monitoring
├── Website Health Check/      # Website availability monitoring
├── venv/                     # Virtual environment
└── README.md                 # This file
```

## 🔧 Usage

Each automation script is self-contained within its respective folder. Navigate to the specific automation directory you want to use and follow the instructions in that folder.

Most automations are designed to run continuously or on scheduled intervals, making them perfect for:
- Cron jobs
- Background processes
- Scheduled monitoring tasks

## 📝 Notes

- Each automation maintains its own logs and output files
- Scripts are designed to handle errors gracefully and continue running
- Virtual environment is shared across all automations for consistency

## 🤝 Contributing

Feel free to add new automations or improve existing ones. Each automation should be self-contained in its own directory with clear documentation.

---

*Built with Python for automation and monitoring tasks*
