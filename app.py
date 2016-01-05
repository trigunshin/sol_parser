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
    name, values = pyamf.sol.decode(sol_file)
    return values

@app.route('/')
def hello():
    return 'Hello World! POST a .SOL file to /decode as a file named "file"'

@app.route('/decode', methods=['POST'])
@cross_origin(methods=['POST'])
def decode():
    sol_file = request.files['file']
    decoded_file = decode_file(sol_file)

    for key, val in decoded_file['inventoryExpiry'].iteritems():
        if val == float('inf'):
            decoded_file['inventoryExpiry'] = -1

    return jsonify(data=decoded_file)

if __name__ == '__main__':
    app.run()
