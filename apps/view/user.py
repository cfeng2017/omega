import requests
from functools import wraps
requests.packages.urllib3.disable_warnings()

from flask import redirect, request, g, url_for, Blueprint, render_template
from apps import OAUTH_URL, CLIENT_ID, CLIENT_SECRET, app, lm, db
from apps.model.user import User
from flask_login import current_user, logout_user, login_user, login_required
from apps.view.error_pages import forbidden

user = Blueprint('user', __name__)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/login/')
def login():
    code = request.args.get('code', None)
    if code is None:
        # get code
        return redirect(OAUTH_URL + '/login/authorize?client_id=' + CLIENT_ID)
    else:
        # get token
        token_url = OAUTH_URL + '/login/token'
        theader = {'Accept': 'application/json'}
        data = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'code': code}
        response = requests.post(token_url, data=data, headers=theader)
        token = response.json()
        access_token = token['access_token']
        token_type = token['token_type']

        # get resource
        r_url = OAUTH_URL + '/user'
        rheader = {'Authorization': token_type + ' ' + access_token}
        resource = requests.get(r_url, headers=rheader)
        _ = resource.json()[0]
        user = User.query.filter(User.uid == _['user_id']).first()
        if not user:
            user = User(uid=_['user_id'],
                        name=_['name'],
                        email=_['email'],
                        mobile=_['mobile'],
                        english_name=_['english_name'],
                        department_name=_['department_name'],
                        is_admin=False,
                        is_alive=True)
            db.session.add(user)
            db.session.commit()
        login_user(user, remember=True)
    return redirect('/')


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('dashboard'))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.get_id() is None:
            # return redirect(url_for('forbidden'))
            return render_template('error_pages/403.html'), 403
        return f(*args, **kwargs)
    return decorated_function


@app.errorhandler(403)
def forbidden():
    return render_template('error_pages/403.html'), 403
# @lm.unauthorized_handler
# def unauthorized():
#     print '~~~~~~~~~~~~~'
#     return redirect(url_for('forbidden'))
