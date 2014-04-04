#!/usr/bin/python2.6

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

import os
from relval import app
from relval.services import tasks_executor


def teardown():
    print "Waiting for executor to finish:", tasks_executor
    tasks_executor.stop()
    print "Executor finished:", tasks_executor


def run_server():
    port_number = 8000 if app.config["ENVIRONMENT"] == "LOCAL" else 80

    port = int(os.environ.get('PORT', port_number))
    app.debug = True
    app.run(host='0.0.0.0', port=port)


if __name__ == "__main__":
    try:
        run_server()

        # executes after server shuts down
        teardown()

    except Exception as ex:
        print ex