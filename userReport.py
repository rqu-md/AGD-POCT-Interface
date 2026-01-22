from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.graphics import Color, BoxShadow, RoundedRectangle, Line
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDListItemLeadingIcon
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.dropdownitem import MDDropDownItem, MDDropDownItemText
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField, MDTextFieldLeadingIcon, MDTextFieldHintText

from mdWidgets import (
    uni_centerBox,
    uni_lowerContainer,
    uni_upperContainer,
    uni_backButton,
    uni_homeButton,
    uni_folderContainer,
    add_debug_outline,
)

class userReport(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 🔥 FORCE ROOT TO FILL THE SCREEN
        self.md_bg_color = (1, 1, 1, 1)
        self.size_hint = (1, 1)
        self.size = Window.size

        top = uni_upperContainer(
            title="Report_Name",
            size_hint=(0.95, None),  # 95% width for padding
            pos_hint={'center_x': 0.5, 'top': 1}
        )
        self.add_widget(top)
        
        # MAIN centered content - FloatLayout centers using pos_hint
        mainContent = uni_folderContainer(
            size_hint=(0.9, 0.65),
            pos_hint={'center_x': 0.5, 'center_y': 0.48},
            bg_color=(1, 1, 1, 1),
            #style="elevated"
        )
        mainContent.set_tabs([
            ("Test Results", self._build_test_results_tab("Project Name", "20XX-XX-XX", "high tolerance")),
            ("Result Details", self._build_result_details_tab("high tolerance")),
            ("Export", self._build_export_tab()),
        ])
        # Add a simple label to verify widget positioning
        #from kivy.uix.label import Label
        #test_label = Label(text="TEST", font_size='30sp', color=(1, 0, 0, 1))
        #mainContent.add_widget(test_label)
        
        #add_debug_outline(mainContent, color=(1, 0, 1, 1))    # Blue
        #mainContent.add_widget(LoadingBar(total_time=50))
        
        

        
        self.add_widget(mainContent)

        # --- Center content ---
        

        

        bottom = uni_lowerContainer( 
            #right_text="NovelBeamUSA",
            size_hint=(1, None),
            pos_hint={'x': 0, 'y': 0}
        )

        bottom.left_box.add_widget(uni_backButton())
        bottom.left_box.add_widget(uni_homeButton())
        # Set initial width to ensure full width from start
        bottom.width = Window.width
        self.add_widget(bottom)
        
        # Update width when window or dashboard resizes
        def update_width(*args):
            if bottom.parent:
                bottom.width = bottom.parent.width
        Window.bind(width=update_width)
        self.bind(width=update_width)

    def _build_simple_tab(self, title):
        box = MDBoxLayout(orientation="vertical")
        label = MDLabel(
            text=title,
            halign="center",
            valign="middle",
            theme_text_color="Secondary",
        )
        label.bind(size=lambda instance, size: setattr(instance, "text_size", size))
        box.add_widget(label)
        return box

    def _build_result_summary(self, result):
        icon_map = {
            "high tolerance": "liquor",
            "LOW tolerance": "glass-wine",
            "extremely low tolerance": "glass-cocktail-off",
            "NON-VALID RESULTS": "alert-remove",
        }
        normalized = " ".join(result.strip().lower().split())
        icon_map_normalized = {k.lower(): v for k, v in icon_map.items()}
        icon_name = icon_map.get(result, icon_map_normalized.get(normalized, "help-circle"))

        styles = {
            "high tolerance": ((0.2, 0.6, 0.3, 1), "High Tolerance"),
            "low tolerance": ((0.82, 0.55, 0.2, 1), "Low Tolerance"),
            "extremely low tolerance": ((0.85, 0.2, 0.2, 1), "Extremely Low Tolerance"),
            "non-valid results": ((0.45, 0.45, 0.45, 1), "Non-Valid Results"),
        }
        result_color, result_text = styles.get(normalized, ((0.2, 0.3, 0.7, 1), result))

        center_block = MDBoxLayout(
            orientation="vertical",
            spacing=dp(4),
            size_hint=(None, None),
            padding=dp(0),
        )
        center_block.bind(minimum_height=center_block.setter("height"))
        center_block.bind(minimum_width=center_block.setter("width"))
        result_title = MDLabel(
            text="This Result:",
            halign="center",
            valign="middle",
            theme_text_color="Custom",
            text_color=(0.2, 0.3, 0.7, 1),
            bold=True,
            padding=dp(0),
            size_hint=(None, None),
            text_size=(None, None),
            adaptive_size=True,
            shorten=True,
            shorten_from="right",
        )
        result_title.font_size = "24sp"
        result_title.bind(texture_size=lambda instance, size: setattr(instance, "size", size))
        #add_debug_outline(result_title, color=(0, 1, 0, 1))
        center_block.add_widget(result_title)

        result_row = MDBoxLayout(orientation="horizontal", spacing=dp(8), adaptive_size=True)
        result_row.bind(minimum_width=result_row.setter("width"))
        result_row.bind(minimum_height=result_row.setter("height"))
        icon = MDListItemLeadingIcon(icon=icon_name)
        icon.theme_text_color = "Custom"
        icon.text_color = result_color
        icon.size_hint = (None, None)
        icon.font_size = "40sp"
        icon.size = (dp(36), dp(36))

        result_label = MDLabel(
            text=result_text,
            halign="left",
            valign="bottom",
            theme_text_color="Custom",
            text_color=result_color,
            font_style="Title",
            size_hint=(None, None),
            text_size=(None, None),
            adaptive_size=True,
            shorten=True,
            shorten_from="right",
        )

        result_label.font_size = "36sp"
        result_label.bind(texture_size=lambda instance, size: setattr(instance, "size", size))

        
        result_row.add_widget(icon)
        result_row.add_widget(result_label)
        #add_debug_outline(result_row, color=(0, 1, 0, 1))
        result_anchor = AnchorLayout(anchor_x="center", anchor_y="center", size_hint=(1, None))
        result_row.bind(height=lambda instance, value: setattr(result_anchor, "height", value))
        result_anchor.height = result_row.height
        #add_debug_outline(result_anchor, color=(0, 1, 0, 1))
        
        result_anchor.add_widget(result_row)
        #add_debug_outline(center_block, color=(0, 1, 0, 1))
        center_block.add_widget(result_anchor)
        return center_block

    def _build_test_results_tab(self, project, time_str, result):
        root = MDBoxLayout(orientation="vertical", spacing=dp(16))
        header_row = MDBoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(32))
        project_label = MDLabel(
            text=project,
            halign="left",
            valign="middle",
            theme_text_color="Primary",
        )
        date_label = MDLabel(
            text=time_str,
            halign="right",
            valign="middle",
            theme_text_color="Primary",
        )
        header_row.add_widget(project_label)
        header_row.add_widget(date_label)
        #add_debug_outline(header_row, color=(0, 1, 0, 1))
        root.add_widget(header_row)

        result_center = AnchorLayout(anchor_x="center", anchor_y="top", size_hint=(1, 1))
        result_center.add_widget(self._build_result_summary(result))
        #add_debug_outline(result_center, color=(0, 1, 0, 1))
        root.add_widget(result_center)
        return root

    def _build_result_details_tab(self, result):
        details_map = {
            "high tolerance": (
                "Your ALDH2 gene is functioning normally, which means your body can properly break down alcohol efficiently. You are less likely to experience flushing or discomfort after drinking. \n\n⚠ Alcohol can still harm your liver, brain, and overall health with excessive use. \n\nTip: Enjoy responsibly! The CDC recommends limiting to 1 drink per day for women and 2 for men. Staying hydrated and giving your body rest days from alcohol is key to long-term health. "
            ),
            "low tolerance": (
                "Your ALDH2 gene carries a variant that reduces your body's ability to break down alcohol efficiently. This can make you flush or feel unwell after even small amounts of alcohol. You may experience facial flushing, nausea, or rapid heartbeat after drinking. \n\n⚠ Regular alcohol consumption can increase your risk of health issues over time, including liver damage, esophageal cancer, and heart issues. \n\nTip: It's strongly advised to limit alcohol consumption. If you choose to drink, keep it to small, occasional amounts. Take it slow, eat beforehand, and stay hydrated to help your body process it more safely."
            ),
            "extremely low tolerance": (
                "Your ALDH2 gene has two inactive copies, meaning your body has a severely impaired ability to process alcohol. Even small amounts of alcohol can lead to a dangerous buildup of acetaldehyde, a toxic and carcinogenic substance that your body can't easily remove. \n\n⚠ Drinking may cause strong flushing, dizziness, nausea, or heart palpitations — and long-term use can significantly increase your risk of cancer, liver damage, and cardiovascular diseases. \n\nTip: The safest choice is to avoid alcohol entirely. If possible, choose non-alcoholic beverages and celebrate with alternatives that protect your long-term health. Your body will thank you for it!"
            ),
            "non-valid results": (
                "This result could not be interpreted. Please re-run the test or consult support if the issue persists."
            ),
        }
        normalized = " ".join(result.strip().lower().split())
        details_text = details_map.get(normalized, "No details available for this result.")

        root = MDBoxLayout(orientation="vertical", spacing=dp(12))

        scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True,
            scroll_type=["bars", "content"],
            bar_width=dp(6),
            bar_color=(0.2, 0.3, 0.7, 0.7),
            bar_inactive_color=(0.2, 0.3, 0.7, 0.35),
        )
        scroll.scroll_y = 1

        scroll_content = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=[0, dp(4), dp(8), dp(8)],
            spacing=dp(16),
        )
        scroll_content.bind(minimum_height=scroll_content.setter("height"))

        result_summary = self._build_result_summary(result)
        result_wrapper = AnchorLayout(anchor_x="center", anchor_y="top", size_hint=(1, None))
        result_wrapper.height = result_summary.height
        result_summary.bind(height=lambda instance, value: setattr(result_wrapper, "height", value))
        result_wrapper.add_widget(result_summary)
        scroll_content.add_widget(result_wrapper)

        details_label = MDLabel(
            text=details_text,
            halign="left",
            valign="top",
            theme_text_color="Primary",
            size_hint_y=None,
        )
        details_label.bind(
            width=lambda instance, value: setattr(instance, "text_size", (value, None))
        )
        details_label.bind(
            texture_size=lambda instance, size: setattr(instance, "height", size[1])
        )

        scroll_content.add_widget(details_label)
        scroll.add_widget(scroll_content)
        root.add_widget(scroll)
        return root

    def _build_export_tab(self, qr_image_path="assets/sampleQR.png"):
        root = MDBoxLayout(orientation="vertical", spacing=dp(16))

        header_row = MDBoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(40))
        left_group = MDBoxLayout(orientation="horizontal", size_hint=(None, 1), spacing=dp(12))
        left_group.bind(minimum_width=left_group.setter("width"))
        header_label = MDLabel(
            text="Select Export Method:",
            halign="left",
            valign="middle",
            #theme_text_color="Primary",
            size_hint=(None, 1),
        )
        header_label.bind(texture_size=lambda instance, size: setattr(instance, "width", size[0]))

        dropdown = MDDropDownItem(size_hint=(None, None))
        dropdown_text = MDDropDownItemText(text="QR Code")
        dropdown.add_widget(dropdown_text)
        dropdown.width = dp(160)
        left_group.add_widget(header_label)
        left_group.add_widget(dropdown)
        header_row.add_widget(left_group)
        header_row.add_widget(Widget())
        root.add_widget(header_row)

        content_holder = MDBoxLayout(orientation="vertical", size_hint=(1, 1))
        root.add_widget(content_holder)

        qr_container = MDBoxLayout(orientation="vertical", spacing=dp(16))
        qr_container.add_widget(AnchorLayout(size_hint=(1, None), height=dp(200)))
        qr_image = Image(
            source=qr_image_path,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(None, None),
            size=(dp(180), dp(180)),
        )
        qr_container.children[0].add_widget(qr_image)

        qr_instructions = MDLabel(
            text="Scan with your mobile device.\nYou will be redirected to a portal where your results will be available for download.",
            halign="center",
            valign="top",
            #theme_text_color="Primary",
        )
        qr_instructions.bind(size=lambda instance, size: setattr(instance, "text_size", size))
        qr_container.add_widget(qr_instructions)

        usb_container = MDBoxLayout(orientation="vertical", spacing=dp(16))
        usb_note = MDLabel(
            text="Make sure your device is properly connected.",
            halign="center",
            valign="middle",
            #theme_text_color="Primary",
        )
        usb_note.bind(size=lambda instance, size: setattr(instance, "text_size", size))
        usb_button = MDButton(style="elevated", size_hint=(None, None))
        usb_label = MDButtonText(text="Export To USB")
        usb_button.add_widget(usb_label)
        def _resize_usb_button(*_):
            usb_button.width = usb_label.texture_size[0] + dp(48)
            usb_button.height = max(usb_label.texture_size[1] + dp(20), dp(48))
        usb_label.bind(texture_size=_resize_usb_button)
        _resize_usb_button()
        usb_container.add_widget(usb_note)
        usb_container.add_widget(AnchorLayout(size_hint=(1, None), height=dp(56)))
        usb_container.children[0].add_widget(usb_button)

        def set_export_view(value):
            dropdown_text.text = value
            content_holder.clear_widgets()
            if value == "USB":
                content_holder.add_widget(usb_container)
            else:
                content_holder.add_widget(qr_container)

        menu_items = [
            {"text": "QR Code", "on_release": lambda *_: set_export_view("QR Code")},
            {"text": "USB", "on_release": lambda *_: set_export_view("USB")},
        ]
        menu = MDDropdownMenu(caller=dropdown, items=menu_items, width_mult=3)
        dropdown.on_release = menu.open

        set_export_view("QR Code")
        return root

    