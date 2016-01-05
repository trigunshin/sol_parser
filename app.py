import os
import binascii, logging, json
import pyamf.sol
from pyamf import Undefined
import pyamf.util.pure
import StringIO

from flask import Flask, request, jsonify
from flask.ext.cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# pyamf.Undefined should translate to ''
class AMFEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if obj == Undefined:
            return ""
        return json.JSONEncoder.default(self, obj)
app.json_encoder = AMFEncoder

def decode_file(sol_file):
    stream = pyamf.util.pure.BufferedByteStream(sol_file)
    name, values = pyamf.sol.decode(stream)
    return values

@app.route('/')
def hello():
    return 'Hello World! POST a .SOL file to /decode as a file named "file"'

@app.route('/decode', methods=['POST'])
@cross_origin(methods=['POST'])
def decode():
    print 'files', request.files
    print 'values', request.values
    print 'form', request.form
    sol_file = request.files['file']
    print sol_file
    decoded_file = decode_file(sol_file)

    return jsonify(data=decoded_file)

if __name__ == '__main__':
    app.run(debug=True)
