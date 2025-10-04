import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure database
def get_db_connection():
    """ Connect to SQLite database """
    conn = sqlite3.connect('bomanis_vaut.db')
    conn.row_factory = sqlite3.Row # dicktionary-like access to rows
    return conn


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    """Show homepage"""
    return render_template("index.html")

# Run the application if executed directly
if __name__ == "__main__":
    app.run(debug=True)
