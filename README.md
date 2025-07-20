# 💻 Online Code Editor & Practice Platform

A full-featured LeetCode-style web application built using Flask, MySQL, HTML/CSS/JS, and a secure local code execution engine (Python, C, C++). Users can solve problems, submit code, track streaks, accuracy, and even view other user's challenges and feedback. Flexible output checkers and admin scripts make it easy to manage and extend.

---

## 🚀 Features

- 🧠 User Auth (signup/login)
- 📝 Code editor with syntax highlighting
- 🧪 Problem submission and solving with flexible validation (exact, ignore whitespace, multiple outputs, custom checker)
- ⏱️ Timer system with pause/resume
- 📊 Leaderboard with score, accuracy, rank
- 💬 Feedback/comment system on problems
- 🧾 View personal code snippets
- 🔍 Filter by tags/difficulty
- ⚡ Local server-side code execution (Python, C, C++)
- 🛠️ Admin/utility scripts for database and debugging

---

## 🧰 Tech Stack

- Flask (Python backend)
- MySQL (data storage)
- HTML + CSS + JS (Frontend)
- Local code execution (Python, C, C++)
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

### 5. (Optional) Insert Dummy Problems
```bash
python insert_dummy_problems.py
```

### 6. Run the App
```bash
python app.py
```

---

## 🛠️ Problems & Solutions During Development

During development, several real-world issues were encountered and solved with custom scripts and code improvements. Here are the main problems and how they were addressed:

### **1. Database Schema Mismatches & Migration**
- **Problem:** Table columns missing or schema not matching code expectations.
- **Solution:**
  - **`migrate_database.py`**: Safely adds missing columns (like `checker_type`, `custom_checker_code`) if needed.
  - **`check_database_schema.py`**: Prints the current schema for quick debugging.

### **2. Foreign Key Constraint Errors**
- **Problem:** Unable to delete problems due to existing submissions referencing them.
- **Solution:**
  - **`fix_database_constraints.py`**: Temporarily disables foreign key checks, clears dependent tables, and re-enables constraints.

### **3. Dummy Data for Testing**
- **Problem:** Needed a set of diverse problems to test all features.
- **Solution:**
  - **`dummy_problems.sql`**: SQL file with 15 problems (various checker types/difficulties).
  - **`insert_dummy_problems.py`**: Python script to insert these problems into the database.

### **4. Local Code Execution & Language ID Debugging**
- **Problem:** Judge0 API limits and language ID mismatches (string vs int).
- **Solution:**
  - **`code_executor.py`**: Secure, local code execution for Python, C, C++.
  - **`debug_language_ids.py`**: Script to test and debug language ID handling.

### **5. Output Checker Logic**
- **Problem:** Needed to test all output checker types (exact, ignore whitespace, multiple outputs, custom).
- **Solution:**
  - **`test_checker_types.py`**: Script to verify all checker logic.
  - **`problem_checker_examples.py`**: Example problems and custom checker code snippets.

### **6. Quick Testing & Validation**
- **Problem:** Needed a fast way to test the execution system end-to-end.
- **Solution:**
  - **`quick_test.py`**: Runs sample code in all supported languages to verify execution.
  - **`test_execution.py`**: More comprehensive execution system tests.

### **7. Pycache/Venv Folder Issues**
- **Problem:** Unwanted files/folders tracked by git.
- **Solution:**
  - **`.gitignore`**: Now includes `__pycache__/` and `venv/` to keep the repo clean.

---

## 📦 Project Structure (Key Files)
- `app.py` — Main Flask app
- `code_executor.py` — Local code execution engine
- `insert_dummy_problems.py` — Insert test problems
- `fix_database_constraints.py` — Fix DB foreign key issues
- `migrate_database.py` — Auto-migrate schema if needed
- `test_checker_types.py`, `quick_test.py`, `test_execution.py` — Testing scripts
- `problem_checker_examples.py` — Sample checker code
- `debug_language_ids.py` — Language ID debug tool
- `check_database_schema.py` — Print DB schema
- `dummy_problems.sql` — SQL for test problems
- `.gitignore` — Ignore venv, pycache, etc.

---

## 📝 What to Do If You Face Issues
- **Database errors:** Run `migrate_database.py` or `fix_database_constraints.py`.
- **Schema mismatch:** Use `check_database_schema.py` to debug.
- **Dummy data needed:** Run `insert_dummy_problems.py`.
- **Code execution not working:** Test with `quick_test.py` or `test_execution.py`.
- **Output checker issues:** Use `test_checker_types.py`.
- **Language ID issues:** Use `debug_language_ids.py`.
- **Unwanted files in git:** Update `.gitignore` and run `git rm --cached <file>`.

---

## 📸 Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Problem Posting
![Problem Posting](screenshots/problem_post.png)

### Code Execution
![Code Execution](screenshots/code_execution.png)

---

## **Step-by-Step: Add Screenshots to Your GitHub Project**

### 1. **Screenshots Folder Banao**
Project root me ek folder banao, jaise:
```
screenshots/
```
Isme apne screenshots (PNG/JPG) daal do, e.g.:
- `screenshots/dashboard.png`
- `screenshots/problem_post.png`
- `screenshots/code_execution.png`

### 2. **Screenshots ko Git me Add Karo**
```bash
git add screenshots/
git commit -m "Add project screenshots"
git push origin main
```

### 3. **README.md Me Screenshots Dikhana**
README.md me jahan dikhana hai, wahan ye markdown use karo:

```markdown
<code_block_to_apply_changes_from>
```

- **Tip:** Screenshot ka naam aur path sahi hona chahiye (case-sensitive).

### 4. **Push README Changes**
```bash
git add README.md
git commit -m "Add screenshots section to README"
git push origin main
```

---

## **Summary Table**

| Step                | Command/Action                                  |
|---------------------|-------------------------------------------------|
| Folder banao        | `mkdir screenshots`                             |
| Screenshot daalo    | (copy-paste images in folder)                   |
| Git add/commit/push | `git add screenshots/` ...                      |
| README update       | Markdown image syntax (upar diya hai)           |
| Push README         | `git add README.md && git commit ... && push`   |

---