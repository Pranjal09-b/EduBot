from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_connection

app = Flask(__name__)
app.secret_key = "edubot_secret_key"   # Change later


# ======================================================
# LOGIN PAGE
# ======================================================
@app.route("/")
def login():
    return render_template("login.html")


# ======================================================
# LOGIN POST (Form Submit)
# ======================================================
@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ Check student by email
    cursor.execute("SELECT * FROM students WHERE email=%s", (email,))
    student = cursor.fetchone()

    cursor.close()
    conn.close()

    # ✅ Password verification
    if student and check_password_hash(student["password_hash"], password):
        session["student"] = student["name"]
        return redirect(url_for("home"))

    # ❌ Incorrect password/email
    return "❌ Incorrect Email or Password"


# ======================================================
# REGISTER PAGE
# ======================================================
@app.route("/register")
def register():
    return render_template("register.html")


# ======================================================
# REGISTER POST
# ======================================================
@app.route("/register", methods=["POST"])
def register_post():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    hashed_password = generate_password_hash(password)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # ✅ Insert into students table
        cursor.execute(
            "INSERT INTO students (name, email, password_hash) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        conn.commit()

    except:
        cursor.close()
        conn.close()
        return "❌ Email already exists!"

    cursor.close()
    conn.close()

    return redirect(url_for("login"))


# ======================================================
# HOME PAGE
# ======================================================
@app.route("/home")
def home():
    if "student" not in session:
        return redirect(url_for("login"))

    return render_template("home.html")


# ======================================================
# CHATBOT PAGE
# ======================================================
@app.route("/chat")
def chat():
    if "student" not in session:
        return redirect(url_for("login"))

    return render_template("chat.html")


# ======================================================
# QUIZ PAGE
# ======================================================
@app.route("/quiz")
def quiz():
    if "student" not in session:
        return redirect(url_for("login"))

    return render_template("quiz.html")


# ======================================================
# FLASHCARD PAGE
# ======================================================
@app.route("/flashcard")
def flashcard():
    if "student" not in session:
        return redirect(url_for("login"))

    return render_template("flashcard.html")


# ======================================================
# PROGRAM PAGE
# ======================================================
@app.route("/program")
def program():
    if "student" not in session:
        return redirect(url_for("login"))

    return render_template("program.html")


# ======================================================
# PROGRESS PAGE
# ======================================================
@app.route("/progress")
def progress():
    if "student" not in session:
        return redirect(url_for("login"))

    return render_template("progress.html")


# ======================================================
# LOGOUT
# ======================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ======================================================
# RUN SERVER
# ======================================================
if __name__ == "__main__":
    app.run(debug=True)
