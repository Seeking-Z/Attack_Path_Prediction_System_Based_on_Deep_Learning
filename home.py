from flask import Blueprint, render_template
from flask_login import login_required, current_user

import settings
import sqlserver

home_blueprint = Blueprint('home', __name__)


@home_blueprint.route('/home')
@login_required
def home():
    """跳转到主页"""
    setting = settings.Settings()
    message_sqlserver = sqlserver.Sqlserver(setting.sqlserver, setting.database, setting.sql_username,
                                            setting.sql_password,
                                            setting.message_table)
    select_columns = setting.message_table_columns
    select_columns.pop(0)
    per_page = setting.per_page

    # 获取数据
    total_data = message_sqlserver.select_data(select_columns)

    data = total_data[-per_page:]
    data = data[::-1]

    message_sqlserver.close()

    is_admin = current_user.is_admin()
    setting = settings.Settings()
    login_sqlserver = sqlserver.Sqlserver(setting.sqlserver, setting.database, setting.sql_username,
                                          setting.sql_password,
                                          setting.login_and_user_table)
    select_columns = setting.login_and_user_table_columns
    select_columns.pop(2)
    user_id = current_user.id
    users = login_sqlserver.select_data(select_columns)
    login_sqlserver.close()

    return render_template('home.html', data=data, is_admin=is_admin, users=users, user_id=user_id)
