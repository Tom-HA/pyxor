from flask import Flask, jsonify, request
from parser import parser

app = Flask(__name__)


@app.route("/health")
def health_check():
    return '', 200


@app.route('/api/yaml_extract', methods=['POST'])
def extract_yaml():
    if not request.is_json:
        return jsonify({"data": "Content-type was not detected as application/json"}), 400
    try:
        data = request.get_json()
        r = parser.extract_values_from_yaml(data['text'], data['expr'])
        resp = jsonify({"data": r})
        return resp, 200
    except Exception as e:
        return jsonify({"data": str(e)}), 400
    

