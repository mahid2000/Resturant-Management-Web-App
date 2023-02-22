-- Menu Table

-- Mains
INSERT INTO menu (name, price, category, calories, allergens)
VALUES
("Beef Tacos", 12.50, "Mains", 800, "Mi"),
("Pork Tacos", 12.50, "Mains", 800, "Mi"),
("Halloumi Tacos", 10.50, "Mains", 750, "Mi"),
("Chicken Enchiladas", 14.50, "Mains", 900, "G"),
("Pork Enchiladas", 14.50, "Mains", 900, "Mi"),
("Jackfruit Enchiladas", 14.50, "Mains", 900, "Mi");

-- Sides
INSERT INTO menu (name, price, category, calories, allergens)
VALUES
("Plain Nachos", 5.50, "Sides", 350, ""),
("Cheesy Nachos", 6.50, "Sides", 400, "Mi");

-- Desserts
INSERT INTO menu (name, price, category, calories, allergens)
VALUES
("Ice Cream Sundae", 5.50, "Desserts", 300, "Mi"),
("Chocolate Brownie", 5.50, "Desserts", 300, "Mi");

-- Drinks
INSERT INTO menu (name, price, category, calories, allergens)
VALUES
("Coca Cola", 3.50, "Drinks", 150, ""),
("Fanta", 3.50, "Drinks", 150, ""),
("Sprite", 3.50, "Drinks", 150, ""),
("Apple Juice", 3.50, "Drinks", 150, ""),
("Orange Juice", 3.50, "Drinks", 150, ""),
("Still Water", 3.50, "Drinks", 150, ""),
("Beer", 3.50, "Drinks", 150, "G");
