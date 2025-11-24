from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from db import Db_api, DB_PATH
import os
import re
import sqlite3
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from dotenv import load_dotenv
# loads .env into environment variables
load_dotenv()

# test data
JOB_DATA = [
    {"title": "Frontend Developer", "description": "Build UI with HTML/CSS/JS.", "owner_id": "2", "location": "1300 65th St"},
    {"title": "Backend Developer", "description": "APIs with Python + Flask.", "owner_id": "2", "location": "1300 65th St"},
    {"title": "Data Analyst", "description": "SQL, charts, and insights.", "owner_id": "3", "location": "1305 64th St"},
    {"title": "UX Designer", "description": "Design flows and prototypes.", "owner_id": "1", "location": "6655 Elvas Ave"},
    {"title": "UX Designer", "description": "Design flows and prototypes.", "owner_id": "1", "location": "6655 Elvas Ave"},
]

USER_DATA = [
    {"user_name": "chen", "email":"chenwang@csus.edu", "password":"Aa12345_"},
    {"user_name": "miles", "email":"mboyle@csus.edu", "password":"Aa12345_"},
    {"user_name":"jared", "email":"jaredshicks@csus.edu", "password":"Aa12345_"}
]

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
def delete_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
delete_db()

db = Db_api(debug=False)
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.urandom(24)

# moved all smtp config data to .env file 
"""
MAIL_SERVER=sandbox.smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=9c626db099d0e7
MAIL_PASSWORD=4137b68a275c8b
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_DEFAULT_SENDER_NAME="GetAJob Team"
MAIL_DEFAULT_SENDER_EMAIL=no-reply@getajob.com
"""

# SMTP configuration for Flask-Mail
app.config.update(
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"), 
    MAIL_USE_TLS=os.getenv("MAIL_USE_TLS") == "True",
    MAIL_USE_SSL=os.getenv("MAIL_USE_SSL") == "True",
    MAIL_DEFAULT_SENDER=(os.getenv("MAIL_DEFAULT_SENDER_NAME"), os.getenv("MAIL_DEFAULT_SENDER_EMAIL"))
)
mail = Mail(app)
s = URLSafeTimedSerializer(app.secret_key)


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
def login():
    if request.method == "POST":
        user_name = request.form.get('username')
        password = request.form.get('password')
        res = db.user.verify_password(user_name, password)
        if res[0]:
            # add to session
            session["user_name"] = user_name
            user_id = db.user.get_user_info(user_name=user_name)[1].get("user_id")
            print(f"logged in user_id: {user_id}")
            session["user_id"] = user_id

            # ---- redirect to whatever page ----
            return render_template('login.html', title='login')

        else:
            # ---- show login fail ----
            print(f"login fail: {res}") # temp
            return render_template('login.html', title='login')

    elif request.method == "GET":
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

        # Call db layer
        success, msg = db.user.create_account(username, password, email, fname, lname)

         # Handle response
        if not success:
            if "UNIQUE constraint failed: user.email" in msg:
                flash("That email is already registered. Please use a different one.", "error")
            elif "UNIQUE constraint failed: user.user_name" in msg:
                flash("That username is already taken.", "error")
            else:
                flash("Something went wrong while creating your account.", "error")
            return redirect(url_for('signup'))

        ### Email verification on success ###

        # generate token using user email
        token = s.dumps(email, salt='email-confirm')

        # create confirmation link
        confirm_url = url_for('confirm_email', token=token, _external=True)

        # send email
        msg = Message("Confirm your GetAJob account" , recipients=[email])
        msg.body = f"Howdy {fname}, \n\nThis is totally not a scam! Please confirm your email address by clicking the link below:\n\n{confirm_url}\n\nIf you did not sign up for a GetAJob account, please ignore this email."

        flash('Account created successfully!', 'success')
        mail.send(msg)

        flash('A confirmation email has been sent to your email address. Please verify to activate your account.', 'info')
        return redirect(url_for('login'))

    return render_template('signup.html')

#email confirmation route
@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)  # 1 hour expiration
    except SignatureExpired:
        flash('The confirmation link has expired. Go to login', 'error')
        return redirect(url_for('login'))

    # update user record to set is_verified = 1
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    cur.execute("UPDATE user SET is_verified = 1 WHERE email = ?", (email,))
    conn.commit()
    conn.close()

    flash('Your email has been confirmed! You can now log in.', 'success')
    return redirect(url_for('login'))


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
def jobs_list(): ##### CHANGED jobs to match new template structure
    ##location = "1151 57th St"

    # --- Query parameters ---
    q = request.args.get('q', '').strip()
    location = request.args.get('location', '').strip()
    raw_tags = request.args.get('tags', '').strip()
    page_num = int(request.args.get('page', 1))

    # Parse multi-tag input: "crypto,binance,ai"
    tags = [t.strip() for t in raw_tags.split(",") if t.strip()] if raw_tags else None

    # Parse keywords: split user query into multiple words
    keywords = [w for w in q.split() if w] if q else None

    # Pagination settings
    ITEMS_PER_PAGE = 5
    offset = (page_num - 1) * ITEMS_PER_PAGE

    # --- Query database ---
    ok, res = db.post.search_posts(
        limit=ITEMS_PER_PAGE + 1,  # fetch 1 extra to detect "next page"
        offset=offset,
        tags=tags,
        key_words=keywords,
        location=location
    )

    if not ok:
        return f"Database error: {res}", 500

    # --- Pagination controls ---
    hide_prev = (page_num == 1)
    hide_next = len(res) <= ITEMS_PER_PAGE

    # Remove the extra record
    posts = res[:ITEMS_PER_PAGE]

    return render_template(
        'jobs/job_list.html', ### Changed template path
        jobs=posts,
        title='Jobs',
        page_num=page_num,
        hide_prev=hide_prev,
        hide_next=hide_next,
        q=q,
        tags=raw_tags,
        location=location
    )

