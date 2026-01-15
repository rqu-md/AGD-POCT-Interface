from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.graphics import Color, BoxShadow, RoundedRectangle, Line
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.textfield import MDTextField, MDTextFieldLeadingIcon, MDTextFieldHintText

from mdWidgets import (
    StatusHeader,
    uni_centerBox,
    uni_lowerContainer,
    uni_upperContainer,
    uni_backButton,
    uni_homeButton,
    genButton,
    LoadingBar,
    InstructionPanel,
    MultiStepInstructionOverlay,
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

class pretest(MDScreen):
    def on_confirm(self):
        print("Confirmation accepted!")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 🔥 FORCE ROOT TO FILL THE SCREEN
        self.md_bg_color = (1, 1, 1, 1)
        self.size_hint = (1, 1)
        self.size = Window.size

        top = uni_upperContainer(
            title="Test",
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
        #mainContent.add_widget(LoadingBar(total_time=50))
        
        

        
        self.add_widget(mainContent)

        # --- Center content ---
        title = MDLabel(
            text="Start New Test",
            font_style="Title",
            halign="center",
            font_size="32sp",
            theme_text_color="Custom",
            text_color=(0.16, 0.30, 0.62, 1),
            size_hint=(1, None),
            height=dp(48)
        )

        input_row = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            padding=[dp(30), dp(0), dp(30), dp(0)],
            height=dp(40),
            spacing=dp(20)
        )

        self.test_name_input = MDTextField(
            MDTextFieldHintText(text="Test Name"),
            mode="outlined",
            size_hint=(0.7, None),
            height=dp(64),
            font_style="Title",
            font_size='48sp'
        )

        start_button = MDButton(
            MDButtonIcon(
                icon="check", 
                #font_style="Title", 
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)),
            MDButtonText(
                text="Start", 
                font_style="Title", 
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)),
            style="elevated",
            size_hint=(0.25, None),
            height=dp(64),
            theme_bg_color="Custom",  # Use custom color
            md_bg_color=(0.1, 0.4, 0.8, 1)
        )
        start_button.bind(on_release=self.on_start_test)

        input_row.add_widget(self.test_name_input)
        input_row.add_widget(start_button)

        help_label = MDLabel(
            text="Need Help?",
            theme_text_color="Custom",
            text_color=(0.16, 0.30, 0.62, 1),
            halign="center",
            size_hint=(1, None),
            height=dp(10),
            font_size="20sp"
        )

        instructions_layout = AnchorLayout(size_hint=(1, None), height=dp(72))
        instructions_button = MDButton(
            MDButtonText(text="View Instructions"),
            style="elevated",
            size_hint=(None, None),
            size=(dp(260), dp(52))
        )
        instructions_button.bind(on_release=self.on_view_instructions)
        instructions_layout.add_widget(instructions_button)

        mainContent.add_widget(title)
        mainContent.add_widget(input_row)
        mainContent.add_widget(help_label)
        mainContent.add_widget(instructions_layout)

        

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

    def on_start_test(self, *args):
        name = self.test_name_input.text.strip()
        if not name:
            print("Please enter a test name before starting.")
            return
        print(f"Starting test: {name}")

    def on_view_instructions(self, *args):
        slides = self._build_instruction_slides()

        if getattr(self, "instruction_overlay", None) and self.instruction_overlay.parent:
            self.remove_widget(self.instruction_overlay)

        self.instruction_overlay = MultiStepInstructionOverlay(
            instructions=slides,
            on_close=self._dismiss_instruction_overlay,
        )
        self.add_widget(self.instruction_overlay)

    # --- Instruction overlay helpers ---
    def _dismiss_instruction_overlay(self, *args):
        if getattr(self, "instruction_overlay", None) and self.instruction_overlay.parent:
            self.remove_widget(self.instruction_overlay)
        self.instruction_overlay = None

    def _build_instruction_slides(self):
        """
        Returns the list of instruction panels shown in the multi-step overlay.
        Add/update steps here; image paths are optional.
        """
        return [
            InstructionPanel(
                title="Introduction",
                body="Have the sample collection kit and POCT device ready.\n1. Swab\n2. Tube A\n3. Tube B\n4. Tube C\n5. POCT Device",
                image=None,
            ),
            InstructionPanel(
                title="Step 1. Preparation",
                body="Make sure to rinse your mouth with water before proceeding.\n\nRemove the Swab from its package. ",
                image=None,
            ),
            InstructionPanel(
                title="Step 2. Mouth Swab",
                body="Insert the Swab into your mouth, and firmly brush the Swab on top of your tongue up and down for 30 seconds.",
                image=None,
            ),
        ]
