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


-- Logins
INSERT INTO users (first_name, last_name, password_hash, role)
VALUES
    -- Waiters
    ("Melissa", "Wilson", -2563970076923659231, 2),
    ("Rory", "Baker", 8099359456894473649, 2),
    ("Amy", "Smith", 7874037471067922999, 2),
    -- Kitchen Staff
    ("Anthony", "Spark", 587923566597843294, 3),
    ("Phoebe", "Taylor", 6962375528586743406, 3),
    ("Matthew", "Williams", -434085788409801296, 3),
    -- Managers
    ("Isabelle", "Davies", -2369642747911977797, 4),
    ("Paul", "Grant", 8845667195580603087, 4),
    -- Owner
    ("Tony", "Atkinson", 3893332994472280238, 4);