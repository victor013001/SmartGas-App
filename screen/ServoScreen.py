from _thread import start_new_thread

from kivy.clock import mainthread
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from comm.ServoListener import ServoListener


class ServoScreen(Screen):
    servoStatus = StringProperty('OFF')

    def __init__(self, **kw):
        super().__init__(**kw)
        servo_listener = ServoListener(self)
        start_new_thread(servo_listener.start, ())

    @mainthread
    def process_servo_status(self, msg):
        if self.is_valid_servo_status_message(msg):
            self.servoStatus = msg

    def go_to_buzzer(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'Buzzer'

    def go_to_mq2(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'MQ2'

    @staticmethod
    def is_valid_servo_status_message(msg):
        return msg in ('ON', 'OFF')
