import pickle
import torch
from torch import nn
import numpy as np

# 协议类型
protocol_type = {'icmp': 0, 'tcp': 1, 'udp': 2}
# 网络服务类型
service = {'IRC': 0, 'X11': 1, 'Z39_50': 2, 'aol': 3, 'auth': 4, 'bgp': 5, 'courier': 6, 'csnet_ns': 7, 'ctf': 8,
           'daytime': 9, 'discard': 10, 'domain': 11, 'domain_u': 12, 'echo': 13, 'eco_i': 14, 'ecr_i': 15, 'efs': 16,
           'exec': 17, 'finger': 18, 'ftp': 19, 'ftp_data': 20, 'gopher': 21, 'harvest': 22, 'hostnames': 23,
           'http': 24, 'http_2784': 25, 'http_443': 26, 'http_8001': 27, 'imap4': 28, 'iso_tsap': 29, 'klogin': 30,
           'kshell': 31, 'ldap': 32, 'link': 33, 'login': 34, 'mtp': 35, 'name': 36, 'netbios_dgm': 37,
           'netbios_ns': 38, 'netbios_ssn': 39, 'netstat': 40, 'nnsp': 41, 'nntp': 42, 'ntp_u': 43, 'other': 44,
           'pm_dump': 45, 'pop_2': 46, 'pop_3': 47, 'printer': 48, 'private': 49, 'red_i': 50, 'remote_job': 51,
           'rje': 52, 'shell': 53, 'smtp': 54, 'sql_net': 55, 'ssh': 56, 'sunrpc': 57, 'supdup': 58, 'systat': 59,
           'telnet': 60, 'tftp_u': 61, 'tim_i': 62, 'time': 63, 'urh_i': 64, 'urp_i': 65, 'uucp': 66, 'uucp_path': 67,
           'vmnet': 68, 'whois': 69}
# 连接正常或错误的状态
flag = {'OTH': 0, 'REJ': 1, 'RSTO': 2, 'RSTOS0': 3, 'RSTR': 4, 'S0': 5, 'S1': 6, 'S2': 7, 'S3': 8, 'SF': 9, 'SH': 10}
# 标签
labels = ['DOS', 'Probing', 'R2L', 'U2R', 'Normal']


# 定义模型
class DNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(28, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 5)
        )

    def forward(self, the_x):
        return self.net(the_x)


def get_label(feature):
    """
    feature应为长度为28的列表，与kdd99extractor返回的相同。
    通过特征值列表获取预测的标签
    """
    model = DNN()
    model.load_state_dict(torch.load('model/best_model_params.pt'))
    model.eval()

    # 将标签转换为编码
    feature[1] = protocol_type[feature[1]]
    feature[2] = service[feature[2]]
    feature[3] = flag[feature[3]]

    # 将字符型转为浮点型
    for i in range(len(feature)):
        if 0 < i < 4:
            continue
        feature[i] = float(feature[i])

    feature = np.array(feature)
    feature = feature.reshape(1, -1)

    # 导入缩放器参数，读取训练时的MinMaxScaler实例进行归一化
    with open('model/scaler_params.pkl', 'rb') as file:
        scaler = pickle.load(file)
    feature = scaler.transform(feature)

    feature = torch.from_numpy(feature).float()

    with torch.no_grad():
        output = model(feature)
        _, predicted = torch.max(output, 1)

    last = labels[predicted.item()]

    return last


# test = [0, 'tcp', 'telnet', 'SF', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0.00, 0.00, 0.00, 0.00,
#         1.00, 0.00, 0.00, 255, 128, 0.50, 0.01, 0.00, 0.00, 0.00, 0.00, 0.66, 0.32]
# test = test[:10] + test[23:]
# print(test)
# for i in range(len(test)):
#     if 0 < i < 4:
#         continue
#     test[i] = str(test[i])
# print(test)
# print(type(test[0]))
# print(len(test))
# print(get_label(test))
