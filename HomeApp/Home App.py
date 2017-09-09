from flask import Flask, render_template
from flask_ask import Ask, question, statement
import Sensor
import threading


app = Flask(__name__)
ask = Ask(app, "/")
mac_name_dict = {}
macs_at_home = []
sensor = Sensor.Sensor()

class SensorRunnerThread(threading.Thread):
    def run(self):
        sensor.run()
@app.route("/")
def homepage():
    """
    gives a homepage for the app. app is hosted over port 5000 since this is a Flask app. This can be used for testing to
    ensure the server is online
    :return: message text to be posted
    """
    return "homepage"


@ask.launch
def start_skill():
    return statement(whoHome())


@ask.intent("WhoHome")
def run_who_hone():
    return statement(whoHome())

@ask.intent("WhoLeft")
def run_who_left(firstName, lastName):
    return statement(whoLeft(firstName, lastName))

def whoHome():
    """
    finds all the macs_at_home translates them into names through the sensor and then give a string that can be spoken
    :return: string that can be spoken by alexa
    """
    global macs_at_home
    count = 0
    names = []
    macs_at_home = get_addresses()
    print macs_at_home
    for m in macs_at_home:
        n = sensor.map_mac(m)
        if n is not None:
            names.append(n)
            count += 1
    message = ""
    if count > 1:
        message = "there are " + str(count) + " people home."
        message += " These people are: "
    elif count == 1:
        message = "there is " + str(count) + " person home."
        message += " This person is: "
    else:
        message = "No one else is home"
    for n in names:
        message += ", " + n
    print "*" * 30
    print count
    print "*" * 30
    return message


def whoLeft(firstName, lastName):

    return "foo"


def get_addresses():
    """

    :return: updates macs at home to have only the macs in the house. returns this new list
    """
    global macs_at_home
    macs = sensor.get_mac_dict()
    macs_at_home = []
    for m in macs:
        if macs[m] is not None:
            macs_at_home.append(m)

    return macs_at_home


if __name__ == '__main__':
    sensor_thread = SensorRunnerThread()
    sensor_thread.setDaemon(True)
    sensor_thread.start()

    app.run(debug=True, use_reloader=False, threaded = True)