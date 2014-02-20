#!/usr/bin/python2.6

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

import os
from relval import app


def run_server():
    port = int(os.environ.get('PORT', 8000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)


if __name__ == "__main__":
    run_server()