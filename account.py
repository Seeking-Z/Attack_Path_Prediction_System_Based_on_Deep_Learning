from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash

import settings
import sqlserver

account_blueprint = Blueprint('account', __name__)


@account_blueprint.route('/account')
@login_required
def account():
    is_admin = current_user.is_admin()
    setting = settings.Settings()
    login_sqlserver = sqlserver.Sqlserver(setting.sqlserver, setting.database, setting.username,
                                          setting.password,
                                          setting.login_and_user_table)
    select_columns = setting.login_and_user_table_columns
    select_columns.pop(2)
    user_id = current_user.id
    users = login_sqlserver.select_data(select_columns)
    login_sqlserver.close()
    return render_template('account.html', is_admin=is_admin, users=users, user_id=user_id)


@account_blueprint.route('/account/account_modify', methods=['POST'])
@login_required
def account_modify():
    setting = settings.Settings()
    login_sqlserver = sqlserver.Sqlserver(setting.sqlserver, setting.database, setting.username,
                                          setting.password,
                                          setting.login_and_user_table)
    select_columns = setting.login_and_user_table_columns
    is_admin = current_user.is_admin()
    if is_admin:
        user_id = request.form['user_id']
    else:
        user_id = current_user.id
    users = login_sqlserver.select_data(select_columns, f"id='{user_id}'")
    username = users[0][1]
    login_sqlserver.close()
    return render_template('account_modify.html', user_id=user_id, username=username, is_admin=is_admin)


@account_blueprint.route('/account/modify_user_process', methods=['POST'])
@login_required
def modify_user_process():
    is_admin = current_user.is_admin()
    username = request.form['username']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    admin = 0
    if is_admin:
        user_id = request.form['user_id']
        admin = request.form['admin']
        admin = int(admin)
    else:
        user_id = current_user.id

    if new_password != confirm_password:
        flash("密码不匹配，请重新输入。", 'error')
        return render_template('account_modify.html', user_id=user_id, username=username, is_admin=is_admin)
    else:
        setting = settings.Settings()
        login_sqlserver = sqlserver.Sqlserver(setting.sqlserver, setting.database, setting.username,
                                              setting.password,
                                              setting.login_and_user_table)
        columns = setting.login_and_user_table_columns
        password = generate_password_hash(new_password)
        data = {
            columns[1]: username,
            columns[2]: password,
            columns[3]: admin
        }
        if login_sqlserver.select_data(['username'], f"{columns[1]}='{username}'"):
            return "<script>alert('用户名已存在');location.href='../account'</script>"
        if user_id == 'None':
            login_sqlserver.insert_data(data)
        else:
            login_sqlserver.update_data(data, f"{columns[0]}={user_id}")
        login_sqlserver.close()
        return "<script>alert('成功');location.href='../account'</script>"


@account_blueprint.route('/account/account_create')
@login_required
def account_create():
    return render_template('account_modify.html', user_id=None, is_admin=1)


@account_blueprint.route('/account/account_delete', methods=['POST'])
@login_required
def account_delete():
    setting = settings.Settings()
    login_sqlserver = sqlserver.Sqlserver(setting.sqlserver, setting.database, setting.username,
                                          setting.password,
                                          setting.login_and_user_table)
    columns = setting.login_and_user_table_columns
    is_admin = current_user.is_admin()
    if is_admin:
        user_id = request.form['user_id']
    else:
        user_id = current_user.id
    test = current_user.id
    if current_user.id == int(user_id):
        return "<script>alert('无法删除当前使用的账户');location.href='../account'</script>"
    else:
        login_sqlserver.delete_data(f"{columns[0]}='{user_id}'")
        return "<script>alert('成功');location.href='../account'</script>"
