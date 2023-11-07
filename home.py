from flask import Blueprint, render_template, request

home_blueprint = Blueprint('home', __name__)


@home_blueprint.route('/home')
def home_page():
    return render_template("home.html")