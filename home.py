from flask import Blueprint, render_template
from flask_login import login_required

home_blueprint = Blueprint('home', __name__)


