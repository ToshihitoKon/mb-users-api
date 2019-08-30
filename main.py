import datetime
import json
from distutils.util import strtobool

from flask import Flask, request

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

configFile = open('config.json', 'r')
config = json.load(configFile)

app = Flask(__name__)

def initialize_admin():
    cred = credentials.Certificate(config['certificateFile'])
    firebase_admin.initialize_app(cred, { 'databaseURL': config['databaseUrl'] })

@app.route('/users/search', methods=['POST'])
def users_search():
    userId = request.form['userId']
    ref = db.reference('/users/' + userId)
    res = ref.get()
    if not res:
        return json.dumps('', ensure_ascii=False), 200
    res['userId'] = userId
    return json.dumps(res, ensure_ascii=False), 200

@app.route('/users/regist', methods=['POST'])
def users_regist():
    user = {
        'userName' : request.form['userName'],
        'contractDate' : datetime.date.today().isoformat(),
    }
    try:
        user['isMonthlyMembership'] = strtobool(request.form['isMonthlyMembership']) == 1
    except:
        user['isMonthlyMembership'] = False

    ref = db.reference('/users')
    newItem = ref.push(user)
    res = newItem.get()
    res['userId'] = newItem.key
    return json.dumps(res, ensure_ascii=False), 200

initialize_admin()
app.run(host=config['host'], port=config['port'])
