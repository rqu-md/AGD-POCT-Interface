from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.graphics import Color, BoxShadow, RoundedRectangle, Line

from mdWidgets import (
    LoadingBar,
    StatusHeader,
    uni_centerBox,
    uni_lowerContainer,
    uni_upperContainer,
    uni_backButton,
    uni_homeButton,
    genButton,
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

class testScreenLive(MDScreen):
    def on_confirm(self):
        print("Confirmation accepted!")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 🔥 FORCE ROOT TO FILL THE SCREEN
        self.md_bg_color = (1, 1, 1, 1)
        self.size_hint = (1, 1)
        self.size = Window.size

        top = uni_upperContainer(
            title="new_test_name",
            size_hint=(0.95, None),  # 95% width for padding
            pos_hint={'center_x': 0.5, 'top': 1}
        )
        self.add_widget(top)
        
        # MAIN centered content - FloatLayout centers using pos_hint
        mainContent = uni_centerBox(
            size_hint=(0.9, 0.65),
            pos_hint={'center_x': 0.5, 'center_y': 0.48},
            #style="elevated"
        )
        # Add a simple label to verify widget positioning
        #from kivy.uix.label import Label
        #test_label = Label(text="TEST", font_size='30sp', color=(1, 0, 0, 1))
        #mainContent.add_widget(test_label)
        
        #add_debug_outline(mainContent, color=(1, 0, 1, 1))    # Blue
        mainContent.add_widget(LoadingBar(total_time=50))
        
        buttonContainer = MDBoxLayout(
            orientation = "horizontal",
            size_hint = (1, 1),
            height = dp(60),
            pos_hint = {'center_x': 0.9, 'center_y': 0.9}
        )
        buttonContainer.add_widget(genButton(
            on_confirm=self.on_confirm,
            text="ABORT TEST", 
            icon="timer-cancel"),
            )
        
        #add_debug_outline(buttonContainer, color=(0, 0, 1, 1))    # Blue
        mainContent.add_widget(buttonContainer)

        
        self.add_widget(mainContent)

        

        bottom = uni_lowerContainer( 
            #right_text="NovelBeamUSA",
            size_hint=(1, None),
            pos_hint={'x': 0, 'y': 0}
        )

        #bottom.left_box.add_widget(uni_backButton())
        #bottom.left_box.add_widget(uni_homeButton())
        # Set initial width to ensure full width from start
        bottom.width = Window.width
        self.add_widget(bottom)
        
        # Update width when window or dashboard resizes
        def update_width(*args):
            if bottom.parent:
                bottom.width = bottom.parent.width
        Window.bind(width=update_width)
        self.bind(width=update_width)
