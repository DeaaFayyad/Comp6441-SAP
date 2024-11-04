from flask import Flask, render_template, request, redirect, url_for
from markupsafe import Markup
from password_checker import (
    check_length,
    check_char_types,
    is_common_password,
)
import sqlite3
from datetime import datetime

app = Flask(__name__, static_folder="../static", template_folder="../templates")


# Initialize the database
def init_db():
    conn = sqlite3.connect("site_data.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY, 
            title TEXT, 
            content TEXT, 
            date TEXT
        )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS blog (
            id INTEGER PRIMARY KEY, 
            title TEXT, 
            content TEXT, 
            date TEXT
        )"""
    )
    conn.commit()
    conn.close()


# Call the init_db function to create tables if they don't exist
init_db()


# Database functions for news
def add_news(title, content, date):
    conn = sqlite3.connect("site_data.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO news (title, content, date) VALUES (?, ?, ?)",
        (title, content, date),
    )
    conn.commit()
    conn.close()


def get_news():
    conn = sqlite3.connect("site_data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM news ORDER BY date DESC")
    news = c.fetchall()
    conn.close()
    return news


# Database functions for blogs
def add_blog(title, content, date):
    conn = sqlite3.connect("site_data.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO blog (title, content, date) VALUES (?, ?, ?)",
        (title, content, date),
    )
    conn.commit()
    conn.close()


def get_blog():
    conn = sqlite3.connect("site_data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM blog ORDER BY date DESC")
    blogs = c.fetchall()
    conn.close()
    return blogs


# Route for the index page
@app.route("/", methods=["GET", "POST"])
def index():
    feedback = []
    if request.method == "POST":
        password = request.form.get("password")
        if not check_length(password):
            feedback.append("Password should be at least 8 characters long.")
        if not check_char_types(password):
            feedback.append(
                "Password should contain uppercase, lowercase, numbers, and symbols."
            )
        if is_common_password(password):
            feedback.append("Password is too common; choose a more unique password.")
        if not feedback:
            feedback.append("Password is strong!")
    return render_template("index.html", feedback=feedback)


# Route for the news page with persistent storage
@app.route("/news", methods=["GET", "POST"])
def news():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        date = datetime.now().strftime("%Y-%m-%d")
        if title and content:
            add_news(title, content, date)
        return redirect(url_for("news"))

    articles = get_news()
    return render_template("news.html", articles=articles)


# Jinja2 filter for truncating text
@app.template_filter()
def truncate(value, length=100):
    if len(value) > length:
        return value[:length] + "..."
    return value


app.jinja_env.filters["truncate"] = truncate


# Route for detailed news view
@app.route("/news/<int:index>")
def news_detail(index):
    conn = sqlite3.connect("site_data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM news WHERE id = ?", (index,))
    article = c.fetchone()
    conn.close()
    if article:
        return render_template("news_detail.html", article=article)
    return redirect(url_for("news"))  # Redirect if article not found


# Route to delete a news article
@app.route("/news/delete/<int:id>", methods=["POST"])
def delete_news(id):
    conn = sqlite3.connect("site_data.db")
    c = conn.cursor()
    c.execute("DELETE FROM news WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("news"))


# Route for the blog page with persistent storage
@app.route("/blog", methods=["GET", "POST"])
def blog():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        date = datetime.now().strftime("%Y-%m-%d")
        if title and content:
            add_blog(title, content, date)
        return redirect(url_for("blog"))

    posts = get_blog()
    return render_template("blog.html", posts=posts)


# Route to delete a blog post
@app.route("/blog/delete/<int:id>", methods=["POST"])
def delete_blog(id):
    conn = sqlite3.connect("site_data.db")
    c = conn.cursor()
    c.execute("DELETE FROM blog WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("blog"))


# Route for the analysis page
@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


if __name__ == "__main__":
    app.run(debug=True)
