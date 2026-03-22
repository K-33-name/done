from flask import Flask, render_template, request, redirect, session
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY


def get_db():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        port=Config.DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == "POST":
        data = request.form

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO users
            (name, email, university, class, age, mobile, password)
            VALUES (%s,%s,%s,%s,%s,%s,%s)""",
            (
                data["name"],
                data["email"],
                data["university"],
                data["class"],
                data["age"],
                data["mobile"],
                generate_password_hash(data["password"])
            )
        )

        conn.commit()
        conn.close()

        return redirect("/log")

    return render_template("reg.html")


@app.route("/log", methods=["GET", "POST"])
def log():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user"] = user
            return redirect("/dash")

        return render_template("log.html", error="Invalid login")

    return render_template("log.html")


@app.route("/dash")
def dash():
    if "user" not in session:
        return redirect("/log")

    return render_template("dash.html", user=session["user"])


@app.route("/out")
def out():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)