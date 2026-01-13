from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
#from mdWidgets import genButton


class LoadingBar(RelativeLayout):
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

        
        # Add time label after other widgets to ensure it's on top
        # Position will be set in _update_graphics

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
