from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp

from database import fetch_orders, update_order_status, delete_order, clear_all_orders, clear_completed_orders


class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orders = []

        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.title = MDLabel(text="Admin Dashboard", halign="center", font_style="H5")
        self.layout.add_widget(self.title)

        self.scroll = ScrollView()
        self.list_view = MDList()
        self.scroll.add_widget(self.list_view)
        self.layout.add_widget(self.scroll)

        self.refresh_button = MDRaisedButton(
            text="Refresh Orders",
            pos_hint={"center_x": 0.5},
            on_release=self.load_orders
        )

        self.return_button = MDRaisedButton(
            text="Return to Main Menu",
            pos_hint={"center_x": 0.5},
            on_release=self.return_to_role_select
        )

        self.clear_completed_button = MDRaisedButton(
            text="Clear Completed Orders",
            pos_hint={"center_x": 0.5},
            md_bg_color=(1, 0.6, 0, 1),
            on_release=self.confirm_clear_completed
        )

        self.clear_all_button = MDRaisedButton(
            text="Clear ALL Orders (Reset)",
            pos_hint={"center_x": 0.5},
            md_bg_color=(1, 0, 0, 1),
            on_release=self.confirm_clear_all
        )

        self.layout.add_widget(self.refresh_button)
        self.layout.add_widget(self.return_button)
        self.layout.add_widget(self.clear_completed_button)
        self.layout.add_widget(self.clear_all_button)

        self.add_widget(self.layout)

    def on_pre_enter(self, *args):
        self.load_orders()

    def load_orders(self, *args):
        self.list_view.clear_widgets()
        self.orders = fetch_orders()

        if not self.orders:
            self.list_view.add_widget(OneLineListItem(text="No orders found."))
            return

        for order in self.orders:
            order_text = f"{order['customer_name']} - {order['item_name']} - ₱{order['price']} ({order['status']})"
            order_item = OneLineListItem(
                text=order_text,
                on_release=lambda x, o=order: self.show_order_options(o)
            )
            self.list_view.add_widget(order_item)

    def show_order_options(self, order):
        dialog = MDDialog(
            title="Order Options",
            text=f"Customer: {order['customer_name']}\nItem: {order['item_name']}\nStatus: {order['status']}",
            buttons=[
                MDRaisedButton(text="Mark as Completed",
                               on_release=lambda x: self.mark_as_completed(order, dialog)),
                MDRaisedButton(text="Remove Order",
                               md_bg_color=(1, 0, 0, 1),
                               on_release=lambda x: self.remove_order(order, dialog)),
                MDRaisedButton(text="Cancel", on_release=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()

    def mark_as_completed(self, order, dialog):
        update_order_status(order['order_id'], "Completed")
        dialog.dismiss()
        self.load_orders()

    def remove_order(self, order, dialog):
        delete_order(order['order_id'])
        dialog.dismiss()
        self.load_orders()

    def return_to_role_select(self, *args):
        app = MDApp.get_running_app()
        app.init_main_screen()
        app.screen_manager.current = "main"

    def confirm_clear_completed(self, *args):
        confirm = MDDialog(
            title="Confirm",
            text="Clear ALL completed orders? This cannot be undone.",
            buttons=[
                MDRaisedButton(text="Cancel", on_release=lambda x: confirm.dismiss()),
                MDRaisedButton(text="Clear", md_bg_color=(1, 0, 0, 1),
                               on_release=lambda x: self.clear_completed(confirm)),
            ]
        )
        confirm.open()

    def clear_completed(self, dialog):
        clear_completed_orders()
        dialog.dismiss()
        self.load_orders()

    def confirm_clear_all(self, *args):
    # 1) Ask for admin password first
        self.reset_pw_field = MDTextField(
            hint_text="Enter admin password",
            password=True,
            helper_text="Required to reset ALL orders",
            helper_text_mode="on_focus",
            size_hint_x=1
        )

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=(dp(8), dp(8), dp(8), dp(8)),
            size_hint_y=None,
            height=dp(90)
        )
        content.add_widget(self.reset_pw_field)

        pw_dialog = MDDialog(
            title="Admin Verification",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(text="Cancel", on_release=lambda x: pw_dialog.dismiss()),
                MDRaisedButton(
                    text="Verify",
                    md_bg_color=(0.2, 0.6, 0.2, 1),
                    on_release=lambda x: self._verify_reset_password(pw_dialog)
                ),
            ]
        )
        pw_dialog.open()

    def _verify_reset_password(self, pw_dialog):
        # Use the SAME password as your admin login
        if self.reset_pw_field.text == "root123":
            pw_dialog.dismiss()
            self._open_final_reset_confirm()
        else:
            # show inline error on the field
            self.reset_pw_field.error = True
            self.reset_pw_field.helper_text = "Wrong password"
            self.reset_pw_field.helper_text_mode = "persistent"


    def _open_final_reset_confirm(self):
        confirm = MDDialog(
            title="CONFIRM RESET",
            text="Clear ALL orders (including pending)? This cannot be undone.",
            buttons=[
                MDRaisedButton(text="Cancel", on_release=lambda x: confirm.dismiss()),
                MDRaisedButton(
                    text="RESET",
                    md_bg_color=(1, 0, 0, 1),
                    on_release=lambda x: self.clear_all(confirm)
                ),
            ]
        )
        confirm.open()

    def clear_all(self, dialog):
        clear_all_orders()
        dialog.dismiss()
        self.load_orders()