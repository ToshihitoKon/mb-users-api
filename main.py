import datetime
import json

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
    userId = request.form['userId']
    user = {
        'userName' : request.form['userName'],
        'isMonthlyMembership' : request.form['isMonthlyMembership'] == 'true',
        'contractDate' : datetime.date.today().isoformat(),
    }

    ref = db.reference('/users/' + userId)
    if ref.get():
        return json.dumps({'error':'userid duplicate'}, ensure_ascii=False), 409

    ref.set(user)
    res = ref.get()
    res['userId'] = userId
    return json.dumps(res, ensure_ascii=False), 200

if __name__ == '__main__':
    initialize_admin()
    app.run(host='0.0.0.0')
