from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from screen.BuzzerScreen import BuzzerScreen
from screen.MQ2Screen import MQ2Screen
from screen.ServoScreen import ServoScreen


class SmartGas(App):
    screenManager = ScreenManager()

    def build(self):
        self.screenManager.add_widget(
            MQ2Screen(
                name='MQ2'
            )
        )
        self.screenManager.add_widget(
            ServoScreen(
                name='Servo'
            )
        )
        self.screenManager.add_widget(
            BuzzerScreen(
                name='Buzzer'
            )
        )
        return self.screenManager


SmartGas().run()
