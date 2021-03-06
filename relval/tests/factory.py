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

def data_step(data_set="test-data-set", files="1", events="1", split="1", ib_block="test-ib-block", run="123,321"):
    return {
        "data_set": data_set,
        "label": "test-label",
        "run": run,
        "ib_block": ib_block,
        "ib_blacklist": "test-ib-blacklist",
        "location": "test-location",
        "files": files,
        "events": events,
        "split": split
    }


def step(title="test-title", parameters_count=1, blobs_count=1, name="",
                 immutable=False, type=StepType.Default):
    return Steps(
        title=title,
        name=name,
        immutable=immutable,
        type=type,
        parameters=[
            Parameters(flag="F%d" % i, value="V%d" % i) for i in range(parameters_count)
        ],
        predefined_blobs=[
            predefined_blob() for _ in range(blobs_count)
        ]
    )


def request(label="test-title", description="desc", immutable=False, cmssw_release="7_0_0",
            run_the_matrix_conf="-l -i", events=20, priority=3, type="mc", steps_count=3):
    return Requests(
        label=label,
        description=description,
        immutable=immutable,
        cmssw_release=cmssw_release,
        run_the_matrix_conf=run_the_matrix_conf,
        events=events,
        priority=priority,
        type=type,
        steps=[
            step() for _ in range(steps_count)
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

    @staticmethod
    def new_request():
        return {
            "label": "test-title",
            "description": "test-description",
            "immutable": True,
            "cmssw_release": "7_0_0",
            "steps": [
                {"id": "1"}, {"id": "2"}
            ],
            "type": "test-type",
            "run_the_matrix_conf": "-wm=init",
            "events": 10,
            "priority": 2
        }
