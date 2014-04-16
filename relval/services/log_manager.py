__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

import os
import shutil
import time
import re
from relval import app


class LogsManager(object):
    """ Service that manages logs from testing submission and other servers.
    """

    def __init__(self):
        self.logs_dir = app.config["LOGS_FROM_SERVER_DIR"]

    def save_testing_log(self, name, errors, info, subdir):
        logs_dir = os.path.join("tests", subdir)
        if errors:
            self.save_log(self.stderr_log(name), errors, logs_dir)
        else:  # remove old log if no errors was
            self.remove_if_exists(self.stderr_log(name), logs_dir)

        self.save_log(self.stdout_log(name), info, logs_dir)

    def save_log(self, name, text, subdir):
        path = os.path.join(self.logs_dir, subdir)
        if not os.path.exists(path):
            os.makedirs(path)
        name = self.__get_file_name(name)
        filename = os.path.join(path, name)
        app.logger.info("Saving log to {0}".format(filename))
        with open(filename, "w") as log_file:
            log_file.write(text)

    def get_logs(self, name, subdir):
        """ Returns both stdout and stderr logs
        """
        return "STDOUT:\n{0}\nSTDERR:\n{1}".format(
            self.get_testing_std_out_log(name, subdir),
            self.get_testing_std_error_log(name, subdir))

    def get_testing_std_error_log(self, name, subdir):
        return self.__get_log(self.stderr_log(name), os.path.join("tests", subdir))

    def get_testing_std_out_log(self, name, subdir):
        return self.__get_log(self.stdout_log(name), os.path.join("tests", subdir))

    def __get_log(self, name, subdir):
        name = self.__get_file_name(name)
        filename = os.path.join(self.logs_dir, subdir, name)
        try:
            with open(filename, "r") as log_file:
                content = log_file.read()
                return content
        except Exception as ex:
            app.logger.info("Failed to find log file {0}. Error: {1}".format(filename, str(ex)))
            return ""

    def delete_old_test_log_files(self):
        minutes_limit = app.config["DAYS_TO_KEEP_LOGS"]
        current_time = time.time()
        # limit = current_time - 60 * 60 * 24 * days_limit

        limit = current_time - 60 * minutes_limit
        path = os.path.join(self.logs_dir, "tests")
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

