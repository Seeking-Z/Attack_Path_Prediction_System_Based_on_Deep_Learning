from flask import Blueprint, render_template
from flask_login import login_required

systeminfo_blueprint = Blueprint('systeminfo', __name__)


@systeminfo_blueprint.route('/systeminfo')
@login_required
def systeminfo():
    return render_template('systeminfo.html')
