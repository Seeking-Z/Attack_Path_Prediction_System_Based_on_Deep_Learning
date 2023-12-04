import subprocess
import requests

host = '192.168.199.1:5000'     # 服务端主机

process = subprocess.Popen(['./kdd99extractor', '-e'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

url = 'http://' + host + '/api/prediction'

while True:
    output = process.stdout.readline()
    if output == b'' and process.poll() is not None:
        break
    if output:
        data = output.decode().strip()
        print(data)
        requests.post(url, data={'data': data})

print(f"致命错误，路径预测子线程已停止。子线程退出代码:{process.poll()}。程序已停止。")

exit(1)