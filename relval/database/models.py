__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.database.models

    Defined models for relval machine database
"""


from relval import db


class Users(db.Model):
    id = db.Column("ID", db.Integer, db.Sequence("user_id_seq"), primary_key= True)
    user_name = db.Column('USER_NAME', db.String(128))
    email = db.Column('EMAIL', db.String(128))
    role = db.Column('ROLE', db.String(64))
    notifications = db.Column('NOTIFICATIONS', db.Boolean, default=True)

    #TODO: add __repr__


class Batches(db.Model):
    id = db.Column("ID", db.Integer, db.Sequence("batch_id_seq"), primary_key=True)
    title = db.Column("TITLE", db.String(256))
    description = db.Column("DESCRIPTION", db.String(2048))

    #TODO: add __repr__


class Requests(db.Model):
    id = db.Column("ID", db.Integer, db.Sequence("request_id_seq"), primary_key=True)
    db.Column("STATUS", db.String(64))
    db.Column("TEST_STATUS", db.String(64))
    db.Column("PRIORITY", db.Integer)
    db.Column("TYPE", db.String(128))
    db.Column("CMSSW_RELEASE", db.String(128))
    db.Column("DESCRIPTION", db.String(2048))
    db.Column("LOG_URL", db.String(1024))
    db.Column("EVENTS", db.Integer)
    db.Column("USER_ID", db.Integer, db.ForeignKey("USERS.ID"), nullable=False)
    db.Column("BATCH_ID", db.Integer, db.ForeignKey("BATCHES.ID"), nullable=False)

    #TODO: add __repr__


class Revisions(db.Model):
    id = db.Column("ID", db.Integer, db.Sequence("revision_id_seq"), primary_key=True)
    db.Column("PROPOSAL_DATE", db.DateTime)
    db.Column("REVISION_NUMBER", db.Integer)
    db.Column("RUN_THE_MATRIX_CONF", db.String(2048))
    db.Column("REQUEST_ID", db.Integer, db.ForeignKey("REQUESTS.ID"), nullable=False)

    #TODO: add __repr__


class Steps(db.Model):
    id = db.Column("ID", db.Integer, db.Sequence("step_id_seq"), primary_key=True)
    db.Column("SEQUENCE_NUMBER", db.Integer)
    db.Column("NAME", db.String(256))
    db.Column("DATA_SET", db.String(1024))
    db.Column("RUN_LUMI", db.Text)
    db.Column("REVISION_ID", db.Integer, db.ForeignKey("REVISIONS.ID"), nullable=False)

    #TODO: add __repr__


class Parameters(db.Model):
    id = db.Column("ID", db.Integer, db.Sequence("parameter_id_seq"), primary_key=True)
    db.Column("FLAG", db.String(256))
    db.Column("VALUE", db.String(256))
    db.Column("STEP_ID", db.Integer, db.ForeignKey("STEPS.ID"), nullable=False)

    #TODO: add __repr__