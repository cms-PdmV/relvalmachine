__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"


""" relval.tests.factory

    Objects factory to create objects for unit tests.
"""

from relval.database.models import \
    Users, Requests, Steps, PredefinedBlob, Parameters, StepType
from datetime import datetime


def user():
    return Users(
        user_name="TestUsername",
        email="test@mail",
        role="user",
        notifications=True)


def predefined_blob(params_count=1):
    return PredefinedBlob(
        title="test-title",
        creation_date=datetime.utcnow(),
        immutable=False,
        parameters=[
            Parameters(flag="F%d" % i, value="V%d" % i) for i in range(params_count)
        ])

def data_step(data_set="test-data-set", files="1", events="1", split="1"):
    return {
        "data_set": data_set,
        "label": "test-label",
        "run": "test-run",
        "ib_block": "test-ib-block",
        "ib_blacklist": "test-ib-blacklist",
        "location": "test-location",
        "files": files,
        "events": events,
        "split": split
    }


def step(title="test-title", parameters_count=1, blobs_count=1,
                 immutable=False, type=StepType.Default, data_set=""):
    return Steps(
        title=title,
        immutable=immutable,
        type=type,
        data_set=data_set,
        parameters=[
            Parameters(flag="F%d" % i, value="V%d" % i) for i in range(parameters_count)
        ],
        predefined_blobs=[
            predefined_blob() for _ in range(blobs_count)
        ]
    )


def parameters(params_count=1):
    return [
        {"flag": "F%d" % i, "value": "V%d" % i} for i in range(params_count)
    ]


class JSONRequests(object):
    """ Class stores methods for request json creation
    """

    new_blob_title = "new-blob-title"

    @staticmethod
    def new_blob():
        return {
            "title": "test-blob-title",
            "immutable": False,
            # "current_time": datetime.now().isoformat(),
            "parameters": [
                {"flag": "flag1", "value": "value1"},
                {"flag": "flag2", "value": "value2"}
            ]
        }

    @staticmethod
    def update_blob():
        return {
            "title": JSONRequests.new_blob_title,
            "immutable": True,
            "parameters": [
                {"flag": "flag1", "value": "value1"},
                {"flag": "flag2", "value": "value2"},
                {"flag": "flag3", "value": "value3"}
            ]
        }

    @staticmethod
    def new_step():
        return {
            "title": "test-title",
            "immutable": True,
            "data_set": "test-data-set",
            "parameters": [
                {"flag": "flag1", "value": "value1"}
            ],
            "blobs": [{"id": 1}],
            "type": StepType.Default
        }

    @staticmethod
    def update_step():
        return {
            "title": JSONRequests.new_blob_title,
            "immutable": True,
            "parameters": [
                {"flag": "flag1", "value": "value1"},
                {"flag": "flag2", "value": "value2"},
                {"flag": "flag3", "value": "value3"}
            ],
            "blobs": [{"id": 1}],
            "type": StepType.Default,
            "data_set": "test-data-set"
        }
