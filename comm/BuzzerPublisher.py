from paho.mqtt import publish

BUZZER_TOPIC = 'UdeA/SmartGas/Buzzer/smargas_esp32_001'
BUZZER_BROKER_URL = '192.168.204.206'
BUZZER_BROKER_PORT = 1883


def _is_off_message(message):
    if message != "OFF":
        # TODO se podra hacer un toast?
        print("SmartGas >> Invalid message. Expected: OFF")
        return False
    return True


class BuzzerPublisher:

    def send_buzzer_off_message(message):
        if _is_off_message(message):
            try:
                print(BUZZER_TOPIC, message, BUZZER_BROKER_PORT)
                publish.single(BUZZER_TOPIC, message, hostname=BUZZER_BROKER_URL, port=BUZZER_BROKER_PORT, qos=1)
            except Exception as ex:
                print('SmartGas >> Error sending the message. ex: {}'.format(ex))

