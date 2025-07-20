from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql.cursors
import requests
import random
import re
from datetime import datetime, timedelta
from code_executor import executor

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

def get_db_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user="rishab",
        password="SouL123@",
        database="practice",
        cursorclass=pymysql.cursors.DictCursor
    )

JUDGE0_URL = "https://judge0-ce.p.rapidapi.com/submissions"
API_HEADERS = {
    "X-RapidAPI-Key": "960c512e30msh0b49d44a6f9c8e9p1d8d94jsn2d74820de492",
    "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com",
    "Content-Type": "application/json"
}

def check_output_flexible(user_output: str, expected_output: str, checker_type: str = 'exact', custom_checker_code: str | None = None) -> bool:
    """
    Check if user output matches expected output based on checker type
    """
    if not user_output or not expected_output:
        return False
    
    user_output = user_output.strip()
    expected_output = expected_output.strip()
    
    if checker_type == 'exact':
        return user_output == expected_output
    
    elif checker_type == 'ignore_whitespace':
        # Remove all whitespace and compare
        user_clean = re.sub(r'\s+', '', user_output)
        expected_clean = re.sub(r'\s+', '', expected_output)
        return user_clean == expected_clean
    
    elif checker_type == 'multiple_outputs':
        # Expected output contains multiple valid outputs separated by '|'
        valid_outputs = [out.strip() for out in expected_output.split('|')]
        return user_output in valid_outputs
    
    elif checker_type == 'custom' and custom_checker_code:
        try:
            # Create a safe execution environment for custom checker
            # This is a simplified version - in production, you'd want more security
            local_vars = {
                'user_output': user_output,
                'expected_output': expected_output,
                'result': False
            }
            exec(custom_checker_code, {}, local_vars)
            return local_vars.get('result', False)
        except Exception as e:
            print(f"Custom checker error: {e}")
            return False
    
    # Default to exact matching
    return user_output == expected_output

