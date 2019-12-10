import subprocess
import start_servers as s

subprocess.Popen([s.GetPythonCommand(), s.loc() + '/config/configuration_manager.py'], shell=False)
