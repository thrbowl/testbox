from flask import Blueprint, render_template, url_for, current_app
from flask.ext.login import login_required

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
@login_required('user')
def index():
    return 'OK'

@main.route('/releasenotes', methods=['GET'])
def releasenotes():
    return 'ok'