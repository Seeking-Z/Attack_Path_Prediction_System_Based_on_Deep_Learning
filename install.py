import os

command_list = [
    'pip install -r requirements.txt',
    'docker pull ljyztzh/rgsqlserverimg',
    'docker images',
    'docker create --name rg_sqlserver -p 1433:1433 ljyztzh/rgsqlserverimg'
    'docker ps -a'
    'docker start rg_sqlserver'
]

for command in command_list:
    try:
        os.system(command)
    except:
        print(f"command filed:{command}")
