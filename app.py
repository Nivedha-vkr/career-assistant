from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from PyPDF2 import PdfReader
import docx
import re
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = "your_secret_key"

# ----------------- LOAD QUIZ DATA FROM JSON -----------------
with open("quiz_data.json") as f:
    quiz_data = json.load(f)

# ----------------- DB INIT -----------------
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Skill progress table to store per-user skill completion
    cur.execute("""
        CREATE TABLE IF NOT EXISTS skill_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            skill TEXT NOT NULL,
            step INTEGER DEFAULT 0,
            completed INTEGER DEFAULT 0,
            UNIQUE(user_email, skill)
        )
    """)

    # user_state stores serialized JSON state per user (answers, suggested careers, track)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT UNIQUE NOT NULL,
            state_json TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()

def get_db_connection():  
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn
'''
# ----------------- AUTH ROUTES -----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for("register"))

        conn = get_db_connection()
        existing_user = conn.execute(
            "SELECT * FROM users WHERE username=? OR email=?", (username, email)
        ).fetchone()

        if existing_user:
            flash("Username or email already exists!", "error")
            conn.close()
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        conn.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )
        conn.commit()
        conn.close()

        session["username"] = username
        session["email"] = email
        flash("Registration successful!", "success")
        return redirect(url_for("home"))

    return render_template("login.html")

#-------LOGIN IN ROUTE---------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            # Save basic session info
            session["username"] = user["username"]
            session["email"] = user["email"]

            # --- RESTORE PREVIOUS QUIZ STATE ---
            conn = get_db_connection()
            row = conn.execute(
                "SELECT state_json FROM user_state WHERE user_email=?",
                (email,)
            ).fetchone()
            conn.close()
            if row:
                state = json.loads(row["state_json"])
                session["answers"] = state.get("answers", {})
                session["ranked_careers"] = state.get("ranked_careers", [])
                session["track"] = state.get("track", "tech")

            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password!", "error")
            return redirect(url_for("login"))

    return render_template("loginfeature.html")
'''
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for("register"))

        conn = get_db_connection()
        existing_user = conn.execute(
            "SELECT * FROM users WHERE username=? OR email=?", (username, email)
        ).fetchone()
        if existing_user:
            flash("Username or email already exists!", "error")
            conn.close()
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        conn.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )
        conn.commit()
        conn.close()

        session["username"] = username
        session["email"] = email
        flash("Registration successful!", "success")
        return redirect(url_for("home"))

    return render_template("register.html")  # <- updated
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["username"] = user["username"]
            session["email"] = user["email"]
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password!", "error")
            return redirect(url_for("login"))

    return render_template("login.html")  # <- updated

