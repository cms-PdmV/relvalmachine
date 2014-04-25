__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

import os
import shutil
import time
import re
from jinja2.environment import Environment
from jinja2.loaders import PackageLoader
from relval import app
from relval.services.ssh_service import SshService


class LogFile(object):
    """ Class to store data of a lig file.
    """
    def __init__(self, path, filename="", content=""):
        self.path = path
        self.filename = filename
        self.content = content

    def full_path(self):
        if not self.filename:
            return self.path
        else:
            return os.path.join(self.path, self.filename)


class LogsManager(object):
    """ Service that manages logs from testing submission and other servers.
    """

    def __init__(self):
        self.logs_dir = app.config["LOGS_FROM_SERVER_DIR"]

        # check if we need to ssh into machine when
        if self.logs_dir.startswith("/afs"):
            self.logs_handler = LogsOnExternalMachineHandler()
        else:
            self.logs_handler = LogsOnFileSystemHandler()

    def save_testing_log(self, name, errors, info, subdir):
        path = os.path.join(self.logs_dir, subdir)
        errors_file_name = self.__get_file_name(self.stderr_log(name))
        info_file_name = self.__get_file_name(self.stdout_log(name))
        files_to_save = []
        if errors:
            files_to_save.append(LogFile(
                path=path,
                filename=errors_file_name,
                content=errors
            ))
        else:  # remove old log if no errors was
            self.logs_handler.remove_log(LogFile(path=os.path.join(path, errors_file_name)))

        files_to_save.append(LogFile(
            path=path,
            filename=info_file_name,
            content=info
        ))
        self.logs_handler.save_log_file(files_to_save)

    def get_logs(self, name, subdir):
        """ Returns both stdout and stderr logs
        """
        path = os.path.join(self.logs_dir, subdir)

        files = [
            LogFile(path=path, filename=self.__get_file_name(self.stdout_log(name))),
            LogFile(path=path, filename=self.__get_file_name(self.stderr_log(name)))
        ]
        contents = self.logs_handler.get_log_file(files)

        return "STDOUT:\n{0}\nSTDERR:\n{1}".format(
            contents[0],
            contents[1])

    def delete_old_test_log_files(self):
        self.logs_handler.delete_old_logs(app.config["DAYS_TO_KEEP_LOGS"], self.logs_dir)

    def __get_file_name(self, name):
        return self.__turn_into_valid_file_name(name) + ".log"

    def __turn_into_valid_file_name(self, name):
        return re.sub(r"[^-a-zA-Z0-9_.() ]+", '', name)

    @classmethod
    def remove_dir_or_file(cls, dir_name):
        if os.path.isfile(dir_name):
            os.unlink(dir_name)
        else:
            shutil.rmtree(dir_name)

    def remove_if_exists(self, name, dir_name):
        path = os.path.join(self.logs_dir, dir_name, self.__get_file_name(name))
        if os.path.exists(path):
            os.remove(path)


    stderr_log = lambda self, name: "%s_stderr" % name
    stdout_log = lambda self, name: "%s_stdout" % name


class LogsHandler(object):

    def save_log_file(self, log_files):
        raise NotImplementedError("LogsHandler is abstract. Please extend and override this method.")

    def get_log_file(self, log_files):
        raise NotImplementedError("LogsHandler is abstract. Please extend and override this method.")

    def remove_log(self, log_files):
        raise NotImplementedError("LogsHandler is abstract. Please extend and override this method.")

    def delete_old_logs(self, time_limit, path):
        raise NotImplementedError("LogsHandler is abstract. Please extend and override this method.")


class LogsOnFileSystemHandler(LogsHandler):

    def save_log_file(self, log_files):
        if type(log_files) is not list:
            log_files = [log_files]
        for log in log_files:
            if not os.path.exists(log.path):
                os.makedirs(log.path)
            app.logger.info("Saving log to {0}".format(log.full_path()))
            with open(log.full_path(), "w") as log_file:
                log_file.write(log.content)

    def get_log_file(self, log_files):
        contents = []
        if type(log_files) is not list:
            log_files = [log_files]
        for log in log_files:
            try:
                with open(log.full_path(), "r") as log_file:
                    content = log_file.read()
                    contents.append(content)
            except Exception as ex:
                app.logger.info("Failed to find log file {0}. Error: {1}".format(log.full_path(), str(ex)))
                contents.append("")
        return contents

    def remove_log(self, log_files):
        if type(log_files) is not list:
            log_files = [log_files]
        for log in log_files:
            if os.path.exists(log.full_path()):
                os.remove(log.full_path())

    def delete_old_logs(self, time_limit, path):
        current_time = time.time()

        # This is days
        # limit = current_time - 60 * 60 * 24 * time_limit
        # This is minutes use only for testing to test. In prod we use days
        limit = current_time - 60 * time_limit

        current_time = time.time()
        if not os.path.exists(path):
            os.makedirs(path)
        for directory in os.listdir(path):
            path_to_file = os.path.join(path, directory)
            st = os.stat(path_to_file)
            mtime = st.st_mtime
            if mtime < limit:
                app.logger.info("Removing old directory %s. It is %d minutes old" % (
                    directory, int((current_time - mtime) / 60)))
                LogsManager.remove_dir_or_file(path_to_file)


class LogsOnExternalMachineHandler(LogsHandler):

    def __init__(self):
        self.ssh = SshService()
        self.env = Environment(loader=PackageLoader("relval", "/templates/bash"))

    def save_log_file(self, log_files):
        if type(log_files) is not list:
            log_files = [log_files]
        for log in log_files:
            try:
                self.ssh.connect_to_server()
                self.ssh.upload_file_to_server(log.path, log.filename, log.content)
            except Exception:
                pass  # do not stop if one file fails

    def get_log_file(self, log_files):
        if type(log_files) is not list:
            log_files = [log_files]
        contents = []
        self.ssh.connect_to_server()
        sftp = self.ssh.get_sftp_client()
        for log in log_files:
            try:
                with sftp.open(log.full_path, "r") as f:
                    contents.append(f.read())
            except Exception as ex:
                app.logger.info("Failed to find log file {0}. Error: {1}".format(log.full_path(), str(ex)))
                return contents.append("")
        return contents

    def remove_log(self, log_files):
        if type(log_files) is not list:
            log_files = [log_files]
        self.ssh.connect_to_server()
        sftp = self.ssh.get_sftp_client()
        for log in log_files:
            try:
                sftp.remove(log.full_path)
            except Exception as ex:
                app.logger.info("Cannot find file {0}".format(log.full_path))
                pass  # file not exists

    def delete_old_logs(self, time_limit, path):  # time limit in days
        template = self.env.get_template('delete_old_logs.sh')

        params = dict(
            days_to_keep_logs=time_limit,
            directory=path)

        command = template.render(params)
        try:
            self.ssh.connect_to_server()
            self.ssh.execute(command)
        except Exception as ex:
            app.logger.error(
                "Failed to execute command on server when cleaning up old log files. Error: {0}".format(str(ex)))
