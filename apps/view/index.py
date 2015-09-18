from flask import render_template
from asset import asset
from apps import app


@app.route('/')
@app.route('/dashboard/')
def dashboard():
    return render_template("dashboard.html")



