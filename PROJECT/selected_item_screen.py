from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import os

class SelectedItemScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()

        self.image = Image(size_hint=(None, None), size=(300, 300), pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.item_name = MDLabel(text="Item Name", halign="center", font_style="H5", pos_hint={'center_x': 0.5, 'center_y': 0.45})
        self.item_price = MDLabel(text="Price", halign="center", font_style="H6", pos_hint={'center_x': 0.5, 'center_y': 0.35})

        self.layout.add_widget(self.image)
        self.layout.add_widget(self.item_name)
        self.layout.add_widget(self.item_price)

        self.add_order_button = MDRaisedButton(
            text="Add to Order",
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            on_release=self.confirm_add_to_order,
            theme_text_color="Custom",
            md_bg_color='white',
            text_color=(0.5, 0.25, 0, 1)
        )

        self.return_button = MDRaisedButton(
            text="Back to Menu",
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            on_release=self.go_back,
            md_bg_color='white',
            text_color=(0.5, 0.25, 0, 1)
        )

        self.layout.add_widget(self.add_order_button)
        self.layout.add_widget(self.return_button)
        self.add_widget(self.layout)

        self.dialog = None
        self.selected_item = None

    def update_item(self, item):
        self.selected_item = item
        self.item_name.text = item["name"]
        self.item_price.text = f"Price: {item['price']}"
        item_image_path = os.path.join(os.path.dirname(__file__), "Image", item["image_filename"])
        self.image.source = item_image_path

    def confirm_add_to_order(self, instance):
        if not self.selected_item:
            return

        if not self.dialog:
            self.dialog = MDDialog(
                title="Confirm Order",
                text="",  # placeholder, we set real text before open
                buttons=[
                    MDFlatButton(text="Cancel", on_release=self.dismiss_dialog),
                    MDRaisedButton(
                        text="Add",
                        md_bg_color=(0.2, 0.6, 0.2, 1),
                        on_release=self.add_to_order
                    )
                ]
        )

    # ✅ update message every time based on current selected item
        self.dialog.text = f"Do you want to add {self.selected_item['name']} to your order?"
        self.dialog.open()

    def dismiss_dialog(self, instance):
        self.dialog.dismiss()

    def add_to_order(self, instance):
        order_summary_screen = self.manager.get_screen("order_summary")
        order_summary_screen.add_item_to_order(self.selected_item)
        self.dialog.dismiss()

    def go_back(self, instance):
        self.manager.current = "menu"
