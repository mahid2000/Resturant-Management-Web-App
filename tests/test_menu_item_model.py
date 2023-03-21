import unittest
from flaskr.menu_item_model import MenuItemModel


class MyTestCase(unittest.TestCase):

    def test_all_blank(self):
        """Test that an exception is raised if invalid data (All None) is provided to the menu item model."""
        self.assertRaises(Exception, MenuItemModel, (None, None, None, None, None))

    def test_name_blank(self):
        """Test that an exception is raised if an invalid name is provided to the menu item model."""
        self.assertRaises(Exception, MenuItemModel, (None, "12.50", "Mains", "900", None))

    def test_price_blank(self):
        """Test that an exception is raised if an invalid price is provided to the menu item model."""
        self.assertRaises(Exception, MenuItemModel, ("Pie", None, "Mains", "900", None))

    def test_calories_blank(self):
        """Test that an exception is raised if an invalid name is provided to the menu item model."""
        self.assertRaises(Exception, MenuItemModel, ("Pie", 12.50, "Mains", None, None))

    def test_correct_data(self):
        """Test that valid data is assigned in the model correctly."""
        menu_item = MenuItemModel("Pie", "12.50", "Mains", "900", ['E', 'Mi', 'N'])
        self.assertEqual(menu_item.name, "Pie")
        self.assertEqual(menu_item.price, "12.50")
        self.assertEqual(menu_item.category, "Mains")
        self.assertEqual(menu_item.calories, "900")
        self.assertEqual(menu_item.allergens, "E, Mi, N")

    def test_allergen_formatting(self):
        """Test that a list of allergens is formatted into a string correctly."""
        menu_item = MenuItemModel("Pie", "12.50", "Mains", "900", ['E', 'Mi', 'N'])
        self.assertEqual(menu_item.allergens, "E, Mi, N")

    def test_blank_allergen_formatting(self):
        """Test that an empty list of allergens is formatted into an empty string."""
        menu_item = MenuItemModel("Pie", "12.50", "Mains", "900", [])
        self.assertEqual(menu_item.allergens, "")


if __name__ == '__main__':
    unittest.main()
