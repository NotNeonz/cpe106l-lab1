from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.list import ThreeLineAvatarIconListItem, ImageLeftWidget, MDList
from kivymd.uix.button import MDRaisedButton
from kivy.uix.scrollview import ScrollView
from menu import Menu
import os

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = Menu()

        logo_filename = "QELogo.jpg"
        logo_path = os.path.join(os.path.dirname(__file__), "Image", logo_filename)

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        logo = Image(source=logo_path, size_hint=(1, 0.2), allow_stretch=False, keep_ratio=False)
        main_layout.add_widget(logo)

        menu_container = AnchorLayout(size_hint=(1, 0.6))
        menu_box = BoxLayout(orientation='vertical', size_hint=(0.9, 0.9), height=400, pos_hint={'center_y': 0.8})

        scroll = ScrollView()
        self.list_view = MDList()
        scroll.add_widget(self.list_view)

        self.populate_menu()

        menu_box.add_widget(scroll)
        menu_container.add_widget(menu_box)

        return_button = MDRaisedButton(
            text='Return',
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'center_x': 0.5},
            on_release=self.return_to_main,
            md_bg_color='white',
            text_color=(0.5, 0.25, 0, 1)
        )

        main_layout.add_widget(menu_container)
        main_layout.add_widget(return_button)
        self.add_widget(main_layout)

    def populate_menu(self):
        self.list_view.clear_widgets()
        for item in self.menu.get_menu_items():
            item_image_path = os.path.join(os.path.dirname(__file__), "Image", item["image_filename"])
            item_image = ImageLeftWidget(source=item_image_path)
            menu_item = ThreeLineAvatarIconListItem(
                text=item["name"],
                secondary_text=f"Price: {item['price']}",
                tertiary_text=f"Tag: {item['tag']}",
                on_release=lambda x, i=item: self.on_item_select(i)
            )
            menu_item.add_widget(item_image)
            self.list_view.add_widget(menu_item)

    def on_item_select(self, item):
        selected_screen = self.manager.get_screen("selected_item")
        selected_screen.update_item(item)
        self.manager.current = "selected_item"

    def return_to_main(self, instance):
        self.manager.current = 'main'
