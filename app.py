from flask import Flask, render_template, request, redirect
import sqlite3
import os
import psycopg2

app = Flask(__name__)


# Home page
@app.route("/")
def home():
	return render_template("home.html")


# About page
@app.route("/about")
def about():
	return render_template("about.html")


# Contact page
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )
        conn.commit()
        conn.close()

        return render_template("contact.html", success=True)

    return render_template("contact.html", success=False)

# Admin page to view messages
@app.route("/admin")
def admin():
    if request.args.get("key") != "secret123":
        return "Unauthorized", 403

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM messages")
    messages = c.fetchall()
    conn.close()

    return render_template("admin.html", messages=messages)

if __name__ == "__main__":
	app.run()
