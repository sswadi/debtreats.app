import functools
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db, get_user_by_email

app = Flask(__name__)
app.secret_key = "dev-secret-change-in-prod"


def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please sign in to continue.", "info")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    if request.method == "GET":
        return render_template("register.html")

    name     = request.form.get("name", "").strip()
    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name or not email or not password:
        return render_template("register.html", error="All fields are required.")
    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.")

    db = get_db()
    existing = db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        db.close()
        return render_template("register.html", error="An account with that email already exists.")

    password_hash = generate_password_hash(password)
    cursor = db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash),
    )
    db.commit()
    db.close()

    session["user_id"]   = cursor.lastrowid
    session["user_name"] = name
    flash(f"Welcome, {name}! Your account has been created.", "success")
    return redirect(url_for("profile"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    if request.method == "GET":
        return render_template("login.html")

    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template("login.html", error="All fields are required.")

    user = get_user_by_email(email)
    if not user or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.")

    session["user_id"]   = user["id"]
    session["user_name"] = user["name"]
    flash(f"Welcome back, {user['name']}!", "success")
    return redirect(url_for("profile"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("login"))


@app.route("/profile")
@login_required
def profile():
    user = {
        "name": "Alex Mercer",
        "email": "alex@example.com",
        "member_since": "January 2024",
        "initials": "AM",
    }
    stats = {
        "total_spent": "$1,284.50",
        "transaction_count": 24,
        "top_category": "Food & Drink",
    }
    transactions = [
        {"date": "May 14, 2026", "description": "Whole Foods Market",   "category": "Food & Drink",  "badge_class": "badge-food",          "amount": "$87.32"},
        {"date": "May 10, 2026", "description": "Uber ride",            "category": "Transport",     "badge_class": "badge-transport",     "amount": "$14.50"},
        {"date": "May 8, 2026",  "description": "Netflix subscription", "category": "Entertainment", "badge_class": "badge-entertainment", "amount": "$15.99"},
        {"date": "May 5, 2026",  "description": "Electric bill",        "category": "Bills",         "badge_class": "badge-bills",         "amount": "$112.00"},
        {"date": "May 2, 2026",  "description": "Trader Joe's",         "category": "Food & Drink",  "badge_class": "badge-food",          "amount": "$63.45"},
    ]
    categories = [
        {"name": "Food & Drink",  "amount": "$432.80", "bar_class": "bar-food bar-w-34"},
        {"name": "Bills",         "amount": "$312.00", "bar_class": "bar-bills bar-w-24"},
        {"name": "Transport",     "amount": "$198.50", "bar_class": "bar-transport bar-w-15"},
        {"name": "Entertainment", "amount": "$156.20", "bar_class": "bar-entertainment bar-w-12"},
    ]
    return render_template("profile.html", user=user, stats=stats,
                           transactions=transactions, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
