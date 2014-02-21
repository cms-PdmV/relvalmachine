__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

#TODO: figure out how to hide those in git
# This is local setup. It works only on my pc :)
RELVAL_DB_PASSWORD = "123456"
RELVAL_DB_USER = "zee"
RELVAL_DB_HOST = "localhost"
RELVAL_DB_PORT = "1521"
RELVAL_DB_SID = "xe"


SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = "oracle+cx_oracle://%s:%s@%s:%s/%s" % (
    RELVAL_DB_USER,
    RELVAL_DB_PASSWORD,
    RELVAL_DB_HOST,
    RELVAL_DB_PORT,
    RELVAL_DB_SID
)