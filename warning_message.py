from flask import Blueprint, render_template
from flask_login import login_required

warning_message_blueprint = Blueprint('warning_message', __name__)


@warning_message_blueprint.route('/warning_massage')
@login_required
def warning_message():
    return render_template('warning_message.html')
