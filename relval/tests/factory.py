__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"


""" relval.tests.factory

    Objects factory to create objects for unit tests.
"""

from relval.database.models import \
    Users, Requests, Revisions, Steps, PredefinedBlob, Parameters
from datetime import datetime

def user():
    return Users(
        user_name="TestUsername",
        email="test@mail",
        role="user",
        notifications=True)


def create_revision(rev_num=1):
    return Revisions(
        revision_number=rev_num,
        run_the_matrix_conf="-wm=init",
        steps=[
            Steps(
                name="step1"
            ),
            Steps(
                name="step2"
            ),
        ])


def request():
    return Requests(
        status="NEW",
        test_status="NOT-TESTED",
        priority=1,
        type="TYPE",
        cmssw_release="7_0_0",
        description="test description",
        log_url="test-log-url",
        event=100,
        user=Users(
            user_name="TestUsername",
            email="test@mail",
            role="user",
            notifications=True),
        revisions=[
            create_revision(1)
        ])


def predefined_blob(params_count=1):
    return PredefinedBlob(
        title="test-title",
        creation_date=datetime.utcnow(),
        parameters=[
            Parameters(flag="F%d" % i, value="V%d" % i) for i in range(params_count)
        ])


def predefined_blob_paramters(params_count=1):
    return [
        {"flag": "F%d" % i, "value": "V%d" % i} for i in range(params_count)
    ]

