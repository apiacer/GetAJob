from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import datetime
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/login', methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
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

# demo data (swap for DB later)
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
    # placeholder—you can render a form here later
    return "<h1>Create Listing (coming soon)</h1>"

from flask import render_template

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


if __name__ == '__main__':
    app.run(debug=True)
