import os

command_list = [
    'apt-get update',
    'apt-get install apt-transport-https ca-certificates curl software-properties-common',
    'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -',
    'add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"',
    'apt-get update',
    'apt-get install docker-ce',
    'docker --version',
    'systemctl start docker'
]

for command in command_list:
    try:
        os.system(command)
    except:
        print(f"command filed:{command}")
