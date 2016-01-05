import os
import binascii, logging, json
import pyamf.sol
from pyamf import Undefined
import pyamf.util.pure
import StringIO

from flask import Flask, request, jsonify

app = Flask(__name__)

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
def decode():
    sol_file = request.files['file']
    decoded_file = decode_file(request.files['file'])

    return jsonify(data=decoded_file)

if __name__ == '__main__':
    app.run()