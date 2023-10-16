import json
import pathlib
from threading import Timer
from google_auth_oauthlib.flow import Flow
from flask import Flask, abort, render_template, request,  url_for, redirect, session, send_file
from authlib.integrations.flask_client import OAuth
import os 
import requests
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
import requests
import socket

PJ_IP = '10.96.0.11'
PJ_PORT = 3629
PJ_state=False
PJ_mute=False
PJ_freeze=False


def update_data(interval):
    arduino.open()
    Timer(interval, update_data, [interval]).start()
    global DATA
    print(arduino.readline())

# update data every second
update_data(2)

app = Flask(__name__)                                                #creates the flask webapp
oauth = OAuth(app)

app.secret_key = "some highway in america or smth"                   #for secure transfer

GOOGLE_CLIENT_ID = "416292616621-e22ail8cbl0d3noh8luc8fmgj02nhr1e.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://10.97.11.200.nip.io/callback"
)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" in session:
            if session['email'] in emails.keys():
                if emails[session['email']]=="admin" or emails[session['email']]=="user":
                    return function()
                else:
                    return "email not on whitelist"
            else:
                return "email not in dict"
        else:
            return redirect("/login")

    return wrapper

def admin_is_required(function):
    def wrappers(*args, **kwargs):
        if "google_id" in session:
            if session['email'] in emails.keys():
                if emails[session['email']]=="admin" or emails[session['email']]=="user":
                    if emails[session['email']]=="admin":
                        return function()
                    else:
                        return "not admin"
                else:
                    return "email not on whitelist1"
            else:
                return "email not in dict1"
        else:
            return redirect("/login")

    return wrappers

debugtxt = "{}:  the value of {} is {}"                              #for formatting strings
brights = {                                                          #dictionary that stores brightness value of each light section from 0-255
    "AllRng" : None,                                                 #all only needs to be used for remembering the value on the webpage, not for changing the lights as the other values are automatically updated by Ruben's js
    "GallaryRng" : None,
    "PublicFRng" : None,
    "PublicBRng" : None,
    "StageRng" : None
}

bitfocusMatrixButtons = [
    [2,3,4,5],
    [10,11,12,13],
    [18,19,20,21],
    [26,27,28,29]
]

bitfocusMatrixPage=10

emails = {
    "luke_plastow@fis.edu" : "admin",
    "randomPerson@fis.edu" : None,
    "luke.caspian.plastow@gmail.com" : "user",
    "julius_ulbrich@fis.edu":"user",
    "ruben_mihm@fis.edu" : "admin",
    "sebastian_bruch@fis.edu" : "admin",
    "fistvmedia@fis.edu":"user",
    "pete_sinclair@fis.edu":"user",
    "alex_westcott@fis.edu":"user",
    "fistvmedia@gmail.com":"user"
}
input="I1"
output="O1"

import serial     
arduino = serial.Serial(port='COM7', baudrate=9600, timeout=.1)

# lights = serial.Serial('/dev/ttyACM0', 9600, bytesize=serial.EIGHTBITS ,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, write_timeout=5)
# print(ser.name)

@app.route("/")                                                      #creates main page at ./ and names it home
@login_is_required
def home():
    # email=dict(session).get('email',None)
    # print (email)
    # print(json.dumps(session, indent = 4))                           #prints current user info
    return render_template('index.html',v=brights)                   #renders index.html and parses the dictionary to be used in the {{}} things

@app.route("/admin") 
@admin_is_required                                                     #creates main page at ./ and names it home
def adminpage():
    return render_template('admin.html')                   #renders admin.html

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID,
        clock_skew_in_seconds=1

    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# @app.route("/protected_area")
# @login_is_required
# def protected_area():
#     return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"

@app.route("/slider_update", methods=["POST"])                       #API to update dictionary when sliders are changed
def slider_update():
    for x in brights:
        brights[x] = request.values.get(x)
        print(debugtxt.format("Slider",x,brights[x]))
        # ser.write(b'test')
    return redirect("/")

