from flask import Blueprint, render_template, url_for, request
from flask.ext.login import login_required

testcase = Blueprint('testcase', __name__)

@testcase.route('/', methods=['GET'])
def index():
    return render_template('testcase/index.html')
