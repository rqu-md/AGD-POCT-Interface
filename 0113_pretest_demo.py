#!/usr/bin/env python3
"""
PreTestScreen Standalone Demo - Educational Version
Purpose: Demonstrate form input and confirmation dialog pattern

Key Learning Topics:
1. MDTextField - text input with icons and hints
2. MDDialog - confirmation dialogs
3. FloatLayout positioning - all components use pos_hint
4. Form validation pattern
5. User input handling
"""

from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import (
    Color,
    RoundedRectangle,
    StencilPush,
    StencilPop,
    StencilUse,
    Ellipse
)
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldLeadingIcon, MDTextFieldHintText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogContentContainer,
    MDDialogButtonContainer
)
from datetime import datetime

# ============================================================================
# uni_backButton - Robert's Back Button
# ============================================================================

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


# ============================================================================
# uni_homeButton - Robert's Home Button
# ============================================================================

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

class PreTestScreen(MDScreen):
    """
    Pre-Test Screen - Test preparation interface
    
    Main Features:
    - Text input for project name
    - Instruction button
    - Start confirmation dialog
    - Real-time date/time display
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Flag variable for dialog control
        self.show_stop_dialog = False
        
        # Set background color
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        
        # ========== Top Navigation Buttons ==========
        
        # Back button (top left)
        # back_button = MDButton(
        #     MDButtonIcon(icon="arrow-left"),
        #     MDButtonText(text="Back", font_style="Title"),
        #     style="elevated",
        #     size_hint=(None, None),
        #     size=(dp(100), dp(40)),
        #     pos_hint={"x": 0.02, "top": 0.98},
        #     on_release=self.on_back_clicked
        # )
        # self.add_widget(back_button)

        # Back button (top left) - Robert's button
        back_button = uni_backButton()
        back_button.size_hint = (None, None)
        back_button.size = (dp(80), dp(50))
        # back_button.pos_hint = {"x": 0.02, "top": 0.98}
        back_button.pos_hint = {"x": 0.02, "y": 0.02}
        self.add_widget(back_button)
        
        # Home button (top right)
        # home_button = MDButton(
        #     MDButtonIcon(icon="home"),
        #     MDButtonText(text="Home", font_style="Title"),
        #     style="elevated",
        #     size_hint=(None, None),
        #     size=(dp(100), dp(40)),
        #     pos_hint={"right": 0.98, "top": 0.98},
        #     on_release=self.on_home_clicked
        # )
        # self.add_widget(home_button)

        # Home button (top right) - Robert's button
        home_button = uni_homeButton()
        home_button.size_hint = (None, None)
        home_button.size = (dp(80), dp(50))
        #home_button.pos_hint = {"right": 0.98, "top": 0.98}
        home_button.pos_hint = {"center_x": 0.15, "y": 0.02}
        home_button.on_home_clicked = lambda *args: self.show_home_confirm_dialog(home_button)
        self.add_widget(home_button)
        
        # ========== Center Instruction Card ==========
        
        # ========== Title Card (top center) ==========

        title_card = MDCard(
            style="elevated",
            size_hint=(None, None),
            size=(dp(400), dp(60)),
            radius=[dp(16)],
            elevation=4,
            pos_hint={"center_x": 0.5, "center_y": 0.92}  # 顶部居中
        )

        title_label = MDLabel(
            text="Test",
            font_style="Title",
            halign="center"
        )
        title_card.add_widget(title_label)
        self.add_widget(title_card)

        # Large card (90% x 60% of screen)
        instr_card = MDCard(
            size_hint=(0.9, 0.6),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            radius=[12],
            padding=dp(8),
            style="elevated"
        )
        
        # Instruction button (inside card, bottom right)
        instr_button = MDButton(
            MDButtonIcon(icon="information"),
            MDButtonText(text="Instruction", font_style="Title"),
            style="elevated",
            size_hint=(None, None),
            size=(dp(180), dp(60)),
            pos_hint={"center_x": 0.9, "center_y": 0.1},
            on_release=self.on_instruction_clicked
        )
        instr_card.add_widget(instr_button)
        
        self.add_widget(instr_card)
        
        # ========== Input Field ==========
        
        # Text field for project name
        self.name_field = MDTextField(
            MDTextFieldLeadingIcon(icon="account"),
            MDTextFieldHintText(text="Input Name"),
            mode="outlined",
            size_hint_x=None,
            width=dp(240),
            pos_hint={"center_x": 0.5, "center_y": 0.65}
        )
        self.add_widget(self.name_field)
        
        # ========== Start Button ==========
        
        # Start button (right of input field)
        start_button = MDButton(
            MDButtonIcon(icon="check"),
            MDButtonText(text="Start", font_style="Title"),
            style="elevated",
            size_hint=(None, None),
            size=(dp(100), dp(50)),
            pos_hint={"center_x": 0.8, "center_y": 0.65},
            on_release=self.show_start_confirm_dialog
        )
        self.add_widget(start_button)
        
        # ========== Bottom Status Bar ==========
        
        # Date card (bottom left)
        self.date_card = MDCard(
            size_hint=(None, None),
            size=(dp(140), dp(40)),
            pos_hint={"center_x": 0.4, "y": 0.02},
            radius=[20],
            elevation=0,
            md_bg_color=(0.9, 0.9, 0.9, 1)
        )
        self.date_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=self.theme_cls.primaryColor
        )
        self.date_card.add_widget(self.date_label)
        self.add_widget(self.date_card)
        
        # Time card (bottom right)
        self.time_card = MDCard(
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            pos_hint={"center_x": 0.6, "y": 0.02},
            radius=[20],
            elevation=0,
            md_bg_color=(0.9, 0.9, 0.9, 1)
        )
        self.time_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=self.theme_cls.primaryColor
        )
        self.time_card.add_widget(self.time_label)
        self.add_widget(self.time_card)
        
        # ========== Start Timer ==========
        Clock.schedule_interval(self.update_time, 1)
        self.update_time(0)
    
    def on_back_clicked(self, *args):
        """Back button click handler"""
        print("⬅️  Back button clicked")
    
    def on_home_clicked(self, *args):
        """Home button click handler"""
        print("🏠 Home button clicked")

    def show_home_confirm_dialog(self, instance = None):
        """Display a confirmation dialog to avoid accidental home navigation."""
        self.home_dialog = MDDialog(
            MDDialogIcon(icon="alert-circle-outline"),
            MDDialogHeadlineText(text="Are you sure you want to go home? Current project will be discarded."),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="Cancel"),
                    style="text",
                    on_release=lambda x: self.home_dialog.dismiss(),
                ),
                MDButton(
                    MDButtonText(text="Confirm"), 
                    style="text",
                    on_release=self.confirm_home_action,
                ),
                spacing="8dp",
            ),
        )
        self.home_dialog.open()

    def confirm_home_action(self, instance):
        """Execute home action after confirmation"""
        self.home_dialog.dismiss()
        print("🏠 Home confirmed - returning to home screen")
        # TODO: Add actual navigation to home screen    
    
    def on_instruction_clicked(self, *args):
        """Instruction button click handler"""
        print("ℹ️  Instruction button clicked")
    
    def show_start_confirm_dialog(self, *args):
        """
        Show confirmation dialog before starting test
        
        This demonstrates:
        - MDDialog creation
        - User input validation
        - Confirmation pattern (prevent accidental actions)
        """
        
        # Get project name from input field
        project_name = self.name_field.text.strip()
        
        # Simple validation
        if not project_name:
            # Show error dialog if name is empty
            error_dialog = MDDialog(
                MDDialogIcon(icon="alert-circle-outline"),
                MDDialogHeadlineText(text="Input Required"),
                MDDialogContentContainer(
                    MDLabel(
                        text="Please enter a project name before starting.",
                        halign="center"
                    ),
                    orientation="vertical",
                ),
                MDDialogButtonContainer(
                    MDButton(
                        MDButtonText(text="OK"),
                        style="text",
                        on_release=lambda x: error_dialog.dismiss()
                    ),
                    spacing="8dp",
                ),
            )
            error_dialog.open()
            return
        
        # Show confirmation dialog
        confirm_dialog = MDDialog(
            MDDialogIcon(icon="alert-circle-outline"),
            MDDialogHeadlineText(text="Start Test Confirmation"),
            MDDialogContentContainer(
                MDLabel(
                    text=f"Make sure the sample is loaded and\nthe device lid is closed properly!\n\nProject: {project_name}",
                    halign="center"
                ),
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="Cancel"),
                    style="text",
                    on_release=lambda x: confirm_dialog.dismiss()
                ),
                MDButton(
                    MDButtonText(text="Confirm"),
                    style="text",
                    on_release=lambda x: self.confirm_start_action(confirm_dialog, project_name)
                ),
                spacing="8dp",
            ),
        )
        confirm_dialog.open()
    
    def confirm_start_action(self, dialog, project_name):
        """
        Execute start action after user confirms
        
        In real application, this would:
        - Navigate to motor control screen
        - Pass project name to next screen
        - Initialize hardware
        """
        dialog.dismiss()
        
        print(f"✅ Test started!")
        print(f"   Project Name: {project_name}")
        print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Clear input field after starting
        self.name_field.text = ""
    
    def update_time(self, dt):
        """
        Update date and time display
        
        Parameters:
            dt: Time interval from Clock (required)
        """
        now = datetime.now()
        
        # Format date: Dec 29, 2025
        self.date_label.text = now.strftime("%b %d, %Y")
        
        # Format time: 2:30 PM
        try:
            self.time_label.text = now.strftime("%-I:%M %p")
        except ValueError:
            # Windows uses %#I instead of %-I
            self.time_label.text = now.strftime("%#I:%M %p")


class DemoApp(MDApp):
    """Demo Application Main Class"""
    
    def build(self):
        """Build application"""
        # Create Screen Manager
        sm = MDScreenManager()
        
        # Add PreTestScreen
        pretest_screen = PreTestScreen(name="pretest")
        sm.add_widget(pretest_screen)
        
        # Set initial screen
        sm.current = "pretest"
        
        return sm
    
    def on_start(self):
        """Callback when application starts"""
        print("\n" + "="*70)
        print("🎓 PreTestScreen Educational Demo")
        print("="*70)
        print("\n📚 Key Learning Points:")
        print("  1. MDTextField - Text input with icons and hints")
        print("  2. MDDialog - Confirmation dialog pattern")
        print("  3. FloatLayout positioning - pos_hint for all components")
        print("  4. Input validation - Check before processing")
        print("  5. User feedback - Show appropriate messages")
        print("\n💡 UI Components:")
        print("  - Large center card (90% x 60%)")
        print("  - Text input field with icon")
        print("  - Start button with confirmation")
        print("  - Bottom status bar (date + time)")
        print("\n🎨 Dialog Types Demonstrated:")
        print("  - Error dialog (when input is empty)")
        print("  - Confirmation dialog (before starting)")
        print("\n🔧 Try these actions:")
        print("  1. Click Start without entering a name (see error dialog)")
        print("  2. Enter a name and click Start (see confirmation)")
        print("  3. Click Confirm to simulate starting the test")
        print("  4. Click Back, Home, or Instruction buttons")
        print("="*70 + "\n")


if __name__ == "__main__":
    DemoApp().run()
