from sqlalchemy.orm.util import all_cascades

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.database.models

    Defined models for relval machine database
"""


from relval import db


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column("id", db.Integer, db.Sequence("user_id_seq"), primary_key=True)
    user_name = db.Column('user_name', db.String(128))
    email = db.Column('email', db.String(128))
    role = db.Column('role', db.String(64))
    notifications = db.Column('notifications', db.Boolean, default=True)

    requests = db.relationship("Requests", backref="user")

    #TODO: add __repr__

requests_batches_association = db.Table(
    'requests_batches_association',
    db.Column('request_id', db.Integer, db.ForeignKey('requests.id')),
    db.Column('batch_id', db.Integer, db.ForeignKey('batches.id'))
)


class Batches(db.Model):
    __tablename__ = "batches"
    id = db.Column("id", db.Integer, db.Sequence("batch_id_seq"), primary_key=True)
    title = db.Column("title", db.String(256))
    description = db.Column("description", db.String(2048))
    immutable = db.Column("immutable", db.Boolean, default=False)
    run_the_matrix_conf = db.Column("run_the_matrix_conf", db.String(2048), nullable=True, default=None)
    priority = db.Column("priority", db.Integer, nullable=True, default=None)
    cmssw_release = db.Column("cmssw_release", db.String(128))

    requests = db.relationship(
        'Requests',
        secondary=requests_batches_association,
        backref=db.backref("batches"))

    #TODO: add __repr__


class RequestStatus(object):
    New = "new"
    CurrentlyTesting = "currentlyTesting"
    TestPassed = "testPassed"
    TestFailed = "testFailed"
    Approved = "approved"
    Disapproved = "disapproved"
    SubmittedSuccessful = "submittedSuccessful"
    SubmittedFailed = "submittedFailed"

    @staticmethod
    def types():
        return [RequestStatus.New, RequestStatus.CurrentlyTesting, RequestStatus.TestPassed,
                RequestStatus.TestFailed, RequestStatus.Approved, RequestStatus.Disapproved,
                RequestStatus.SubmittedSuccessful, RequestStatus.SubmittedFailed]


class StepsRequestsAssociation(db.Model):
    __tablename__ = "steps_requests_association"
    id = db.Column("id", db.Integer, db.Sequence("requests_steps_assoc_id_seq"), primary_key=True)
    step_id = db.Column('step_id', db.Integer, db.ForeignKey('steps.id'))
    request_id = db.Column('request_id', db.Integer, db.ForeignKey('requests.id'))

    sequence_number = db.Column('sequence_number', db.Integer)

    step = db.relationship('Steps', backref=db.backref("requests_assoc", cascade="all,delete-orphan"))
    request = db.relationship('Requests', backref=db.backref("steps_assoc", cascade="all,delete-orphan"))


class Requests(db.Model):
    __tablename__ = "requests"
    id = db.Column("id", db.Integer, db.Sequence("request_id_seq"), primary_key=True)
    label = db.Column("label", db.String(256))
    description = db.Column("description", db.String(2048))
    status = db.Column("status", db.Enum(*RequestStatus.types()))
    priority = db.Column("priority", db.Integer)
    type = db.Column("type", db.String(128))
    cmssw_release = db.Column("cmssw_release", db.String(128))
    log_url = db.Column("log_url", db.String(1024))
    events = db.Column("events", db.Integer)
    run_the_matrix_conf = db.Column("run_the_matrix_conf", db.String(2048))
    updated = db.Column("updated", db.DateTime)
    immutable = db.Column("immutable", db.Boolean, default=False)

    ancestor_request_id = db.Column("ancestor_request_id", db.Integer, db.ForeignKey("requests.id"), nullable=True)
    ancestor_request = db.relationship("Requests", remote_side=[id])

    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"), nullable=True)

    #TODO: add __repr__


blobs_steps_association = db.Table(
    'blobs_steps_association',
    db.Column('step_id', db.Integer, db.ForeignKey('steps.id')),
    db.Column('predefined_blob_id', db.Integer, db.ForeignKey('predefined_blob.id'))
)


class StepType(object):
    Default = "default"
    FirstMc = "first_mc"
    FirstData = "first_data"

    @staticmethod
    def types():
        return [StepType.Default, StepType.FirstMc, StepType.FirstData]


class DataStep(db.Model):
    __tablename__ = "data_step"
    id = db.Column("id", db.Integer, db.Sequence("data_step_id_seq"), primary_key=True)
    data_set = db.Column("data_set", db.String(1024))
    label = db.Column("label", db.String(1024))
    run = db.Column("run", db.String(1024))
    ib_block = db.Column("ib_block", db.String(1024))
    ib_blacklist = db.Column("ib_blacklist", db.String(1024))
    files = db.Column("files", db.Integer, default=None)
    events = db.Column("events", db.Integer, default=None)
    split = db.Column("split", db.Integer, default=None)
    location = db.Column("location", db.String(1024))

    step_id = db.Column("step_id", db.Integer, db.ForeignKey("steps.id"), nullable=False)

    #TODO: add __repr__


class Steps(db.Model):
    __tablename__ = "steps"
    id = db.Column("id", db.Integer, db.Sequence("step_id_seq"), primary_key=True)
    title = db.Column("title", db.String(256))
    name = db.Column("name", db.String(512), default="")
    immutable = db.Column("immutable", db.Boolean, default=False)
    type = db.Column("type", db.Enum(*StepType.types()))

    data_step = db.relationship("DataStep", uselist=False, backref="step")
    parameters = db.relationship("Parameters", backref="step")
    predefined_blobs = db.relationship(
        'PredefinedBlob',
        secondary=blobs_steps_association,
        backref=db.backref("steps", lazy="dynamic"))

    #TODO: add __repr__


class PredefinedBlob(db.Model):
    __tablename__ = "predefined_blob"
    id = db.Column("id", db.Integer, db.Sequence("predefined_blob_id_seq"), primary_key=True)
    title = db.Column("title", db.String(256))
    immutable = db.Column("immutable", db.Boolean, default=False)
    creation_date = db.Column("creation_date", db.DateTime)

    parameters = db.relationship(
        "Parameters",
        backref="predefined_blob",
        cascade="all")

    #TODO: add __repr__


class Parameters(db.Model):
    id = db.Column("id", db.Integer, db.Sequence("parameter_id_seq"), primary_key=True)
    flag = db.Column("flag", db.String(256))
    value = db.Column("value", db.String(256))
    step_id = db.Column("step_id", db.Integer, db.ForeignKey("steps.id"), nullable=True)
    predefined_blob_id = db.Column(
        "predefined_blob_id", db.Integer, db.ForeignKey("predefined_blob.id"), nullable=True)

    #TODO: add __repr__