def submit_form():
    # Get the user input from the form
    user_input = request.form['username']
    
    # Process the input (e.g., save to a database, modify it)
    new_default_value = f"Updated: {user_input}"
    
    # Redirect back to the form page, passing the new value as a query parameter
    # or render a new template with the value
    return redirect(url_for('index', current_username=new_default_value))

######## Job detail page (minimal) ############ CHANGED FROM HERE
'''
@app.route('/job/<int:job_id>')
def job_detail(job_id):
    job = next((j for j in JOB_DATA if j["id"] == job_id), None)
    if not job:
        return render_template('404.html'), 404
    # Minimal detail page for now:
    return f"<h1>{job['title']}</h1><p>{job['description']}</p>"
'''
##### Full job detail page ############ CHANGES FROM HERE
# ##### TO HERE ##########

@app.route('/jobs/<int:post_id>')
def job_view(post_id):
    ok, rows = db.post.select_post(post_id)
    if not ok or not rows:
        return render_template('404.html'), 404
    post = rows[0]

    # fetch tags and derive availability flags
    ok_t, tag_list = db.post.get_post_tags(post_id)
    tag_list = tag_list if ok_t else []
    post["tags"] = [t for t in tag_list if not t.startswith("avail:")]

    post["availability_morning"] = 1 if "avail:morning" in tag_list else 0
    post["availability_afternoon"] = 1 if "avail:afternoon" in tag_list else 0
    post["availability_evening"] = 1 if "avail:evening" in tag_list else 0

    return render_template('jobs/job_view.html', post=post, title=post["title"])
###### TO HERE ##########

### #### Job create / edit / delete #####
@app.route('/jobs/new', methods=['GET'])
def job_new():
    return render_template('jobs/job_new.html', title='New Job')

@app.route('/jobs', methods=['POST'])
def job_create():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    location = request.form.get("location", "").strip()
    budget = request.form.get("budget", "").strip()
    raw_tags = request.form.get("tags", "").strip()

    # required fields (keep simple)
    if not title or not description or not location:
        flash("Title, description, and location are required.", "error")
        return redirect(url_for('job_new'))

    # owner: no auth yet, assume 1
    owner_id = 1

    # create post (no change to teammate DB API)
    ok, res = db.post.create_post(title, description, owner_id, location, budget)
    if not ok:
        flash(f"DB error creating post: {res}", "error")
        return redirect(url_for('job_new'))

    # find new id (minimal and safe for single-user local dev)
    ok_id, row = db.post.get_last_post_id()
    post_id = row[0]["id"] if ok_id and row and row[0]["id"] is not None else None
    if not post_id:
        flash("Could not determine new post id.", "error")
        return redirect(url_for('jobs_list'))

    # tags: parse + availability as tags
    tags = [t.strip() for t in raw_tags.split(",") if t.strip()] if raw_tags else []
    if request.form.get("availability_morning"):
        tags.append("avail:morning")
    if request.form.get("availability_afternoon"):
        tags.append("avail:afternoon")
    if request.form.get("availability_evening"):
        tags.append("avail:evening")

    db.post.set_post_tags(post_id, tags)

    return redirect(url_for('upload_success', id=post_id))

@app.route('/jobs/<int:post_id>/edit', methods=['GET'])
def job_edit(post_id):
    ok, rows = db.post.select_post(post_id)
    if not ok or not rows:
        return render_template('404.html'), 404
    post = rows[0]

    ok_t, tag_list = db.post.get_post_tags(post_id)
    tag_list = tag_list if ok_t else []
    user_tags = [t for t in tag_list if not t.startswith("avail:")]
    tags_str = ", ".join(user_tags)

    post["availability_morning"] = 1 if "avail:morning" in tag_list else 0
    post["availability_afternoon"] = 1 if "avail:afternoon" in tag_list else 0
    post["availability_evening"] = 1 if "avail:evening" in tag_list else 0

    return render_template('jobs/job_edit.html', post=post, tags=tags_str, title=f"Edit: {post['title']}")

@app.route('/jobs/<int:post_id>/edit', methods=['POST'])
def job_update(post_id):
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    location = request.form.get("location", "").strip()
    raw_tags = request.form.get("tags", "").strip()

    # update core fields; NOTE teammate typo: locaiton
    db.post.update_post(
        post_id,
        title=title if title else None,
        description=description if description else None,
        location=location if location else None  # <- yes, spelled 'locaiton' in teammate code
    )

    # rebuild tags
    tags = [t.strip() for t in raw_tags.split(",") if t.strip()] if raw_tags else []
    if request.form.get("availability_morning"):
        tags.append("avail:morning")
    if request.form.get("availability_afternoon"):
        tags.append("avail:afternoon")
    if request.form.get("availability_evening"):
        tags.append("avail:evening")
    db.post.set_post_tags(post_id, tags)

    return redirect(url_for('job_view', post_id=post_id))

@app.route('/jobs/<int:post_id>/delete', methods=['POST'])
def job_delete(post_id):
    db.post.delete_post(post_id)
    # post_tag rows will cascade delete
    flash("Listing deleted.", "success")
    return redirect(url_for('jobs_list'))

@app.route('/jobs/success')
def upload_success():
    post_id = request.args.get("id")
    return render_template('jobs/upload_success.html', post_id=post_id, title="Success")



##### Maps page with job locations #####
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

# Global error handler for database integrity errors
@app.errorhandler(sqlite3.IntegrityError)
def handle_db_error(e):
    flash("Database constraint error. Please check your input.", "error")
    return redirect(request.referrer or url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
