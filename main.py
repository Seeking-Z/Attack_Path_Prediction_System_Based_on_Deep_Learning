from flask import Flask, redirect
from flask_login import LoginManager

import user

from login import login_blueprint
from home import home_blueprint
from warning_message import warning_message_blueprint
from systeminfo import systeminfo_blueprint
from system_setting import system_setting_blueprint
from account import account_blueprint

app = Flask(__name__)
app.secret_key = 'hello_world'

app.register_blueprint(login_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(warning_message_blueprint)
app.register_blueprint(systeminfo_blueprint)
app.register_blueprint(system_setting_blueprint)
app.register_blueprint(account_blueprint)

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return user.User.get(user_id)


@app.route('/')
def index():
    """默认跳转到登录界面"""
    return redirect('/login')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
