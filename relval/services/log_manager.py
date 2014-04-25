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
        if errors:
            self.logs_handler.save_log_file(errors_file_name, path, errors)
        else:  # remove old log if no errors was
            self.logs_handler.remove_log(os.path.join(path, errors_file_name))

        self.logs_handler.save_log_file(info_file_name, path, info)

    def get_logs(self, name, subdir):
        """ Returns both stdout and stderr logs
        """
        path = os.path.join(self.logs_dir, subdir)
        return "STDOUT:\n{0}\nSTDERR:\n{1}".format(
            self.get_testing_std_out_log(name, path),
            self.get_testing_std_error_log(name, path))

    def get_testing_std_error_log(self, name, path):
        file_name = self.__get_file_name(self.stderr_log(name))
        path = os.path.join(path, file_name)
        return self.logs_handler.get_log_file(path)

    def get_testing_std_out_log(self, name, path):
        file_name = self.__get_file_name(self.stdout_log(name))
        path = os.path.join(path, file_name)
        return self.logs_handler.get_log_file(path)

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

    def save_log_file(self, name, path, content):
        raise NotImplementedError("LogsHandler is abstract. Please extend and override this method.")

    def get_log_file(self, path):
        raise NotImplementedError("LogsHandler is abstract. Please extend and override this method.")

    def remove_log(self, path):
        raise NotImplementedError("LogsHandler is abstract. Please extend and override this method.")

    def delete_old_logs(self, time_limit, path):
        raise NotImplementedError("LogsHandler is abstract. Please extend and override this method.")


class LogsOnFileSystemHandler(LogsHandler):

    def save_log_file(self, name, path, content):
        if not os.path.exists(path):
            os.makedirs(path)
        filename = os.path.join(path, name)
        app.logger.info("Saving log to {0}".format(filename))
        with open(filename, "w") as log_file:
            log_file.write(content)

    def get_log_file(self, path):
        try:
            with open(path, "r") as log_file:
                content = log_file.read()
                return content
        except Exception as ex:
            app.logger.info("Failed to find log file {0}. Error: {1}".format(path, str(ex)))
            return ""

    def remove_log(self, path):
        if os.path.exists(path):
            os.remove(path)

    def delete_old_logs(self, time_limit, path):
        current_time = time.time()

        # This is days
        # limit = current_time - 60 * 60 * 24 * time_limit
        # This is minutes
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

    def save_log_file(self, name, path, content):
        self.ssh.connect_to_server();
        self.ssh.upload_file_to_server(path, name, content)

    def get_log_file(self, path):
        self.ssh.connect_to_server();
        try:
            content = self.ssh.get_file_content(path)
            return content
        except Exception as ex:
            app.logger.info("Failed to find log file {0}. Error: {1}".format(path, str(ex)))
            return ""

    def remove_log(self, path):
        self.ssh.connect_to_server()
        try:
            self.ssh.remove_file(path)
        except Exception as ex:
            app.logger.info("Cannot find file {0}".format(path))
            pass  # file not exists

    def delete_old_logs(self, time_limit, path):  # time limit in days
        template = self.env.get_template('delete_old_logs.sh')

        params = dict(
            days_to_keep_logs=time_limit,
            directory=path)

        command = template.render(params)
        try:
            self.ssh.execute(command)
        except Exception as ex:
            app.logger.error(
                "Failed to execute command on server when cleaning up old log files. Error: {0}".format(str(ex)))
