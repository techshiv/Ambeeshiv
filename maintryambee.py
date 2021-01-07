import paho.mqtt.client as mqtt
from flask import Flask, render_template, request
import time 
#import sqlite3
import json
from flask_socketio import SocketIO, emit
import pymongo
import datetime

global name
global val
global node1
global node2
global db
global sg
global jd
global client1
global found
found = 1

sg = None
jd = {}



client = pymongo.MongoClient("mongodb+srv://ambeedev:Ambee90526@ambee-db1-jwqfm.mongodb.net/ambee_gdata?retryWrites=true&w=majority")
db = client.ambee_gdata
col = db.devices
col2 = db.readings
#mydb = myclient["sensorvalue"]
#mycol = mydb["dht11"]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

calb = ""
'''
@socketio.on('json')
def handle_json(message):
    print('received message: ' +message)
'''
@socketio.on('myevent')
def handle_my_custom_event(json):
    #print(json["data"])
    #print('received json: ' + str(json["data"]))
    global sg
    sg = str(json["data"])
    global found
    found = 0
     

    


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client1, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client1.subscribe("outTopic")

# The callback for when a PUBLISH message is received from the ESP8266.
def on_message(client1, userdata, message):
   #socketio.emit('my variable')
   # print("Received message '" + str(message.payload) + "' on topic '"
   #     + message.topic + "' with QoS " + str(message.qos))
    
    try:
        
        data = (message.payload)
        data = data.decode('utf8')
       # print(message.payload) 
        data = json.loads(data)
        #print(sg)
        print("new data helooooooo")
        print(data)
       # print(data["MAC"])
       # print(y)   
        #print(data)
        #print(data["MAC"])
        jd["mac"] = data["MAC"]
        #jd["data"] = sg
        jsondata= json.dumps(jd)
        
        global found
        print(found)
           
        if found == 0:
            found
            print(sg)
            print("hellorrrfdsdsdfrfbrkhgfrjhgfhrjfjhrfjhrbfrb")
            client1.publish('devices',sg)
           # found =1
            found = 1 
        
        socketio.emit('mac', {'data': data["MAC"]})
        socketio.emit('time', {'data': data["Tim"]})
        socketio.emit('temp', {'data': data["Tem"]})
        socketio.emit('pressure', {'data': data["pres"]})
        socketio.emit('humudity', {'data': data["hum"]})
        socketio.emit('PM1', {'data': data["P1"]})
        socketio.emit('PM25', {'data': data["P25"]})
        socketio.emit('PM10', {'data': data["P10"]})
        socketio.emit('CO', {'data': data["co2"]})
        
            
        {
        "devID":data["MAC"],
        "createdAT": data["Tim"],
        "temperature": data["Tem"], 
        "humidity": data["hum"],
        "Pressure":data["pres"],
        "PM1":data["P1"],
        "PM25":data["P25"],
        "PM10":data["P10"],
        "CO":data["co2"]
        }
        mac = str(data["MAC"])
        col.update_one({"devId":mac},{"$set":{"devId":mac,
        "updatedAt":datetime.datetime.now(),
        "temperature": data["Tem"], 
        "humidity": data["hum"],
        "Pressure":data["pres"],
        "PM1":data["P1"],
        "PM25":data["P25"],
        "PM10":data["P10"],
        "CO2":data["co2"] }},upsert=True )
        print("im IEMI NUMBER")
        print(data["MAC"])
        
        col2.insert_one({"devId":mac,
        "createdAt":datetime.datetime.now(),
        "temperature": data["Tem"],
        "humidity": data["hum"],
        "Pressure":data["pres"],
        "PM1":data["P1"],
        "PM25":data["P25"],
        "PM10":data["P10"],
        "CO2":data["co2"] } )
        print("im IEMI NUMBER")
        print(data["MAC"])
    except:
        print("Invalid data format")
    '''##   global name
        global val
        global node1
        global node2
        name=str(key)
        val=str(value)
        #print(name)
        if name=='node1':
            node1=val
            socketio.emit('dht_temperature', {'data': val})
            mydict = { "temprature": node1, "humudity":  37 }
            x = mycol.insert_one(mydict)
           # print(node1)
                    
        if name=='node2':
            node2=val
            socketio.emit('dht_humidity', {'data': val})
   # con = sqlite3.connect('sensr.db')
    #cursorObj = con.cursor()
    #query = "INSERT INTO "+name+" (val)VALUES("+val+");"
    #print(query)
    #cursorObj.execute(query)
    #con.commit()
   
    
    
   # print(reading)
  '''  
'''
@socketio.on('myevent')
def handle_my_custom_event(json):
    #print(json["data"])
    #print('received json: ' + str(json["data"]))
    global sg
    sg = str(json["data"])
    client.publish('inTopic',"hiiii")   
 '''   
def dap():
   # client1.publish('inTopic',sg)
   # print(sg)
    sg = None
   
mqttc=mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.username_pw_set(username="ambee",password="sensordata")
mqttc.connect("localhost",1883,60)
mqttc.loop_start()

@app.route("/")
def main():
    global node1
    # Pass the template data into the template main.html and return it to the user
    return render_template('main.html')


if __name__ == "__main__":
   socketio.run(app, host='0.0.0.0', port=8181)
