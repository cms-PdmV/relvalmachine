__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from relval import app
import os
from flask import make_response, send_from_directory

HTML_TEMPLATES = "relval/templates/%s"

@app.route('/')
def index():
    print app.template_folder
    return make_response(open(HTML_TEMPLATES % 'index.html').read())

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'), 'favicon.ico')