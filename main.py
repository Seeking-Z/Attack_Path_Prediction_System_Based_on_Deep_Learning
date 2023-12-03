import subprocess
import requests
from flask import Flask, redirect
from flask_login import LoginManager
import threading

import settings
import user

from login import login_blueprint
from home import home_blueprint
from warning_message import warning_message_blueprint
from systeminfo import systeminfo_blueprint
from system_setting import system_setting_blueprint
from account import account_blueprint
from attack_path_prediction import prediction_blueprint

app = Flask(__name__)
app.secret_key = 'hello_world'

app.register_blueprint(login_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(warning_message_blueprint)
app.register_blueprint(systeminfo_blueprint)
app.register_blueprint(system_setting_blueprint)
app.register_blueprint(account_blueprint)
app.register_blueprint(prediction_blueprint)

login_manager = LoginManager(app)


# 获取用户
@login_manager.user_loader
def load_user(user_id):
    return user.User.get(user_id)


# 默认路由
@app.route('/')
def index():
    """默认跳转到登录界面"""
    return redirect('/login')


def get_data():
    process = subprocess.Popen(['./model_and_extractor/kdd99extractor', '-e'], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    setting = settings.Settings()
    url = 'http://' + setting.url + '/api/prediction'

    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            data = output.decode().strip()
            requests.post(url, data={'data': data})

    print(f"致命错误，路径预测子线程已停止。子线程退出代码:{process.poll()}。程序已停止。")

    exit(1)


if __name__ == "__main__":
    # thread = threading.Thread(target=get_data)
    # thread.start()
    app.run(host="0.0.0.0", debug=True)
