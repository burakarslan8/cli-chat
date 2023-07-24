import os
import json
from paramiko import SSHClient, AutoAddPolicy

f = open('config.json')

config = json.load(f)

host = config['host']
port = config['ssh-port']
username = config['username']

def establish_ssh_connection(host, port, username):
    client = SSHClient()
    known_hosts_path = os.path.expanduser("~/.ssh/known_hosts")
    client.load_host_keys(known_hosts_path)
    client.load_system_host_keys()
    client.set_missing_host_key_policy(AutoAddPolicy())

    client.connect(host, port, username=username)
    return client

def main():
    ssh_client = establish_ssh_connection(host=host, port=port, username=username)

    commands = [
        'hostname',
        'uptime',
        'cd cli-chat',
        'python3 cli-chat/server.py'
    ]

    for cmd in commands:
        stdin, stdout, stderr = ssh_client.exec_command(cmd)

        print(stdout.read().decode())
        print(stderr.read().decode())

    ssh_client.close()

if __name__ == "__main__":
    main()