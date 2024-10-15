from flask import Flask, request, Response, render_template, jsonify

app = Flask(__name__)

# simple http echo client (put name=<INSERT_VALUE_HERE>, do not include spaces in the value)
# to verify this, use cmd and type: 
# curl -d name=<INSERT_VALUE_HERE> http://127.0.0.1:5000/user/prompt
@app.route('/user/prompt', methods = ['POST'])
def processPrompt():
    if request.method == 'POST':
        response = request.form.to_dict()
        #response = {"message":request.get_data}
        #return response
        return jsonify({"message":response.get("name")})

app.run(port = 5000)