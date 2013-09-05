from flask import Blueprint, render_template

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


def logout():
    pass