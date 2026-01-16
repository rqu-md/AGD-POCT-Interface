
##Using mdWidgets.py##

All the components can be found in mdWidgets.py. They can be organized between **universal widgets** that are used repeatedly and necessary on all pages, and **unique components** which are often unique to one specific page.

##Universal Widgets##

Universal widgets are any components that are used frequently on multiple different pages. The main structure of all the pages are dependent on majority of the components in this category.

These components are:

uni_upperContainer - Upper header
uni_centerBox - Main container
uni_lowerContainer - Lower footer
uni_backButton - Back button
uni_homeButton - Home button

##uni_upperContainer##

This is a header container for the top of the page. It includes a center title location and two smaller containers to the right and left for other widgets.

##uni_centerBox

This is the main container. Any contents (text, text fields, loading bars, lists, etc) should be in this container.

##uni_lowerContainer

This is the footer container. It stays at the bottom of the page, and has a clock in the center by default. The `left_box` container is for the nav buttons (back and home), but they may not always be present (ex: test screen)

##uni_backButton##

This is the universal back button for pages. It is intended to be in `left_box` in `uni_lowerContainer`.

##uni_homeButton##

This is the universal home button for pages. It is intended to be in `left_box` in `uni_lowerContainer`.

Example Usage (Nav buttons in the footer)

```
bottom = uni_lowerContainer( 
    size_hint=(1, None),
    pos_hint={'x': 0, 'y': 0}
)

bottom.left_box.add_widget(uni_backButton())
bottom.left_box.add_widget(uni_homeButton())

bottom.width = Window.width
self.add_widget(bottom)
```


Classes

`InstructionPanel`

Data object for a single slide.
* Fields
    * `title` (str): heading for the left panel.
    * `body` (str): body text for the left panel.
    * `image` (str | None): image path for the right panel; if None, the right panel shows a placeholder with the title.

`InstructionNavButton`

Clickable navigation control used by the overlay.
* Purpose: Provides left/right navigation buttons with a ripple effect.
* Key behavior
    * `direction` (“left” | “right”) controls which arrow image is used.
    * Uses `assets/LNav.png` and `assets/RNav.png`.
    * Grays out when disabled=True.
    * Ripple feedback on tap.

You normally don’t instantiate this directly; `MultiStepInstructionOverlay` creates and wires them.

`OverlayCloseButton`

Top-left circular close button.
* Purpose: Dismisses the overlay when tapped.
* Key behavior
    * Uses assets/x.png for the icon.
    * Ripple effect on tap.
    * Click handler is wired by `MultiStepInstructionOverlay`.

`MultiStepInstructionOverlay`

Fullscreen overlay that renders the instruction flow.
* Constructor
    * `instructions`: list of `InstructionPanel` objects.
    * `on_close`: optional callback invoked when the overlay closes.
* Behavior
    * Dims the background.
    * Two square panels: left text panel, right image panel.
    * Navigation via left/right buttons and swipe gestures.
    * Tap outside the content dismisses the overlay.
    * Slide content fades out/in on page change (containers remain static).
* Useful methods
    * `set_instructions(instructions)`: replace slides and reset to the first step.
    * `next_slide()`, `previous_slide()`: manual navigation.
    * `close_overlay()`: dismiss programmatically.

Usage Example
```
from mdWidgets import InstructionPanel, MultiStepInstructionOverlay

steps = [
    InstructionPanel(
        title="Introduction",
        body="Have the sample kit ready.\n1. Swab\n2. Tube A\n3. Tube B\n4. Tube C\n5. POCT Device",
        image=None,
    ),
    InstructionPanel(
        title="Step 2",
        body="Add your step details here.",
        image="assets/step2.png",
    ),
]

overlay = MultiStepInstructionOverlay(
    instructions=steps,
    on_close=lambda: print("Overlay closed"),
)

root_widget.add_widget(overlay)
```


Notes
* Assets: Ensure `assets/LNav.png`, `assets/RNav.png`, and `assets/x.png` exist.
* Swipe: Horizontal swipe over the content area switches slides.
* Dismiss: Tap outside the panels or use the X button.
