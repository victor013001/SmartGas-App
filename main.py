from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from screen.SmartGasScreen import SmartGasScreen


class SmartGas(App):
    screenManager = ScreenManager()

    def build(self):
        self.screenManager.add_widget(
            SmartGasScreen(
                name='SmartGas'
            )
        )
        return self.screenManager


SmartGas().run()
