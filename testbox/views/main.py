from flask import Blueprint, render_template, url_for, current_app
from flask.ext.login import login_required, redirect

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
@login_required
def index():
    return redirect(url_for('dashboard.index'))


@main.route('/releasenotes', methods=['GET'])
def releasenotes():
    return 'ok'


@main.route('/changelog', methods=['GET'])
def changelog():
    return 'ok'
