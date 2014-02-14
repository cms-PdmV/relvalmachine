#!/usr/bin/python2.6

import os
from flask import Flask
from flask import send_from_directory, make_response

app = Flask(__name__)

def run_server():
    port = int(os.environ.get('PORT', 8000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)

@app.route('/')
def index():
    return make_response(open('templates/index.html').read())

@app.route('/new')
def new_request():
    print "New req"
    return make_response(open('templates/index.html').read())

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'), 'favicon.ico')


if __name__ == "__main__":
    run_server()