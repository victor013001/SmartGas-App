from _thread import start_new_thread

from kivy.clock import mainthread
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from comm.BuzzerListener import BuzzerListener
from comm.BuzzerPublisher import BuzzerPublisher


class BuzzerScreen(Screen):
    buzzerStatus = StringProperty('OFF')

    def __init__(self, **kw):
        super().__init__(**kw)
        buzzer_listener = BuzzerListener(self)
        start_new_thread(buzzer_listener.start, ())

    def turn_off_buzzer(self):
        BuzzerPublisher.send_buzzer_off_message('OFF')

    def go_to_servo(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'Servo'

    def go_to_mq2(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'MQ2'

    @mainthread
    def process_buzzer_status(self, msg):
        if self.is_valid_buzzer_status_message(msg):
            self.buzzerStatus = msg

    @staticmethod
    def is_valid_buzzer_status_message(msg):
        return msg in ('ON', 'OFF')
