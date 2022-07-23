from flask import Flask, render_template, request,  url_for, redirect
app = Flask(__name__)
app.secret_key = "ssssh don't tell anyone"

brights = {
    "GallaryRng" : None,
    "front" : None,
    "back" : None,
    "stage" : None
}
c=20
print ("test"+str(c))
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get('action1') == 'VALUE1':
            print("yayaya")
        print("Moving Forward...")
        test = request.form.get('GallaryRnga')
        print (test)
    elif request.method == 'GET': 
        return render_template('index.html',c=c)
    return render_template('index.html',c=c)
@app.route('/slider_update', methods=['POST', 'GET'])
def slider():
    received_data = request.data
    print("test")
    print(received_data)
    return received_data

@app.route("/add-compliment", methods=["POST"])
def add_compliment():
    brights["GallaryRng"] = request.values.get('GallaryRng')
    print("value:  "+ brights["GallaryRng"])
    return redirect(url_for('home'))
#do something
# @app.route("/test", methods=["POST","GET"])
# def test():
#     AllRng = request.form["AllRng"]
#     print (AllRng)
#     return AllRng
