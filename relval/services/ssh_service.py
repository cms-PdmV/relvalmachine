__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from relval import app
import paramiko
import os


class SshService(object):
    """ Service for communicating with ssh server
    """

    def __init__(self, hostname=None, username=None, password=None):
        self.hostname = hostname or app.config["SSH_HOSTNAME"]
        self.username = username or app.config["SSH_USER"]
        self.password = password or app.config["SSH_PASSWORD"]
        self.port = 22

        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect_to_server(self):
        try:
            app.logger.info("Connecting to server %s with user %s and password %s" %
                            (self.hostname, self.username, self.password))
            self.ssh_client.connect(
                self.hostname,  port=self.port, username=self.username,  password=self.password)
        except paramiko.AuthenticationException:
            app.logger.error("Authentication failed. ")
            raise
        except paramiko.SSHException:
            app.logger.error("Cannot connect to server via SSH. Server: %s" % self.hostname)
            raise
        except Exception:
            app.logger.error("Unknown error connecting to ssh server %s" % self.hostname)
            raise

    def execute(self, command):
        app.logger.info("Executing command in server\n%s\n" % command)
        _, stdout, stderr = self.ssh_client.exec_command(command)

        logs = stdout.read()
        errors = stderr.read()

        app.logger.info("STDOUT from server: " + logs)
        app.logger.info("STDERR from server: " + errors)

        return logs, errors

    def get_sftp_client(self):
        return self.ssh_client.open_sftp()

    def upload_file_to_server(self, path, file_name, data):
        # make sure dir exists for file if not create it
        _, errors = self.execute("mkdir -p {0}".format(path))
        if errors:
            print "ERROR: ", errors
            raise Exception("Failed to upload file. Cannot create dir for json files. {0}".format(errors))
        app.logger.info("Uploading:\n{0}\nInto {1}".format(data, path))
        try:
            sftp_client = self.ssh_client.open_sftp()
            with sftp_client.open(os.path.join(path, file_name), "wb") as f:
                f.write(data)
        except Exception as ex:
            print "Not uploaded"
            app.logger.error("Failed to upload file: {0}".format(str(ex)))
            raise ex

    def get_file_content(self, path):
        sftp_client = self.ssh_client.open_sftp()
        with sftp_client.open(path, "r") as f:
            return f.read()

    def remove_file(self, path):
        sftp_client = self.ssh_client.open_sftp()
        sftp_client.remove(path)






class Job(object):
    pass