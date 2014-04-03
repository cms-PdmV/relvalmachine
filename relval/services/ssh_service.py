__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from relval import app
import paramiko


class SshService(object):

    def __init__(self, hostname=None, username=None, password=None):
        self.hostname = hostname or app.config["HOSTNAME"]
        self.username = username or app.config["USER"]
        self.password = password or app.config["PASSWORD"]
        self.port = 22

        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def execute(self, command):
        self.ssh_client.connect(
            self.hostname,  port=self.port, username=self.username,  password=self.password)
        stdin, stdout, stderr = self.ssh_client.exec_command(command)

        print "Out: ", stdout.read()
        print "Err: ", stderr.read()






class Job(object):
    pass