from _thread import start_new_thread

from kivy.clock import mainthread
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from comm.MQ2Listener import MQ2Listener


class MQ2Screen(Screen):
    gasValue = StringProperty('0')

    def __init__(self, **kw):
        super().__init__(**kw)
        mq2_listener = MQ2Listener(self)
        start_new_thread(mq2_listener.start, ())

    def go_to_servo(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'Servo'

    def go_to_buzzer(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'Buzzer'

    @mainthread
    def process_mq2_value(self, msg):
        self.gasValue = msg
