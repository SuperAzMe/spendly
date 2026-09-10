import os
import re

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash

from database.db import create_user, get_db, get_user_by_email, init_db, seed_db

app = Flask(__name__)
app.secret_key = os.environ.get("SPENDLY_SECRET_KEY", "dev-secret-key-change-in-production")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    error = None
    password_mismatch = False
    if not name:
        error = "Name is required."
    elif not email or not EMAIL_RE.match(email):
        error = "Enter a valid email address."
    elif len(password) < 8:
        error = "Password must be at least 8 characters."
    elif password != confirm_password:
        error = "Passwords do not match."
        password_mismatch = True
    elif get_user_by_email(email) is not None:
        error = "Account already exists."

    if error:
        return render_template(
            "register.html",
            error=error,
            name=name,
            email=email,
            password_mismatch=password_mismatch,
        ), 400

    password_hash = generate_password_hash(password)
    create_user(name, email, password_hash)
    flash("Account created successfully. Please sign in.", "success")
    return redirect(url_for("login"))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    return "Logout — coming in Step 3"


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


with app.app_context():
    init_db()
    seed_db()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
