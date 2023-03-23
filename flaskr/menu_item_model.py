import re


class MenuItemModel:
    """Validates, then represents a new menu item."""
    def __init__(self, name, price, category, calories, allergen):
        self.validate_name(name)
        self.validate_price(price)
        self.validate_calories(calories)

        self.name = name
        self.price = price
        self.category = category
        self.calories = calories
        self.allergens = self.format_allergens(allergen)

    @staticmethod
    def validate_name(name):
        """Throws an exception if the item name has been left blank."""
        if not name:
            raise Exception("Name cannot be left blank")

    @staticmethod
    def validate_price(price):
        """Throws an exception if the price is blank, or not a valid integer or decimal to 2 decimal places."""
        if not price:
            raise Exception("Price cannot be left blank.")
        elif not bool(re.match(r'^\d+(\.\d{0,2})?$', price)):
            raise Exception("Price must be a valid decimal number eg. 12.34")

    @staticmethod
    def validate_calories(calories):
        """Throws an exception if the calories are left blank, or are not a valid integer."""
        if not calories:
            raise Exception("Calories cannot be left blank.")
        elif not calories.isdigit():
            raise Exception("Calories must be a valid whole number.")

    @staticmethod
    def format_allergens(allergen):
        """Formats the allergens as comma-separated-values in a string."""
        allergens = ', '.join(allergen)
        return allergens
