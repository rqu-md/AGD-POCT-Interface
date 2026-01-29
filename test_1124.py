from kivy.core.window import Window
from kivymd.app import MDApp
from test_dashboard import testScreenLive
from pretest import pretest
from userReport import userReport
from lockScreen import LockScreen
from userLoginScreen import UserLoginScreen

#this is the test for the testing in progress screen

class MyApp(MDApp):
    def build(self):
        #Window.clearcolor = (1, 1, 1, 1)   
        self.current_user = {
            "username": "Black Paint",
            "password": "999",
            "color": "green"
        }
        login_screen = UserLoginScreen()
        login_screen.set_user(self.current_user)
        return login_screen

if __name__ == "__main__":
    MyApp().run()
