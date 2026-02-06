from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_connection

app = Flask(
    __name__,
    template_folder="../Frontend"
)

app.secret_key = "edubot_secret_key"


# ======================================================
# ================= TEST ===============================
# ======================================================
@app.route("/test")
def test():
    return "Flask is working!"


# ======================================================
# ================= STUDENT AUTH =======================
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

    cursor.execute(
        "SELECT student_id, name, password_hash FROM students WHERE email=%s",
        (email,)
    )
    student = cursor.fetchone()

    cursor.close()
    conn.close()

    if student and check_password_hash(student["password_hash"], password):
        session["student_id"] = student["student_id"]
        session["student_name"] = student["name"]
        return redirect(url_for("home"))

    return render_template("login.html", error="Incorrect email or password")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_post():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    password_hash = generate_password_hash(password)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO students (name, email, password_hash) VALUES (%s,%s,%s)",
            (name, email, password_hash)
        )
        conn.commit()
    except:
        cursor.close()
        conn.close()
        return render_template("register.html", error="Email already exists")

    cursor.close()
    conn.close()
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ======================================================
# ================= STUDENT HOME =======================
# ======================================================

@app.route("/home")
def home():
    if "student_id" not in session:
        return redirect(url_for("login"))

    return render_template("home.html", name=session["student_name"])


# ======================================================
# ================= CHAT ===============================
# ======================================================

@app.route("/chat")
def chat():
    if "student_id" not in session:
        return redirect(url_for("login"))

    return render_template("chat.html")


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
# ================= QUIZ MODULE ========================
# ======================================================

@app.route("/quiz")
def quiz():
    if "student_id" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # show all quizzes (easy testing)
    cursor.execute("SELECT quiz_id, title FROM quizzes")
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

    cursor.execute(
        "SELECT * FROM quizzes WHERE quiz_id=%s",
        (quiz_id,)
    )
    quiz = cursor.fetchone()

    cursor.execute(
        "SELECT * FROM questions WHERE quiz_id=%s",
        (quiz_id,)
    )
    questions = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "start_quiz.html",
        quiz=quiz,
        questions=questions
    )


@app.route("/submit_quiz/<int:quiz_id>", methods=["POST"])
def submit_quiz(quiz_id):
    if "student_id" not in session:
        return redirect(url_for("login"))

    student_id = session["student_id"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM questions WHERE quiz_id=%s",
        (quiz_id,)
    )
    questions = cursor.fetchall()

    score = 0
    results = []

    for q in questions:
        selected = request.form.get(f"q{q['question_id']}", "Not Answered")
        correct = q["correct_option"]

        if selected == correct:
            score += 1

        results.append({
            "question": q["question_text"],
            "selected": selected,
            "correct": correct,
            "option_a": q["option_a"],
            "option_b": q["option_b"],
            "option_c": q["option_c"],
            "option_d": q["option_d"]
        })

    cursor2 = conn.cursor()
    cursor2.execute(
        "INSERT INTO results (student_id, quiz_id, score) VALUES (%s,%s,%s)",
        (student_id, quiz_id, score)
    )
    conn.commit()

    cursor2.close()
    cursor.close()
    conn.close()

    return render_template(
        "quiz_result.html",
        results=results,
        score=score,
        total=len(questions)
    )


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
# ================= ADMIN AUTH =========================
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

    cursor.execute(
        "SELECT admin_id, name, password_hash FROM admins WHERE email=%s",
        (email,)
    )
    admin = cursor.fetchone()

    cursor.close()
    conn.close()

    if admin and check_password_hash(admin["password_hash"], password):
        session["admin_id"] = admin["admin_id"]
        session["admin_name"] = admin["name"]
        return redirect(url_for("admin_dashboard"))

    return render_template("admin_login.html", error="Invalid admin credentials")


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
# ================= RUN SERVER =========================
# ======================================================

if __name__ == "__main__":
    app.run(debug=True)
