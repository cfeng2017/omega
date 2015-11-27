from flask import render_template
from apps import app


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_pages/404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('error_pages/403.html'), 403

