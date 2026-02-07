from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_connection

app = FastAPI()

# ======================================================
# ================= SESSION ============================
# ======================================================

app.add_middleware(
    SessionMiddleware,
    secret_key="edubot_secret_key",
    same_site="lax"
)

# ======================================================
# ================= TEMPLATES ==========================
# ======================================================

templates = Jinja2Templates(directory="../Frontend")

# ======================================================
# ================= TEST ===============================
# ======================================================

@app.get("/test")
def test():
    return {"message": "FastAPI is working!"}

# ======================================================
# ================= STUDENT AUTH =======================
# ======================================================

@app.get("/", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
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
        request.session["student_id"] = student["student_id"]
        request.session["student_name"] = student["name"]
        return RedirectResponse("/home", status_code=303)

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Incorrect email or password"}
    )

@app.get("/register", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register_post(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
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
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Email already exists"}
        )

    cursor.close()
    conn.close()

    return RedirectResponse("/", status_code=303)

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)

# ======================================================
# ================= HOME ===============================
# ======================================================

@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    if "student_id" not in request.session:
        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "name": request.session["student_name"]
        }
    )

# ======================================================
# ================= CHAT ===============================
# ======================================================

@app.get("/chat", response_class=HTMLResponse)
def chat(request: Request):
    if "student_id" not in request.session:
        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse("chat.html", {"request": request})

# ======================================================
# ================= PROGRAMS ===========================
# ======================================================

@app.get("/program", response_class=HTMLResponse)
def program(request: Request):
    if "student_id" not in request.session:
        return RedirectResponse("/", status_code=303)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT title, code_snippet FROM programs")
    programs = cursor.fetchall()

    cursor.close()
    conn.close()

    return templates.TemplateResponse(
        "program.html",
        {"request": request, "programs": programs}
    )

# ======================================================
# ================= QUIZ ===============================
# ======================================================

@app.get("/quiz", response_class=HTMLResponse)
def quiz(request: Request):
    if "student_id" not in request.session:
        return RedirectResponse("/", status_code=303)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT quiz_id, title FROM quizzes")
    quizzes = cursor.fetchall()

    cursor.close()
    conn.close()

    return templates.TemplateResponse(
        "quiz.html",
        {"request": request, "quizzes": quizzes}
    )

@app.get("/start_quiz/{quiz_id}", response_class=HTMLResponse)
def start_quiz(request: Request, quiz_id: int):
    if "student_id" not in request.session:
        return RedirectResponse("/", status_code=303)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM quizzes WHERE quiz_id=%s", (quiz_id,))
    quiz = cursor.fetchone()

    cursor.execute("SELECT * FROM questions WHERE quiz_id=%s", (quiz_id,))
    questions = cursor.fetchall()

    cursor.close()
    conn.close()

    return templates.TemplateResponse(
        "start_quiz.html",
        {
            "request": request,
            "quiz": quiz,
            "questions": questions
        }
    )

@app.post("/submit_quiz/{quiz_id}", response_class=HTMLResponse)
async def submit_quiz(request: Request, quiz_id: int):
    if "student_id" not in request.session:
        return RedirectResponse("/", status_code=303)

    form = await request.form()
    student_id = request.session["student_id"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM questions WHERE quiz_id=%s", (quiz_id,))
    questions = cursor.fetchall()

    score = 0
    results = []

    for q in questions:
        selected = form.get(f"q{q['question_id']}")
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
            "option_d": q["option_d"],
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

    return templates.TemplateResponse(
        "quiz_result.html",
        {
            "request": request,
            "results": results,
            "score": score,
            "total": len(questions)
        }
    )

# ======================================================
# ================= FLASHCARDS =========================
# ======================================================

@app.get("/flashcard", response_class=HTMLResponse)
def flashcard(request: Request):
    if "student_id" not in request.session:
        return RedirectResponse("/", status_code=303)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT topic, content FROM flashcards")
    flashcards = cursor.fetchall()

    cursor.close()
    conn.close()

    return templates.TemplateResponse(
        "flashcard.html",
        {"request": request, "flashcards": flashcards}
    )

# ======================================================
# ================= PROGRESS ===========================
# ======================================================

@app.get("/progress", response_class=HTMLResponse)
def progress(request: Request):
    if "student_id" not in request.session:
        return RedirectResponse("/", status_code=303)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT quizzes.title, results.score
        FROM results
        JOIN quizzes ON quizzes.quiz_id = results.quiz_id
        WHERE results.student_id=%s
    """, (request.session["student_id"],))

    progress = cursor.fetchall()

    cursor.close()
    conn.close()

    return templates.TemplateResponse(
        "progress.html",
        {"request": request, "progress": progress}
    )

# ======================================================
# ================= ADMIN ==============================
# ======================================================

@app.get("/admin", response_class=HTMLResponse)
def admin_login(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin/login")
def admin_login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
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
        request.session["admin_id"] = admin["admin_name"] = admin["name"]
        return RedirectResponse("/admin/dashboard", status_code=303)

    return templates.TemplateResponse(
        "admin_login.html",
        {"request": request, "error": "Invalid admin credentials"}
    )

@app.get("/admin/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    if "admin_id" not in request.session:
        return RedirectResponse("/admin", status_code=303)

    return templates.TemplateResponse(
        "admin_dashboard.html",
        {"request": request, "admin": request.session["admin_name"]}
    )

@app.get("/admin/logout")
def admin_logout(request: Request):
    request.session.clear()
    return RedirectResponse("/admin", status_code=303)
