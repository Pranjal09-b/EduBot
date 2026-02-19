
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
# ================= LANDING PAGE =======================
# ======================================================

@app.get("/", response_class=HTMLResponse)
@app.get("/home", response_class=HTMLResponse)
def root(request: Request):
    student_name = request.session.get("student_name")
    is_logged_in = request.session.get("role") == "student"

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "name": student_name,
            "is_logged_in": is_logged_in
        }
    )


# ======================================================
# ================= LOGIN ==============================
# ======================================================

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login_post(
    request: Request,
    role: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    # Clean inputs
    role = role.strip().lower()
    email = email.strip()

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        # ========== ADMIN LOGIN ==========
        if role == "admin":
            cur.execute(
                "SELECT admin_id, name, password_hash FROM admins WHERE email=%s",
                (email,)
            )
            admin = cur.fetchone()

            if admin and check_password_hash(admin["password_hash"], password):
                request.session.clear()
                request.session["admin_id"] = admin["admin_id"]
                request.session["admin_name"] = admin["name"]
                request.session["role"] = "admin"

                return RedirectResponse("/admin", status_code=303)

        # ========== STUDENT LOGIN ==========
        elif role == "student":
            cur.execute(
                "SELECT student_id, name, password_hash FROM students WHERE email=%s",
                (email,)
            )
            student = cur.fetchone()

            if student and check_password_hash(student["password_hash"], password):
                request.session.clear()
                request.session["student_id"] = student["student_id"]
                request.session["student_name"] = student["name"]
                request.session["role"] = "student"

                return RedirectResponse("/", status_code=303)

        # If role invalid
        else:
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "error": "Invalid role selected"}
            )

        # If credentials wrong
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid credentials"}
        )

    finally:
        cur.close()
        conn.close()

# ======================================================
# ================= REGISTER ===========================
# ======================================================

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
def register_post(
    request: Request,
    role: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    # Clean inputs
    role = role.strip().lower()
    name = name.strip()
    email = email.strip()

    # -------- VALIDATION --------
    if len(name) < 3:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Name must be at least 3 characters"}
        )

    if password != confirm_password:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Passwords do not match"}
        )

    if len(password) < 6:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Password must be at least 6 characters"}
        )

    conn = get_connection()
    cur = conn.cursor()

    try:
        # -------- CHECK EMAIL FIRST --------
        if role == "student":
            cur.execute("SELECT 1 FROM students WHERE email=%s", (email,))
        elif role == "admin":
            cur.execute("SELECT 1 FROM admins WHERE email=%s", (email,))
        else:
            return templates.TemplateResponse(
                "register.html",
                {"request": request, "error": "Invalid role selected"}
            )

        if cur.fetchone():
            return templates.TemplateResponse(
                "register.html",
                {"request": request, "error": "Email already exists"}
            )

        # -------- INSERT USER --------
        password_hash = generate_password_hash(password)

        if role == "student":
            cur.execute(
                "INSERT INTO students (name, email, password_hash) VALUES (%s,%s,%s)",
                (name, email, password_hash)
            )
        else:  # admin
            cur.execute(
                "INSERT INTO admins (name, email, password_hash) VALUES (%s,%s,%s)",
                (name, email, password_hash)
            )

        conn.commit()

        return RedirectResponse("/login", status_code=303)

    except Exception as e:
        print("Registration Error:", e)
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Something went wrong. Please try again."}
        )

    finally:
        cur.close()
        conn.close()

    return RedirectResponse("/login", status_code=303)

# ======================================================
# ================= LOGOUT =============================
# ======================================================

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)

# ======================================================
# ================= STUDENT FEATURES ===================
# ======================================================

def require_student(request: Request):
    return request.session.get("role") == "student"


@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    if not require_student(request):
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse("chat.html", {"request": request})

from fastapi.responses import JSONResponse

