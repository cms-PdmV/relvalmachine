from sqlalchemy.orm import backref

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.database.models

    Defined models for relval machine database
"""


from relval import db


class Users(db.Model):
    __tablename__ = "USERS"
    id = db.Column("ID", db.Integer, db.Sequence("user_id_seq"), primary_key=True)
    user_name = db.Column('USER_NAME', db.String(128))
    email = db.Column('EMAIL', db.String(128))
    role = db.Column('ROLE', db.String(64))
    notifications = db.Column('NOTIFICATIONS', db.Boolean, default=True)

    requests = db.relationship("Requests", backref="user")

    #TODO: add __repr__


class Batches(db.Model):
    __tablename__ = "BATCHES"
    id = db.Column("ID", db.Integer, db.Sequence("batch_id_seq"), primary_key=True)
    title = db.Column("TITLE", db.String(256))
    description = db.Column("DESCRIPTION", db.String(2048))

    requests = db.relationship("Requests", backref="batch")

    #TODO: add __repr__


class Requests(db.Model):
    __tablename__ = "REQUESTS"
    id = db.Column("ID", db.Integer, db.Sequence("request_id_seq"), primary_key=True)
    status = db.Column("STATUS", db.String(64))
    test_status = db.Column("TEST_STATUS", db.String(64))
    priority = db.Column("PRIORITY", db.Integer)
    type = db.Column("TYPE", db.String(128))
    cmssw_release = db.Column("CMSSW_RELEASE", db.String(128))
    description = db.Column("DESCRIPTION", db.String(2048))
    log_url = db.Column("LOG_URL", db.String(1024))
    event = db.Column("EVENTS", db.Integer)
    user_id = db.Column("USER_ID", db.Integer, db.ForeignKey("USERS.ID"), nullable=False)
    batch_id = db.Column("BATCH_ID", db.Integer, db.ForeignKey("BATCHES.ID"), nullable=True)

    revisions = db.relationship("Revisions", backref="request")

    #TODO: add __repr__


class Revisions(db.Model):
    __tablename__ = "REVISIONS"
    id = db.Column("ID", db.Integer, db.Sequence("revision_id_seq"), primary_key=True)
    proposal_date = db.Column("PROPOSAL_DATE", db.DateTime)
    revision_number = db.Column("REVISION_NUMBER", db.Integer)
    run_the_matrix_conf = db.Column("RUN_THE_MATRIX_CONF", db.String(2048))
    request_id = db.Column("REQUEST_ID", db.Integer, db.ForeignKey("REQUESTS.ID"), nullable=False)

    steps = db.relationship("Steps", backref="revision")

    #TODO: add __repr__


class Steps(db.Model):
    __tablename__ = "STEPS"
    id = db.Column("ID", db.Integer, db.Sequence("step_id_seq"), primary_key=True)
    sequence_number = db.Column("SEQUENCE_NUMBER", db.Integer)
    name = db.Column("NAME", db.String(256))
    data_set = db.Column("DATA_SET", db.String(1024))
    run_lumi = db.Column("RUN_LUMI", db.Text)
    revision_id = db.Column("REVISION_ID", db.Integer, db.ForeignKey("REVISIONS.ID"), nullable=False)

    parameters = db.relationship("Parameters", backref="step")

    #TODO: add __repr__


class Parameters(db.Model):
    id = db.Column("ID", db.Integer, db.Sequence("parameter_id_seq"), primary_key=True)
    flag = db.Column("FLAG", db.String(256))
    value = db.Column("VALUE", db.String(256))
    step_id = db.Column("STEP_ID", db.Integer, db.ForeignKey("STEPS.ID"), nullable=False)

    #TODO: add __repr__