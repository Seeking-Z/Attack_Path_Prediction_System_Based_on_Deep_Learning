from flask import Blueprint, render_template
from flask_login import login_required

home_blueprint = Blueprint('home', __name__)


@home_blueprint.route('/home')
@login_required
def home():
    """跳转到主页"""
    return render_template('home.html')
