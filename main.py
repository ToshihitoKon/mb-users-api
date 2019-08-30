import datetime
import json
from distutils.util import strtobool

from flask import Flask, request, jsonify
from flask_cors import CORS

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

configFile = open('config.json', 'r')
config = json.load(configFile)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

def initialize_admin():
    cred = credentials.Certificate(config['certificateFile'])
    firebase_admin.initialize_app(cred, { 'databaseURL': config['databaseUrl'] })

@app.route('/users/search', methods=['POST'])
def users_search():
    try:
        userId = request.json['userId']
    except:
        return jsonify(), 400

    ref = db.reference('/users/' + userId)
    res = ref.get()
    if not res:
        return jsonify(), 200
    res['userId'] = userId
    return jsonify(res), 200

@app.route('/users/regist', methods=['POST'])
def users_regist():
    user = dict()

    # require args
    try:
        user['userName'] = request.json['userName']
    except:
        return jsonify(), 400

    # optional args
    try:
        user['isMonthlyMembership'] = strtobool(request.json['isMonthlyMembership']) == 1
    except:
        user['isMonthlyMembership'] = False

    user['contractDate'] = datetime.date.today().isoformat()
    ref = db.reference('/users')
    newItem = ref.push(user)

    res = newItem.get()
    res['userId'] = newItem.key
    return jsonify(res), 200

initialize_admin()
app.run(host=config['host'], port=config['port'])
