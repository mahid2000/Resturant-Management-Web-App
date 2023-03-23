import re


class MenuItemModel:
    def __init__(self, name, price, category, calories, allergen, image_location):
        self.validate_name(name)
        self.validate_price(price)
        self.validate_calories(calories)

        self.name = name
        self.price = price
        self.category = category
        self.calories = calories
        self.allergens = self.format_allergens(allergen)
        self.image_location = image_location

    @staticmethod
    def validate_name(name):
        if not name:
            raise Exception("Name cannot be left blank")

    @staticmethod
    def validate_price(price):
        if not price:
            raise Exception("Price cannot be left blank.")
        elif not bool(re.match(r'^\d+(\.\d{0,2})?$', price)):
            raise Exception("Price must be a valid decimal number eg. 12.34")

    @staticmethod
    def validate_calories(calories):
        if not calories:
            raise Exception("Calories cannot be left blank.")
        elif not calories.isdigit():
            raise Exception("Calories must be a valid whole number.")

    @staticmethod
    def format_allergens(allergen):
        allergens = ', '.join(allergen)
        return allergens
