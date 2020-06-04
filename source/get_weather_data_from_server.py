from paramiko import SSHClient
from scp import SCPClient
import tarfile, os, shutil

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect('34.72.152.18', username="marekjachym99")

# SCPCLient takes a paramiko transport as an argument
scp = SCPClient(ssh.get_transport())

scp.get("/home/marekjachym99/lavalanche/weather.tar", "D:\\GitHub\\LaVaLanche\\data")

# Uploading the 'test' directory with its content in the
# '/home/user/dump' remote directory

scp.close()

# extract .tar file
archive = tarfile.open("..\\data\\weather.tar", "r")
archive.extractall("..\\data\\")
archive.close()
shutil.rmtree("..\\data\\weather_data")
shutil.move("..\\data\\home\\marekjachym99\\lavalanche\\weather_data", "..\\data\\")
os.remove("..\\data\\weather.tar")
shutil.rmtree("..\\data\\home")
