#!/usr/bin/env python3
"""
MotorControlScreen with LoadingBar Demo - Standalone Version
完全独立版本，包含LoadingBar类定义

新布局：
- Back/Home按钮（顶部左右）
- Project Name（顶部居中）
- LoadingBar进度条（正中间，自带Time Remaining）
- Abort Test按钮（进度条下方，红色）
- Temperature、Date/Time、Logo（底部）
"""

from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.label import MDLabel
from datetime import datetime
import random


# ============================================================================
# LoadingBar Class - Horizontal Progress Bar with Timer
# ============================================================================

class LoadingBar(RelativeLayout):
    """
    横向进度条组件 - 带倒计时功能
    
    特点：
    - 自动倒计时
    - 显示百分比（大字叠加）
    - 显示剩余时间（顶部）
    - 圆角设计
    """
    
    def __init__(self, total_time, **kwargs):
        super().__init__(**kwargs)

        self.total_time = total_time
        self.elapsed = 0

        # Fill full width of parent, then center the bar graphics inside
        self.size_hint_x = 1  # Take full width of parent
        self.size_hint_y = None  # Fixed height
        self.height = dp(140)   # increased for time label
        
        # Bar will be centered within this widget
        self.bar_max_width = dp(600)  # Maximum width for the bar itself

        #
        # --- TIME REMAINING LABEL ---
        #
        self.time_label = Label(
            text="Time Remaining: 00:00",
            font_size="20sp",
            color=(0, 0, 1, 1),
            size_hint=(1, None),
            height=dp(40),
            text_size=(self.width, dp(40)),
            halign="center",
            valign="middle",
        )

        #
        # --- PROGRESS BAR DRAWING ---
        #
        with self.canvas:
            Color(0.9, 0.9, 0.9, 1)
            self.bg_rect = RoundedRectangle(
                pos=(0, 0),
                size=(100, 100),
                radius=[dp(20)]
            )

            Color(0.1, 0.3, 0.7, 1)
            self.fg_rect = RoundedRectangle(
                pos=(0, 0),
                size=(0, 100),
                radius=[dp(20)]
            )

        #
        # --- PERCENT LABEL OVERLAY ---
        #
        self.percent_label = Label(
            text="0%",
            font_size='50sp',
            bold=True,
            color=(1, 1, 1, 1),
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(100)
        )
        super().add_widget(self.percent_label)
        
        # Add time label last so it appears on top
        super().add_widget(self.time_label)

        #
        # --- BIND RESIZING ---
        #
        self.bind(pos=self._update_graphics)
        self.bind(size=self._update_graphics)

        #
        # --- UPDATE TIMER ---
        #
        self._event = Clock.schedule_interval(self.update_progress, 1)

    def _update_graphics(self, *args):
        # position of bar (lower portion) - use relative coordinates
        bar_y = 0  # Bottom of widget
        bar_height = self.height - dp(40)   # subtract time label height
        
        # Calculate bar width (centered) and x position
        bar_width = min(self.bar_max_width, self.width * 0.9)  # Max width or 90% of widget width
        bar_x = (self.width - bar_width) / 2  # Center the bar horizontally

        # bg bar - canvas coordinates are relative to widget, centered
        self.bg_rect.pos = (bar_x, bar_y)
        self.bg_rect.size = (bar_width, bar_height)

        # fg fill - progress width based on bar width, not widget width
        progress_width = (self.elapsed / self.total_time) * bar_width
        self.fg_rect.pos = (bar_x, bar_y)
        self.fg_rect.size = (progress_width, bar_height)

        # Center the percentage label inside the bar - use relative coordinates
        self.percent_label.pos = (bar_x, bar_y)
        self.percent_label.size = (bar_width, bar_height)
        
        # Position time label at the top of the widget (above the bar) - use relative coordinates
        time_label_y = bar_height  # Position above the bar
        self.time_label.pos = (0, time_label_y)
        self.time_label.size = (self.width, dp(40))
        self.time_label.text_size = (self.width, dp(40))

    def update_progress(self, dt):
        #
        # update elapsed time - but don't go past total_time
        #
        if self.elapsed < self.total_time:
            self.elapsed += 1
        else:
            # Already at or past total_time, cancel the timer
            self._event.cancel()
        
        # Clamp elapsed to total_time to prevent going over
        self.elapsed = min(self.elapsed, self.total_time)
        progress_ratio = self.elapsed / self.total_time

        #
        # percent text - clamp to 100% maximum
        #
        percentage = min(int(progress_ratio * 100), 100)
        self.percent_label.text = f"{percentage}%"

        #
        # time remaining text (MM:SS)
        #
        remaining = max(0, self.total_time - self.elapsed)
        mm = remaining // 60
        ss = remaining % 60
        self.time_label.text = f"Time Remaining: {mm:02d}:{ss:02d}"

        #
        # redraw bar
        #
        self._update_graphics()


# ============================================================================
# MotorControlScreen Class - Main Test Interface
# ============================================================================

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


# ============================================================================
# Demo Application
# ============================================================================

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
        print("🎓 MotorControlScreen with LoadingBar Demo - Standalone Version")
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
        print("\n✅ This is a standalone version - no external dependencies!")
        print("="*70 + "\n")


if __name__ == "__main__":
    DemoApp().run()