@app.post("/ask")
async def ask_question(request: Request):

    if not require_student(request):
        return JSONResponse({"reply": "Unauthorized"}, status_code=401)

    data = await request.json()
    message = data.get("message", "").lower()
    student_id = request.session.get("student_id")

    conn = get_connection()
    cur = conn.cursor()

    # Get keywords
    cur.execute("SELECT keyword, response FROM chatbot_keywords")
    keywords = cur.fetchall()

    reply = "Sorry, I don't understand. Please try another question."

    for keyword, response in keywords:
        if keyword.lower() in message:
            reply = response
            break

    # Save chat
    cur.execute("""
        INSERT INTO chat_messages (student_id, question, answer)
        VALUES (%s, %s, %s)
    """, (student_id, message, reply))

    conn.commit()
    cur.close()
    conn.close()

    return {"reply": reply}

@app.get("/chat-history")
def get_chat_history(request: Request):

    if not require_student(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    student_id = request.session.get("student_id")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT question, answer 
        FROM chat_messages
        WHERE student_id = %s
        ORDER BY created_at
    """, (student_id,))

    chats = cur.fetchall()

    cur.close()
    conn.close()

    return {"chats": chats}


@app.get("/program", response_class=HTMLResponse)
def programs_page(request: Request):
    if not require_student(request):
        return RedirectResponse("/login", status_code=303)

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT program_id, title, code_snippet
        FROM programs
        ORDER BY program_id DESC
    """)
    programs = cur.fetchall()

    cur.close()
    conn.close()

    return templates.TemplateResponse(
        "program.html",
        {"request": request, "programs": programs}
    )


@app.get("/quiz", response_class=HTMLResponse)
def quiz_page(request: Request):
    if not require_student(request):
        return RedirectResponse("/login", status_code=303)

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT quiz_id, title FROM quizzes")
    quizzes = cur.fetchall()

    cur.close()
    conn.close()

    return templates.TemplateResponse(
        "quiz.html",
        {"request": request, "quizzes": quizzes}
    )
@app.get("/start_quiz/{quiz_id}", response_class=HTMLResponse)
def start_quiz(request: Request, quiz_id: int):

    if request.session.get("role") != "student":
        return RedirectResponse("/login", status_code=303)

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Get quiz
    cur.execute("SELECT title FROM quizzes WHERE quiz_id=%s", (quiz_id,))
    quiz = cur.fetchone()

    if not quiz:
        cur.close()
        conn.close()
        return HTMLResponse("Quiz not found", status_code=404)

    # Get questions (FIXED COLUMN NAME)
    cur.execute("""
        SELECT question_id,
               question_text,
               option_a,
               option_b,
               option_c,
               option_d
        FROM questions
        WHERE quiz_id=%s
    """, (quiz_id,))

    questions = cur.fetchall()

    cur.close()
    conn.close()

    return templates.TemplateResponse(
        "start_quiz.html",
        {
            "request": request,
            "quiz": quiz,
            "questions": questions,
            "quiz_id": quiz_id
        }
    )
@app.post("/submit_quiz/{quiz_id}")
async def submit_quiz(request: Request, quiz_id: int):

    if request.session.get("role") != "student":
        return RedirectResponse("/login", status_code=303)

    form = await request.form()

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Get quiz title
    cur.execute("SELECT title FROM quizzes WHERE quiz_id=%s", (quiz_id,))
    quiz = cur.fetchone()
    quiz_title = quiz["title"] if quiz else "Quiz"

    # Get questions
    cur.execute("""
        SELECT question_id,
               question_text,
               option_a,
               option_b,
               option_c,
               option_d,
               correct_option
        FROM questions
        WHERE quiz_id=%s
    """, (quiz_id,))

    questions = cur.fetchall()

    results = []
    score = 0

    for q in questions:
        selected = form.get(f"q{q['question_id']}")
        correct = q["correct_option"]

        if selected == correct:
            score += 1

        results.append({
            "question": q["question_text"],
            "option_a": q["option_a"],
            "option_b": q["option_b"],
            "option_c": q["option_c"],
            "option_d": q["option_d"],
            "selected": selected,
            "correct": correct
        })

    student_id = request.session["student_id"]

    # ✅ Save score
    cur.execute("""
        INSERT INTO results (student_id, quiz_id, score)
        VALUES (%s, %s, %s)
    """, (student_id, quiz_id, score))

    # ✅ Log activity
    cur.execute("""
        INSERT INTO student_activity (student_id, activity_type, description)
        VALUES (%s, 'quiz', %s)
    """, (student_id, f"Completed {quiz_title} (Score: {score})"))

    conn.commit()
    cur.close()
    conn.close()

    return templates.TemplateResponse(
        "quiz_result.html",
        {
            "request": request,
            "score": score,
            "total": len(questions),
            "results": results
        }
    )





