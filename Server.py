from flask import Flask
from flask import jsonify
from flask import render_template
from flask import url_for
from sense_hat import SenseHat

app = Flask(__name__) #Create server
sense = SenseHat()#Create sense hat object
sense.clear()#clear screen

with app.test_request_context():
    url_for('static', filename='app.js')#Link statick app.js
    

@app.route('/api')

def api():
    tempC = sense.get_temperature()
    tempF = tempC * (9/5) + 32
    pressure = sense.get_pressure()
    hum = sense.get_humidity()
    pre = sense.get_pressure()
    pPsi = pressure * 0.0145038
    
   
    return jsonify({ "temperature": { "C": tempC, "F": tempF }, "pressure": { "pPsi": pPsi, "pMb": pressure },
                     "humidity": humidity })
#Set Router
@app.route('/')

#Defing Route
def home():
    #Render HTML file 
    return render_template('./home.html')
