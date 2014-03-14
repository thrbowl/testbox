from flask import Blueprint, render_template, url_for, request
from flask.ext.login import login_required, login_user, redirect, logout_user, current_user
from ..forms import LoginForm
from ..models import db, User
from ..utils import ldap_verify_user, ldap_query_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    next = request.args.get('next', url_for('main.index'))
    if current_user.is_authenticated():
        return redirect(next)

    login_failed = False
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        coreid = form.coreid.data
        password = form.password.data
        remember = form.remember.data
        if ldap_verify_user(coreid, password):
            user = User.get(coreid)
            if not user:
                data = ldap_query_user(coreid, 'displayName', 'mail')
                assert data is not None
                user = User(coreid, data['displayName'], data['mail'])
                db.session.add(user)
                db.session.commit()
            login_user(user, remember=remember)
            return redirect(next)
        else:
            login_failed = True
    return render_template('auth/login.html', login_failed=login_failed, next=next)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
