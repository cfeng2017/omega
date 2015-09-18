from flask import Blueprint, render_template

asset = Blueprint('asset', __name__, template_folder='templates')

MYSQL_TYPE_ID = 1


@asset.route('/')
def index():
    return render_template('asset/index.html')
