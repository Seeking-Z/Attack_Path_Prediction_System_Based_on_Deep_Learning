from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user

import user

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login_process', methods=['POST'])
def login_process():
    username = request.form['username']
    password = request.form['password']
    the_user = user.User(username)
    if the_user.verify_username():
        if the_user.verify_password(password):
            login_user(the_user)
            return redirect(url_for('home'))
        else:
            return "<script>alert('用户名或密码错误，请重新登陆');location.href='login'</script>"
    else:
        return "<script>alert('用户名或密码错误，请重新登陆');location.href='login'</script>"
