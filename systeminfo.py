from flask import Blueprint, render_template, jsonify
from flask_login import login_required
import psutil
import GPUtil

systeminfo_blueprint = Blueprint('systeminfo', __name__)


@systeminfo_blueprint.route('/systeminfo')
@login_required
def systeminfo():
    return render_template('systeminfo.html')


@systeminfo_blueprint.route('/api/systeminfo')
@login_required
def systeminfo_api():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent

    # Get GPU information
    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        gpu_info.append({
            'id': gpu.id,
            'name': gpu.name,
            'load': gpu.load,
            'memoryUtil': gpu.memoryUtil
        })

    # Get network information
    network_info = psutil.net_io_counters()
    bytes_sent = network_info.bytes_sent
    bytes_recv = network_info.bytes_recv

    return jsonify(cpu_percent=cpu_percent, memory_percent=memory_percent, gpu_info=gpu_info, bytes_sent=bytes_sent,
                   bytes_recv=bytes_recv)
