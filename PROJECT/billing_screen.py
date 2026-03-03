from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import os

class BillingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        self.image_path = os.path.join(os.path.dirname(__file__), "Image", "GCashQR.jpg")
        self.qr_image = Image(
            source=self.image_path,
            size_hint=(None, None),
            size=(500, 500),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            opacity=0
        )
        layout.add_widget(self.qr_image)

        self.status_label = MDLabel(
            text="Select a billing option",
            halign="center",
            size_hint=(None, None),
            width=300,
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            font_style="H5"
        )
        layout.add_widget(self.status_label)

        self.button_box = BoxLayout(
            orientation="vertical",
            spacing=20,
            size_hint=(0.8, 0.3),
            pos_hint={"center_x": 0.43, "y": 0.1}
        )

        self.manual_billing_btn = MDRaisedButton(
            text="Manual Billing",
            on_release=self.process_manual_billing
        )
        self.digital_payment_btn = MDRaisedButton(
            text="Digital Payment",
            on_release=self.show_qr_code
        )
        self.return_button = MDRaisedButton(
            text="Return",
            on_release=self.return_to_main
        )

        self.button_box.add_widget(self.manual_billing_btn)
        self.button_box.add_widget(self.digital_payment_btn)
        self.button_box.add_widget(self.return_button)

        layout.add_widget(self.button_box)
        self.add_widget(layout)

    def on_pre_enter(self):
        self.qr_image.opacity = 0
        self.status_label.opacity = 1
        self.status_label.text = "Select a billing option"
        self.status_label.pos_hint = {"center_x": 0.5, "center_y": 0.7}

        self.button_box.clear_widgets()
        self.button_box.add_widget(self.manual_billing_btn)
        self.button_box.add_widget(self.digital_payment_btn)
        self.button_box.add_widget(self.return_button)

    def process_manual_billing(self, instance):
        self.status_label.text = "Manual Billing has been processed, please wait."
        self.qr_image.opacity = 0
        Clock.schedule_once(self.reset_status, 3)

    def show_qr_code(self, instance):
        self.qr_image.opacity = 1
        self.status_label.opacity = 0

        if self.manual_billing_btn in self.button_box.children:
            self.button_box.remove_widget(self.manual_billing_btn)

    def return_to_main(self, instance):
        self.qr_image.opacity = 0 
        self.status_label.opacity = 1
        self.status_label.pos_hint = {"center_x": 0.5, "center_y": 0.7}  # Reset label position

        self.button_box.clear_widgets()
        self.button_box.add_widget(self.manual_billing_btn)
        self.button_box.add_widget(self.digital_payment_btn)
        self.button_box.add_widget(self.return_button)

        self.manager.current = "main"

    def reset_status(self, dt):
        self.status_label.text = "Select a billing option"
