from datetime import datetime

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import (
    BoxShadow,
    Color,
    Ellipse,
    Line,
    RoundedRectangle,
    StencilPop,
    StencilPush,
    StencilUse,
)
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel


# ---------------------------------------------------------------------------
# Dialog helpers
# ---------------------------------------------------------------------------
def confirmOverlay(confirm_callback, **kwargs):
    """
    Create and return a confirmation dialog.
    In KivyMD 2.0, MDDialog doesn't accept title/text/type/buttons in __init__.
    We'll build the dialog content manually.
    """
    dialog_kwargs = {
        k: v
        for k, v in kwargs.items()
        if k
        not in [
            "title",
            "text",
            "type",
            "buttons",
            "completion_title",
            "completion_text",
            "completion_callback",
        ]
    }
    dialog = MDDialog(**dialog_kwargs)

    dialog.size_hint = (0.8, None)
    dialog.size_hint_max_x = dp(400)
    dialog.pos_hint = {"center_x": 0.5, "center_y": 0.5}

    if hasattr(dialog, "padding"):
        dialog.padding = [0, 0, 0, 0]
    if hasattr(dialog, "spacing"):
        dialog.spacing = 0

    completion_kwargs = {
        "confirm_callback": kwargs.get("completion_callback"),
        "title": kwargs.get("completion_title", "Experiment Aborted"),
        "text": kwargs.get(
            "completion_text", "Please remove and discard the test sample."
        ),
    }

    cancel_btn = MDButton(style="elevated", on_release=lambda *_: dialog.dismiss())
    cancel_btn.add_widget(MDButtonText(text="No", font_style="Title"))

    ok_btn = MDButton(
        style="elevated",
        on_release=lambda *_: _on_confirm(dialog, confirm_callback, completion_kwargs),
        theme_bg_color="Custom",
        md_bg_color=(0.8, 0.2, 0.2, 1),
    )
    ok_btn.elevation = 4
    ok_btn.add_widget(
        MDButtonText(
            theme_text_color="Custom",
            font_style="Title",
            text_color=(1, 1, 1, 1),
            text="Abort Test",
        )
    )

    padding_val = dp(24)
    content = MDBoxLayout(
        orientation="vertical",
        spacing="12dp",
        padding=[padding_val, padding_val, padding_val, padding_val],
        adaptive_height=True,
        size_hint=(1, None),
        pos_hint={"x": 0, "y": 0},
    )

    title_label = MDLabel(
        text=kwargs.get("title", "Confirm Action"),
        theme_text_color="Primary",
        font_size="20sp",
        bold=True,
        adaptive_height=True,
        halign="center",
        valign="middle",
        size_hint_x=1,
        text_size=(None, None),
    )

    def set_title_text_size(instance, value):
        if value > 0:
            title_label.text_size = (value, None)

    def update_title_size():
        if title_label.width > 0:
            title_label.text_size = (title_label.width, None)

    title_label.bind(width=set_title_text_size)
    content.add_widget(title_label)

    text_label = MDLabel(
        text=kwargs.get("text", "Are you sure you want to stop the test?"),
        theme_text_color="Secondary",
        font_size="16sp",
        adaptive_height=True,
        halign="center",
        valign="middle",
        size_hint_x=1,
        text_size=(None, None),
    )

    def set_text_text_size(instance, value):
        if value > 0:
            text_label.text_size = (value, None)

    def update_text_size():
        if text_label.width > 0:
            text_label.text_size = (text_label.width, None)

    text_label.bind(width=set_text_text_size)
    content.add_widget(text_label)

    button_container = MDBoxLayout(
        orientation="horizontal",
        spacing="12dp",
        adaptive_height=True,
        size_hint_x=1,
        padding=[0, dp(8), 0, 0],
    )
    spacer = Widget(size_hint_x=1)
    button_container.add_widget(spacer)
    button_container.add_widget(cancel_btn)
    button_container.add_widget(ok_btn)
    spacer2 = Widget(size_hint_x=1)
    button_container.add_widget(spacer2)
    content.add_widget(button_container)

    if hasattr(dialog, "ids") and "content_container" in dialog.ids:
        dialog.ids.content_container.add_widget(content)
    else:
        dialog.add_widget(content)

    def update_dialog_height(*args):
        if content.height > 0:
            dialog.height = content.height

    content.bind(height=update_dialog_height)

    def ensure_centered(dt):
        if dialog.parent:
            dialog.pos_hint = {"center_x": 0.5, "center_y": 0.5}
            if dialog.width > 0 and dialog.height > 0:
                dialog.center = (Window.width / 2, Window.height / 2)
            update_title_size()
            update_text_size()

    Clock.schedule_once(ensure_centered, 0.05)
    Clock.schedule_once(ensure_centered, 0.15)
    Clock.schedule_once(ensure_centered, 0.3)

    return dialog


