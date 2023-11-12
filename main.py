from flask import Flask, redirect, url_for, render_template
from flask_login import LoginManager, login_required, logout_user

import user
from login import login_blueprint
from home import home_blueprint
# from warning_message import warning_message_blueprint

app = Flask(__name__)
app.secret_key = 'hello_world'

app.register_blueprint(login_blueprint)
app.register_blueprint(home_blueprint)
# app.register_blueprint(warning_message_blueprint)

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return user.User.get(user_id)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/warning_massage')
@login_required
def warning_message():
    return render_template('warning_message.html')


@app.route('/systeminfo')
@login_required
def systeminfo():
    return render_template('systeminfo.html')


@app.route('/system_setting')
@login_required
def system_setting():
    return render_template('system_setting.html')


@app.route('/account')
@login_required
def account():
    return render_template('account.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
