from paramiko import SSHClient
from scp import SCPClient
import tarfile, os, shutil, time

overall_time = time.time()
start_time = time.time()
ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect('34.72.152.18', username="marekjachym99")
print("ssh connection took: ", time.time() - start_time)

start_time = time.time()
# SCPCLient takes a paramiko transport as an argument
scp = SCPClient(ssh.get_transport())
scp.get("/home/marekjachym99/lavalanche/weather.tar", "../data")
scp.close()
print("scp copying took: ", time.time() - start_time)
# extract .tar file
start_time = time.time()
archive = tarfile.open("../data/weather.tar", "r")
archive.extractall("../data/")
archive.close()
if os.path.isdir("../data/weather_data"):
    shutil.rmtree("../data/weather_data")
shutil.move("../data/home/marekjachym99/lavalanche/weather_data", "../data/")
os.remove("../data/weather.tar")
shutil.rmtree("../data/home")
print("file handling took: ", time.time() - start_time)
print("whole process took: ", time.time() - overall_time)
