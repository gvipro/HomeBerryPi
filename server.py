from flask import Flask #Fask to create web server
from flask import url_for #url for static files
from flask import jsonify #JSON format
from flask import render_template #Render home page

from sense_hat import SenseHat #Sense Hat Sensor

app = Flask(__name__) #Create server
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # Set caching off

SenseHat = SenseHat()#Create sense hat object
SenseHat.clear()#clear screen

#Request static files
with app.test_request_context():
    url_for('static', filename='app.js') #Link statick app.js
    url_for('static', filename='style.css') #Link statick CSS file
    
#Set up router for api request
@app.route('/api')

def api(): #Define api
    
    tC = SenseHat.get_temperature() #Call SenseHat method to get temperature
    tF = tC * (9/5) + 32 #Convert Temperature C to F
    pM = SenseHat.get_pressure() #Get pressure from Sense Hat
    pP = pM * 0.0145038 #Convert to 
    h = SenseHat.get_humidity()
    #Convert units to JSON format for get request
    return jsonify({ "temp": { "tC": tC, "tF": tF }, "pres": { "pP": pP, "pM": pM }, "hum": h })
    
#Set Router
@app.route('/')

#Defing Route
def home():
    #Render HTML file 
    return render_template('./home.html')