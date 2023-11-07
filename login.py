from flask import Blueprint, render_template, request

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login')
def login_page():
    return render_template("login.html")


# @login.route('/loginProcess', methods=['POST'])
# def login_process():
#     username = request.form['username']
#     password = request.form['password']
