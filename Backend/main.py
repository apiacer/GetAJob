import os
import sys
import sqlite3
import datetime
from flask import Flask, render_template, request, jsonify

# keep repo root templates/static layout
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.urandom(24)

# ---------- SQLite helpers ----------
DB_PATH = os.path.join(os.path.dirname(__file__), "jobs.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Ensure ON DELETE CASCADE works as expected
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            location TEXT NOT NULL,
            availability_morning INTEGER NOT NULL DEFAULT 0,
            availability_afternoon INTEGER NOT NULL DEFAULT 0,
            availability_evening INTEGER NOT NULL DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS job_tags (
            job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
            tag TEXT NOT NULL,
            PRIMARY KEY(job_id, tag)
        )
    """)
    conn.commit()
    conn.close()

def _get_tags(conn, job_id:int):
    rows = conn.execute("SELECT tag FROM job_tags WHERE job_id=?", (job_id,)).fetchall()
    return [r["tag"] for r in rows]


def _job_row(conn, r):
    return {
        "id": r["id"],
        "title": r["title"],
        "description": r["description"],
        "location": r["location"],
        "availability": {
            "morning": bool(r["availability_morning"]),
            "afternoon": bool(r["availability_afternoon"]),
            "evening": bool(r["availability_evening"]),
        },
        "tags": _get_tags(conn, r["id"]),
        "createdAt": r["created_at"],
        "updatedAt": r["updated_at"],
    }


# initialize tables at import time
init_db()

# ---------- HTML routes already in project ----------
@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/login', methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        # demo prints
        print(f"user name: {request.form.get('username')}")
        print(f"password: {request.form.get('password')}")
    return render_template('login.html', title='login')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/account')
def account():
    return render_template('account.html', title='Account')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        print(f"name: {request.form.get('name')}")
        print(f"email: {request.form.get('email')}")
        print(f"password: {request.form.get('password')}")
    return render_template('signup.html', title='Sign Up')

# demo data for legacy /jobs template
JOB_DATA = [
    {"id": 1, "title": "Frontend Developer", "description": "Build UI with HTML/CSS/JS."},
    {"id": 2, "title": "Backend Developer", "description": "APIs with Python + Flask."},
    {"id": 3, "title": "Data Analyst", "description": "SQL, charts, and insights."},
    {"id": 4, "title": "UX Designer", "description": "Design flows and prototypes."},
]

@app.route('/jobs')
def jobs():
    q = request.args.get('q', '').strip().lower()
    jobs = JOB_DATA
    if q:
        jobs = [j for j in JOB_DATA
                if q in j["title"].lower() or q in j["description"].lower()]

    return render_template('jobs.html', jobs=jobs, title='Jobs')

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    job = next((j for j in JOB_DATA if j["id"] == job_id), None)
    if not job:
        return render_template('404.html'), 404
    # Minimal detail page for now:
    return f"<h1>{job['title']}</h1><p>{job['description']}</p>"

@app.route('/create-listing', methods=["GET", "POST"])
def create_listing():
    return "<h1>Create Listing (coming soon)</h1>"

@app.route('/maps')
def maps():
    # demo data — replace with DB rows (id, title, description, lat, lng, location, type)
    jobs = [
        {"id": 101, "title": "Barista", "description": "Morning shift near Midtown.",
        "lat": 38.571, "lng": -121.486, "location":"Midtown, Sacramento", "type":"Part-time"},
        {"id": 102, "title": "Front Desk", "description": "Evening shift, downtown.",
        "lat": 38.581, "lng": -121.494, "location":"Downtown", "type":"Full-time"},
        {"id": 103, "title": "Prep Cook", "description": "Kitchen support role.",
        "lat": 38.563, "lng": -121.442, "location":"East Sac", "type":"Part-time"},
    ]
    return render_template('maps.html', jobs=jobs, title='Maps')

# ---------- JSON API for SPA ----------
@app.route("/api/jobs", methods=["GET"])
def api_list_jobs():
    q = request.args.get("q", "").strip()
    conn = get_db()
    if q:
        like = f"%{q}%"
        rows = conn.execute(
            """SELECT * FROM jobs
            WHERE title LIKE ? OR description LIKE ? OR location LIKE ?
            ORDER BY created_at DESC""",
            (like, like, like),
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM jobs ORDER BY created_at DESC").fetchall()

    data = [_job_row(conn, r) for r in rows]
    conn.close()
    return jsonify(data), 200


@app.route("/api/jobs/<int:job_id>", methods=["GET"])
def api_get_job(job_id):
    conn = get_db()
    r = conn.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
    if not r:
        conn.close()
        return jsonify({"error": "not found"}), 404
    data = _job_row(conn, r)
    conn.close()
    return jsonify(data), 200


@app.route("/api/jobs", methods=["POST"])
def api_create_job():
    data = request.get_json(force=True) or {}
    title = (data.get("title") or "").strip()
    description = (data.get("description") or "").strip()
    location = (data.get("location") or "").strip()
    availability = data.get("availability") or {}
    tags = data.get("tags") or []

    if not title or not description or not location:
        return jsonify({"error": "title, description, location are required"}), 400

    am = 1 if availability.get("morning") else 0
    pm = 1 if availability.get("afternoon") else 0
    eve = 1 if availability.get("evening") else 0

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO jobs(title, description, location,
                            availability_morning, availability_afternoon, availability_evening)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (title, description, location, am, pm, eve),
    )
    job_id = cur.lastrowid
    # write tags
    for t in {str(t).strip() for t in tags if str(t).strip()}:
        cur.execute("INSERT OR IGNORE INTO job_tags(job_id, tag) VALUES (?, ?)", (job_id, t))
    conn.commit()

    r = conn.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
    out = _job_row(conn, r)
    conn.close()
    return jsonify(out), 201


@app.route("/api/jobs/<int:job_id>", methods=["PUT"])
def api_update_job(job_id):
    data = request.get_json(force=True) or {}
    fields, vals = [], []

    def set_field(col, val):
        fields.append(f"{col}=?")
        vals.append(val)

    if "title" in data:
        set_field("title", (data["title"] or "").strip())
    if "description" in data:
        set_field("description", (data["description"] or "").strip())
    if "location" in data:
        set_field("location", (data["location"] or "").strip())
    if "availability" in data:
        avail = data["availability"] or {}
        set_field("availability_morning", 1 if avail.get("morning") else 0)
        set_field("availability_afternoon", 1 if avail.get("afternoon") else 0)
        set_field("availability_evening", 1 if avail.get("evening") else 0)

    if fields:
        set_field("updated_at", datetime.datetime.utcnow().isoformat(sep=" ", timespec="seconds"))
    vals.append(job_id)

    conn = get_db()
    cur = conn.cursor()
    # verify exists
    if not cur.execute("SELECT 1 FROM jobs WHERE id=?", (job_id,)).fetchone():
        conn.close()
        return jsonify({"error": "not found"}), 404

    if fields:
        cur.execute(f"UPDATE jobs SET {', '.join(fields)} WHERE id=?", tuple(vals))

    # replace tags if provided
    if "tags" in data:
        cur.execute("DELETE FROM job_tags WHERE job_id=?", (job_id,))
        for t in {str(t).strip() for t in (data.get("tags") or []) if str(t).strip()}:
            cur.execute("INSERT OR IGNORE INTO job_tags(job_id, tag) VALUES (?, ?)", (job_id, t))

    conn.commit()
    r = cur.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
    out = _job_row(conn, r)
    conn.close()
    return jsonify(out), 200


@app.route("/api/jobs/<int:job_id>", methods=["DELETE"])
def api_delete_job(job_id):
    conn = get_db()
    cur = conn.cursor()
    res = cur.execute("DELETE FROM jobs WHERE id=?", (job_id,))
    conn.commit()
    conn.close()
    if res.rowcount == 0:
        return jsonify({"error": "not found"}), 404
    return jsonify({"ok": True}), 200


if __name__ == '__main__':
    app.run(debug=True)
