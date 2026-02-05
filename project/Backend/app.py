from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_connection
from datetime import datetime

app = Flask(
    __name__,
    template_folder="../Frontend",
    static_folder="../Frontend"
)

app.secret_key = "edubot_secret_key"

# ======================================================
# ================= STUDENT MODULE =====================
# ======================================================

@app.route("/")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students WHERE email=%s", (email,))
    student = cursor.fetchone()

    if student and check_password_hash(student["password_hash"], password):
        session["student_id"] = student["student_id"]
        session["student_name"] = student["name"]

        cursor.execute(
            "INSERT INTO sessions (student_id, login_time) VALUES (%s,%s)",
            (student["student_id"], datetime.now())
        )
        conn.commit()

        cursor.close()
        conn.close()
        return redirect(url_for("home"))

    cursor.close()
    conn.close()
    return render_template("login.html", error="Incorrect Email or Password")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_post():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    hashed = generate_password_hash(password)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO students (name,email,password_hash) VALUES (%s,%s,%s)",
            (name, email, hashed)
        )
        conn.commit()
    except:
        cursor.close()
        conn.close()
        return render_template("register.html", error="Email already exists")

    cursor.close()
    conn.close()
    return redirect(url_for("login"))


@app.route("/home")
def home():
    if "student_id" not in session:
        return redirect(url_for("login"))

    return render_template("home.html", name=session["student_name"])


# ======================================================
# ================= QUIZ MODULE ========================
# ======================================================

@app.route("/quiz")
def quiz():
    if "student_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    #  show only assigned quizzes
    cursor.execute("""
        SELECT q.quiz_id, q.title
        FROM quizzes q
        JOIN student_quizzes sq ON q.quiz_id = sq.quiz_id
        WHERE sq.student_id = %s
    """, (session["student_id"],))

    quizzes = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("quiz.html", quizzes=quizzes)


@app.route("/start_quiz/<int:quiz_id>")
def start_quiz(quiz_id):
    if "student_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    #  verify quiz access
    cursor.execute("""
        SELECT * FROM student_quizzes
        WHERE student_id=%s AND quiz_id=%s
    """, (session["student_id"], quiz_id))

    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return redirect(url_for("quiz"))

    #  prevent re-attempt
    cursor.execute("""
        SELECT * FROM results
        WHERE student_id=%s AND quiz_id=%s
    """, (session["student_id"], quiz_id))

    if cursor.fetchone():
        cursor.close()
        conn.close()
        return redirect(url_for("progress"))

    cursor.execute("SELECT * FROM quizzes WHERE quiz_id=%s", (quiz_id,))
    quiz = cursor.fetchone()

    cursor.execute("SELECT * FROM questions WHERE quiz_id=%s", (quiz_id,))
    questions = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("start_quiz.html", quiz=quiz, questions=questions)


@app.route("/submit_quiz/<int:quiz_id>", methods=["POST"])
def submit_quiz(quiz_id):
    if "student_id" not in session:
        return redirect(url_for("login"))

    student_id = session["student_id"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM questions WHERE quiz_id=%s", (quiz_id,))
    questions = cursor.fetchall()

    score = 0
    for q in questions:
        selected = request.form.get(f"q{q['question_id']}")
        if selected == q["correct_option"]:
            score += 1

    cursor2 = conn.cursor()
    cursor2.execute(
        "INSERT INTO results (student_id, quiz_id, score) VALUES (%s,%s,%s)",
        (student_id, quiz_id, score)
    )
    conn.commit()

    cursor2.close()
    cursor.close()
    conn.close()

    return redirect(url_for("progress"))


# ======================================================
# ================= FLASHCARDS =========================
# ======================================================

@app.route("/flashcard")
def flashcard():
    if "student_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM flashcards")
    flashcards = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("flashcard.html", flashcards=flashcards)


# ======================================================
# ================= PROGRAMS ===========================
# ======================================================

@app.route("/program")
def program():
    if "student_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM programs")
    programs = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("program.html", programs=programs)


# ======================================================
# ================= PROGRESS ===========================
# ======================================================

@app.route("/progress")
def progress():
    if "student_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT quizzes.title, results.score
        FROM results
        JOIN quizzes ON quizzes.quiz_id = results.quiz_id
        WHERE results.student_id=%s
    """, (session["student_id"],))

    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("progress.html", progress=data)


# ======================================================
# ================= ADMIN MODULE =======================
# ======================================================

@app.route("/admin")
def admin_login():
    return render_template("admin_login.html")


@app.route("/admin/login", methods=["POST"])
def admin_login_post():
    email = request.form["email"]
    password = request.form["password"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM admins WHERE email=%s", (email,))
    admin = cursor.fetchone()

    cursor.close()
    conn.close()

    if admin and check_password_hash(admin["password_hash"], password):
        session["admin_id"] = admin["admin_id"]
        session["admin_name"] = admin["name"]
        return redirect(url_for("admin_dashboard"))

    return render_template("admin_login.html", error="Invalid Admin Login")


@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    return render_template("admin_dashboard.html", admin=session["admin_name"])


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


# ======================================================
# ================= LOGOUT =============================
# ======================================================

@app.route("/logout")
def logout():
    if "student_id" in session:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE sessions
            SET logout_time=%s
            WHERE student_id=%s AND logout_time IS NULL
        """, (datetime.now(), session["student_id"]))

        conn.commit()
        cursor.close()
        conn.close()

    session.clear()
    return redirect(url_for("login"))


# ======================================================
# ================= RUN SERVER =========================
# ======================================================

if __name__ == "__main__":
    app.run(debug=True)
