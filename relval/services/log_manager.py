__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

import os
from relval import app

class LogsManager(object):
    """ Service that manages logs from testing submission and other servers.
    """

    def __init__(self):
        self.logs_dir = app.config["LOGS_FROM_SERVER_DIR"]

    def save_testing_log(self, name, text):
        self.save_log(name, text, "tests")

    def save_log(self, name, text, subdir):
        path = os.path.join(self.logs_dir, subdir)
        print path
        if not os.path.exists(path):
            os.makedirs(path)
        name = self.__get_file_name(name)
        filename = os.path.join(path, name)
        print filename
        with open(filename, "w") as log_file:
            log_file.write(text)

    def get_testing_log(self, name):
        return self.get_log(name, "tests")

    def get_log(self, name, subdir):
        name = self.__get_file_name(name)
        filename = os.path.join(self.logs_dir, subdir, name)
        print filename
        with open(filename, "r") as log_file:
            content = log_file.read()
            return content

    def __get_file_name(self, name):
        return self.__turn_into_valid_file_name(name) + ".log"

    def __turn_into_valid_file_name(self, name):
        return "".join(x for x in name if x.isalnum())
