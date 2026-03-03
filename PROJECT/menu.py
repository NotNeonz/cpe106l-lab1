class Menu:
    def __init__(self):
        self.items = [
            {"name": "Classic Cheeseburger", "price": "₱95", "tag": 1, "image_filename": "1.jpg"},
            {"name": "Margherita Pizza", "price": "₱440", "tag": 2, "image_filename": "2.jpg"},
            {"name": "Grilled Chicken Caesar Salad", "price": "₱200", "tag": 3, "image_filename": "3.jpg"},
            {"name": "Spicy Chicken Tacos (3pcs)", "price": "₱140", "tag": 4, "image_filename": "4.jpg"},
            {"name": "Vegetable Stir-Fry", "price": "₱140", "tag": 5, "image_filename": "5.jpg"},
            {"name": "Fish and Chips", "price": "₱120", "tag": 6, "image_filename": "6.jpg"},
            {"name": "Mushroom Risotto", "price": "₱180", "tag": 7, "image_filename": "7.jpg"},
            {"name": "BBQ Pulled Pork Sandwich", "price": "₱120", "tag": 8, "image_filename": "8.jpg"},
            {"name": "Caprese Panini", "price": "₱80", "tag": 9, "image_filename": "9.jpg"},
            {"name": "Chocolate Lava Cake", "price": "₱200", "tag": 10, "image_filename": "10.jpg"},
        ]

    def get_menu_items(self):
        return self.items
