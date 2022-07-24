from flask import Flask, render_template, request,  url_for, redirect
app = Flask(__name__)                                                #creates the flask webapp

# import serial                                                       
# ser = serial.Serial('COM2', 9600, bytesize=serial.SEVENBITS ,parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, write_timeout=5)
# print(ser.name)

app.secret_key = "some highway in america or smth"                   #for secure transfer
debugtxt = "{}:  the value of {} is {}"                              #for formatting strings
brights = {                                                          #dictionary that stores brightness value of each light section from 0-255
    "AllRng" : None,                                                 #all only needs to be used for remembering the value on the webpage, not for changing the lights as the other values are automatically updated by Ruben's js
    "GallaryRng" : None,
    "PublicFRng" : None,
    "PublicBRng" : None,
    "StageRng" : None
}
@app.route("/")                                                      #creates main page at ./ and names it home
def home():
    return render_template('index.html',v=brights)                   #renders index.html and parses the dictionary to be used in the {{}} things
@app.route("/slider_update", methods=["POST"])                       #API to update dictionary when sliders are changed
def slider_update():
    for x in brights:
        brights[x] = request.values.get(x)
        print(debugtxt.format("Slider",x,brights[x]))
        # ser.write(b'test')
    return redirect(url_for('home'))

@app.route("/api/<string:keyIn>/<int:brightIn>/")                   #API to interface with Bitfocus (streamdeck thing)
def api(keyIn, brightIn):
    if (brightIn<=255) and (keyIn in brights.keys()):
        brights[keyIn]=brightIn
        print(debugtxt.format("StreamDeck",keyIn, brightIn))
        return keyIn + str(brightIn)
    else:
        print ("invalid")
        return keyIn + str(brightIn)
