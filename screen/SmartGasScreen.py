from _thread import start_new_thread

from kivy.clock import mainthread
from kivy.properties import StringProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.uix.screenmanager import Screen
from comm.MQ2Listener import MQ2Listener
from comm.ServoListener import ServoListener
from comm.BuzzerListener import BuzzerListener
from comm.BuzzerPublisher import BuzzerPublisher


class SmartGasScreen(Screen):
    gasValue = StringProperty('0')

    goodGasValue = 500
    warningGasValue = 1500

    isBuzzerDisabled = BooleanProperty(True)

    gasValueBackgroundColor = ListProperty([0, 0.7, 0, 1])

    imageServoStatus = StringProperty('images/ventilationOff.png')
    imageBuzzerStatus = StringProperty('images/alarmOff.png')

    def __init__(self, **kw):
        super().__init__(**kw)
        mq2_listener = MQ2Listener(self)
        start_new_thread(mq2_listener.start, ())
        servo_listener = ServoListener(self)
        start_new_thread(servo_listener.start, ())
        buzzer_listener = BuzzerListener(self)
        start_new_thread(buzzer_listener.start, ())

    def turn_off_buzzer(self):
        BuzzerPublisher.send_buzzer_off_message('OFF')

    @mainthread
    def process_mq2_value(self, msg):
        self.gasValue = msg
        intGasValue = int(self.gasValue)
        if intGasValue < self.goodGasValue:
            self.gasValueBackgroundColor = [0, 0.7, 0, 1]
        elif intGasValue < self.warningGasValue:
            self.gasValueBackgroundColor = [1, 0.8, 0, 1]
        else:
            self.gasValueBackgroundColor = [0.7, 0, 0, 1]

    @mainthread
    def process_servo_status(self, msg):
        if self.is_valid_status_message(msg):
            if msg == 'ON':
                self.imageServoStatus = 'images/ventilationOn.png'
            else:
                self.imageServoStatus = 'images/ventilationOff.png'

    @mainthread
    def process_buzzer_status(self, msg):
        if self.is_valid_status_message(msg):
            if msg == 'ON':
                self.imageBuzzerStatus = 'images/alarmOn.png'
                self.isBuzzerDisabled = False
            else:
                self.imageBuzzerStatus = 'images/alarmOff.png'
                self.isBuzzerDisabled = True

    @staticmethod
    def is_valid_status_message(msg):
        return msg in ('ON', 'OFF')
