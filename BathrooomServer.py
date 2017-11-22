from flask import Flask
from flask import request
from collections import deque
from Models import Person
import datetime
import threading
app = Flask(__name__)

reserveBathroom = deque([])
bathroomOccupied = False
now = datetime.datetime.now()
thirty_minutes_seconds = 30 * 60 * 60

### Constraints only 1 person can have 1 reservation at a time
@app.route('/reserve', methods = [POST])
def reserve_bathroom():
    error = None
    if request.method == 'POST':
        data = request.form.keys()[0]
        user = data.user_id
        ## first check, whether this user has a reservation
        userReservation = checkUserReseravation(user)
        if userReservation:
            ## first check, whether this user has a reservation
        else:
            reserveBathroom.append(Person(user))
            ## respond back with their reservation time


@app.route('available', methods = [POST])
def bathroom_availability():
    if request.method == 'POST':
        data = request.form.keys()[0]
        bathroomOccupied = data.occupancy


# Check whether this user has made a reservation
@staticmethod
def checkUserReservation(user):
    for user_id in reserveBathroom:
        if user == user_id:
            return true
    return false


# check the users whose reservation have gone over limit
@staticmethod
def remove_reservation_waisters():
    threading.Timer(10.0, remove_reservation_waisters).start()
    for person in reserve_bathroom:
        if person.date is not None && now.timestamp() - person.date.timestamp() >= thirty_minutes_seconds:
            removed_user = reserve_bathroom.popLeft()
            # TO-DO: alert the removed user, their reservation has gone over limit
