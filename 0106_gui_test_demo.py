#!/usr/bin/env python3
"""
MotorControlScreen with LoadingBar Demo
替换圆饼图为横向进度条

新布局：
- Back/Home按钮（顶部左右）
- Project Name（顶部居中）
- LoadingBar进度条（正中间，自带Time Remaining）
- Abort Test按钮（进度条下方，红色）
- Temperature、Date/Time、Logo（底部）
"""

from kivy.metrics import dp
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.label import MDLabel
from datetime import datetime
import random

# Import LoadingBar from consolidated widgets
from mdWidgets import LoadingBar


class MotorControlScreen(MDScreen):
    """
    Motor Control Screen - with LoadingBar
    
    Main Features:
    1. Horizontal progress bar (replaces pie chart)
    2. Single column layout
    3. Simplified interface
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Initialize variables
        self.project_name = ""
        self.stop_requested = False
        
        # Call build_ui() to construct the interface
        ui = self.build_ui()
        self.add_widget(ui)
    
    def build_ui(self):
        """
        Build user interface - Single column layout
        """
        
        # Set theme
        self.theme_cls = MDApp.get_running_app().theme_cls
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        
        # Create main screen
        screen = MDScreen(md_bg_color=(1, 1, 1, 1))
        
        # Main layout - single FloatLayout
        layout = MDFloatLayout()
        
        # ========== Top Navigation Buttons ==========
        
        # Back button (top left)
        back_button = MDButton(
            MDButtonIcon(icon="arrow-left"),
            MDButtonText(text="Back", font_style="Title"),
            style="elevated",
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            pos_hint={"x": 0.02, "top": 0.98},
            on_release=self.on_back_clicked
        )
        layout.add_widget(back_button)
        
        # Home button (top right)
        home_button = MDButton(
            MDButtonIcon(icon="home"),
            MDButtonText(text="Home", font_style="Title"),
            style="elevated",
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            pos_hint={"right": 0.98, "top": 0.98},
            on_release=self.on_home_clicked
        )
        layout.add_widget(home_button)
        
        # ========== Project Name (top center) ==========
        
        project_label = MDLabel(
            text="Project: Demo Project",
            font_style="Title",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.9}
        )
        layout.add_widget(project_label)
        
        # ========== LoadingBar Progress (center) ==========
        
        self.loading_bar = LoadingBar(
            total_time=300,  # 5 minutes = 300 seconds
            size_hint=(0.8, None),
            height=dp(140),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        layout.add_widget(self.loading_bar)
        
        # ========== Abort Test Button (below progress bar) ==========
        
        abort_button = MDButton(
            MDButtonText(text="Abort Test", font_style="Title"),
            style="filled",
            md_bg_color=(0.8, 0.1, 0.1, 1),  # Red color
            pos_hint={"center_x": 0.5, "center_y": 0.28},
            size_hint=(0.3, None),
            height=dp(56),
            on_press=self.on_stop_clicked
        )
        layout.add_widget(abort_button)
        
        # ========== Temperature Label (bottom left area) ==========
        
        self.temperature_label = MDLabel(
            text="Current Temperature: -- °C",
            halign="left",
            pos_hint={"x": 0.05, "center_y": 0.15}
        )
        layout.add_widget(self.temperature_label)
        
        # ========== Date/Time Label (bottom left) ==========
        
        self.date_time_label = MDLabel(
            text="YYYY-MM-DD HH:MM:SS",
            halign="left",
            size_hint=(None, None),
            size=(dp(200), dp(40)),
            pos_hint={"x": 0.05, "y": 0.02}
        )
        layout.add_widget(self.date_time_label)
        
        # ========== Logo (bottom right) ==========
        
        logo = MDLabel(
            text="NovelBeamUSA",
            halign="right",
            font_style="Title",
            size_hint=(None, None),
            size=(dp(150), dp(40)),
            pos_hint={"right": 0.95, "y": 0.02}
        )
        layout.add_widget(logo)
        
        # ========== Add layout to screen ==========
        
        screen.add_widget(layout)
        
        # ========== Start timers ==========
        
        # Update temperature every 0.5 seconds
        Clock.schedule_interval(self.update_actual_temperature, 0.5)
        
        # Update date/time every second
        Clock.schedule_interval(self.update_date_time, 1)
        
        return screen
    
    def update_actual_temperature(self, dt):
        """
        Update temperature display
        
        In real application, this would read from actual sensor
        Here we just simulate with random values
        """
        temp = 25 + random.random() * 10  # Simulate 25-35°C
        self.temperature_label.text = f"Current Temperature: {temp:.1f} °C"
    
    def update_date_time(self, dt):
        """Update date/time display"""
        now = datetime.now()
        self.date_time_label.text = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # ========== Button event handlers ==========
    
    def on_home_clicked(self, *args):
        """Home button clicked"""
        print("🏠 Home button clicked")
    
    def on_back_clicked(self, *args):
        """Back button clicked"""
        print("⬅️  Back button clicked")
    
    def on_stop_clicked(self, *args):
        """Abort Test button clicked"""
        print("⏹️  Abort Test button clicked")
        self.stop_requested = True


class DemoApp(MDApp):
    """Demo Application Main Class"""
    
    def build(self):
        """Build application"""
        # Create Screen Manager
        sm = MDScreenManager()
        
        # Add MotorControlScreen
        motor_screen = MotorControlScreen(name="motor")
        sm.add_widget(motor_screen)
        
        # Set initial screen
        sm.current = "motor"
        
        return sm
    
    def on_start(self):
        """Callback when application starts"""
        print("\n" + "="*70)
        print("🎓 MotorControlScreen with LoadingBar Demo")
        print("="*70)
        print("\n📚 New Features:")
        print("  1. Horizontal progress bar (replaces pie chart)")
        print("  2. Single column layout (simplified)")
        print("  3. LoadingBar with built-in Time Remaining display")
        print("  4. Red 'Abort Test' button")
        print("\n💡 Layout Structure:")
        print("  - Back/Home buttons (top corners)")
        print("  - Project Name (top center)")
        print("  - Progress bar (center)")
        print("  - Abort button (below progress)")
        print("  - Temperature/Date/Logo (bottom)")
        print("\n🔧 Usage:")
        print("  - LoadingBar automatically counts down from 300 seconds")
        print("  - Temperature updates every 0.5 seconds")
        print("  - Date/time updates every second")
        print("="*70 + "\n")


if __name__ == "__main__":
    DemoApp().run()