from flask import Blueprint, render_template, jsonify
from flask_login import login_required
import psutil
import GPUtil

systeminfo_blueprint = Blueprint('systeminfo', __name__)
prev_net_info = psutil.net_io_counters()


@systeminfo_blueprint.route('/systeminfo')
@login_required
def systeminfo():
    """跳转到系统信息界面"""
    return render_template('systeminfo.html')


@systeminfo_blueprint.route('/api/systeminfo')
@login_required
def systeminfo_api():
    """获取系统信息的api"""
    global prev_net_info
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent

    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        gpu_info.append({
            'id': gpu.id,
            'name': gpu.name,
            'load': gpu.load,
            'memoryUtil': gpu.memoryUtil
        })

    network_info = psutil.net_io_counters()
    bytes_sent = round((network_info.bytes_sent - prev_net_info.bytes_sent) / 1024, 2)
    bytes_recv = round((network_info.bytes_recv - prev_net_info.bytes_recv) / 1024, 2)

    prev_net_info = network_info

    return jsonify(cpu_percent=cpu_percent, memory_percent=memory_percent, gpu_info=gpu_info, bytes_sent=bytes_sent,
                   bytes_recv=bytes_recv)
