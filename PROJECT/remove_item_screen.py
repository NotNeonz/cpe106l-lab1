from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from database import insert_order

class RemoveItemFromOrder(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orders = []

        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.title = MDLabel(text="Remove Item", halign="center", font_style="H5")
        self.layout.add_widget(self.title)

        self.scroll = ScrollView()
        self.list_view = MDList()
        self.scroll.add_widget(self.list_view)

        self.layout.add_widget(self.scroll)


        self.complete_order_button = MDRaisedButton(
            text="Complete Order",
            pos_hint={"center_x": 0.5},
            md_bg_color=(0.2, 0.6, 0.2, 1),
            on_release=self.submit_order
        )

        self.return_button = MDRaisedButton(
            text="Back",
            pos_hint={"center_x": 0.5},
            on_release=self.return_to_main
        )

        self.layout.add_widget(self.complete_order_button)
        self.layout.add_widget(self.return_button)
        self.add_widget(self.layout)

    def submit_order(self, instance):
        if not self.orders:
            dialog = MDDialog(
                title="Error",
                text="No orders to submit.",
                buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
            )
            dialog.open()
            return

        for item in self.orders:
            item_name = item['name']

            price_str = item['price'].replace('₱', '').strip()
            try:
                price = float(price_str)
            except ValueError:
                print(f"Invalid price format: {item['price']}")
                continue

            insert_order(item_name, price)

        dialog = MDDialog(
            title="Success",
            text="Order submitted successfully!",
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

        self.orders.clear()
        self.update_order_list()

        self.manager.current = "submit_order"

    def set_orders(self, orders):
        self.orders = orders
        self.update_order_summary()

    def update_order_summary(self):
        self.list_view.clear_widgets()
        for item in self.orders:
            order_item = OneLineListItem(
                text=f"{item['name']} - {item['price']}",
                on_release=lambda x, i=item: self.remove_selected_item(i)
            )
            self.list_view.add_widget(order_item)

    def remove_selected_item(self, item):
        if item in self.orders:
            self.orders.remove(item)
            self.update_order_summary()

            order_summary_screen = self.manager.get_screen('order_summary')
            if hasattr(order_summary_screen, 'update_order_summary_from_remove'):
                order_summary_screen.update_order_summary_from_remove(self.orders)

    def return_to_summary(self, instance):
        self.manager.current = 'order_summary'

    def return_to_main(self, instance):
        order_summary_screen = self.manager.get_screen("order_summary")
        order_summary_screen.update_order_summary_from_remove(self.orders)

        self.manager.current = "main"
