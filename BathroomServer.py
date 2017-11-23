from flask import Flask, request, jsonify
from collections import deque
from Person import Person
import json
import os
import requests
import datetime
import threading
app = Flask(__name__)

reservations = []
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
    user = request.form['user_id']
    response_url = request.form['response_url']

    reservations.append(user)

    data = {'text': 'Your reservation has been made!'}

    r = requests.post(response_url, json.dumps(data))
    print(r.text)
    return
    # if request.method == 'POST':
    #     user = request.form['user_id']
    #     response_url = request.form['response_url']
    #     response_token = request.form['token']
    #     if response_token == token:
    #         # first check, whether this user has a reservation
    #         userReservation = checkUserReservation(user)
    #         if userReservation:
    #             data = {'response_type': 'ephemeral',
    #                     'text': 'You\'ve already made a reservation!'}
    #             if response_url != '':
    #                 r = requests.post(response_url, json.dumps(data))
    #                 if r.status_code != requests.codes.ok:
    #                     data = {'Error': 'Status code: {r.status_code}'}
    #                     return jsonify(data)
    #                 else:
    #                     return
    #             else:
    #                 return "response url empty"
    #         else:
    #             # new user reservation
    #             reserveBathroom.append(Person(user))
    #             data = {'text': 'Your reservation has been made!'}
    #             if response_url != '':
    #                 r = requests.post(response_url, json.dumps(data))
    #                 if r.status_code != requests.codes.ok:
    #                     data = {'Error': 'Status code: {r.status_code}'}
    #                     return jsonify(data)
    #                 else:
    #                     return
    #             else:
    #                 return "response url empty"
    #         # data = {'Success': 'Status code 200'}
    #         return
    #     else:
    #         data = {'Error': 'Access denied!'}
    #         return jsonify(data)


@app.route('/update', methods=['POST'])
def bathroom_update():
    value = request.get_json()['occupancy']
    data = ""
    if value == 'False':
        bathroomOccupied = False
    elif value == 'True':
        bathroomOccupied = True
        token = "xoxp-2170879045-242313655713-270485729315-d"\
                "4d1ade035d98920f721559ba543cb01"
        header = {'Content-Type': 'application/json'}
        create_im_request = requests.post("https://slack.com/api/im.open",
                                          data=json.dumps({"token": token,
                                                           "user": reservations[0],
                                                           "return_im": True}),
                                          header=header)
        return create_im_request.text
    else:
        data = 'Failiure :()'
    data = 'Succesfully updated!'
    return json.dumps(data)


@app.route('/available', methods=['POST'])
def bathroom_availability():
    if request.method == 'POST':
        response_url = request.form['response_url']
        response_token = request.form['token']
        data = {}
        if not bathroomOccupied:
            data = {'text': 'Bathroom available!'}
        else:
            data = {'text': 'Bathroom not available!'}

        if response_url != '' and response_token == token:
            r = requests.post(response_url, json.dumps(data))
            if r.status_code != requests.codes.ok:
                data = {'Error': 'Status code: {r.status_code}'}
                return jsonify(data)
            else:
                return
        else:
            return "response url empty"
    else:
        return


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
