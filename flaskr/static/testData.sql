-- Menu Table

-- Mains
INSERT INTO menu (name, price, category, calories, allergens, image_location)
VALUES
    ("Beef Tacos", 12.50, "Mains", 800, "Mi","static/images/Beef_Tacos.jpg"),
    ("Pork Tacos", 12.50, "Mains", 800, "Mi","static/images/Pork_Tacos.jpg"),
    ("Halloumi Tacos", 10.50, "Mains", 750, "Mi","static/images/Halloumi_Tacos.jpg"),
    ("Chicken Enchiladas", 14.50, "Mains", 900, "G","static/images/Chicken_Enchiladas.jpg"),
    ("Pork Enchiladas", 14.50, "Mains", 900, "Mi","static/images/Pork_Enchiladas.jpg"),
    ("Jackfruit Enchiladas", 14.50, "Mains", 900, "Mi","static/images/Jackfruit_Enchiladas.jpg");

-- Sides
INSERT INTO menu (name, price, category, calories, allergens, image_location)
VALUES
    ("Plain Nachos", 5.50, "Sides", 350, "","static/images/Plain_Nachos.jpg"),
    ("Cheesy Nachos", 6.50, "Sides", 400, "Mi","static/images/Cheesy_Nachos.jpg");

-- Desserts
INSERT INTO menu (name, price, category, calories, allergens, image_location)
VALUES
    ("Ice Cream Sundae", 5.50, "Desserts", 300, "Mi","static/images/Ice_Cream_Sundae.jpg"),
    ("Chocolate Brownie", 5.50, "Desserts", 300, "Mi","static/images/Chocolate_Brownie.jpg");

-- Drinks
INSERT INTO menu (name, price, category, calories, allergens, image_location)
VALUES
    ("Coca Cola", 3.50, "Drinks", 150, "","static/images/Coca_Cola.jpg"),
    ("Fanta", 3.50, "Drinks", 150, "","static/images/Fanta.jpg"),
    ("Sprite", 3.50, "Drinks", 150, "","static/images/Sprite.jpg"),
    ("Apple Juice", 3.50, "Drinks", 150, "","static/images/Apple_Juice.jpg"),
    ("Orange Juice", 3.50, "Drinks", 150, "","static/images/Orange_Juice.jpg"),
    ("Still Water", 3.50, "Drinks", 150, "","static/images/Still_Water.jpg"),
    ("Beer", 3.50, "Drinks", 150, "G","static/images/Beer.jpg");


-- Logins
INSERT INTO users (first_name, last_name, password_hash, role)
VALUES
    -- Waiters
    ("Melissa", "Wilson", "15eb3b49fce780facecf0b761712328b0ae12e62a41c573a9629523fa2709dd7", 2),
    ("Rory", "Baker", "52c5f34607e2922524e8a323a0148b72d95919695bb381983858176be05add8e", 2),
    ("Amy", "Smith", "26f569da2d75f45870aa7c0ec11b83dcf9a2f2ae6cc673fedc57e9a49241a71b", 2),
    -- Kitchen Staff
    ("Anthony", "Spark", "1aa5f6f0e0e330b26de90da1968103250d4376f6c877c7539d5eb4781d231f5f", 3),
    ("Phoebe", "Taylor", "ef8667d2b0a7b4981a81e684765d6532e9b28b3cc79c968cacf73639997d6623", 3),
    ("Matthew", "Williams", "33caf999a6403a65eccee276210f1b6c1802f8bba2b3a4007028aa26c1569f8c", 3),
    -- Managers
    ("Isabelle", "Davies", "c4ffc94910796e8633061539e3815c10cada0d4092a596c150c0812f32a31a15", 4),
    ("Paul", "Grant", "3e3b916b101b24d3ebf206254acd53a81ed4163d42e0c1aa42d7ebd09c87a643", 4),
    -- Owner
    ("Tony", "Atkinson", "7507c2b6bf438cd0137632eb1734dc42b14e724bf604554410091f5bfd4baae0", 4);