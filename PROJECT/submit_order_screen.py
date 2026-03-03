from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel

class SubmitOrderScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orders = []  # Store orders

        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.title = MDLabel(text="Submit Order", halign="center", font_style="H5")
        self.layout.add_widget(self.title)

        self.scroll = ScrollView()
        self.list_view = MDList()
        self.scroll.add_widget(self.list_view)
        self.layout.add_widget(self.scroll)

        self.confirm_button = MDRaisedButton(
            text="Confirm Order",
            pos_hint={"center_x": 0.5},
            md_bg_color=(0.2, 0.6, 0.2, 1),
            on_release=self.confirm_order
        )

        self.return_button = MDRaisedButton(
            text="Back",
            pos_hint={"center_x": 0.5},
            on_release=self.return_to_main
        )

        self.layout.add_widget(self.confirm_button)
        self.layout.add_widget(self.return_button)
        self.add_widget(self.layout)

    def set_orders(self, orders):
        self.orders = orders
        self.update_order_list()

    def update_order_list(self):
        self.list_view.clear_widgets()
        for item in self.orders:
            order_item = OneLineListItem(text=f"{item['name']} - {item['price']}")
            self.list_view.add_widget(order_item)

    def confirm_order(self, instance):
        dialog = MDDialog(
            title="Order Confirmation",
            text="Order submitted successfully!",
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

    def return_to_main(self, instance):
        self.manager.current = "main"
