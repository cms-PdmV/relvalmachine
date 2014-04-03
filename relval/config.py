__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

import ConfigParser

# Set this property before deployment to identify environment
# Available environments "LOCAL", "DEVELOPMENT", "PRODUCTION"
ENVIRONMENT = "LOCAL"

LOCAL_ENV_CONFIG_FILE = "relval/configuration/local.properties"
DEVELOPMENT_ENV_CONFIG_FILE = "/afs/cern.ch/user/z/zgatelis/development.properties"
PRODUCTION_ENV_CONFIG_FILE = ""


# Load configuration from another file
if ENVIRONMENT == "LOCAL":
    config_file = LOCAL_ENV_CONFIG_FILE
elif ENVIRONMENT == "DEVELOPMENT":
    config_file = DEVELOPMENT_ENV_CONFIG_FILE
elif ENVIRONMENT == "PRODUCTION":
    config_file = PRODUCTION_ENV_CONFIG_FILE
else:
    raise Exception("%s is not valid environment. Use one of: [LOCAL, DEVELOPMENT, PRODUCTION]")

configuration = ConfigParser.ConfigParser()
configuration.readfp(open(config_file))


#
# Configuration setup
#
RELVAL_DB_PASSWORD = configuration.get("DB", "PASSWORD")
RELVAL_DB_USER = configuration.get("DB", "USER")
RELVAL_DB_HOST = configuration.get("DB", "HOST")
RELVAL_DB_PORT = configuration.get("DB", "PORT")
RELVAL_DB_SID = configuration.get("DB", "SID")

SSH_HOSTNAME = configuration.get("SSH", "HOSTNAME")
SSH_USER = configuration.get("SSH", "USER")
SSH_PASSWORD = configuration.get("SSH", "PASSWORD")

SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = "oracle+cx_oracle://%s:%s@%s:%s/%s" % (
    RELVAL_DB_USER,
    RELVAL_DB_PASSWORD,
    RELVAL_DB_HOST,
    RELVAL_DB_PORT,
    RELVAL_DB_SID
)
LOGGER_NAME="relval"

BLOBS_PER_PAGE=20
STEPS_PER_PAGE=20
REQUESTS_PER_PAGE=20
BATCHES_PER_PAGE=20