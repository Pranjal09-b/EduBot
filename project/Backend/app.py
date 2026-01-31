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
    username = request.form["username"]
    password = request.form["password"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    # Check password
    if user and check_password_hash(user["password"], password):
        session["user"] = username
        return redirect(url_for("home"))

    return "❌ Invalid Username or Password"


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
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    hashed_password = generate_password_hash(password)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        conn.commit()

    except:
        cursor.close()
        conn.close()
        return "❌ Username already exists!"

    cursor.close()
    conn.close()

    return redirect(url_for("login"))


# ======================================================
# HOME PAGE
# ======================================================
@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("home.html")


# ======================================================
# CHATBOT PAGE
# ======================================================
@app.route("/chat")
def chat():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("chat.html")


# ======================================================
# QUIZ PAGE
# ======================================================
@app.route("/quiz")
def quiz():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("quiz.html")


# ======================================================
# FLASHCARD PAGE
# ======================================================
@app.route("/flashcard")
def flashcard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("flashcard.html")


# ======================================================
# PROGRAM PAGE
# ======================================================
@app.route("/program")
def program():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("program.html")


# ======================================================
# PROGRESS PAGE
# ======================================================
@app.route("/progress")
def progress():
    if "user" not in session:
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
