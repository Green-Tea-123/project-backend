from flask import Flask, request, Response, render_template, jsonify

app = Flask(__name__)

# simple http echo client (put name=<INSERT_VALUE_HERE>, do not include spaces in the value)
# to verify this, use cmd and type (for post request ONLY): 
# curl -d name=<INSERT_VALUE_HERE> http://127.0.0.1:5000/user/prompt
# to call http GET, use cmd and type the following:
# curl http://127.0.0.1:5000/user/<SPECIFIC_ROUTE>
@app.route('/user/bp', methods = ['GET'])
def getBloodPressure():
    bloodPressure = "120/80" # replace this with db retrieval
    return jsonify({"message" : bloodPressure})

@app.route('user/heart_rate')
def getHeartRate():
    heartRate = "63" # replace this with db retrieval
    return heartRate

@app.route('user/temp')
def getTemperature():
    temperature = "36.9" # replace this with db retrieval
    return temperature

@app.route('user/spo2')
def getSpo2():
    spo2 = "95" # replace this with db retrieval
    return 

@app.route('user/blood_glucose')
def getBloodGlucose():
    bloodGlucose = "6.4" # replace this with db retrieval
    return bloodGlucose

app.run(port = 5000)