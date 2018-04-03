from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import serial
import time

sero = serial.Serial(port='COM13', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)

# Globals - move to env variables?
endpoint = "a1uaa04qhg9yj1.iot.ap-southeast-1.amazonaws.com"
rootCAPath = "VeriSign.pem"
privateKey = "83656fe2b7-private.pem.key"
deviceCertificate = "83656fe2b7-certificate.pem.crt"

#rf_address = (b'\x2B\x12\x01\x3C\xC1\xF6\x01\x00\x00\x00\x04\x00\x01\x00\x2D\x01\x00\x00\x2E')

def main(event=None,context=None):
    # Init AWSIoTMQTTClient
    myMQTTClient = AWSIoTMQTTClient("myClientID1")
    myMQTTClient.configureEndpoint(endpoint, 8883)
    myMQTTClient.configureCredentials(rootCAPath, privateKey, deviceCertificate)

    #AWSIoTMQTTClient connection configuration
    #myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sc


    # Connect to AWS IoT
    myMQTTClient.connect()

    def callback(client, userdata, message):
        print ("Information received:")
        print (message.payload)
        print ("From topic:")
        print (message.topic)
        s=(message.payload).decode('UTF-8')
        datas = json.loads(s)

        Lamp = (datas["state"]["desired"]["Lamp"])
        Time1H = (datas["state"]["desired"]["Time1H"])
        Time1M = (datas["state"]["desired"]["Time1M"])
        Time2H = (datas["state"]["desired"]["Time2H"])
        Time2M = (datas["state"]["desired"]["Time2M"])
        Time3H = (datas["state"]["desired"]["Time3H"])
        Time3M = (datas["state"]["desired"]["Time3M"])
        Time4H = (datas["state"]["desired"]["Time4H"])
        Time4M = (datas["state"]["desired"]["Time4M"])
        Time5H = (datas["state"]["desired"]["Time5H"])
        Time5M = (datas["state"]["desired"]["Time5M"])
        Time1B = (datas["state"]["desired"]["Time1B"])
        Time2B = (datas["state"]["desired"]["Time2B"])
        Time3B = (datas["state"]["desired"]["Time3B"])
        Time4B = (datas["state"]["desired"]["Time4B"])
        Test1 = (datas["state"]["desired"]["Test1"])
        Test2 = (datas["state"]["desired"]["Test2"])

        packet = bytearray()
        packet.append(0x2B)
        packet.append(0x1E)
        packet.append(0x01)
        packet.append(0x3C)
        packet.append(0xC1)
        packet.append(0xF6)
        packet.append(0x04)
        packet.append(0x00)
        packet.append(0x00)
        packet.append(0x00)

        Lamps = int(str(hex(int(Lamp))), 16)
        Times1 = int(str(hex(int(Time1H))),16)
        Times2 = int(str(hex(int(Time1M))),16)
        Times3 = int(str(hex(int(Time2H))),16)
        Times4 = int(str(hex(int(Time2M))),16)
        Times5 = int(str(hex(int(Time3H))),16)
        Times6 = int(str(hex(int(Time3M))),16)
        Times7 = int(str(hex(int(Time4H))),16)
        Times8 = int(str(hex(int(Time4M))),16)
        Times9 = int(str(hex(int(Time5H))),16)
        Times10 = int(str(hex(int(Time5M))),16)
        Bright1 = int(str(hex(int(Time1B))),16)
        Bright2 = int(str(hex(int(Time2B))),16)
        Bright3 = int(str(hex(int(Time3B))),16)
        Bright4 = int(str(hex(int(Time4B))),16)
        Test1 = int(str(hex(int(Test1))),16)
        Test2 = int(str(hex(int(Test2))),16)

        #int(str(hex(int("70"))),16)
        packet.append(Lamps)
        packet.append(0x00)
        packet.append(0x01)
        packet.append(0x00)
        packet.append(0x46)
        packet.append(Times1)
        packet.append(Times2)
        packet.append(Times3)
        packet.append(Times4)
        packet.append(Times5)
        packet.append(Times6)
        packet.append(Times7)
        packet.append(Times8)
        packet.append(Times9)
        packet.append(Times10)
        packet.append(Bright1)
        packet.append(Bright2)
        packet.append(Bright3)
        packet.append(Bright4)
        packet.append(Test1)
        packet.append(Test2)

        print(packet)
        sero.write(packet)

    myMQTTClient.subscribe("$aws/things/demo/shadow/update", 1, callback)

    #myMQTTClient.disconnect()
    #myMQTTClient.unsubscribe("$aws/things/demo/shadow/update")
    while True:
        time.sleep(1)

main()