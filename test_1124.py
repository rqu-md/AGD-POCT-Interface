from kivy.core.window import Window
from kivymd.app import MDApp
from test_dashboard import testScreenLive
from pretest import pretest

#this is the test for the testing in progress screen

class MyApp(MDApp):
    def build(self):
        #Window.clearcolor = (1, 1, 1, 1)    
        return pretest()

if __name__ == "__main__":
    MyApp().run()
