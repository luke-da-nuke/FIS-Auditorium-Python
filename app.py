from flask import Flask, render_template, request,  url_for, redirect
app = Flask(__name__)                                               #creates the flask webapp
app.secret_key = "some highway in america or smth"                  #for secure transfer
brights = {                                                         #dictionary that stores brightness value of each light section from 0-255
    "AllRng" : None,                                                #all only needs to be used for remembering the value on the webpage, not for changing the lights as the other values are automatically updated by Ruben's js
    "GallaryRng" : None,
    "PublicFRng" : None,
    "PublicBRng" : None,
    "StageRng" : None
}
c=20
@app.route("/")                                                      #creates main page at ./ and names it home
def home():
    return render_template('index.html',v=brights)                   #renders index.html and parses the dictionary to be used in the {{}} things
@app.route("/slider_update", methods=["POST"])                       #API to update dictionary when sliders are changed
def slider_update():
    for x in brights:
        brights[x] = request.values.get(x)
        debugtxt = "the value of {} is {}"
        print(debugtxt.format(x,brights[x]))
    return redirect(url_for('home'))