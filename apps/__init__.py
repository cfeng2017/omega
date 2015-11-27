#! -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
sys.path.append(os.path.abspath(__file__))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(config.DevConfig)
app.secret_key = 'Am I secret?'
db = SQLAlchemy(app)

# login
from flask_login import LoginManager
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = u'Please login!'


# oauth
OAUTH_URL = 'https://auth.corp.anjuke.com/oauth/2.0'
CLIENT_ID = 'r80080org0ikzra3b91d'
CLIENT_SECRET = '9xlo04722zx0ljtx8ig5r8pz2vhog2mh9apkycav'

# blueprint
from view import *

modules = {
    'asset': asset,
    'monitor': monitor,
    'config': config
}

for k, v in modules.iteritems():
    app.register_blueprint(v, url_prefix='/' + k)