def actionCompletedOverlay(
    confirm_callback=None, title="Action Completed", text="Your action has been completed.", **kwargs
):
    """
    Lightweight overlay shown after the user confirms an action.
    Keeps the same sizing/centering approach as confirmOverlay.
    """
    dialog_kwargs = {k: v for k, v in kwargs.items() if k not in ["title", "text", "type", "buttons"]}
    dialog = MDDialog(**dialog_kwargs)

    dialog.size_hint = (0.8, None)
    dialog.size_hint_max_x = dp(400)
    dialog.pos_hint = {"center_x": 0.5, "center_y": 0.5}

    if hasattr(dialog, "padding"):
        dialog.padding = [0, 0, 0, 0]
    if hasattr(dialog, "spacing"):
        dialog.spacing = 0

    padding_val = dp(24)
    content = MDBoxLayout(
        orientation="vertical",
        spacing="12dp",
        padding=[padding_val, padding_val, padding_val, padding_val],
        adaptive_height=True,
        size_hint=(1, None),
        pos_hint={"x": 0, "y": 0},
    )

    title_label = MDLabel(
        text=title,
        theme_text_color="Primary",
        font_size="20sp",
        bold=True,
        adaptive_height=True,
        halign="center",
        valign="middle",
        size_hint_x=1,
        text_size=(None, None),
    )

    def set_title_text_size(instance, value):
        if value > 0:
            title_label.text_size = (value, None)

    title_label.bind(width=set_title_text_size)
    content.add_widget(title_label)

    text_label = MDLabel(
        text=text,
        theme_text_color="Secondary",
        font_size="16sp",
        adaptive_height=True,
        halign="center",
        valign="middle",
        size_hint_x=1,
        text_size=(None, None),
    )

    def set_text_text_size(instance, value):
        if value > 0:
            text_label.text_size = (value, None)

    text_label.bind(width=set_text_text_size)
    content.add_widget(text_label)

    ok_btn = MDButton(
        style="elevated",
        on_release=lambda *_: _on_completed(dialog, confirm_callback),
    )
    ok_btn.add_widget(MDButtonText(text="OK", font_style="Title"))

    button_container = MDBoxLayout(
        orientation="horizontal",
        spacing="12dp",
        adaptive_height=True,
        size_hint_x=1,
        padding=[0, dp(8), 0, 0],
    )
    button_container.add_widget(Widget(size_hint_x=1))
    button_container.add_widget(ok_btn)
    button_container.add_widget(Widget(size_hint_x=1))
    content.add_widget(button_container)

    if hasattr(dialog, "ids") and "content_container" in dialog.ids:
        dialog.ids.content_container.add_widget(content)
    else:
        dialog.add_widget(content)

    def update_dialog_height(*args):
        if content.height > 0:
            dialog.height = content.height

    content.bind(height=update_dialog_height)

    def ensure_centered(dt):
        if dialog.parent:
            dialog.pos_hint = {"center_x": 0.5, "center_y": 0.5}
            if dialog.width > 0 and dialog.height > 0:
                dialog.center = (Window.width / 2, Window.height / 2)
            title_label.text_size = (title_label.width, None)
            text_label.text_size = (text_label.width, None)

    Clock.schedule_once(ensure_centered, 0.05)
    Clock.schedule_once(ensure_centered, 0.15)

    return dialog


