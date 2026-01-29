from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.textfield import MDTextField
from kivymd.uix.textfield import MDTextFieldLeadingIcon
from kivymd.uix.textfield import MDTextFieldHintText
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock
from kivy.uix.widget import Widget

class UserCard(MDCard):
    def on_touch_down(self, touch):
        return False

    def on_touch_move(self, touch):
        return False

    def on_touch_up(self, touch):
        return False

class UserLoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.md_bg_color = (1, 1, 1, 1)
        self.size_hint = (1, 1)
        self.size = Window.size

        self.current_user = None

        layout = MDFloatLayout()

        profile_colors = {
            "blue": [0.161, 0.278, 0.576, 1],
            "red": [0.816, 0.235, 0.212, 1],
            "green": [0.235, 0.561, 0.322, 1],
            "lightBlue": [0.306, 0.749, 0.839, 1],
            "orange": [0.859, 0.545, 0.082, 1],
            "black": [0.133, 0.094, 0.082, 1],
            "gray": [0.82, 0.82, 0.824, 1],
        }

        # Center container inside a scroll view (disabled by default).
        self.center_scroll = MDScrollView(
            do_scroll_x=False,
            do_scroll_y=False,
            bar_width=0,
            size_hint=(1, 1),
        )
        self.center_container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(24),
            padding=[0, dp(24), 0, dp(24)],
            size_hint=(None, None),
            width=dp(360),
        )
        self.center_container.bind(minimum_height=self.center_container.setter("height"))
        self._keyboard_height = dp(300)
        self._scroll_extra = dp(120)
        self._focused = False

        self.center_container_anchor = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint=(1, None),
        )
        self.center_container_anchor.add_widget(self.center_container)

        self.top_spacer = Widget(size_hint=(1, None), height=0)
        self.bottom_spacer = Widget(size_hint=(1, None), height=0)

        self.center_content = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
        )
        self.center_content.add_widget(self.top_spacer)
        self.center_content.add_widget(self.center_container_anchor)
        self.center_content.add_widget(self.bottom_spacer)

        # 用户卡片（替代标题）
        self.user_card = UserCard(
            style="elevated",
            size_hint=(None, None),
            size=(dp(200), dp(200)),
            radius=[dp(18)],
            elevation=8,
            theme_bg_color="Custom",
            md_bg_color=(1, 1, 1, 1),
        )
        card_content = MDBoxLayout(
            orientation="vertical",
            padding=[dp(12), dp(12), dp(12), dp(12)],
            spacing=dp(8),
        )
        icon_anchor = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint=(1, 1),
        )
        self.user_icon = MDIcon(
            icon="account-circle",
            theme_icon_color="Custom",
            icon_color=profile_colors["blue"],
            theme_font_size="Custom",
            font_size="96sp",
        )
        icon_anchor.add_widget(self.user_icon)
        card_content.add_widget(icon_anchor)
        self.user_name_label = MDLabel(
            text="User Name",
            halign="center",
            font_style="Title",
            size_hint=(1, None),
            height=dp(28),
        )
        card_content.add_widget(self.user_name_label)
        self.user_card.add_widget(card_content)
        self.user_card_anchor = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint=(1, None),
            height=self.user_card.height,
        )
        self.user_card_anchor.add_widget(self.user_card)
        self.center_container.add_widget(self.user_card_anchor)

        self.status_label = MDLabel(
            text="",
            halign="center",
            font_style="Body",
            size_hint=(1, None),
            height=dp(20),
            adaptive_size=True,
            theme_text_color="Custom",
            text_color=(0.816, 0.235, 0.212, 1),
        )
        self.center_container.add_widget(self.status_label)

        # 密码输入框
        self.password_field = MDTextField(
            MDTextFieldLeadingIcon(icon="lock"),
            MDTextFieldHintText(text="Enter password"),
            password=True,
            size_hint=(None, None),
            width=dp(260),
        )

        # Done 按钮（和输入框平行）
        login_btn = MDButton(
            MDButtonIcon(
                icon="arrow-right",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                theme_font_size="Custom",
                font_size="48sp",
            ),
            style="elevated",
            size_hint=(None, None),
            height=dp(60),
            width=dp(72),
            theme_bg_color="Custom",  # Use custom color
            md_bg_color=(0.1, 0.4, 0.8, 1),
            on_release=self.check_password
        )
        self.login_row = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(12),
            size_hint=(None, None),
            height=dp(60),
        )
        self.login_row.width = self.password_field.width + login_btn.width + dp(12)
        self.login_row.add_widget(self.password_field)
        self.login_row.add_widget(login_btn)
        self.center_container.add_widget(self.login_row)

        self.center_scroll.add_widget(self.center_content)
        layout.add_widget(self.center_scroll)

        # Back 按钮固定左上角
        back_btn = MDButton(
            MDButtonIcon(icon="arrow-left"),
            MDButtonText(text="Back", font_style="Title"),
            style="elevated",
            size_hint=(0.25, 0.1),
            pos_hint={"x": 0.02, "top": 0.98},
            on_release=self.go_back
        )
        layout.add_widget(back_btn)

        self.add_widget(layout)

        self.password_field.bind(focus=self._on_password_focus)
        self.center_container.bind(height=lambda *_: self._update_scroll_layout())
        Window.bind(on_resize=self._on_window_resize)
        self._update_scroll_layout()

    def _on_window_resize(self, *_args):
        self._update_scroll_layout()

    def _on_password_focus(self, _instance, focused):
        self._focused = bool(focused)
        self.center_scroll.do_scroll_y = self._focused
        self._update_scroll_layout()
        if focused:
            Clock.schedule_once(self._scroll_login_row_into_view, 0)
            Clock.schedule_once(self._scroll_login_row_into_view, 0.2)

    def _scroll_login_row_into_view(self, *_args):
        self.center_scroll.scroll_to(self.login_row, padding=self._keyboard_height, animate=False)

    def _update_scroll_layout(self):
        available_height = Window.height
        container_height = max(self.center_container.height, dp(1))
        extra = (self._keyboard_height + self._scroll_extra) if self._focused else 0
        content_height = max(available_height, container_height + extra)
        padding_total = content_height - container_height
        if self._focused:
            bottom = max(self._keyboard_height, padding_total / 2)
            top = max(dp(8), padding_total - bottom)
        else:
            top = padding_total / 2
            bottom = padding_total / 2
        self.center_content.height = content_height
        self.center_container_anchor.height = container_height
        self.top_spacer.height = top
        self.bottom_spacer.height = bottom

    def set_user(self, user):
        self.current_user = user
        self.user_name_label.text = user.get("username", "")
        profile_colors = {
            "blue": [0.161, 0.278, 0.576, 1],
            "red": [0.816, 0.235, 0.212, 1],
            "green": [0.235, 0.561, 0.322, 1],
            "lightBlue": [0.306, 0.749, 0.839, 1],
            "orange": [0.859, 0.545, 0.082, 1],
            "black": [0.133, 0.094, 0.082, 1],
            "gray": [0.82, 0.82, 0.824, 1],
        }
        self.user_icon.icon_color = profile_colors.get(user.get("color", "blue"), profile_colors["blue"])
        self.status_label.text = ""

    def check_password(self, *args):
        if self.current_user and self.password_field.text == self.current_user["password"]:
            self.manager.current = "main"  # 🔑 登录成功 → 进入主界面
        else:
            self.status_label.text = "Wrong password!"

    def go_back(self, *args):
        self.manager.current = "lock"