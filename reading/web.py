from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from authomatic import Authomatic
from authomatic.adapters import WerkzeugAdapter
from flask import Flask, g, jsonify, make_response, response, render_template
from flask.ext.login import LoginManager, login_required, login_user
from werkzeug.contrib.fixers import ProxyFix

from . import config
from . import utils
from .controllers import twilio_controller


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
config.configure_app(app)

authomatic = Authomatic(app.config['authomatic_config'],
                        app.config['secretKey'],
                        report_errors=True)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(email):
    g.db.load_user(email)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('authorized'))


@login_manager.request_loader
def load_user_from_basic_auth(req):
    auth = req.authorization
    if auth:
        api_key = auth.password
        user = g.db.load_user_via_api_key(api_key)
        if user:
            return user
    return None


@app.route('/authorized', methods=['GET', 'POST'])
def authorized():
    response = make_response()
    result = authomatic.login(WerkzeugAdapter(request, response), 'google')
    if result:
        if result.user:
            result.user.update()
            user = g.db.load_user(result.user.email)
            if user is None:
                g.db.save_user(models.User(result.user.email))
                user = g.db.load_user(result.user.email)
            if user is not None:
                login_user(user)
                return redirect(url_for('index'))
            else:
                return redirect(url_for('invalid_user'))
    return response


@app.route('/invalid-user')
def invalid_user():
    return 'User unknown'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
def index():
    """ The homepage """
    return jsonify({'hi': config.get_config().testvalue})


@app.route('/send', methods=['GET', 'POST'])
def send():
    """ Send a text message """
    if request.method == 'POST':
        message = request.form['message']
        to_numbers = utils.split_numbers(request.form['recipients'])
        twilio_controller.send(message, to_numbers)
    else:
        render_template('send_message.html')

