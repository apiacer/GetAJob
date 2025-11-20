from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from db import Database_api, DB_PATH
import os
import math

# test data
JOB_DATA = [
    {"title": "Frontend Developer", "description": "Build UI with HTML/CSS/JS.", "owner_id": "2", "location": "1300 65th St"},
    {"title": "Backend Developer", "description": "APIs with Python + Flask.", "owner_id": "2", "location": "1300 65th St"},
    {"title": "Data Analyst", "description": "SQL, charts, and insights.", "owner_id": "3", "location": "1305 64th St"},
    {"title": "UX Designer", "description": "Design flows and prototypes.", "owner_id": "1", "location": "6655 Elvas Ave"},
    {"title": "UX Designer", "description": "Design flows and prototypes.", "owner_id": "1", "location": "6655 Elvas Ave"},
]

USER_DATA = [
    {"user_name": "chen", "email":"chenwang@csus.edu", "password":"asdfasdf"},
    {"user_name": "miles", "email":"mboyle@csus.edu", "password":"asdfasdf"},
    {"user_name":"jared", "email":"jaredshicks@csus.edu", "password":"asdfasdf"}
]

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

db = Database_api()
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.urandom(24)
# demo data (swap for DB later)


# add to database
def add_data():
    for user in USER_DATA:
        res = db.user.create_account(user["user_name"], user["password"], user["email"])
        print(res)

    for job in JOB_DATA:
        res = db.post.create_post(job["title"], job["description"], job["owner_id"], job["location"])
        print(res)


add_data()


@app.route('/')
def home():
    return render_template('index.html', title='Home')
    
@app.route('/login', methods=["GET", "POST"])
def login_page():
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

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        print(f"name: {request.form.get('name')}")
        print(f"email: {request.form.get('email')}")
        print(f"password: {request.form.get('password')}")
    return render_template('signup.html', title='Sign Up')

@app.route('/jobs')
def jobs():
    q = request.args.get('q', '').strip().lower()
    page_num = int(request.args.get('page', 1)) # Get current page from URL
    items_per_page = 3
    start_index = (page_num - 1) * items_per_page

    # test with database
    paginated_data = db.post.select_latest_n_posts(items_per_page+1, start_index)[1]
    hide_prev = page_num == 1
    hide_next = len(paginated_data)<=items_per_page
    paginated_data = paginated_data[:-1]

    # hide_next = page_num == math.ceil( len(JOB_DATA) / items_per_page )
    if q:
        jobs = [j for j in JOB_DATA
                if q in j["title"].lower() or q in j["description"].lower()]

    return render_template('jobs.html', jobs=paginated_data, title='Jobs', page_num=page_num, hide_prev=hide_prev, hide_next=hide_next)

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
    
@app.route('/api/jobs/locations')
def api_job_locations():
    """
    Returns job locations as a GeoJSON FeatureCollection.
    This endpoint:
    - Attempts to read posts via db.post.select_latest_n_posts(...)
    - Converts any rows that include numeric latitude/longitude into GeoJSON features
    - Falls back to demo data if no geo-enabled rows are found
    """
    features = []
    try:
        res = db.post.select_latest_n_posts(1000, 0)
        rows = res[1] if isinstance(res, (list, tuple)) and len(res) > 1 else res
        for r in rows:
            # Support dict rows (recommended). If your DB returns tuples, adapt here.
            if isinstance(r, dict):
                lat = r.get('lat') or r.get('latitude') or r.get('latitude_float')
                lng = r.get('lng') or r.get('longitude') or r.get('longitude_float')
                try:
                    lat = float(lat) if lat is not None else None
                    lng = float(lng) if lng is not None else None
                except Exception:
                    lat = None
                    lng = None
                if lat is None or lng is None:
                    continue
                props = {
                    'id': r.get('id'),
                    'title': r.get('title'),
                    'description': r.get('description'),
                    'location': r.get('location'),
                    'url': r.get('url')
                }
                features.append({
                    'type': 'Feature',
                    'geometry': {'type': 'Point', 'coordinates': [lng, lat]},
                    'properties': props
                })
            # else: skip non-dict rows to avoid guessing column indices
    except Exception as e:
        print('Error while fetching posts for /api/jobs/locations:', e)

    if not features:
        # fallback demo features
        demo_jobs = [
            {"id": 101, "title": "Barista", "description": "Morning shift near Midtown.", "lat": 38.571, "lng": -121.486, "location":"Midtown, Sacramento"},
            {"id": 102, "title": "Front Desk", "description": "Evening shift, downtown.", "lat": 38.581, "lng": -121.494, "location":"Downtown"},
            {"id": 103, "title": "Prep Cook", "description": "Kitchen support role.", "lat": 38.563, "lng": -121.442, "location":"East Sac"},
        ]
        for j in demo_jobs:
            features.append({
                'type': 'Feature',
                'geometry': {'type': 'Point', 'coordinates': [j['lng'], j['lat']]},
                'properties': {
                    'id': j['id'],
                    'title': j['title'],
                    'description': j['description'],
                    'location': j['location'],
                    'url': None
                }
            })

    return jsonify({'type': 'FeatureCollection', 'features': features})
    
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
