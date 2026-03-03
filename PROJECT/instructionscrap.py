from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton, MDFlatButton


def create_instructions2(user_name, role, handlers):
    instructions_layout = BoxLayout(
        orientation='vertical',
        padding=10,
        spacing=10,
        size_hint=(None, None),
        size=(400, 400),
        pos_hint={'center_x': 0.5, 'center_y': 0.5}
    )

    #welcome_label = MDLabel(
        #text=f"Welcome to Quick-Eats, {user_name}!",
        #halign = 'center',
        #pos_hint={'center_y':1},
        #theme_text_color="Primary"
    #)
    #instructions_layout.add_widget(welcome_label)

    options = [
        ("Show Menu", "S"),
        ("Order Summary", "O"),
        ("Request Waiter for Manual Billing", "W"),
        ("New Customer", "logout"), 
    ]

    for option_text, option_value in options:
        button = MDFlatButton(
            text=option_text,
            size_hint=(0.8, None),
            height=40,
            pos_hint={'center_x': 0.5},
            on_release=handlers.get(option_value),
            theme_text_color = "Custom",
            md_bg_color = (1, 0, 0, 1),
            text_color = (1, 1, 1, 1)
            )
        instructions_layout.add_widget(button)

    return instructions_layout
