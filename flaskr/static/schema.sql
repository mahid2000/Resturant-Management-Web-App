DROP TABLE IF EXISTS menu;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS orderDetails;

CREATE TABLE menu (
    itemID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TINYTEXT NOT NULL,
    price DOUBLE(4, 2) NOT NULL,
    category TINYTEXT NOT NULL,
    calories SMALLINT NOT NULL,
    allergens TEXT
);

CREATE TABLE users (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TINYTEXT NOT NULL,
    last_name TINYTEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TINYINT NOT NULL
);

CREATE TABLE orders (
    orderID INTEGER PRIMARY KEY AUTOINCREMENT,
    tableNum TINYINT NOT NULL,
    paid TINYINT NOT NULL
);

CREATE TABLE orderDetails (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    orderID INTEGER NOT NULL,
    itemID INTEGER NOT NULL,
    customerID INTEGER NOT NULL,
    qty TINYINT NOT NULL,
    state TINYINT NOT NULL,
    ordertime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (orderID) REFERENCES orders(orderID),
    FOREIGN KEY (itemID) REFERENCES menu(itemID),
    FOREIGN KEY (customerID) REFERENCES users(userID)
);

INSERT INTO users
    (first_name, last_name, password_hash, role)
    VALUES ('John', 'Smith', 'password', 4);

CREATE TABLE tableAssignments (
    waiter_id INTEGER PRIMARY KEY,
    tableNum TINYINT NOT NULL,
    FOREIGN KEY (tableNum) REFERENCES orders(tableNum)
);