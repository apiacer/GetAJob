from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from db import Database_api
import os
import re
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# test data
JOB_DATA = [
    {"id": 1, "title": "Frontend Developer", "description": "Build UI with HTML/CSS/JS."},
    {"id": 2, "title": "Backend Developer", "description": "APIs with Python + Flask."},
    {"id": 3, "title": "Data Analyst", "description": "SQL, charts, and insights."},
    {"id": 4, "title": "UX Designer", "description": "Design flows and prototypes."},
]

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
db = Database_api()
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.urandom(24)
# demo data (swap for DB later)


@app.route('/')
def home():
    return render_template('index.html', title='Home')
    
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_name = request.form.get('username')
        password = request.form.get('password')
        res = db.user.verify_password(user_name, password)
        if res[0]:
            # add to session
            return redirect()

        else:
            pass

    return render_template('login.html', title='login')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/account')
def account():
    return render_template('account.html', title='Account')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Basic field check
        if not all([fname, lname, username, email, password]):
            flash('All fields are required.', 'error')
            return redirect(url_for('signup'))

        # Call your db layer
        success, msg = db.user.create_account(username, password, email, fname, lname)

        if not success:
            flash(msg, 'error')
            return redirect(url_for('signup'))

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/check_username')
def check_username():
    username = request.args.get('username')

    conn = sqlite3.connect('test.db') # connect to database
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM user WHERE user_name = ?", (username,))  # table: user, column: user_name
    exists = cur.fetchone() is not None

    conn.close()
    return jsonify({"exists": exists})


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

@app.route('/dashboard')
def signedin():
    # Later, you could check if a user is logged in here
    # Example: if not session.get("user_id"): return redirect("/login")
    return render_template('signedin.html', title='Dashboard')

@app.route('/create-listing', methods=["GET", "POST"])
def create_listing():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        print(f"New Job Listing → Title: {title}, Description: {description}")
        # later: save to database
        flash("Job listing created successfully!", "success")
        return redirect("/jobs")
    return render_template("create_listing.html", title="Create Listing")

@app.route('/notifications')
def notifications():
    notifications = [
        "You have a new message about your application to Job #2.",
        "Your job listing #11 was approved."
    ]
    return render_template('notifications.html', notifications=notifications, title='Notifications')

@app.route('/messaging', methods=["GET", "POST"])
def messaging():
    # Fake in-memory message list (replace with DB later)
    messages = [
        {"sender": "Employer", "text": "Hi, are you available for an interview?"}
    ]

    if request.method == "POST":
        new_msg = request.form.get("message")
        if new_msg:
            messages.append({"sender": "You", "text": new_msg})
            flash("Message sent!", "success")
            # In a real app, you'd save it to a database here

    return render_template("messaging.html", messages=messages, title="Messages")

@app.route('/admin')
def admin():
    # Later, you could restrict access:
    # if not session.get("is_admin"): return redirect("/")
    return render_template('admin.html', title='Admin Panel')


if __name__ == '__main__':
    app.run(debug=True)
