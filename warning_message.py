from flask import Blueprint, render_template, request
from flask_login import login_required

import settings
import sqlserver

warning_message_blueprint = Blueprint('warning_message', __name__)


@warning_message_blueprint.route('/warning_massage')
@login_required
def warning_message():
    """跳转到告警页面"""
    page = request.args.get('page', 1, type=int)

    setting = settings.Settings()
    message_sqlserver = sqlserver.Sqlserver(setting.sqlserver, setting.database, setting.sql_username,
                                            setting.sql_password,
                                            setting.message_table)
    select_columns = setting.message_table_columns
    select_columns.pop(0)
    per_page = setting.per_page

    # 获取数据
    total_data = message_sqlserver.select_data(select_columns)

    message_sqlserver.close()

    total_page = len(total_data) // per_page + 1

    if page > total_page:
        page = total_page

    if len(total_data) < per_page:
        data = total_data[::-1]
    else:
        data = total_data[-page * per_page:]
        data = data[:per_page]
        data = data[::-1]

    return render_template('warning_message.html', data=data, page=page, total_page=total_page)