@app.get("/flashcard", response_class=HTMLResponse)
def flashcards(request: Request):

    if not require_student(request):
        return RedirectResponse("/login", status_code=303)

    student_id = request.session["student_id"]

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Get flashcards
    cur.execute("SELECT flashcard_id, topic, content FROM flashcards")
    flashcards = cur.fetchall()

    # ✅ Log activity (only once per visit)
    cur.execute("""
        INSERT INTO student_activity (student_id, activity_type, description)
        VALUES (%s, 'flashcard', 'Viewed flashcards')
    """, (student_id,))

    conn.commit()

    cur.close()
    conn.close()

    return templates.TemplateResponse(
        "flashcard.html",
        {"request": request, "flashcards": flashcards}
    )



@app.get("/progress", response_class=HTMLResponse)
def progress(request: Request):

    if not require_student(request):
        return RedirectResponse("/login", status_code=303)

    student_id = request.session["student_id"]
    MAX_SCORE = 5

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Quizzes completed
    cur.execute("""
        SELECT COUNT(DISTINCT quiz_id) AS total
        FROM results
        WHERE student_id=%s
    """, (student_id,))
    quizzes_completed = cur.fetchone()["total"]

    # Average score
    cur.execute("""
        SELECT COALESCE(AVG(score),0) AS avg_score
        FROM results
        WHERE student_id=%s
    """, (student_id,))
    avg_raw = cur.fetchone()["avg_score"]
    avg_score = round((avg_raw / MAX_SCORE) * 100, 1) if avg_raw else 0

    # Perfect scores
    cur.execute("""
        SELECT COUNT(*) AS perfect
        FROM results
        WHERE student_id=%s AND score=%s
    """, (student_id, MAX_SCORE))
    perfect_scores = cur.fetchone()["perfect"]

    # Course progress (example logic)
    progress_percent = min(quizzes_completed * 20, 100)

    # Recent activity
    cur.execute("""
        SELECT activity_type, description, created_at
        FROM student_activity
        WHERE student_id=%s
        ORDER BY created_at DESC
        LIMIT 5
    """, (student_id,))
    recent_activity = cur.fetchall()

    cur.close()
    conn.close()

    return templates.TemplateResponse(
        "progress.html",
        {
            "request": request,
            "quizzes_completed": quizzes_completed,
            "avg_score": avg_score,
            "perfect_scores": perfect_scores,
            "progress_percent": progress_percent,
            "recent_activity": recent_activity
        }
    )
@app.get("/help", response_class=HTMLResponse)
def help_page(request: Request):
    return templates.TemplateResponse("help.html", {"request": request})



# ======================================================
# ================= ADMIN PANEL ========================
# ======================================================

@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    if request.session.get("role") != "admin":
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "name": request.session["admin_name"]
        }
    )

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
        request.session["admin_id"] = admin["admin_id"]
        request.session["admin_name"] = admin["name"]
        return RedirectResponse("/admin/dashboard", status_code=303)


    return templates.TemplateResponse(
        "admin_login.html",
        {"request": request, "error": "Invalid admin credentials"}
    )

