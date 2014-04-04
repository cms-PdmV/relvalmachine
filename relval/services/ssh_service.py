__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from relval import app
import paramiko


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

    def execute(self, command):
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

        app.logger.debug("Executing command in server\n%s\n" % command)
        _, stdout, stderr = self.ssh_client.exec_command(command)

        logs = stdout.read()
        errors = stderr.read()

        app.logger.debug("STDOUT from server: " + logs)
        app.logger.debug("STDERR from server: " + errors)

        # todo save logs or what?

        return logs, errors


class Job(object):
    pass