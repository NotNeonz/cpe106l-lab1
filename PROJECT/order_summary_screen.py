from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from database import insert_order
from kivymd.app import MDApp

class OrderSummaryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orders = []
        self.customer_name = "Guest"

        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.title = MDLabel(text="Order Summary", halign="center", font_style="H5")
        self.layout.add_widget(self.title)

        self.scroll = ScrollView()
        self.list_view = MDList()
        self.scroll.add_widget(self.list_view)
        self.layout.add_widget(self.scroll)

        self.submit_button = MDRaisedButton(
            text="Submit Order",
            pos_hint={"center_x": 0.5},
            on_release=self.submit_order,
            md_bg_color='white',
            text_color=(0.5, 0.25, 0, 1)
        )

        self.remove_button = MDRaisedButton(
            text="Remove Order",
            pos_hint={"center_x": 0.5},
            on_release=self.remove_order,
            md_bg_color='white',
            text_color=(0.5, 0.25, 0, 1)
        )

        self.return_button = MDRaisedButton(
            text="Back",
            pos_hint={"center_x": 0.5},
            on_release=self.return_to_main,
            md_bg_color='white',
            text_color=(0.5, 0.25, 0, 1)
        )

        self.layout.add_widget(self.submit_button)
        self.layout.add_widget(self.return_button)
        self.layout.add_widget(self.remove_button)
        self.add_widget(self.layout)

    def set_orders(self, orders, customer_name="Guest"):
        self.orders = orders
        self.customer_name = customer_name
        self.update_order_list()

    def add_item_to_order(self, item):
        self.orders.append(item)
        self.update_order_list()

    def update_order_list(self):
        self.list_view.clear_widgets()
        for item in self.orders:
            order_item = OneLineListItem(text=f"{item['name']} - {item['price']}")
            self.list_view.add_widget(order_item)

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
                continue

            insert_order(self.customer_name, item_name, price)

        # clear current session orders
        self.orders.clear()
        self.update_order_list()

        app = MDApp.get_running_app()

        def go_to_customer_login(_btn):
            success_dialog.dismiss()
            # go back to customer login
            app.logout_customer()  # make sure logout_customer opens login("customer")

        success_dialog = MDDialog(
            title="Success",
            text="Order submitted successfully!",
            buttons=[MDRaisedButton(text="OK", on_release=go_to_customer_login)]
        )
        success_dialog.open()

        self.orders.clear()
        self.update_order_list()

        self.manager.current = "submit_order"

    def remove_order(self, instance):
        remove_screen = self.manager.get_screen("remove_item")
        remove_screen.set_orders(self.orders)
        self.manager.current = "remove_item"

    def confirm_remove(self, item_instance):
        item_text = item_instance.text
        for item in self.orders:
            if f"{item['name']} - {item['price']}" == item_text:
                self.orders.remove(item)
                break

        self.update_order_list()

    def update_order_summary_from_remove(self, updated_orders):
        self.orders = updated_orders
        self.update_order_list()

    def return_to_main(self, instance):
        self.manager.current = "main"
