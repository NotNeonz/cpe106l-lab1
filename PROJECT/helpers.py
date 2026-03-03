admin_helper = """ 
BoxLayout:
    orientation: 'vertical'
    spacing: dp(5)
    size_hint_y: None
    height: self.minimum_height
    pos_hint: {'center_x': 0.5, 'center_y': 0.4}
    size_hint_x: None
    width: 300

    MDTextField:
        id: username
        hint_text: "Enter username"
        helper_text: "Welcome Admin!"
        helper_text_mode: "on_focus"
        icon_right: "food-fork-drink"
        icon_right_color: app.theme_cls.primary_color
        size_hint_x: 1

    MDTextField:
        id: password
        hint_text: 'Enter Password'
        password: True
        required: True
        helper_text_mode: 'on_focus'
        helper_text: 'Please, enter Your Password.'
        size_hint_x: 1
        line_color_focus: app.theme_cls.primary_color
        current_hint_text_color: app.theme_cls.primary_color
"""

customer_helper = """ 
BoxLayout:
    orientation: 'vertical'
    spacing: dp(10)
    size_hint_y: None
    height: self.minimum_height
    pos_hint: {'center_x': 0.5, 'center_y': 0.4}
    size_hint_x: None
    width: 300

    MDTextField:
        id: username
        hint_text: "Enter username"
        helper_text: "Welcome Customer!"
        helper_text_mode: "on_focus"
        icon_right: "food-fork-drink"
        icon_right_color: app.theme_cls.primary_color
        size_hint_x: 1
"""
