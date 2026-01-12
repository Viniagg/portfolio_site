from flask import Flask, render_template, request, redirect
import os
import psycopg2

conn = psycopg2.connect(os.environ["DATABASE_URL"])
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT,
    message TEXT
)
""")

conn.commit()
cur.close()
conn.close()
app = Flask(__name__)
conn = psycopg2.connect(os.environ["DATABASE_URL"])
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT,
    message TEXT
)
""")

conn.commit()
cur.close()
conn.close()

# Home page
@app.route("/")
def home():
	return render_template("home.html")


# About page
@app.route("/about")
def about():
	return render_template("about.html")

def get_db_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))
	
# Contact page
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO messages (name, email, message)
            VALUES (%s, %s, %s)
            """,
            (name, email, message)
        )
        conn.commit()
        cur.close()
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
