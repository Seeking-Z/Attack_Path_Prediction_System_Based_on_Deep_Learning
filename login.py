from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user
import hashlib
import pyotp
import qrcode
import base64
from io import BytesIO

import sqlserver
import user
import settings

login_blueprint = Blueprint('login', __name__)
sec = ''


@login_blueprint.route('/login')
def login():
    """跳转到登录页面"""
    return render_template('login.html')


@login_blueprint.route('/login/verification_process', methods=['POST'])
def verification_process():
    """二步验证进程"""
    global sec
    id = request.form['id']
    hash = request.form['data']
    first = int(request.form['first'])
    setting = settings.Settings()
    login_sqlserver = sqlserver.Sqlserver(setting.sqlserver, setting.database, setting.sql_username,
                                          setting.sql_password,
                                          setting.login_and_user_table)
    select_columns = setting.login_and_user_table_columns
    data = login_sqlserver.select_data(select_columns, [select_columns[0], id])
    sha256 = hashlib.sha256()
    sha256.update((data[0][1] + setting.salt).encode('utf-8'))

    if hash != sha256.hexdigest():
        return redirect('/login')
    else:
        code = request.form['code']
        totp = pyotp.TOTP(sec)
        flag = False
        try:
            flag = totp.verify(int(code))

        except:
            return redirect(url_for('login.login_verification', id=id, flag=first, data=hash))

        if flag:
            if first == 1:
                login_sqlserver.update_data({select_columns[4]: sec}, select_columns[0], id)
            the_user = user.User(data[0][1])
            the_user.verify_username()
            login_user(the_user)
            return redirect('/home')
        else:
            return redirect(url_for('login.login_verification', id=id, flag=first, data=hash))


@login_blueprint.route('/login/login_verification')
def login_verification():
    """二步验证"""
    global sec
    id = request.args.get('id')
    hash = request.args.get('data')
    setting = settings.Settings()
    login_sqlserver = sqlserver.Sqlserver(setting.sqlserver, setting.database, setting.sql_username,
                                          setting.sql_password,
                                          setting.login_and_user_table)
    select_columns = setting.login_and_user_table_columns
    data = login_sqlserver.select_data(select_columns, [select_columns[0], id])
    login_sqlserver.close()
    sha256 = hashlib.sha256()
    sha256.update((data[0][1] + setting.salt).encode('utf-8'))
    if hash != sha256.hexdigest():
        return redirect('/login')
    else:
        if data[0][4] is None:
            sec = pyotp.random_base32()
            qr_uri = pyotp.totp.TOTP(sec).provisioning_uri(setting.host + ' ' + data[0][1])
            img = qrcode.make(qr_uri)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")
            return render_template('login_verification.html', the_img=base64_img, flag=1, id=id, data=hash)
        else:
            sec = data[0][4]
            return render_template('login_verification.html', the_img=None, flag=0, id=id, data=hash)


@login_blueprint.route('/login/login_process', methods=['POST'])
def login_process():
    """登录进程"""
    username = request.form['username']
    password = request.form['password']
    the_user = user.User(username)
    setting = settings.Settings()
    if the_user.verify_username():
        if the_user.verify_password(password):
            sha256 = hashlib.sha256()
            sha256.update((username + setting.salt).encode('utf-8'))
            return redirect(url_for('login.login_verification', id=the_user.get_id(), data=sha256.hexdigest()))
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
