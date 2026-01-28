from functools import partial

from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.graphics import BoxShadow, Color
from kivy.clock import Clock
#from kivy.core.window import Window

from mdWidgets import (
    add_debug_outline
)


class UserCard(MDCard):
    def __init__(self, index, on_press_cb, on_release_cb, on_move_out_cb, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.on_press_cb = on_press_cb
        self.on_release_cb = on_release_cb
        self.on_move_out_cb = on_move_out_cb

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            if self.on_press_cb:
                self.on_press_cb(self.index)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            if self.collide_point(*touch.pos):
                if self.on_press_cb:
                    self.on_press_cb(self.index)
            else:
                if self.on_move_out_cb:
                    self.on_move_out_cb(self.index)
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            if self.on_release_cb:
                self.on_release_cb(self.index, self.collide_point(*touch.pos))
            return True
        return super().on_touch_up(touch)


class LockScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.md_bg_color = (1, 1, 1, 1)
        # self.size_hint = (1, 1)
        # self.size = Window.size

        

        # user = [
        #         {
        #             "username": "123",
        #             "password": "123",
        #             "color": "blue"
        #         },
        #         {
        #             "username": "80808",
        #             "password": "7355608",
        #             "color": "red"
        #         },
        #         {
        #             "username": "You think he loves you but I know what he really loves you for it's your leopard skinned pillbox hat",
        #             "password": "7355608",
        #             "color": "green"
        #         },
        #         {
        #             "username": "80811",
        #             "password": "7355608",
        #             "color": "lightBlue"
        #         },
        #         {
        #             "username": "80812",
        #             "password": "7355608",
        #             "color": "orange"
        #         },
        #         {
        #             "username": "80813",
        #             "password": "7355608",
        #             "color": "black"
        #         },
        #         {
        #             "username": "80814",
        #             "password": "7355608",
        #             "color": "gray"
        #         },
        #         {
        #             "username": "80814",
        #             "password": "7355608",
                    
        #         },
        #     ]
        
        self.users = load_users()["users"]
        self.current_index = 0
        self.active_index = None
        self.highlight_min_duration = 0.33
        self._highlight_event = None

        # 主布局改为 FloatLayout
        layout = MDFloatLayout(
            pos_hint={"center_x": 0.5, "center_y": 0.4},
        )

        welcome_label = MDLabel(
            text="Welcome",
            halign="center",
            font_style="Title",
            pos_hint={"center_x": 0.5, "center_y": 0.9},
            size_hint=(None, None),
        )
        welcome_label.color = (0.161, 0.278, 0.576, 1)
        layout.add_widget(welcome_label)

        self.card_width = dp(180)
        self.card_height = dp(210)
        self.card_spacing = dp(20)
        self.carousel_scroll_step = self.card_width + self.card_spacing
        self.user_cards = []

        carousel_container = MDFloatLayout(
            size_hint=(0.85, 0.5),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
        )

        left_btn = MDIconButton(
            icon="chevron-left",
            pos_hint={"center_x": 0, "center_y": 0.5},
            size_hint=(None, None),
            on_release=self.prev_user,
            theme_font_size="Custom",
            font_size="84sp",
        )
        left_btn.size = (left_btn.font_size * 1.2, left_btn.font_size * 1.2)
        left_btn.bind(
            font_size=lambda instance, value: setattr(instance, "size", (value * 1.2, value * 1.2))
        )
        right_btn = MDIconButton(
            icon="chevron-right",
            pos_hint={"center_x": 1, "center_y": 0.5},
            size_hint=(None, None),
            on_release=self.next_user,
            theme_font_size="Custom",
            font_size="84sp",
        )
        right_btn.size = (right_btn.font_size * 1.2, right_btn.font_size * 1.2)
        right_btn.bind(
            font_size=lambda instance, value: setattr(instance, "size", (value * 1.2, value * 1.2))
        )
        carousel_container.add_widget(left_btn)
        carousel_container.add_widget(right_btn)

        self.user_carousel = MDScrollView(
            do_scroll_y=False,
            do_scroll_x=True,
            bar_width=0,
            size_hint=(0.85, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},

        )

        self.carousel_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=self.card_spacing,
            padding=[self.card_spacing, 0, self.card_spacing, 0],
            size_hint=(None, 1),
        )
        self.carousel_layout.bind(minimum_width=self.carousel_layout.setter("width"))
        self.user_carousel.add_widget(self.carousel_layout)
        #add_debug_outline(self.user_carousel)
        self.add_inner_shadow(self.user_carousel)
        carousel_container.add_widget(self.user_carousel)
        #add_debug_outline(carousel_container)
        layout.add_widget(carousel_container)

        for index, user_info in enumerate(self.users):
            self.add_user_card(user_info, index)

        self.update_selected_card()


        subtitle_label = MDLabel(
            text="Please Select a Profile",
            halign="center",
            font_style="Title",
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            size_hint=(None, None),
            adaptive_size=True,
            shorten=True,
            shorten_from="right",
        )
        subtitle_label.color = (0.161, 0.278, 0.576, 1)
        layout.add_widget(subtitle_label)

        create_btn = MDButton(
            MDButtonText(text="Create New Profile", font_style="Title"),
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            size_hint=(0.5, 0.1),
            on_release=self.go_to_create_user,
        )
        layout.add_widget(create_btn)

        self.add_widget(layout)


    def add_user_card(self, user_info, index):

        profileColors = {
            "blue": [0.161, 0.278, 0.576, 1],
            "red": [0.816, 0.235, 0.212, 1],
            "green": [0.235, 0.561, 0.322, 1],
            "lightBlue": [0.306, 0.749, 0.839, 1],
            "orange": [0.859, 0.545, 0.082, 1],
            "black": [0.133, 0.094, 0.082, 1],
            "gray": [0.82, 0.82, 0.824, 1],
        }

        card_anchor = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint=(None, 1),
            width=self.card_width,
        )
        card = UserCard(
            index=index,
            on_press_cb=self.set_active_user,
            on_release_cb=self.release_user,
            on_move_out_cb=self.clear_active_user,
            style="elevated",
            size_hint=(None, None),
            size=(self.card_width, self.card_height),
            radius=[dp(18)],
            elevation=8,
            theme_bg_color="Custom",
            md_bg_color=(1, 1, 1, 1),
        )

        content = MDBoxLayout(
            orientation="vertical",
            padding=[dp(12), dp(12), dp(12), dp(12)],
            spacing=dp(8),
        )

        icon_anchor = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint=(1, 1),
            #height=dp(80),
        )
        icon_button = MDIconButton(
            icon="account-circle",
            size_hint=(None, None),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            theme_icon_color="Custom",
            icon_color=profileColors[user_info.get("color", "blue")],
            theme_font_size="Custom",
            font_size="96sp",
            on_press=partial(self.set_active_user, index),
            on_release=partial(self.release_user, index, True),
        )
        icon_button.size = (icon_button.font_size * 1.2, icon_button.font_size * 1.2)
        icon_button.bind(
            font_size=lambda instance, value: setattr(instance, "size", (value * 1.2, value * 1.2))
        )
        #add_debug_outline(icon_button)
        #add_debug_outline(icon_anchor)
        icon_anchor.add_widget(icon_button)
        content.add_widget(icon_anchor)

        name_label = MDLabel(
            text=user_info.get("username", ""),
            halign="center",
            font_style="Title",
            size_hint=(1, None),
            height=dp(28),
        )
        content.add_widget(name_label)

        card.add_widget(content)
        #add_debug_outline(card)
        card_anchor.add_widget(card)
        self.carousel_layout.add_widget(card_anchor)
        self.user_cards.append(card)

    def add_inner_shadow(self, widget, blur_radius=dp(18), spread=dp(-10), color=(0, 0, 0, 0.18)):
        with widget.canvas.after:
            shadow_color = Color(*color)
            inset_shadow = BoxShadow(
                pos=widget.pos,
                size=widget.size,
                offset=(0, 0),
                blur_radius=blur_radius,
                spread=spread,
                inset=True,
                border_radius=(dp(12), dp(12), dp(12), dp(12)),
            )

        def update_shadow(*args):
            inset_shadow.pos = widget.pos
            inset_shadow.size = widget.size

        widget.bind(pos=update_shadow, size=update_shadow)
        update_shadow()

    def update_selected_card(self):
        for index, card in enumerate(self.user_cards):
            if index == self.active_index:
                card.md_bg_color = (0.92, 0.95, 1, 1)
            else:
                card.md_bg_color = (1, 1, 1, 1)

    def scroll_carousel(self, delta_px):
        if not self.user_carousel or not self.carousel_layout.width:
            return
        max_scroll = self.carousel_layout.width - self.user_carousel.width
        if max_scroll <= 0:
            self.user_carousel.scroll_x = 0
            return
        delta = delta_px / max_scroll
        self.user_carousel.scroll_x = min(1.0, max(0.0, self.user_carousel.scroll_x + delta))

    def prev_user(self, *args):
        self.scroll_carousel(-self.carousel_scroll_step)

    def next_user(self, *args):
        self.scroll_carousel(self.carousel_scroll_step)

    def select_user(self, index, *args):
        if not self.users:
            return
        self.current_index = index % len(self.users)
        self.go_to_login()

    def set_active_user(self, index, *args):
        if not self.users:
            return
        if self._highlight_event:
            self._highlight_event.cancel()
            self._highlight_event = None
        self.active_index = index % len(self.users)
        self.update_selected_card()

    def clear_active_user(self, index=None, *args):
        if self.active_index is None:
            return
        if index is None or self.active_index == index:
            self.active_index = None
            self.update_selected_card()

    def release_user(self, index, did_activate=True, *args):
        if did_activate:
            self.select_user(index)
        if self._highlight_event:
            self._highlight_event.cancel()
        self._highlight_event = Clock.schedule_once(
            lambda *_: self.clear_active_user(index),
            self.highlight_min_duration,
        )

    def go_to_create_user(self, *args):
        self.manager.current = "create_user"

    def go_to_login(self, *args):
        if self.users:
            login_screen = self.manager.get_screen("user_login")
            login_screen.set_user(self.users[self.current_index])
            self.manager.current = "user_login"
        #print(f"login with user {self.users[self.current_index]}")