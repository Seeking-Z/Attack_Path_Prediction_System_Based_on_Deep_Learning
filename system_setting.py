from flask import Blueprint, render_template
from flask_login import login_required

system_setting_blueprint = Blueprint('system_setting', __name__)


@system_setting_blueprint.route('/system_setting')
@login_required
def system_setting():
    """跳转到系统设置"""
    return render_template('system_setting.html')