# Initialize database tables
def init_db():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Create code_snippets table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS code_snippets (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    problem_id INT,
                    source_code TEXT,
                    language_id INT,
                    created_at DATETIME,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (problem_id) REFERENCES problems(id)
                )
            """)
            # Ensure problems table has user_id and new checker columns
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS problems (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    title VARCHAR(255),
                    description TEXT,
                    difficulty ENUM('Easy', 'Medium', 'Hard'),
                    solution TEXT,
                    expected_output TEXT,
                    checker_type ENUM('exact', 'ignore_whitespace', 'custom', 'multiple_outputs') DEFAULT 'exact',
                    custom_checker_code TEXT NULL,
                    tags VARCHAR(255),
                    created_at DATETIME DEFAULT NOW(),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            # Ensure feedback table references problems
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    problem_id INT,
                    feedback TEXT,
                    created_at DATETIME DEFAULT NOW(),
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (problem_id) REFERENCES problems(id)
                )
            """)
            connection.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        connection.close()

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
                connection.commit()
                return redirect(url_for("home"))
        except Exception as e:
                return render_template("signup.html", error=f"Error: {str(e)}")
        finally:
            connection.close()
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
                if user and check_password_hash(user['password'], password):
                    session['user_id'] = user['id']
                    session['user_name'] = user['name']
                    session['email'] = user['email']
                    return redirect(url_for("dashboard"))
                else:
                    return render_template("login.html", error="Invalid email or password")
        finally:
            connection.close()
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch problems
            cursor.execute("SELECT id, title, difficulty, tags FROM problems")
            problems = cursor.fetchall()

            # Fetch snippets
            cursor.execute("""
                SELECT s.id, s.problem_id, s.source_code, s.language_id, s.created_at, p.title
                FROM code_snippets s
                JOIN problems p ON s.problem_id = p.id
                WHERE s.user_id = %s
                ORDER BY s.created_at DESC
            """, (session['user_id'],))
            snippets = cursor.fetchall()

            # Collect unique tags
            all_tags = set()
            for prob in problems:
                if prob['tags']:
                    all_tags.update(tag.strip() for tag in prob['tags'].split(',') if tag.strip())
            all_tags = sorted(all_tags)

            # Fetch user email
            cursor.execute("SELECT email FROM users WHERE id = %s", (session['user_id'],))
            user = cursor.fetchone()

            # Fetch all users except current user
            cursor.execute("SELECT id, name FROM users WHERE id != %s ORDER BY name ASC", (session['user_id'],))
            users = cursor.fetchall()

            # Calculate solved count
            cursor.execute("SELECT COUNT(DISTINCT problem_id) as solved_count FROM submissions WHERE user_id = %s AND status = 'Accepted'", (session['user_id'],))
            solved_result = cursor.fetchone()
            solved_count = solved_result['solved_count'] if solved_result else 0

            # Calculate accuracy
            cursor.execute("""
                SELECT problem_id, status, COUNT(*) as attempts
                FROM submissions
                WHERE user_id = %s
                GROUP BY problem_id, status
            """, (session['user_id'],))
            submissions_for_accuracy = cursor.fetchall()
            total_attempts = 0
            solved_problems = set()
            penalty = 0
            for sub in submissions_for_accuracy:
                total_attempts += sub['attempts']
                if sub['status'] == 'Accepted':
                    solved_problems.add(sub['problem_id'])
                else:
                    penalty += sub['attempts'] * 5
            total_problems_attempted = len(set(sub['problem_id'] for sub in submissions_for_accuracy))
            if total_problems_attempted == 0:
                accuracy = 0
            else:
                base_accuracy = (len(solved_problems) / total_problems_attempted) * 100
                if total_attempts == len(solved_problems):
                    accuracy = min(90 + random.randint(-5, 5), 95)
                else:
                    accuracy = max(base_accuracy - penalty, 10)
                accuracy = round(accuracy, 2)

            # Calculate streak
            cursor.execute("""
                SELECT DISTINCT DATE(created_at) as solve_date
                FROM submissions
                WHERE user_id = %s AND status = 'Accepted'
                ORDER BY solve_date DESC
            """, (session['user_id'],))
            solve_dates = [row['solve_date'] for row in cursor.fetchall()]
            streak = 0
            today = datetime.now().date()
            expected_date = today
            for solve_date in solve_dates:
                if solve_date == expected_date:
                    streak += 1
                    expected_date -= timedelta(days=1)
                elif solve_date > expected_date:
                    continue
                else:
                    break

            # Calculate rank
            cursor.execute("""
                SELECT user_id, problems_solved
                FROM leaderboard
                ORDER BY score DESC, problems_solved DESC
            """)
            leaderboard_ranks = cursor.fetchall()
            rank = next((i + 1 for i, row in enumerate(leaderboard_ranks) if row['user_id'] == session['user_id']), len(leaderboard_ranks) + 1)

            # Fetch submissions
            cursor.execute("SELECT problem_id, status, created_at, time_spent FROM submissions WHERE user_id = %s ORDER BY created_at DESC LIMIT 10", (session['user_id'],))
            submissions = cursor.fetchall()

            # Fetch leaderboard
            cursor.execute("""
                SELECT u.name, l.problems_solved, l.score
                FROM leaderboard l
                JOIN users u ON l.user_id = u.id
                ORDER BY l.score DESC, l.problems_solved DESC
                LIMIT 10
            """)
            leaderboard = cursor.fetchall()

            # Add tried and accepted status to problems
            for prob in problems:
                cursor.execute("SELECT COUNT(*) as tried FROM submissions WHERE user_id = %s AND problem_id = %s", (session['user_id'], prob['id']))
                tried_result = cursor.fetchone()
                prob['tried'] = tried_result['tried'] > 0 if tried_result else False
                
                cursor.execute("SELECT COUNT(*) as accepted FROM submissions WHERE user_id = %s AND problem_id = %s AND status = 'Accepted'", (session['user_id'], prob['id']))
                accepted_result = cursor.fetchone()
                prob['accepted'] = accepted_result['accepted'] > 0 if accepted_result else False

    finally:
        connection.close()

    return render_template("dashboard.html", 
                          name=session['user_name'], 
                          email=user['email'] if user else '', 
                          problems=problems, 
                          snippets=snippets,
                          solved_count=solved_count, 
                          accuracy=accuracy, 
                          streak=streak, 
                          rank=rank, 
                          submissions=submissions,
                          leaderboard=leaderboard,
                          all_tags=all_tags,
                          users=users,
                          active_tab='profile')

