from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import serial
import time
import threading

# intitialize serial port
try:
    seri = serial.Serial(port='COM13', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)
except:
    print("Cannot open serial port")

# initialize an empty array for storing all rf data that is recievied
jarray = []

#function to post valid lamp data to iot
def mqttWorkingPost(item):
    data = {
        "state":{
            "reported":{
                "data":item
            }
        }
    }

    endpoint = "a1uaa04qhg9yj1.iot.ap-southeast-1.amazonaws.com"
    rootCAPath = "rootCA.pem"
    privateKey = "3353ec2073-private.pem.key"
    deviceCertificate = "3353ec2073-certificate.pem.crt"

    myMQTTClient = AWSIoTMQTTClient("myClientID")
    myMQTTClient.configureEndpoint(endpoint,8883)
    myMQTTClient.configureCredentials(rootCAPath, privateKey, deviceCertificate)

    myMQTTClient.configureOfflinePublishQueueing(-1)
    myMQTTClient.configureDrainingFrequency(2)
    myMQTTClient.configureConnectDisconnectTimeout(10)
    myMQTTClient.configureMQTTOperationTimeout(5)

    myMQTTClient.connect()

    myMQTTClient.publish("$aws/things/manipal_udpi_lamp_working/shadow/update", json.dumps(data),0)

    myMQTTClient.disconnect()

#loop function to run in thread
def loop():

    #run an infinite loop
    while True:

        #set start to zero
        start = 0

        #wait for 60 seconds before sending to IOT
        while(start!=60):
            time.sleep(1)
            start = start+1

        #if jarray is not empty send to mqtt otherwise do nothing
        if(len(jarray)!=0):
            print("Post to IOT")
            mqttWorkingPost(jarray)
        else:
            continue

#thread to run loop
threading.Thread(target=loop).start()

# function to check if an item already exists in an array
def inArr(item,ind):
    #create a substring so that only lamp number is recieved
    tofind = item[1:ind]

    #initialize count to zero
    count = 0

    #now check if the substring containing the lamp number is in the array or not
    for x in jarray:
        if tofind == x[1:ind]:
            break
        else:
            count = count + 1
            continue

    #if yes then return 0 else return 1
    if len(jarray) == count:
        return 0
    else:
        return 1


# in an infinite loop do the following
while True:

    try:
        # read 1000 bytes of data from serial port
        s = seri.read(1000)

        # convert the byte data into a string
        s = s.decode("utf-8", "ignore")

        # separate data after delimiter i.e. brk and store lamp data into s and also strip all the additional lines
        s = s.split("brk")[-1].strip()

        # if string is not null then do the following
        if (s != ""):
            print(s)

            # s[7] = lamp number
            index = 7

            # get lamp number
            item = s[index]

            # now until " is recieved keep concatenating the remaining values in the lamp number
            while s[index + 1] != '"':
                index = index + 1
                item = item + s[index]

            # after the whole number has been concatenated into item, create jindex by concatenating "Lampd" + lampnumber
            jindex = "Lampd" + item

            # now convert the recieved string into json so that querying is easy
            s = json.loads(s)

            # assign lamp number to parent variable for ease of search: so that we can type parent["temperature] instead of s[jindex]["Temperature"]
            parent = s[jindex]

            # assign values to variables
            temp = parent["Temperature"]
            count = parent["Count"]
            loop = parent["Loop"]
            timenow = parent["timenow"]
            ack = parent["Ack"]

            # format data into a desired pattern
            jarraydata = ""
            jarraydata = jarraydata + "{Lamp:" + item + ","
            jarraydata = jarraydata + "Temperature:" + str(temp) + ","
            jarraydata = jarraydata + "Count:" + str(count) + ","
            jarraydata = jarraydata + "Loop:" + str(loop) + ","
            jarraydata = jarraydata + "Timenow:" + str(timenow) + ","
            jarraydata = jarraydata + "Ack:" + str(ack)
            jarraydata = jarraydata + "}"

            # print(jarraydata)



            if inArr(jarraydata,index):
                # if value already exists in array then do not push into array, instead replace the old value
                for n,i in enumerate(jarray):
                    if i[1:index] == jarraydata[1:index]:
                        jarray[n] = jarraydata

                print(jarray)
            else:
                # this means that the value recieved is a new value. Push this into the array
                jarray.append(jarraydata)
                print(jarray)
    except:
        print("Cannot read serial data")
