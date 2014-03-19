__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from relval import app
import os
from flask import make_response, send_from_directory
from flask import jsonify, request


HTML_TEMPLATES = "relval/templates/%s"

@app.route('/')
def index():
    return make_response(open(HTML_TEMPLATES % 'index.html').read())

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'), 'favicon.ico')\

@app.route("/api/validate/step", methods=['POST'])
def validate_step():
    print "Validating", request.data
    return jsonify(
        valid=False
    )