@app.route("/view_snippets")
def view_snippets():
    if 'user_id' not in session:
        return redirect(url_for("login"))
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT s.id, s.problem_id, s.source_code, s.language_id, s.created_at, p.title
                FROM code_snippets s
                JOIN problems p ON s.problem_id = p.id
                WHERE s.user_id = %s
                ORDER BY s.created_at DESC
            """, (session['user_id'],))
            snippets = cursor.fetchall()

            # Map language_id to language name
            language_map = {54: 'C++', 50: 'C', 71: 'Python'}
            for snippet in snippets:
                snippet['language'] = language_map.get(snippet['language_id'], 'Unknown')
    finally:
        connection.close()
    
    return render_template("code_snippets.html", snippets=snippets, name=session['user_name'])

@app.route("/get_snippet/<int:snippet_id>")
def get_snippet(snippet_id):
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Please login'}), 401
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT s.source_code, s.language_id
                FROM code_snippets s
                WHERE s.id = %s AND s.user_id = %s
            """, (snippet_id, session['user_id']))
            snippet = cursor.fetchone()
            if not snippet:
                return jsonify({'status': 'error', 'message': 'Snippet not found'}), 404
            
            language_map = {54: 'C++', 50: 'C', 71: 'Python'}
            return jsonify({
                'status': 'success',
                'source_code': snippet['source_code'],
                'language': language_map.get(snippet['language_id'], 'Unknown')
            })
    except Exception as e:
        return jsonify({'status': 'error', 'message': f"Database error: {str(e)}"}), 500
    finally:
        connection.close()

@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form["name"]
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE users SET name = %s WHERE id = %s", (name, session['user_id']))
                connection.commit()
                session['user_name'] = name
                return redirect(url_for("dashboard"))
        finally:
            connection.close()
    return render_template("edit_profile.html", name=session['user_name'])

@app.route("/problems/<int:problem_id>")
def solve_problem(problem_id):
    if 'user_id' not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, description, expected_output FROM problems WHERE id = %s", (problem_id,))
            problem = cursor.fetchone()
    finally:
        connection.close()

    if problem:
        return render_template("index.html", problem=problem)
    else:
        return "Problem not found", 404

