from kivymd.uix.screen import MDScreen
from kivy.core.window import Window

from mdWidgets import (
    uni_lowerContainer,
    uni_upperContainer,
    uni_backButton,
    uni_homeButton,
    uni_folderContainer,
    build_test_results_tab,
    build_result_details_tab,
    build_export_tab,
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
            ("Test Results", build_test_results_tab("Project Name", "20XX-XX-XX", "high tolerance")),
            ("Result Details", build_result_details_tab("high tolerance")),
            ("Export", build_export_tab()),
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

    