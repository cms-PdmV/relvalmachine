__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"


class UsersManagementService(object):

    def get_username(self, header):
        return UsersManagementService.get_from_header(header, "Login")

    def get_email(self, header):
        return UsersManagementService.get_from_header(header, "Email")

    @staticmethod
    def get_from_header(header, value, default=""):
        value = "Adfs-{0}".format(value)
        return header.get(value, default=default)