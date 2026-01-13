
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

##uni_centerBox##

This is the main container. Any contents (text, text fields, loading bars, lists, etc) should be in this container.

##uni_lowerContainer##

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