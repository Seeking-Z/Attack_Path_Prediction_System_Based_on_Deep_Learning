from flask import Blueprint, render_template, request, redirect
from flask_login import login_user, login_required, logout_user

import user

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login')
def login():
    """跳转到登录页面"""
    return render_template('login.html')


@login_blueprint.route('/login/login_process', methods=['POST'])
def login_process():
    """登录进程"""
    username = request.form['username']
    password = request.form['password']
    the_user = user.User(username)
    if the_user.verify_username():
        if the_user.verify_password(password):
            login_user(the_user)
            return redirect('/home')
        else:
            return "<script>alert('用户名或密码错误，请重新登陆');location.href='..'</script>"
    else:
        return "<script>alert('用户名或密码错误，请重新登陆');location.href='..'</script>"


@login_blueprint.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    return redirect('/login')
