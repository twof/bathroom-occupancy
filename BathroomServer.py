from flask import Flask, request, jsonify
from collections import deque
from Person import Person
import json
import os
import requests
import datetime
import threading
app = Flask(__name__)

reserveBathroom = deque([])
now = datetime.datetime.now()
response_url = ''
token = 'U9asCwmXUbaFgAtsEpBZjIEj'
thirty_minutes_seconds = 30 * 60 * 60
bathroomOccupied = False


@app.route('/')
def hello():
    return 'Hello, welcome to Bathroom Server'


# Check whether this user has made a reservation
def checkUserReservation(user):
    for user_id in reserveBathroom:
        if user == user_id:
            return True
    return False


# check the users whose reservation have gone over limit
def remove_reservation_waisters():
    threading.Timer(10.0, remove_reservation_waisters).start()
    for person in reserve_bathroom:
        difference = now.timestamp() - person.date.timestamp()
        if person.date is not None and difference >= thirty_minutes_seconds:
            removed_user = reserve_bathroom.popLeft()
            # TO-DO: alert the removed user, their reservation has limit


# Constraints only 1 person can have 1 reservation at a time
@app.route('/reserve', methods=['POST'])
def reserve_bathroom():
    error = None
    if request.method == 'POST':
        user = request.form['user_id']
        response_url = request.form['response_url']
        response_token = request.form['token']
        if response_token == token:
            # first check, whether this user has a reservation
            userReservation = checkUserReservation(user)
            if userReservation:
                data = {'response_type': 'ephemeral',
                        'text': 'You\'ve already made a reservation!'}
                if response_url != '':
                    r = requests.post(response_url, json.dumps(data))
                    if r.status_code != requests.codes.ok:
                        data = {'Error': 'Status code: {r.status_code}'}
                        return jsonify(data)
                    else:
                        return "statuscode not okay"
                else:
                    return "response url empty"
            else:
                # new user reservation
                reserveBathroom.append(Person(user))
                data = {'text': 'You\'re reservation has been made!'}
                if response_url != '':
                    r = requests.post(response_url, json.dumps(data))
                    if r.status_code != requests.codes.ok:
                        data = {'Error': 'Status code: {r.status_code}'}
                        return jsonify(data)
                    else:
                        return "statuscode not okay"
                else:
                    return "response url empty"
            # data = {'Success': 'Status code 200'}
            return
        else:
            data = {'Error': 'Access denied!'}
            return jsonify(data)


@app.route('/update', methods=['POST'])
def bathroom_update():
    if request.method == 'POST':
        value = request.form['occupancy']
        if value != '':
            if value[0] == 'F':
                bathroomOccupied = False
            else:
                bathroomOccupied = True
            data = {'Succesfully updated!'}
            return jsonify(list(data))
        else:
            data = {'Error': 'Could not update'}
            return jsonify(data)


@app.route('/available', methods=['POST'])
def bathroom_availability():
    if request.method == 'POST':
        response_url = request.form['response_url']
        response_token = request.form['token']
        data = ''
        if not bathroomOccupied:
            data = {'response_type': 'ephemeral',
                    'text': 'Bathroom available!'}
        else:
            data = {'response_type': 'ephemeral',
                    'text': 'Bathroom not available!'}

        if response_url != '' and response_token == token:
            r = requests.post(response_url, json.dumps(data))
            if r.status_code != requests.codes.ok:
                data = {'Error': 'Status code: {r.status_code}'}
                return jsonify(data)
            else:
                return
        else:
            data = {'Error': 'Access denied'}
            return jsonify(data)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
