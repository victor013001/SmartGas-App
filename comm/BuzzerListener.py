import paho.mqtt.client as mqttc

BUZZER_STATUS_TOPIC = 'UdeA/SmartGas/Buzzer/smargas_esp32_001/Status'
BUZZER_BROKER_URL = '192.168.204.206'
BUZZER_BROKER_PORT = 1883


class BuzzerListener:
    def __init__(self, observer):
        self.client = mqttc.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.observer = observer
        try:
            self.client.connect(BUZZER_BROKER_URL, BUZZER_BROKER_PORT, 60)
        except Exception as ex:
            print('SmartGas >> Failed broker connection. ex: {}'.format(ex))

    def on_connect(self, client, userdata, flags, rc):
        print('SmartGas >> Attempting MQTT connection to: ', BUZZER_STATUS_TOPIC)
        client.subscribe(topic=BUZZER_STATUS_TOPIC, qos=1)

    def on_message(self, client, userdata, msg):
        print('Message arrived: ', msg.payload.decode('utf-8'))
        self.observer.process_buzzer_status(msg.payload.decode('utf-8'))

    def start(self):
        print('SmartGas >> Looping')
        self.client.loop_forever()
