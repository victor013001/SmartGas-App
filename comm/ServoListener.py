import paho.mqtt.client as mqttc

SERVO_STATUS_TOPIC = 'UdeA/SmartGas/Servo/smargas_esp32_002/Status'
SERVO_BROKER_URL = '192.168.204.206'
SERVO_BROKER_PORT = 1883


class ServoListener:
    def __init__(self, observer):
        self.client = mqttc.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.observer = observer
        try:
            self.client.connect(SERVO_BROKER_URL, SERVO_BROKER_PORT, 60)
        except Exception as ex:
            print('SmartGas >> Failed broker connection. ex: {}'.format(ex))

    def on_connect(self, client, userdata, flags, rc):
        print('SmartGas >> Attempting MQTT connection to: ', SERVO_STATUS_TOPIC)
        client.subscribe(topic=SERVO_STATUS_TOPIC, qos=1)

    def on_message(self, client, userdata, msg):
        print('Message arrived: ', msg.payload.decode('utf-8'))
        self.observer.process_servo_status(msg.payload.decode('utf-8'))

    def start(self):
        print('SmartGas >> Looping')
        self.client.loop_forever()
