# Attack_Path_Prediction_System_Based_on_Deep_Learning
基于深度学习的攻击路径预测系统  
软件工程实践项目  
Seeking-Z

# 注意！本项目为实践作业，未经过完整、系统的安全性测试，不可用于生产环境！ #

# 初始账号密码为    admin/zadmin2023 #  

本系统的入侵检测部分的人工智能模型训练部分在以下仓库
`https://github.com/Seeking-Z/KDD99-DeepLearning`  
-----------------
# 环境约束 #   

以下是开发环境
服务端使用`Windows 11`，客户端使用`Ubuntu 22.04`。服务端拥有`Docker`。服务端和客户端都使用`Python 3.11`。  
如须将服务端移动到`Linux`上使用，请自行修改`sqlserver.py`文件，使其可以与数据库交互。  
如不使用`Docker`，可以在`sqlserver.py`中找到建库和建表语句，请自行建立数据库。  
本系统会进行二步验证，请自行下载身份认证器之类的软件。
---------------------
# 安装 #  
服务端  
首先获取`Docker`镜像并创建、运行容器。 顺序执行以下命令：  
```
docker pull ljyztzh/rgsqlserverimg
docker create --name rg_sqlserver -p 1433:1433 ljyztzh/rgsqlserverimg
docker start rg_sqlserver
```
此时一个名为`rg_sqlserver`的容器应该已经启动并将端口映射到了1433  
对系统设置进行修改  
系统设置都在`settings.py`中。必改项为本主机的监听IP和端口以及客户端所在的主机。请修改为实际的值。  
切换到本系统的目录下，运行`python main.py`。依主机设置，可能需要使用`python3`代替`python`  
如使用默认设置，此时访问`127.0.0.1:5000`应该可以访问到系统
  
客户端  
将目录下的`client`移动到运行客户端的主机，并在目录下运行  
`sudo python client.py`  
运行前请将host改为真实的服务端主机的值


