# 💻 Online Code Editor & Practice Platform

A full-featured LeetCode-style web application built using Flask, MySQL, HTML/CSS/JS, and Judge0 API. Users can solve problems, submit code, track streaks, accuracy, and even view other user's challenges and feedback.

---

## 🚀 Features

- 🧠 User Auth (signup/login)
- 📝 Code editor with syntax highlighting (Judge0 API)
- 🧪 Problem submission and solving with validation
- ⏱️ Timer system with pause/resume
- 📊 Leaderboard with score, accuracy, rank
- 💬 Feedback/comment system on problems
- 🧾 View personal code snippets
- 🔍 Filter by tags/difficulty

---

## 🧰 Tech Stack

- Flask (Python backend)
- MySQL (data storage)
- HTML + CSS + JS (Frontend)
- Judge0 API (code execution engine)
- Jinja2 (templating)
- Session-based user auth

---

## ⚙️ Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/being-souL1230/online-editor.git
cd online-editor
```

### 2. Set Up Virtual Environment (optional but recommended)
```bash
python -m venv env
env\Scripts\activate    # On Windows
source env/bin/activate  # On Linux/Mac
```

### 3. Install Required Packages
```bash
pip install flask pymysql requests werkzeug
```

### 4. Configure Database
```bash
host='127.0.0.1'
user='username'
password='database_password'
database='database_name'
```
- Run the app once to auto-create tables:
```bash
python app.py
```

### 5. Judge0 API Setup
```bash
"X-RapidAPI-Key": "YOUR_KEY_HERE"
```
- Get your key from RapidAPI Judge0

### 6. Run the App
```bash
python app.py
```
