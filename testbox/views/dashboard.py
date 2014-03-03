from flask import Blueprint, render_template, url_for, request
from flask.ext.login import login_required

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/', methods=['GET'])
def index():
    return render_template('dashboard/index.html')
