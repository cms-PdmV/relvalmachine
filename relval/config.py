__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

#TODO: figure out how to hide those in git
RELVAL_DB__PASSWORD = "123456"
RELVAL_DB_USER      = "zee"


SQLALCHEMY_DATABASE_URI = "oracle+cx_oracle://%s:%s@localhost:1521/xe" % (
    RELVAL_DB_USER,
    RELVAL_DB__PASSWORD
)