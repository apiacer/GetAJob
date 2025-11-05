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
def login():
    if request.method == "POST":
        print(f"user name: {request.form.get('username')}")
        print(f"password: {request.form.get('password')}")

    return render_template('login.html', title='login')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)