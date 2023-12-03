import os

command_list = [
    'pip install -r requirements.txt',
    'docker pull ljyztzh/rgsqlserverimg',
    'docker images'
]

for command in command_list:
    try:
        os.system(command)
    except:
        print(f"command filed:{command}")
