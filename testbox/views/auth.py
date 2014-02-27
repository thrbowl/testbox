from flask import Blueprint, render_template, url_for, request
from flask.ext.login import login_required

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    next = request.args.get('next')
    if request.method == 'POST':
        pass
    return render_template('auth/login.html')


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    pass
