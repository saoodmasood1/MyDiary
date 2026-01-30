import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import analyze_mood

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# --- REPLACEMENT FOR CS50 SQL ---
def db_execute(query, *args):
    """Helper function to execute SQLite queries without the CS50 library"""
    with sqlite3.connect("diary.db") as conn:
        conn.row_factory = sqlite3.Row  # Allows accessing columns by name like a dictionary
        db = conn.cursor()
        db.execute(query, args)
        if query.strip().upper().startswith("SELECT"):
            # Return a list of dicts to match CS50's style
            return [dict(row) for row in db.fetchall()]
        conn.commit()
        return db.lastrowid

@app.route("/")
def index():
    if not session.get("user_id"):
        return redirect("/login")
    
    # Use db_execute instead of db.execute
    entries = db_execute("SELECT primary_mood FROM entries WHERE user_id = ?", session["user_id"])
    total = len(entries)
    
    mood_stats = {}
    if total > 0:
        counts = {}
        for row in entries:
            m = row["primary_mood"]
            counts[m] = counts.get(m, 0) + 1
        for m, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            mood_stats[m] = round((count / total) * 100)

    return render_template("index.html", total=total, mood_stats=mood_stats)

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")
        rows = db_execute("SELECT * FROM users WHERE username = ?", u)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], p):
            return render_template("login.html", error="Invalid Credentials")
        
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        return redirect("/")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")
        if not u or not p:
            return render_template("register.html", error="Required Fields Missing")
        try:
            db_execute("INSERT INTO users (username, hash) VALUES (?, ?)", u, generate_password_hash(p))
            return redirect("/login")
        except sqlite3.IntegrityError:
            return render_template("register.html", error="Username Taken")
    return render_template("register.html")

@app.route("/write", methods=["GET", "POST"])
def write():
    if not session.get("user_id"): return redirect("/login")
    if request.method == "POST":
        t, c = request.form.get("title"), request.form.get("content")
        analysis = analyze_mood(c)
        db_execute("INSERT INTO entries (user_id, title, content, primary_mood, confidence) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], t, c, analysis["primary_mood"], analysis["confidence"])
        return redirect("/entries")
    return render_template("write.html")

@app.route("/entries")
def entries():
    if not session.get("user_id"): return redirect("/login")
    rows = db_execute("SELECT * FROM entries WHERE user_id = ? ORDER BY entry_date DESC", session["user_id"])
    return render_template("entries.html", entries=rows)

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if not session.get("user_id"): return redirect("/login")
    db_execute("DELETE FROM entries WHERE id = ? AND user_id = ?", id, session["user_id"])
    return redirect("/entries")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")