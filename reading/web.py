from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from flask import Flask, jsonify
from werkzeug.contrib.fixers import ProxyFix

from . import config
from . import utils
from .controllers import twilio_controller


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
config.configure_app(app)


@app.route('/')
def index():
    return jsonify({'hi': config.get_config().testvalue})


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        message = request.form['message']
        to_numbers = utils.split_numbers(request.form['recipients'])
        twilio_controller.send(message, to_numbers)
    else:
        render_template('send_message.html')

