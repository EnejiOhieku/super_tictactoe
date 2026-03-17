
import os
from os import mkdir
from os.path import join, exists
import random
import webbrowser

from kivy.clock import Clock
from kivy.utils import platform
from kivy.config import Config

Config.set("graphics", "width", 350)
Config.set("graphics", "height", 700)
if platform not in ["android", "ios"]:
    Config.set("input", "mouse", "mouse, disable_multitouch")


from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import SlideTransition
from kivy.properties import StringProperty, BooleanProperty
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from board.boardwidget import BoardWidget





class RootWidget(MDBoxLayout):
    
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)




class SuperTicTacToeApp(MDApp):
    def __init__(self, **kwargs):
        super(SuperTicTacToeApp, self).__init__(**kwargs)
        
        Window.bind(on_keyboard=self.back_click)


    def back_click(self, window, key, *largs):
        if key == 27:
            pass

    def load_kv_files(self, *args):
        Builder.load_file("main.kv")

    def build(self):
        self.title = "Super TicTacToe"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        self.load_kv_files()

        return RootWidget()

    def switch_theme(self):
        self.theme_cls.theme_style = "Dark" if (self.theme_cls.theme_style == "Light") else "Light"
        
    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def get_file(self, name):
        return os.path.join(os.getcwd(), name)
    


if __name__ == "__main__":
    SuperTicTacToeApp().run()