@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json()
    source_code = data.get("code")
    language_id = data.get("language")
    user_input = data.get("stdin", "")
    problem_id = data.get("problem_id")
    action = data.get("action")
    submission_id = data.get("submission_id")

    if not all([source_code, language_id, problem_id, action]) or not source_code.strip():
        return jsonify({"status": "Error", "output": "Code cannot be empty"}), 400

    time_spent = 0
    if action == "submit" and submission_id:
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT TIMESTAMPDIFF(SECOND, start_time, NOW()) as time_spent
                    FROM submissions 
                    WHERE id = %s AND user_id = %s
                """, (submission_id, session['user_id']))
                result = cursor.fetchone()
                time_spent = result['time_spent'] if result else 0
        finally:
            connection.close()

    # Use our own code executor instead of Judge0
    try:
        # Convert language_id to int if it's a string
        if isinstance(language_id, str):
            language_id = int(language_id)
        
        result = executor.execute_code(source_code, language_id, user_input, timeout=10)
        status = result.get('status', 'Unknown')
        output = result.get('output', '') or result.get('error', 'No output produced')
    except Exception as e:
        return jsonify({"status": "Error", "output": f"Execution error: {str(e)}"}), 500

    if action == "submit":
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # First, check if the new columns exist
                try:
                    cursor.execute("""
                        SELECT expected_output, checker_type, custom_checker_code 
                        FROM problems 
                        WHERE id = %s
                    """, (problem_id,))
                    problem = cursor.fetchone()
                    expected_output = problem['expected_output'] if problem else None
                    checker_type = problem.get('checker_type', 'exact') if problem else 'exact'
                    custom_checker_code = problem.get('custom_checker_code') if problem else None
                except Exception as db_error:
                    # If new columns don't exist, fall back to old query
                    print(f"Database column error: {db_error}")
                    cursor.execute("""
                        SELECT expected_output 
                        FROM problems 
                        WHERE id = %s
                    """, (problem_id,))
                    problem = cursor.fetchone()
                    expected_output = problem['expected_output'] if problem else None
                    checker_type = 'exact'  # Default to exact matching
                    custom_checker_code = None

                cursor.execute("SELECT COUNT(*) as attempts FROM submissions WHERE user_id = %s AND problem_id = %s", (session['user_id'], problem_id))
                attempts_result = cursor.fetchone()
                attempt_count = attempts_result['attempts'] + 1 if attempts_result else 1

                if expected_output and check_output_flexible(output, expected_output, checker_type, custom_checker_code):
                    status = "Accepted"
                    cursor.execute("SELECT COUNT(*) as solved FROM submissions WHERE user_id = %s AND problem_id = %s AND status = 'Accepted'", (session['user_id'], problem_id))
                    solved_result = cursor.fetchone()
                    already_solved = solved_result['solved'] > 0 if solved_result else False
                    
                    cursor.execute(
                        "INSERT INTO submissions (user_id, problem_id, status, time_spent, created_at) VALUES (%s, %s, %s, %s, NOW())",
                        (session['user_id'], problem_id, status, time_spent)
                    )
                    
                    if not already_solved:
                        cursor.execute("""
                            INSERT INTO code_snippets (user_id, problem_id, source_code, language_id, created_at)
                            VALUES (%s, %s, %s, %s, NOW())
                        """, (session['user_id'], problem_id, source_code, language_id))
                        cursor.execute(
                            "INSERT INTO leaderboard (user_id, score, problems_solved) "
                            "VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE "
                            "score = score + %s, problems_solved = problems_solved + 1, last_updated = NOW()",
                            (session['user_id'], 10, 1, 10)
                        )
                    
                    connection.commit()
                    return jsonify({"status": "Correct", "output": output})
                else:
                    status = "Wrong Answer"
                    cursor.execute(
                        "INSERT INTO submissions (user_id, problem_id, status, time_spent, created_at) VALUES (%s, %s, %s, %s, NOW())",
                        (session['user_id'], problem_id, status, time_spent)
                    )
                    connection.commit()
                    return jsonify({"status": "Wrong", "output": "Wrong Answer: Output does not match expected output"})
        except Exception as e:
            connection.rollback()
            return jsonify({"status": "Error", "output": f"Database error: {str(e)}"}), 500
        finally:
            connection.close()
    else:
        return jsonify({"status": status, "output": output})

@app.route('/start-timer', methods=['POST'])
def start_timer():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    data = request.get_json()
    problem_id = data['problem_id']
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO submissions 
                (user_id, problem_id, status, start_time, created_at) 
                VALUES (%s, %s, 'started', NOW(), NOW())
            """, (session['user_id'], problem_id))
            connection.commit()
            return jsonify({
                'success': True, 
                'submission_id': cursor.lastrowid
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/timer-action', methods=['POST'])
def timer_action():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    data = request.get_json()
    submission_id = data['submission_id']
    action = data['action']
    time_spent = data.get('time_spent', 0)
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            if action == 'pause':
                cursor.execute("""
                    UPDATE submissions 
                    SET time_spent = %s 
                    WHERE id = %s AND user_id = %s
                """, (time_spent, submission_id, session['user_id']))
            elif action == 'resume':
                cursor.execute("""
                    UPDATE submissions 
                    SET start_time = NOW() - INTERVAL %s SECOND
                    WHERE id = %s AND user_id = %s
                """, (time_spent, submission_id, session['user_id']))
            
            connection.commit()
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route("/post_problem", methods=["GET", "POST"])
def post_problem():
    if 'user_id' not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('description')
        difficulty = request.form.get('difficulty')
        solution = request.form.get('solution')
        expected_output = request.form.get('expected_output')
        checker_type = request.form.get('checker_type', 'exact')
        custom_checker_code = request.form.get('custom_checker_code')
        tags = request.form.get('tags')
        
        if not all([title, description, difficulty, expected_output]):
            return render_template('post_problem.html', error='All required fields must be filled.')
        if difficulty not in ['Easy', 'Medium', 'Hard']:
            return render_template('post_problem.html', error='Invalid difficulty.')
        if checker_type not in ['exact', 'ignore_whitespace', 'custom', 'multiple_outputs']:
            return render_template('post_problem.html', error='Invalid checker type.')
        if title and len(title) > 255:
            return render_template('post_problem.html', error='Title too long.')
        if tags and len(tags) > 255:
            return render_template('post_problem.html', error='Tags too long.')
        
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO problems (user_id, title, description, difficulty, solution, expected_output, checker_type, custom_checker_code, tags)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (session['user_id'], title, description, difficulty, solution, expected_output, checker_type, custom_checker_code, tags))
                connection.commit()
        except Exception as e:
            return render_template('post_problem.html', error=f"Database error: {str(e)}")
        finally:
            connection.close()
        
        return redirect(url_for('dashboard'))
    
    return render_template('post_problem.html')

@app.route("/submit_solution/<int:problem_id>", methods=["POST"])
def submit_solution(problem_id):
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Please login'}), 401
    
    data = request.get_json()
    print(f"Received submission for problem_id: {problem_id}, data: {data}")
    
    source_code = data.get("code")
    language_id = data.get("language")
    user_input = data.get("stdin", "")
    submission_id = data.get("submission_id")

    if not source_code or not source_code.strip():
        print("Error: Source code is empty or missing")
        return jsonify({"status": "Error", "output": "Code cannot be empty"}), 400
    
    if not language_id:
        print("Error: Language ID is missing")
        return jsonify({"status": "Error", "output": "Language ID is required"}), 400
    
    # Calculate time spent
    time_spent = 0
    if submission_id:
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT TIMESTAMPDIFF(SECOND, start_time, NOW()) as time_spent
                    FROM submissions 
                    WHERE id = %s AND user_id = %s
                """, (submission_id, session['user_id']))
                result = cursor.fetchone()
                time_spent = result['time_spent'] if result else 0
        except Exception as e:
            print(f"Error calculating time_spent: {str(e)}")
        finally:
            connection.close()

    # Use our own code executor instead of Judge0
    try:
        # Convert language_id to int if it's a string
        if isinstance(language_id, str):
            language_id = int(language_id)
        
        print(f"Executing code with language_id: {language_id}")
        result = executor.execute_code(source_code, language_id, user_input, timeout=10)
        print(f"Execution result: {result}")
        output = result.get('output', '') or result.get('error', 'No output produced')
        status = result.get('status', 'Unknown')
    except Exception as e:
        print(f"Execution error: {str(e)}")
        return jsonify({"status": "Error", "output": f"Execution error: {str(e)}"}), 500
    
    # In submit_solution, fix the try block for fetching problem details
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Get problem details including checker type
            try:
                cursor.execute("""
                    SELECT expected_output, checker_type, custom_checker_code 
                    FROM problems 
                    WHERE id = %s
                """, (problem_id,))
                problem = cursor.fetchone()
                if not problem:
                    print(f"Error: Problem ID {problem_id} not found")
                    return jsonify({'status': 'error', 'message': 'Problem not found'}), 404
                expected_output = problem['expected_output']
                checker_type = problem.get('checker_type', 'exact')
                custom_checker_code = problem.get('custom_checker_code')
            except Exception as db_error:
                # If new columns don't exist, fall back to old query
                print(f"Database column error in submit_solution: {db_error}")
                cursor.execute("""
                    SELECT expected_output 
                    FROM problems 
                    WHERE id = %s
                """, (problem_id,))
                problem = cursor.fetchone()
                if not problem:
                    print(f"Error: Problem ID {problem_id} not found")
                    return jsonify({'status': 'error', 'message': 'Problem not found'}), 404
                expected_output = problem['expected_output']
                checker_type = 'exact'  # Default to exact matching
                custom_checker_code = None

            cursor.execute("SELECT COUNT(*) as attempts FROM submissions WHERE user_id = %s AND problem_id = %s", (session['user_id'], problem_id))
            attempts_result = cursor.fetchone()
            attempt_count = attempts_result['attempts'] + 1 if attempts_result else 1

            # Use flexible output checking
            is_correct = check_output_flexible(output, expected_output, checker_type, custom_checker_code)
            
            if is_correct:
                status = "Accepted"
                cursor.execute("SELECT COUNT(*) as solved FROM submissions WHERE user_id = %s AND problem_id = %s AND status = 'Accepted'", (session['user_id'], problem_id))
                solved_result = cursor.fetchone()
                already_solved = solved_result['solved'] > 0 if solved_result else False
                
                cursor.execute(
                    "INSERT INTO submissions (user_id, problem_id, status, time_spent, created_at) VALUES (%s, %s, %s, %s, NOW())",
                    (session['user_id'], problem_id, status, time_spent)
                )
                
                # Only save snippet and update leaderboard if this is the first time solving
                if not already_solved:
                    print(f"Saving snippet for user_id: {session['user_id']}, problem_id: {problem_id}")
                    cursor.execute("""
                        INSERT INTO code_snippets (user_id, problem_id, source_code, language_id, created_at)
                        VALUES (%s, %s, %s, %s, NOW())
                    """, (session['user_id'], problem_id, source_code, language_id))
                    print("Snippet saved successfully")
                    
                    cursor.execute(
                        "INSERT INTO leaderboard (user_id, score, problems_solved) "
                        "VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE "
                        "score = score + %s, problems_solved = problems_solved + 1, last_updated = NOW()",
                        (session['user_id'], 10, 1, 10)
                    )
                
                connection.commit()
                return jsonify({"status": "Correct", "output": output})
            else:
                status = "Wrong Answer"
                cursor.execute(
                    "INSERT INTO submissions (user_id, problem_id, status, time_spent, created_at) VALUES (%s, %s, %s, %s, NOW())",
                    (session['user_id'], problem_id, status, time_spent)
                )
                connection.commit()
                return jsonify({"status": "Wrong", "output": "Wrong Answer: Output does not match expected output"})
    except Exception as e:
        connection.rollback()
        print(f"Database error: {str(e)}")
        return jsonify({"status": "Error", "output": f"Database error: {str(e)}"}), 500
    finally:
        connection.close()

@app.route("/post_feedback/<int:problem_id>", methods=["POST"])
def post_feedback(problem_id):
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Please login'}), 401
    
    feedback_text = request.form.get('feedback')
    if not feedback_text or len(feedback_text.strip()) == 0:
        return jsonify({'status': 'error', 'message': 'Feedback cannot be empty'}), 400
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO feedback (user_id, problem_id, feedback)
                VALUES (%s, %s, %s)
            """, (session['user_id'], problem_id, feedback_text.strip()))
            connection.commit()
            
            cursor.execute('SELECT LAST_INSERT_ID() AS id')
            feedback_result = cursor.fetchone()
            feedback_id = feedback_result['id'] if feedback_result else None
            
            cursor.execute('SELECT name FROM users WHERE id = %s', (session['user_id'],))
            user_result = cursor.fetchone()
            user_name = user_result['name'] if user_result else 'Unknown'
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': f"Database error: {str(e)}"}), 500
    finally:
        connection.close()
    
    return jsonify({
        'status': 'success',
        'feedback': {
            'id': feedback_id,
            'user_name': user_name,
            'feedback': feedback_text.strip(),
            'created_at': 'Just now'
        }
    })

