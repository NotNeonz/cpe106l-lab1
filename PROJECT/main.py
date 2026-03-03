# main.py
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDRaisedButton
from kivy.graphics import Rectangle, Color
import os

from instructionscrap import create_instructions2
from helpers import customer_helper, admin_helper
from menu_module import MenuScreen
from selected_item_screen import SelectedItemScreen
from order_summary_screen import OrderSummaryScreen
from remove_item_screen import RemoveItemFromOrder
from submit_order_screen import SubmitOrderScreen
from billing_screen import BillingScreen
from admin_screen import AdminScreen
from database import generate_customer_id


class QuickEatsApp(MDApp):
    def build(self):
        self.screen_manager = ScreenManager()

        # Screens
        self.main_screen = Screen(name="main")      # role select OR customer home (instructions)
        self.login_screen = Screen(name="login")    # login form
        self.menu_screen = MenuScreen(name="menu")
        self.selected_item_screen = SelectedItemScreen(name="selected_item")
        self.order_summary_screen = OrderSummaryScreen(name="order_summary")
        self.remove_item_screen = RemoveItemFromOrder(name="remove_item")
        self.submit_order_screen = SubmitOrderScreen(name="submit_order")
        self.billing_screen = BillingScreen(name="billing")
        self.admin_screen = AdminScreen(name="admin")

        # Add screens
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.add_widget(self.menu_screen)
        self.screen_manager.add_widget(self.selected_item_screen)
        self.screen_manager.add_widget(self.order_summary_screen)
        self.screen_manager.add_widget(self.remove_item_screen)
        self.screen_manager.add_widget(self.submit_order_screen)
        self.screen_manager.add_widget(self.billing_screen)
        self.screen_manager.add_widget(self.admin_screen)

        self.init_main_screen()
        return self.screen_manager

    # ----------------------------
    # MAIN ROLE SELECT SCREEN
    # ----------------------------
    def init_main_screen(self):
        self.main_screen.clear_widgets()

        # Create background once (don't clear canvas.before repeatedly)
        if not hasattr(self, "rect"):
            with self.main_screen.canvas.before:
                Color(1, 1, 1, 0.3)
                self.rect = Rectangle(size=self.main_screen.size, pos=self.main_screen.pos)
            self.main_screen.bind(size=self._update_rect, pos=self._update_rect)

        top_box = RelativeLayout(size_hint=(1, 0.2), pos_hint={'center_x': 0.5, 'top': 1})

        base_dir = os.path.dirname(__file__)
        image_dir = os.path.join(base_dir, "Image")
        logo_path = os.path.join(image_dir, "QELogo.jpg")

        logo = Image(
            source=logo_path,
            size_hint=(None, None),
            size=(300, 300),
            pos_hint={'center_x': 0.5, 'center_y': 0}
        )
        top_box.add_widget(logo)

        button_box = FloatLayout(size_hint=(1, 0.4), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        admin_button = MDRaisedButton(
            text='Enter Admin',
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            on_release=self.enter_admin_role,
            theme_text_color="Custom",
            md_bg_color='white',
            text_color=(0.5, 0.25, 0, 1)
        )
        customer_button = MDRaisedButton(
            text='Enter Customer',
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            on_release=self.enter_customer_role,
            theme_text_color="Custom",
            md_bg_color='white',
            text_color=(0.5, 0.25, 0, 1)
        )

        button_box.add_widget(admin_button)
        button_box.add_widget(customer_button)

        self.main_screen.add_widget(top_box)
        self.main_screen.add_widget(button_box)

        self.screen_manager.current = "main"

    def _update_rect(self, *args):
        self.rect.pos = self.main_screen.pos
        self.rect.size = self.main_screen.size

    # ----------------------------
    # LOGIN SCREEN (ADMIN/CUSTOMER)
    # ----------------------------
    def enter_admin_role(self, obj):
        self.open_login("admin")

    def enter_customer_role(self, obj):
        self.open_login("customer")

    def open_login(self, role):
        self.login_screen.clear_widgets()
        root = FloatLayout()

        if role == 'admin':
            self.username_layout = Builder.load_string(admin_helper)
        else:
            self.username_layout = Builder.load_string(customer_helper)

        self.username_layout.pos_hint = {"center_x": 0.5, "center_y": 0.55}

        login_btn = MDRaisedButton(
            text='Log in',
            size_hint=(None, None),
            size=(160, 48),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            on_release=lambda x: self.show_data(x, role=role),
            theme_text_color="Custom",
            md_bg_color='white',
            text_color=(0.2, 0.1, 0, 1),
        )

        root.add_widget(self.username_layout)
        root.add_widget(login_btn)

        # ✅ Return button ONLY for admin login
        if role == "admin":
            return_btn = MDRaisedButton(
                text='Return',
                size_hint=(None, None),
                size=(160, 48),
                pos_hint={'center_x': 0.5, 'center_y': 0.15},
                on_release=self.back_to_role_select,
                theme_text_color="Custom",
                md_bg_color='white',
                text_color=(0.2, 0.1, 0, 1),
            )
            root.add_widget(return_btn)

        self.login_screen.add_widget(root)
        self.screen_manager.current = "login"

    def back_to_role_select(self, *args):
        self.login_screen.clear_widgets()
        self.init_main_screen()
        self.screen_manager.current = "main"

    # ----------------------------
    # LOGIN VALIDATION
    # ----------------------------
    def show_data(self, obj, role):
        if not (hasattr(self, "username_layout") and hasattr(self.username_layout, "ids")):
            self.show_error_dialog("Login form not loaded properly.")
            return

        username_field = self.username_layout.ids.get("username")
        password_field = self.username_layout.ids.get("password")

        if not username_field:
            self.show_error_dialog('Username field not found!')
            return

        if username_field.text.strip() == "":
            self.show_error_dialog('Please enter a name')
            return

        if role == "admin":
            if not password_field:
                self.show_error_dialog('Password field not found!')
                return
            if password_field.text.strip() == "":
                self.show_error_dialog('Please enter a password')
                return
            if username_field.text != "root" or password_field.text != "root123":
                self.show_error_dialog('Invalid username or password')
                return

        self.show_instructions(role)

    def show_error_dialog(self, message):
        btn = MDRaisedButton(
            text='Continue',
            on_release=self.close_dialog,
            theme_text_color="Custom",
            md_bg_color='white',
            text_color=(0.2, 0.1, 0, 1)
        )
        self.dialog = MDDialog(
            title='Error',
            text=message,
            buttons=[btn],
            background_color=[1, 1, 1, 1]
        )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    # ----------------------------
    # POST-LOGIN ROUTING
    # ----------------------------
    def show_instructions(self, role):
        # clear login UI after success
        self.login_screen.clear_widgets()

        if role == 'admin':
            self.screen_manager.current = 'admin'
            return

        # CUSTOMER HOME (instructions on main screen)
        user_name = self.username_layout.ids.username.text.strip()

        # make sure DB insert uses correct customer name
        self.order_summary_screen.customer_name = user_name

        # optional: customer id (your function currently checks DB; may fail if DB offline)
        try:
            customer_id = generate_customer_id()
        except Exception:
            customer_id = None

        handlers = {
            "S": self.show_menu,
            "P": self.place_order,
            "O": self.order_summary,
            "R": self.remove_item,
            "T": self.submit_order,
            "W": self.request_waiter,
            "logout": self.logout_customer,   # ✅ New Customer / Logout
            "quit": self.quit_program,        # ✅ Quit from customer home
        }

        instructions_layout = create_instructions2(user_name, role, handlers)

        self.main_screen.clear_widgets()
        self.main_screen.add_widget(instructions_layout)
        self.screen_manager.current = "main"

        if customer_id:
            print(f"Customer {user_name} logged in with ID: {customer_id}")
        else:
            print(f"Customer {user_name} logged in (ID not generated).")

    # ----------------------------
    # CUSTOMER ACTIONS
    # ----------------------------
    def show_menu(self, obj):
        self.screen_manager.current = "menu"

    def place_order(self, obj):
        self.screen_manager.current = "menu"

    def order_summary(self, obj):
        if not self.order_summary_screen.orders:
            dialog = MDDialog(
                title="Order Summary",
                text="There are no orders listed.",
                buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
            )
            dialog.open()
        else:
            self.screen_manager.current = "order_summary"

    def remove_item(self, obj):
        self.screen_manager.current = "remove_item"

    def submit_order(self, obj):
        # ✅ FIXED: set_orders returns None, so don't use "if not set_orders(...)"
        if not self.order_summary_screen.orders:
            dialog = MDDialog(
                title="Submit Order",
                text="There are no orders listed.",
                buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
            )
            dialog.open()
            return

        self.submit_order_screen.set_orders(self.order_summary_screen.orders)
        self.screen_manager.current = "submit_order"

    def request_waiter(self, obj):
        self.screen_manager.current = "billing"

    def quit_program(self, obj=None):
        self.stop()

    def logout_customer(self, *args):
        # clear current session orders
        self.order_summary_screen.orders.clear()
        self.remove_item_screen.orders.clear()

        # reset customer name (optional but clean)
        self.order_summary_screen.customer_name = "Guest"

        # go straight back to CUSTOMER login (not role select)
        self.open_login("customer")


if __name__ == "__main__":
    QuickEatsApp().run()