@app.get("/admin/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    if "admin_id" not in request.session:
        return RedirectResponse("/admin", status_code=303)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM quizzes")
    total_quizzes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM programs")
    total_programs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM flashcards")
    total_flashcards = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return templates.TemplateResponse(
        "admin_dashboard.html",
        {
            "request": request,
            "admin": request.session["admin_name"],
            "total_quizzes": total_quizzes,
            "total_programs": total_programs,
            "total_flashcards": total_flashcards,
            "total_students": total_students
        }
    )


@app.get("/admin/logout")
def admin_logout(request: Request):
    request.session.clear()
    return RedirectResponse("/admin", status_code=303)

#ADMIN LOGIC

#Admin View Programs
@app.get("/admin/programs", response_class=HTMLResponse)
def admin_programs(request: Request):
    if "admin_id" not in request.session:
        return RedirectResponse("/admin", status_code=303)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM programs")
    programs = cursor.fetchall()

    cursor.close()
    conn.close()

    return templates.TemplateResponse(
        "admin_programs.html",
        {"request": request, "programs": programs}
    )

# Admin Add Program
@app.get("/admin/add_program", response_class=HTMLResponse)
def add_program_page(request: Request):
    if "admin_id" not in request.session:
        return RedirectResponse("/admin", status_code=303)

    return templates.TemplateResponse("add_program.html", {"request": request})


@app.post("/admin/add_program")
def add_program(
    request: Request,
    title: str = Form(...),
    language: str = Form(...),
    topic: str = Form(...),
    keywords: str = Form(...),
    code_snippet: str = Form(...)
):
    if "admin_id" not in request.session:
        return RedirectResponse("/admin", status_code=303)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO programs (title, language, topic, keywords, code_snippet, created_by)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (title, language, topic, keywords, code_snippet, request.session["admin_id"]))

    conn.commit()
    cursor.close()
    conn.close()

    return RedirectResponse("/admin/programs", status_code=303)

# Admin Add Quiz
@app.get("/admin/add_quiz", response_class=HTMLResponse)
def add_quiz_page(request: Request):
    if "admin_id" not in request.session:
        return RedirectResponse("/admin", status_code=303)

    return templates.TemplateResponse("add_quiz.html", {"request": request})


@app.post("/admin/add_quiz")
def add_quiz(
    request: Request,
    title: str = Form(...)
):
    if "admin_id" not in request.session:
        return RedirectResponse("/admin", status_code=303)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO quizzes (title, created_by) VALUES (%s,%s)",
        (title, request.session["admin_id"])
    )

    conn.commit()
    cursor.close()
    conn.close()

    return RedirectResponse("/admin/dashboard", status_code=303)

# Admin add Question to Quiz
@app.get("/admin/add_question/{quiz_id}", response_class=HTMLResponse)
def add_question_page(request: Request, quiz_id: int):
    if "admin_id" not in request.session:
        return RedirectResponse("/admin", status_code=303)

    return templates.TemplateResponse(
        "add_question.html",
        {"request": request, "quiz_id": quiz_id}
    )


@app.post("/admin/add_question/{quiz_id}")
def add_question(
    request: Request,
    quiz_id: int,
    question_text: str = Form(...),
    correct_option: str = Form(...),
    option_a: str = Form(...),
    option_b: str = Form(...),
    option_c: str = Form(...),
    option_d: str = Form(...)
):
    if "admin_id" not in request.session:
        return RedirectResponse("/admin", status_code=303)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO questions 
        (quiz_id, question_text, correct_option, option_a, option_b, option_c, option_d)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (quiz_id, question_text, correct_option, option_a, option_b, option_c, option_d))

    conn.commit()
    cursor.close()
    conn.close()

    return RedirectResponse("/admin/dashboard", status_code=303)

# Admin Add Flashcard
@app.get("/admin/add_flashcard", response_class=HTMLResponse)
def add_flashcard_page(request: Request):
    if "admin_id" not in request.session:
        return RedirectResponse("/admin", status_code=303)

    return templates.TemplateResponse("add_flashcard.html", {"request": request})


@app.post("/admin/add_flashcard")
def add_flashcard(
    request: Request,
    topic: str = Form(...),
    content: str = Form(...)
):
    if "admin_id" not in request.session:
        return RedirectResponse("/admin", status_code=303)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO flashcards (topic, content, created_by)
        VALUES (%s,%s,%s)
    """, (topic, content, request.session["admin_id"]))

    conn.commit()
    cursor.close()
    conn.close()

    return RedirectResponse("/admin/dashboard", status_code=303)
