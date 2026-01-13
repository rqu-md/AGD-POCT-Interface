from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp


class WideLoadingBar(RelativeLayout):
    def __init__(self, total_time, **kwargs):
        super().__init__(**kwargs)

        self.total_time = total_time
        self.elapsed = 0

        self.size_hint = (0.9, None)
        self.height = dp(100)

        # Background bar + filled bar
        with self.canvas:
            Color(0.9, 0.9, 0.9, 1)  # light grey background
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(20)]
            )

            Color(0.1, 0.3, 0.7, 1)  # dark blue progress bar
            self.fg_rect = RoundedRectangle(
                pos=self.pos,
                size=(0, self.height),
                radius=[dp(20)]
            )

        # Label on top
        self.percent_label = Label(
            text="0%",
            font_size='50sp',
            bold=True,
            color=(1, 1, 1, 1),
            halign="center",
            valign="middle"
        )
        self.add_widget(self.percent_label)

        # Track changes so rects move/resize when layout updates
        self.bind(pos=self._update_graphics)
        self.bind(size=self._update_graphics)

        # schedule updates (timer)
        self._event = Clock.schedule_interval(self.update_progress, 1)

    def _update_graphics(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        progress_width = (self.elapsed / self.total_time) * self.width
        self.fg_rect.pos = self.pos
        self.fg_rect.size = (progress_width, self.height)

        self.percent_label.center = self.center

    def update_progress(self, dt):
        if self.elapsed >= self.total_time:
            self._event.cancel()
            return

        self.elapsed += 1
        percentage = int((self.elapsed / self.total_time) * 100)
        self.percent_label.text = f"{percentage}%"
        self._update_graphics()


""" class TestApp(App):
    def build(self):
        layout = BoxLayout(padding=dp(20), orientation='vertical')
        layout.add_widget(WideLoadingBar(total_time=30))
        return layout


if __name__ == "__main__":
    TestApp().run()
 """