@app.route("/user_problems/<int:user_id>", methods=["GET"])
def user_problems(user_id):
    if 'user_id' not in session:
        return redirect(url_for("login"))
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch user info
            cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                return "User not found", 404
            
            # Fetch user's posted problems
            cursor.execute("SELECT id, title, difficulty, tags, created_at FROM users_problems WHERE user_id = %s", (user_id,))
            problems = cursor.fetchall()
            
            # Fetch feedback for each problem
            for problem in problems:
                cursor.execute('''
                    SELECT f.id, f.user_id, f.feedback, f.created_at, u.name AS user_name
                    FROM feedback f
                    JOIN users u ON f.user_id = u.id
                    WHERE f.users_problem_id = %s
                    ORDER BY f.created_at DESC
                ''', (problem['id'],))
                problem['feedback'] = cursor.fetchall()
    
    finally:
        connection.close()
    
    return render_template('users_problem.html', user=user, problems=problems)

@app.template_filter('icon_class')
def icon_class(language):
    icons = {
        'python': 'fab fa-python',
        'javascript': 'fab fa-js',
        'java': 'fab fa-java',
        'html': 'fab fa-html5',
        'css': 'fab fa-css3-alt',
        'c++': 'fas fa-code',
        'c': 'fas fa-code',
        'go': 'fas fa-golang',
        'typescript': 'fas fa-code',
        'php': 'fab fa-php'
    }
    return icons.get(language.lower(), 'fas fa-code')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
    