from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.graphics import Color, BoxShadow, RoundedRectangle, Line
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDListItemLeadingIcon
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.textfield import MDTextField, MDTextFieldLeadingIcon, MDTextFieldHintText

from mdWidgets import (
    uni_centerBox,
    uni_lowerContainer,
    uni_upperContainer,
    uni_backButton,
    uni_homeButton,
    uni_folderContainer,
)


def add_debug_outline(widget, color=(1, 0, 0, 1), line_width=1.5):
    """
    Adds a colored outline to a Kivy widget for debugging layout issues 
    using the Line instruction with rounded corners format.
    """
    with widget.canvas.after:
        Color(*color)
        # Change from RoundedRectangle to Line
        widget._debug_line = Line(
            rounded_rectangle=(
                widget.x, widget.y, 
                widget.width, widget.height, 
                0, # Assumes 0 radius for debug outline, adjust if needed
            ),
            width=line_width,
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
            ("Test Results", self._build_test_results_tab("Project Name", "20XX-XX-XX", "NON-VALID RESULTS")),
            ("Result Details", self._build_simple_tab("Result Details")),
            ("Export", self._build_simple_tab("Export")),
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

    def _build_test_results_tab(self, project, time_str, result):
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
        root.add_widget(header_row)

        center_block = MDBoxLayout(orientation="vertical", spacing=dp(12), size_hint=(1, 1))
        result_title = MDLabel(
            text="This Result:",
            halign="center",
            valign="middle",
            theme_text_color="Custom",
            text_color=(0.2, 0.3, 0.7, 1),
            bold=True,
        )
        result_title.bind(size=lambda instance, size: setattr(instance, "text_size", size))
        center_block.add_widget(result_title)

        result_row = MDBoxLayout(orientation="horizontal", spacing=dp(8), size_hint=(None, None))
        result_row.bind(minimum_width=result_row.setter("width"))
        result_row.bind(minimum_height=result_row.setter("height"))
        icon = MDListItemLeadingIcon(icon=icon_name)
        icon.theme_text_color = "Custom"
        icon.text_color = result_color
        icon.size_hint = (None, None)
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
        result_label.bind(texture_size=lambda instance, size: setattr(instance, "size", size))

        
        result_row.add_widget(icon)
        result_row.add_widget(result_label)

        result_anchor = AnchorLayout(anchor_x="center", anchor_y="center")
        result_anchor.add_widget(result_row)
        center_block.add_widget(result_anchor)

        root.add_widget(center_block)
        return root

    