@app.route("/home")
def home():
    if "username" in session:
        return render_template("home.html", username=session["username"])
    else:
        flash("Please log in first!", "error")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("email", None)
    session.pop("answers", None)
    session.pop("careers", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/")
def index():
    return redirect(url_for("login"))
#------SETTING IN NAV BAR----

@app.route('/settings')
def settings():
    # You can render a settings page or redirect somewhere
    return render_template("settings.html", username=session.get("username"))
#-------------ACCOUNT----------
@app.route('/account')
def account():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("account.html", username=session.get("username"))

#--------CHOOSE TRACK------------
@app.route("/choose_track", methods=["GET", "POST"])
def choose_track():
    if request.method == "POST":
        selected_track = request.form.get("track")
        if selected_track not in ["tech", "nontech"]:
            flash("Invalid track selected.", "error")
            return redirect(url_for("choose_track"))

        session["track"] = selected_track
        return redirect(url_for("quiz", track=selected_track))

    return render_template("choose_track.html")
# ----------------- QUIZ ROUTE -----------------
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    # --- Determine track safely ---
    track = request.args.get("track") or session.get("track", "tech")
    session["track"] = track  # save to session
    quiz_file = os.path.join("data", f"{track.lower()}_quiz.json")
    
    with open(quiz_file, "r") as f:
        quiz_data = json.load(f)

    # Enumerate questions for template
    quiz_data['questions_enumerated'] = list(enumerate(quiz_data['questions']))

    # Load previous state safely
    previous_answers = {}
    previous_careers = []

    if "email" in session:
        conn = get_db_connection()
        row = conn.execute(
            "SELECT state_json FROM user_state WHERE user_email=?",
            (session["email"],)
        ).fetchone()
        conn.close()
        if row:
            state = json.loads(row["state_json"])
            previous_answers = state.get("answers", {})
            previous_careers = state.get("ranked_careers", [])

    if request.method == "POST":
        user_answers = request.form
        career_scores = {}

        # Clear old ranked careers
        session["ranked_careers"] = []

        for key, answer_value in user_answers.items():
            q_index = int(key.split("_")[1])
            question = quiz_data["questions"][q_index]
            mapping = quiz_data["career_mappings"].get(answer_value)
            if mapping:
                for career_name in mapping["careers"]:
                    career_clean = career_name.strip()  # exact match with skills/resources
                    score = mapping["weight"] * question["weight"]
                    career_scores[career_clean] = career_scores.get(career_clean, 0) + score

        # Sort careers by score
        ranked_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
        session["ranked_careers"] = ranked_careers

        # Save state to DB
        if "email" in session:
            conn = get_db_connection()
            state_json = json.dumps({
                "answers": dict(user_answers),
                "ranked_careers": ranked_careers,
                "track": track
            })
            conn.execute("""
                INSERT INTO user_state (user_email, state_json)
                VALUES (?, ?)
                ON CONFLICT(user_email) DO UPDATE SET state_json=excluded.state_json
            """, (session["email"], state_json))
            conn.commit()
            conn.close()

        return redirect(url_for("result"))

    return render_template("quiz.html", quiz_data=quiz_data, previous_answers=previous_answers)

# ------RESULT--------
@app.route("/result")
def result():
    track = session.get("track", "tech")
    ranked_careers = session.get("ranked_careers", [])

    # Show only top 3 careers
    top_ranked_careers = ranked_careers[:3]

    # Load quiz JSON based on track
    quiz_file = os.path.join("data", f"{track.lower()}_quiz.json")
    with open(quiz_file, "r") as f:
        quiz_data = json.load(f)

    results = []
    for career, score in top_ranked_careers:
        career_clean = career.strip()  # remove accidental spaces
        career_data = quiz_data.get("career_skills_resources", {}).get(career_clean, {})

        if not career_data:
            # Debugging warning for missing career
            print(f"[WARNING] No skills/resources found for career: '{career_clean}'")

        results.append({
            "career": career_clean,
            "score": round(score, 2),
            "skills": career_data.get("skills", []),
            "resources": career_data.get("resources", [])
        })

    return render_template("result.html", results=results, track=track)


#-------TRACK ALL SKILL ROUTE------
@app.route("/track_all_skills", methods=["GET", "POST"])
def track_all_skills():
    if "email" not in session:
        flash("Please log in to track your skills", "error")
        return redirect(url_for("login"))

    email = session["email"]
    career = request.args.get("career")

    # Load JSON file based on track
    track = session.get("track", "tech")
    quiz_file = os.path.join("data", f"{track}_quiz.json")
    with open(quiz_file, "r") as f:
        quiz_data = json.load(f)

    # Determine which career's skills to show
    if career:
        session['selected_career_for_skills'] = career
        skills = quiz_data["career_skills_resources"].get(career, {}).get("skills", [])
    elif 'selected_career_for_skills' in session:
        career = session['selected_career_for_skills']
        skills = quiz_data["career_skills_resources"].get(career, {}).get("skills", [])
    else:
        # fallback: show first suggested career only
        ranked_careers = session.get("ranked_careers", [])
        if ranked_careers:
            career = ranked_careers[0][0]
            skills = quiz_data["career_skills_resources"].get(career, {}).get("skills", [])
        else:
            skills = []

    conn = get_db_connection()

    # -------- Handle adding a custom skill --------
    if request.method == "POST" and "add_skill" in request.form:
        new_skill = request.form.get("new_skill", "").strip()
        if new_skill:
            conn.execute("""
                INSERT INTO skill_progress (user_email, skill, step, completed)
                VALUES (?, ?, ?, ?)
            """, (email, new_skill, 0, 0))
            conn.commit()
            flash(f"Skill '{new_skill}' added successfully!", "success")
            return redirect(url_for("track_all_skills"))

    # -------- Handle saving progress --------
    if request.method == "POST" and "add_skill" not in request.form:
        completed_skills = request.form.getlist("completed")
        for skill in skills:
            done = 1 if skill in completed_skills else 0
            conn.execute("""
                INSERT INTO skill_progress (user_email, skill, step, completed)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_email, skill) DO UPDATE SET completed=excluded.completed
            """, (email, skill, 0, done))
        conn.commit()

    # -------- Load saved progress --------
    rows = conn.execute(
        "SELECT skill, completed FROM skill_progress WHERE user_email=?", (email,)
    ).fetchall()
    conn.close()

    saved_progress = {row["skill"]: row["completed"] for row in rows}

    # Calculate progress %
    progress = int(sum(saved_progress.get(s, 0) for s in skills) / len(skills) * 100) if skills else 0

    return render_template(
        "track_all_skills.html",
        skills={s: saved_progress.get(s, 0) for s in skills},
        progress=progress
    )

@app.route("/resume_analyzer", methods=["GET", "POST"])
def resume_analyzer():
    feedback = []

    # Load user's tracked skills
    email = session.get("email")
    user_skills = []
    if email:
        conn = get_db_connection()
        rows = conn.execute(
            "SELECT skill FROM skill_progress WHERE user_email=? AND completed=1",
            (email,)
        ).fetchall()
        conn.close()
        user_skills = [row["skill"].lower() for row in rows]  # convert to lowercase for matching

    # Get top suggested career
    top_career = session.get("ranked_careers", [])
    if top_career:
        top_career_name = top_career[0][0]
    else:
        top_career_name = None

    if request.method == "POST":
        file = request.files.get("resume")
        if file and file.filename:
            text = ""

            # Extract text
            if file.filename.endswith(".pdf"):
                from PyPDF2 import PdfReader
                reader = PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() or ""
            elif file.filename.endswith(".docx"):
                import docx
                doc = docx.Document(file)
                text = " ".join([para.text for para in doc.paragraphs])
            else:
                feedback.append("⚠️ Unsupported file type. Please upload PDF or DOCX.")

            text_lower = text.lower()

            # 1️⃣ Required Sections
            required_sections = ["education", "experience", "skills", "projects"]
            for section in required_sections:
                if section not in text_lower:
                    feedback.append(f"⚠️ Missing section: {section.title()}")
                else:
                    feedback.append(f"✅ Section found: {section.title()}")

            # 2️⃣ Skills Analysis
            matched_skills = [s for s in user_skills if s in text_lower]
            missing_skills = [s for s in user_skills if s not in text_lower]

            if matched_skills:
                feedback.append(f"✅ Skills from your tracker detected: {', '.join(matched_skills)}")
            if missing_skills:
                feedback.append(f"⚠️ Skills missing in resume: {', '.join(missing_skills)}")

            # 3️⃣ Career Match Analysis (optional)
            if top_career_name:
                feedback.append(f"🎯 Top suggested career: {top_career_name}")
                # Optionally, we can suggest adding specific skills/resources from JSON
                track = session.get("track", "tech")
                quiz_file = os.path.join("data", f"{track.lower()}_quiz.json")
                if os.path.exists(quiz_file):
                    with open(quiz_file, "r") as f:
                        quiz_data = json.load(f)
                    career_skills = quiz_data.get("career_skills_resources", {}).get(top_career_name, {}).get("skills", [])
                    career_skills_lower = [s.lower() for s in career_skills]
                    missing_for_career = [s for s in career_skills_lower if s not in text_lower]
                    if missing_for_career:
                        feedback.append(f"⚠️ Skills important for '{top_career_name}' missing: {', '.join(missing_for_career)}")
                    else:
                        feedback.append(f"✅ Your resume aligns well with '{top_career_name}' skills!")

            # 4️⃣ Resume Length
            word_count = len(text.split())
            if word_count < 200:
                feedback.append("⚠️ Resume is too short. Add more details.")
            elif word_count > 800:
                feedback.append("⚠️ Resume may be too long. Keep it concise (1-2 pages).")
            else:
                feedback.append("✅ Resume length looks good.")

            # 5️⃣ Contact Info
            if not re.search(r"\b\d{10}\b", text) and "@" not in text:
                feedback.append("⚠️ Contact details (email/phone) missing.")
            else:
                feedback.append("✅ Contact info detected.")

    return render_template("resume_analyzer.html", feedback=feedback)

# ----------------- RUN -----------------
if __name__ == "__main__":
    app.run(debug=True)