from flask import Flask, redirect, url_for, render_template

from login import login_blueprint
from home import home_blueprint

app = Flask(__name__)

app.register_blueprint(login_blueprint)
app.register_blueprint(home_blueprint)


@app.route('/')
def index():
    return redirect(url_for('login.login_page'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/warning_massage')
def warning_message():
    return render_template('warning_message.html')


@app.route('/systeminfo')
def systeminfo():
    return render_template('systeminfo.html')


@app.route('/system_setting')
def system_setting():
    return render_template('system_setting.html')


@app.route('/account')
def account():
    return render_template('account.html')


if __name__ == "__main__":
    print(app.url_map)
    app.run(port=80, host="127.0.0.1", debug=True)