def _on_completed(dialog, callback):
    dialog.dismiss()
    if callback:
        callback()


def _on_confirm(dialog, callback, completion_kwargs=None):
    dialog.dismiss()

    def open_completion_overlay(dt):
        completion_dialog = actionCompletedOverlay(**(completion_kwargs or {}))
        completion_dialog.open()

    try:
        if callback:
            callback()
    finally:
        Clock.schedule_once(open_completion_overlay, 0.05)


# ---------------------------------------------------------------------------
# Widgets
# ---------------------------------------------------------------------------
class StatusHeader(BoxLayout):
    def __init__(self, title="Header", **kwargs):
        super().__init__(orientation="horizontal", padding=10, **kwargs)
        self.add_widget(Label(text=title))


class uni_backButton(ButtonBehavior, Widget):
    bg_color = (0.1, 0.4, 0.8, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ripple_alpha = 0
        self.ripple_pos = (0, 0)
        self.ripple_radius = 0

        self.icon = Image(
            source="assets/backArrow.png",
            allow_stretch=True,
            keep_ratio=True,
            size=(dp(36), dp(36)),
        )
        self.add_widget(self.icon)

        self.ripple_color = (1, 1, 1, self.ripple_alpha)

        with self.canvas.before:
            Color(*self.bg_color)
            self.bg = RoundedRectangle(radius=[(dp(0), dp(0)), (16, 16), (0, 0), (0, 0)])

        with self.canvas:
            StencilPush()
            self.stencil_shape = RoundedRectangle(radius=[(dp(0), dp(0)), (16, 16), (0, 0), (0, 0)])
            StencilUse()

            self.ripple_color_instruction = Color(*self.ripple_color)

            self.ripple = Ellipse(size=(0, 0))

            StencilPop()

        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

        self.stencil_shape.pos = self.pos
        self.stencil_shape.size = self.size

        self.icon.pos = (
            self.x + self.width / 2 - self.icon.width / 2,
            self.y + self.height / 2 - self.icon.height / 2,
        )

        self.ripple_color_instruction.rgba = (1, 1, 1, self.ripple_alpha)

        r = self.ripple_radius
        self.ripple.size = (r * 2, r * 2)
        self.ripple.pos = (self.x + self.ripple_pos[0] - r, self.y + self.ripple_pos[1] - r)

    def reset_ripple(self, *args):
        self.ripple_radius = 0
        self.ripple_alpha = 0
        self.update_graphics()

    def on_press(self):
        touch = self.last_touch
        self.ripple_pos = (touch.x - self.x, touch.y - self.y)
        self.ripple_radius = 0
        self.ripple_alpha = 0.4
        self.on_back_clicked()

        max_r = max(self.width, self.height) * 1.2

        expand = Animation(ripple_radius=max_r, d=0.23, t="out_quad")
        fade = Animation(ripple_alpha=0, d=0.18, t="out_quad")

        anim = expand + fade
        anim.bind(on_progress=lambda *a: self.update_graphics())
        anim.bind(on_complete=self.reset_ripple)
        anim.start(self)

    def on_back_clicked(self, *args):
        print("⬅️  Back button clicked")


class uni_homeButton(ButtonBehavior, Widget):
    bg_color = (1, 1, 1, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ripple_alpha = 0
        self.ripple_pos = (0, 0)
        self.ripple_radius = 0

        self.icon = Image(
            source="assets/home.png",
            allow_stretch=True,
            keep_ratio=True,
            size=(dp(36), dp(36)),
        )
        self.add_widget(self.icon)

        self.ripple_color = (0.75, 0.75, 0.75, self.ripple_alpha)

        with self.canvas.before:
            Color(*self.bg_color)
            self.bg = RoundedRectangle(radius=[(dp(0), dp(0)), (16, 16), (0, 0), (0, 0)])

        with self.canvas:
            StencilPush()
            self.stencil_shape = RoundedRectangle(radius=[(dp(0), dp(0)), (16, 16), (0, 0), (0, 0)])
            StencilUse()

            self.ripple_color_instruction = Color(*self.ripple_color)

            self.ripple = Ellipse(size=(0, 0))

            StencilPop()

        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

        self.stencil_shape.pos = self.pos
        self.stencil_shape.size = self.size

        self.icon.pos = (
            self.x + self.width / 2 - self.icon.width / 2,
            self.y + self.height / 2 - self.icon.height / 2,
        )

        self.ripple_color_instruction.rgba = (0.75, 0.75, 0.75, self.ripple_alpha)

        r = self.ripple_radius
        self.ripple.size = (r * 2, r * 2)
        self.ripple.pos = (self.x + self.ripple_pos[0] - r, self.y + self.ripple_pos[1] - r)

    def reset_ripple(self, *args):
        self.ripple_radius = 0
        self.ripple_alpha = 0
        self.update_graphics()

    def on_press(self):
        touch = self.last_touch
        self.ripple_pos = (touch.x - self.x, touch.y - self.y)
        self.ripple_radius = 0
        self.ripple_alpha = 0.4
        self.on_home_clicked()

        max_r = max(self.width, self.height) * 1.2

        expand = Animation(ripple_radius=max_r, d=0.23, t="out_quad")
        fade = Animation(ripple_alpha=0, d=0.18, t="out_quad")

        anim = expand + fade
        anim.bind(on_progress=lambda *a: self.update_graphics())
        anim.bind(on_complete=self.reset_ripple)
        anim.start(self)

    def on_home_clicked(self, *args):
        print("🏠 Home button clicked")


class RippleButton(ButtonBehavior, Widget):
    bg_color = (0.1, 0.4, 0.8, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ripple_alpha = 0
        self.ripple_pos = (0, 0)
        self.ripple_radius = 0

        self.icon = Image(
            source="assets/backArrow.png",
            allow_stretch=True,
            keep_ratio=True,
            size=(dp(36), dp(36)),
        )
        self.add_widget(self.icon)

        self.ripple_color = (1, 1, 1, self.ripple_alpha)

        with self.canvas.before:
            Color(*self.bg_color)
            self.bg = RoundedRectangle(radius=[(dp(0), dp(0)), (16, 16), (0, 0), (0, 0)])

        with self.canvas:
            StencilPush()
            self.stencil_shape = RoundedRectangle(radius=[(dp(0), dp(0)), (16, 16), (0, 0), (0, 0)])
            StencilUse()

            self.ripple_color_instruction = Color(*self.ripple_color)

            self.ripple = Ellipse(size=(0, 0))

            StencilPop()

        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

        self.stencil_shape.pos = self.pos
        self.stencil_shape.size = self.size

        self.icon.pos = (
            self.x + self.width / 2 - self.icon.width / 2,
            self.y + self.height / 2 - self.icon.height / 2,
        )

        self.ripple_color_instruction.rgba = (1, 1, 1, self.ripple_alpha)

        r = self.ripple_radius
        self.ripple.size = (r * 2, r * 2)
        self.ripple.pos = (self.x + self.ripple_pos[0] - r, self.y + self.ripple_pos[1] - r)

    def reset_ripple(self, *args):
        self.ripple_radius = 0
        self.ripple_alpha = 0
        self.update_graphics()

    def on_press(self):
        touch = self.last_touch
        self.ripple_pos = (touch.x - self.x, touch.y - self.y)
        self.ripple_radius = 0
        self.ripple_alpha = 0.4

        max_r = max(self.width, self.height) * 1.2

        expand = Animation(ripple_radius=max_r, d=0.23, t="out_quad")
        fade = Animation(ripple_alpha=0, d=0.18, t="out_quad")

        anim = expand + fade
        anim.bind(on_progress=lambda *a: self.update_graphics())
        anim.bind(on_complete=self.reset_ripple)
        anim.start(self)


class uni_centerBox(RelativeLayout):
    bg_color = ListProperty([1, 1, 1, 1])
    radius = ListProperty([25, 25, 25, 25])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            self.shadow_color = Color(0, 0, 0, 0.10)

            self.shadow = BoxShadow(
                pos=self.pos,
                size=self.size,
                radius=self.radius,
                offset=(0, 0),
                spread=dp(20),
                blur_radius=dp(16),
                border_radius=(20, 20, 20, 20),
            )

            Color(*self.bg_color)
            self.bg_rect = RoundedRectangle(
                pos=(0, 0),
                size_hint=(100, 100),
                radius=self.radius,
            )

        self.content = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
        )

        super().add_widget(self.content)
        self.bind(pos=self.update_rect, size=self.update_rect, x=self.update_rect, y=self.update_rect)

        def delayed_update(dt):
            self.update_rect()
            Clock.schedule_once(lambda dt2: self.update_rect(), 0.05)

        Clock.schedule_once(delayed_update, 0.1)

    def update_rect(self, *args):
        if self.size[0] == 0 or self.size[1] == 0:
            return

        self.shadow.pos = (0, 0)
        self.shadow.size = self.size

        self.bg_rect.pos = (0, 0)
        self.bg_rect.size = self.size

    def add_widget(self, widget, *args, **kwargs):
        if widget is not self.content:
            return self.content.add_widget(widget)
        return super().add_widget(widget, *args, **kwargs)


def add_debug_outline(widget, color=(1, 0, 0, 1), line_width=1.5):
    """
    Adds a colored outline to a Kivy widget for debugging layout issues using the Line instruction.
    """
    with widget.canvas.after:
        Color(*color)
        widget._debug_line = Line(
            rounded_rectangle=(
                widget.x,
                widget.y,
                widget.width,
                widget.height,
                0,
            ),
            width=line_width,
        )

    def update_debug_line(*args):
        widget._debug_line.rounded_rectangle = (
            widget.x,
            widget.y,
            widget.width,
            widget.height,
            0,
        )

    widget.bind(pos=update_debug_line, size=update_debug_line)


class RoundedLabelBox(BoxLayout):
    """A pill-shaped background box for date and time."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, None)
        self.height = dp(40)
        self.width = dp(140)
        self.padding = dp(10)

        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.bg = RoundedRectangle(radius=[10, 10, 10, 10])

        self.label = Label(color=(0, 0.4, 1, 1))
        self.add_widget(self.label)

        self.bind(pos=self.update_bg, size=self.update_bg)

    def set_text(self, text):
        self.label.text = text

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


class uni_lowerContainer(BoxLayout):
    def __init__(self, left_text=None, right_text=None, **kwargs):
        kwargs.setdefault("size_hint_x", 1)
        kwargs.setdefault("size_hint_y", None)
        super().__init__(**kwargs)

        self.orientation = "horizontal"
        self.height = dp(60)
        self.padding = [dp(0), dp(0)]
        self.spacing = dp(20)

        self.shadow_color = Color(0, 0, 0, 0.10)

        self.left_frame = BoxLayout(
            size_hint=(1, 1),
            padding=0,
        )

        self.left_box = BoxLayout(
            orientation="horizontal",
            size_hint=(None, 1),
            padding=0,
            spacing=dp(0),
        )

        with self.left_box.canvas.before:
            self.left_shadow_color = Color(0, 0, 0, 0.1)
            self.left_shadow = BoxShadow(
                pos=self.left_box.pos,
                size=self.left_box.size,
                offset=(0, -2),
                blur_radius=dp(16),
                spread=dp(8),
                border_radius=(0, 16, 0, 0),
            )

            Color(1, 1, 1, 1)
            self.left_bg = RoundedRectangle(
                pos=self.left_box.pos,
                size=self.left_box.size,
                radius=[0, 16, 0, 0],
            )

        def update_left_box_graphics(*args):
            self.left_shadow.pos = self.left_box.pos
            self.left_shadow.size = self.left_box.size
            self.left_bg.pos = self.left_box.pos
            self.left_bg.size = self.left_box.size

        self.left_box.bind(pos=update_left_box_graphics, size=update_left_box_graphics)
        self.left_frame.add_widget(self.left_box)

        self.left_box.bind(children=lambda *args: self.update_left_width(), size=lambda *args: self.update_left_width())

        def update_left_width(self=None, *args):
            if self is None:
                return
            total_width = 0
            for child in self.left_box.children:
                total_width += child.width
                total_width += self.left_box.spacing
            if self.left_box.children:
                total_width -= self.left_box.spacing
            self.left_box.width = total_width

        center = BoxLayout(
            orientation="horizontal",
            size_hint=(None, 1),
            spacing=dp(10),
        )

        self.date_box = RoundedLabelBox(pos_hint={"center_y": 0.5})
        self.time_box = RoundedLabelBox(pos_hint={"center_y": 0.5})

        center.width = dp(140) * 2 + dp(10)
        center.add_widget(self.date_box)
        center.add_widget(self.time_box)

        self.center_box = center

        self.right_frame = BoxLayout(
            size_hint=(1, 1),
            padding=0,
        )

        self.right_box = BoxLayout(
            orientation="horizontal",
            size_hint=(None, 1),
            padding=0,
            spacing=dp(8),
        )
        self.right_frame.add_widget(self.right_box)

        self.right_box.bind(children=lambda *args: self.update_right_width(), size=lambda *args: self.update_right_width())

        self.add_widget(self.left_frame)
        self.add_widget(center)
        self.add_widget(self.right_frame)

        Clock.schedule_interval(self.update_clock, 1)
        self.update_clock(0)

    def update_clock(self, dt):
        now = datetime.now()
        self.date_box.set_text(now.strftime("%b %d, %Y"))
        self.time_box.set_text(now.strftime("%I:%M %p"))

    def update_left_width(self, *args):
        total_width = 0
        for child in self.left_box.children:
            total_width += child.width + self.left_box.spacing
        if self.left_box.children:
            total_width -= self.left_box.spacing
        self.left_box.width = total_width

    def update_right_width(self, *args):
        total_width = 0
        for child in self.right_box.children:
            total_width += child.width + self.left_box.spacing
        if self.right_box.children:
            total_width -= self.right_box.spacing
        self.right_box.width = total_width


class uni_upperContainer(RelativeLayout):
    def __init__(self, title="New_Test_Name", **kwargs):
        if "size_hint" not in kwargs:
            kwargs.setdefault("size_hint_x", 1)
            kwargs.setdefault("size_hint_y", None)

        super().__init__(**kwargs)

        self.height = dp(80)
        self.padding = dp(10)

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg = RoundedRectangle(radius=[dp(20)])

        self.bind(pos=self._update_bg, size=self._update_bg)

        row = BoxLayout(
            orientation="horizontal",
            spacing=dp(20),
            size_hint=(1, 1),
            padding=[dp(20), 10, dp(20), 0],
        )
        self.add_widget(row)

        self.left_slot = BoxLayout(
            size_hint=(1, 1),
        )
        row.add_widget(self.left_slot)

        self.title_container = RelativeLayout(
            size_hint=(None, 1),
            width=dp(400),
        )
        row.add_widget(self.title_container)

        with self.title_container.canvas.before:
            Color(0.95, 0.95, 1, 1)
            self.title_bg = RoundedRectangle(radius=[dp(30)])

        self.title_container.bind(pos=self._update_title_bg, size=self._update_title_bg)

        self.title_label = Label(
            text=title,
            color=(0.2, 0.3, 0.7, 1),
            font_size="26sp",
            halign="center",
            valign="middle",
            size_hint=(1, 1),
            text_size=(None, None),
        )

        def update_title_text_size(instance, value):
            self.title_label.text_size = (self.title_container.width, self.title_container.height)

        self.title_container.bind(size=update_title_text_size, width=update_title_text_size, height=update_title_text_size)
        self.title_container.add_widget(self.title_label)

        self.right_slot = BoxLayout(
            size_hint=(1, 1),
        )
        row.add_widget(self.right_slot)

    def _update_bg(self, *args):
        self.bg.pos = (0, 0)
        self.bg.size = self.size

    def _update_title_bg(self, *args):
        self.title_bg.pos = (0, 0)
        self.title_bg.size = self.title_container.size


class LoadingBar(RelativeLayout):
    def __init__(self, total_time, **kwargs):
        super().__init__(**kwargs)

        self.total_time = total_time
        self.elapsed = 0

        self.size_hint_x = 1
        self.size_hint_y = None
        self.height = dp(140)

        self.bar_max_width = dp(600)

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

        with self.canvas:
            Color(0.9, 0.9, 0.9, 1)
            self.bg_rect = RoundedRectangle(
                pos=(0, 0),
                size=(100, 100),
                radius=[dp(20)],
            )

            Color(0.1, 0.3, 0.7, 1)
            self.fg_rect = RoundedRectangle(
                pos=(0, 0),
                size=(0, 100),
                radius=[dp(20)],
            )

        self.percent_label = Label(
            text="0%",
            font_size="50sp",
            bold=True,
            color=(1, 1, 1, 1),
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(100),
        )
        super().add_widget(self.percent_label)

        super().add_widget(self.time_label)

        self.bind(pos=self._update_graphics)
        self.bind(size=self._update_graphics)

        self._event = Clock.schedule_interval(self.update_progress, 1)

    def _update_graphics(self, *args):
        bar_y = 0
        bar_height = self.height - dp(40)

        bar_width = min(self.bar_max_width, self.width * 0.9)
        bar_x = (self.width - bar_width) / 2

        self.bg_rect.pos = (bar_x, bar_y)
        self.bg_rect.size = (bar_width, bar_height)

        progress_width = (self.elapsed / self.total_time) * bar_width
        self.fg_rect.pos = (bar_x, bar_y)
        self.fg_rect.size = (progress_width, bar_height)

        self.percent_label.pos = (bar_x, bar_y)
        self.percent_label.size = (bar_width, bar_height)

        time_label_y = bar_height
        self.time_label.pos = (0, time_label_y)
        self.time_label.size = (self.width, dp(40))
        self.time_label.text_size = (self.width, dp(40))

    def update_progress(self, dt):
        if self.elapsed < self.total_time:
            self.elapsed += 1
        else:
            self._event.cancel()

        self.elapsed = min(self.elapsed, self.total_time)
        progress_ratio = self.elapsed / self.total_time

        percentage = min(int(progress_ratio * 100), 100)
        self.percent_label.text = f"{percentage}%"

        remaining = max(0, self.total_time - self.elapsed)
        mm = remaining // 60
        ss = remaining % 60
        self.time_label.text = f"Time Remaining: {mm:02d}:{ss:02d}"

        self._update_graphics()


class genButton(MDButton):
    def __init__(self, on_confirm, text="", icon=None, **kwargs):
        kwargs.setdefault("size_hint", (None, None))

        self.on_confirm = on_confirm

        children = []

        if icon:
            children.append(MDButtonIcon(icon=icon))

        if text:
            children.append(MDButtonText(text=text, font_style="Title"))

        super().__init__(*children, **kwargs)
        
        self.bind(on_release=self.open_overlay)
        self.bind(children=lambda *_: self.update_size())
        self.update_size()
    
    def open_overlay(self, *args):
        if not self.on_confirm:
            return
            
        try:
            dialog = confirmOverlay(confirm_callback=self.on_confirm)
            dialog.open()
        except Exception as e:
            print(f"Error opening dialog: {e}")
            import traceback

            traceback.print_exc()

    def update_size(self, *args):
        self.do_layout()
        min_w = sum(c.width for c in self.children) + dp(12)
        min_h = max((c.height for c in self.children), default=dp(40))
        self.width = min_w
        self.height = min_h