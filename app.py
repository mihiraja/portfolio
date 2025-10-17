from flask import Flask, render_template, abort, request, redirect, url_for, flash
import json, os
from slugify import slugify
from markdown import markdown

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-key-change-me")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def load_json(name):
    path = os.path.join(DATA_DIR, f"{name}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_projects():
    projects = load_json("projects")
    for p in projects:
        p.setdefault("slug", slugify(p.get("title","")))
    return projects

def get_posts():
    posts = load_json("posts")
    for p in posts:
        p.setdefault("slug", slugify(p.get("title","")))
        p["html"] = markdown(p.get("content",""))
    return posts

@app.context_processor
def inject_globals():
    meta = load_json("site")
    return {"site": meta}

@app.route("/")
def home():
    return render_template("index.html", projects=get_projects()[:3], posts=get_posts()[:2])

@app.route("/projects")
def projects():
    return render_template("projects.html", projects=get_projects())

@app.route("/projects/<slug>")
def project_detail(slug):
    for p in get_projects():
        if p["slug"] == slug:
            return render_template("project_detail.html", project=p)
    abort(404)

@app.route("/blog")
def blog():
    return render_template("blog.html", posts=get_posts())

@app.route("/blog/<slug>")
def blog_post(slug):
    for p in get_posts():
        if p["slug"] == slug:
            return render_template("blog_post.html", post=p)
    abort(404)

@app.post("/contact")
def contact():
    name = request.form.get("name","").strip()
    email = request.form.get("email","").strip()
    message = request.form.get("message","").strip()
    if not name or not email or not message:
        flash("Please fill out all fields.", "error")
        return redirect(url_for("home") + "#contact")
    inbox_path = os.path.join(DATA_DIR, "messages.jsonl")
    with open(inbox_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({"name": name, "email": email, "message": message}) + "\n")
    flash("Thanks! Your message has been received.", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)