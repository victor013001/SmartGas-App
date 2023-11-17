import paho.mqtt.client as mqttc

MQ2_STATUS_TOPIC = 'UdeA/SmartGas/MQ2/smargas_esp32_001'
MQ2_BROKER_URL = '192.168.204.206'
MQ2_BROKER_PORT = 1883


class MQ2Listener:
    def __init__(self, observer):
        self.client = mqttc.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.observer = observer
        try:
            self.client.connect(MQ2_BROKER_URL, MQ2_BROKER_PORT, 60)
        except Exception as ex:
            print('SmartGas >> Failed broker connection. ex: {}'.format(ex))

    def on_connect(self, client, userdata, flags, rc):
        print('SmartGas >> Attempting MQTT connection to: ', MQ2_STATUS_TOPIC)
        client.subscribe(MQ2_STATUS_TOPIC)

    def on_message(self, client, userdata, msg):
        print('Message arrived: ', msg.payload.decode('utf-8'))
        self.observer.process_mq2_value(msg.payload.decode('utf-8'))

    def start(self):
        print('SmartGas >> Looping')
        self.client.loop_forever()
