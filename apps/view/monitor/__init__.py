from flask import Blueprint, render_template

monitor = Blueprint('monitor', __name__, template_folder='templates')


@monitor.route('/')
def index():
    return render_template('monitor/index.html')