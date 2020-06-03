from paramiko import SSHClient
from scp import SCPClient

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect('34.72.152.18', username="marekjachym99")

# SCPCLient takes a paramiko transport as an argument
scp = SCPClient(ssh.get_transport())

scp.get("/home/marekjachym99/lavalanche/weather_data", "D:\\GitHub\\LaVaLanche\\data", recursive=True)

# Uploading the 'test' directory with its content in the
# '/home/user/dump' remote directory

scp.close()