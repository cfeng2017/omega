from flask import render_template, jsonify
from apps import app


@app.route('/')
@app.route('/dashboard/')
def dashboard():
    return render_template("dashboard.html")


@app.route('/search/<q>')
def search(q):
    results = {"tttt": {"name": "t1", "results": [{"title": "Result Title",\
                                                         "description": "Optional Description"}]}}

    return jsonify(results=results)