@app.route("/io", methods=['POST'])
def io():
    global input, output
    for i in range (1,10):
        if request.form.get("i")==str(i):
            input=i
            print(input)
        elif request.form.get("o")==str(i):
            output=i
            # print("CI"+input+"O"+output+"T")
            # ser.write(("C"+input+output+"T").encode())
            print("/"+str(bitfocusMatrixPage)+"/"+str(bitfocusMatrixButtons[input-1][output-1]))
            requests.get('http://127.0.0.1:8888/press/bank'+"/"+str(bitfocusMatrixPage)+"/"+str(bitfocusMatrixButtons[input-1][output-1]))
    return redirect("/")

@app.route("/pj", methods=['POST'])
def pj():
    global PJ_state, PJ_mute, PJ_freeze
    a = str(request.form.get("pj"))
    if a=="Screen":
        arduino.open()
        arduino.write(bytes("begin",'utf-8'))
        time.sleep(2)
        arduino.write(bytes("S",'utf-8'))
        arduino.close()
        print("hi")
    else:
        pjs=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pjs.connect((PJ_IP, PJ_PORT))
        if a=="PWRToggle":
            pjs.send(bytes.fromhex('45 53 43 2F 56 50 2E 6E 65 74 10 03 00 00 00 00'))
            if PJ_state==True:
                PJ_state=False
                pjs.send(bytes.fromhex("PWR OFF".encode('utf-8').hex()+" 0d"))
            else:
                PJ_state=True
                pjs.send(bytes.fromhex("PWR ON".encode('utf-8').hex()+" 0d"))
        elif a=="AVToggle":
            pjs.send(bytes.fromhex('45 53 43 2F 56 50 2E 6E 65 74 10 03 00 00 00 00'))
            if PJ_mute==True:
                PJ_mute=False
                pjs.send(bytes.fromhex("MUTE OFF".encode('utf-8').hex()+" 0d"))
            else:
                PJ_mute=True
                pjs.send(bytes.fromhex("MUTE ON".encode('utf-8').hex()+" 0d"))

        elif a=="FreezeToggle":
            pjs.send(bytes.fromhex('45 53 43 2F 56 50 2E 6E 65 74 10 03 00 00 00 00'))
            if PJ_freeze==True:
                PJ_freeze=False
                pjs.send(bytes.fromhex("FREEZE OFF".encode('utf-8').hex()+" 0d"))
            else:
                PJ_freeze=True
                pjs.send(bytes.fromhex("FREEZE ON".encode('utf-8').hex()+" 0d"))

            # pjs.send(bytes.fromhex("PWR?".encode('utf-8').hex()+" 0d"))
            # status=pjs.recv(18)
            # # print(status)
            # if status=="01" or status=="02":
            #     pjs.send(bytes.fromhex("PWR OFF".encode('utf-8').hex()+" 0d"))
            # else:
            #     pjs.send(bytes.fromhex("PWR ON".encode('utf-8').hex()+" 0d"))
        else:
            pjs.send(bytes.fromhex('45 53 43 2F 56 50 2E 6E 65 74 10 03 00 00 00 00'))
            pjs.send(bytes.fromhex(a.encode('utf-8').hex()+" 0d"))
        pjs.shutdown(1)
        pjs.close()
    return redirect("/")

@app.route("/api/<string:keyIn>/<int:brightIn>/")                   #API to interface with Bitfocus (streamdeck thing)
def api(keyIn, brightIn):
    if (brightIn<=255) and (keyIn in brights.keys()):
        brights[keyIn]=brightIn
        print(debugtxt.format("StreamDeck",keyIn, brightIn))
        return keyIn + str(brightIn)
    else:
        print ("invalid")
        return "invalid:   " + keyIn + str(brightIn)
    
@app.route("/api/status/<string:command>/")
def status(command):
    global PJ_state, PJ_mute, PJ_freeze
    pjs=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pjs.connect((PJ_IP, PJ_PORT))
    pjs.send(bytes.fromhex('45 53 43 2F 56 50 2E 6E 65 74 10 03 00 00 00 00'))
    pjs.send(bytes.fromhex((command+"?").encode('utf-8').hex()+" 0d"))
    pjs.recv(1024)
    status=pjs.recv(6)
    if command=="PWR":
        if bytes(status)==bytes("PWR=01",'utf-8') or bytes(status)==bytes("PWR=02",'utf-8'):
            PJ_state=True
            return send_file("On.png", mimetype='image/gif')
        else:
            PJ_state=False
            return send_file("Off.png", mimetype='image/gif')
            # return status

    print(status)
    pjs.shutdown(1)
    pjs.close()

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
