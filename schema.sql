DROP TABLE IF EXISTS menu;
-- DROP TABLE IF EXISTS customer;
-- DROP TABLE IF EXISTS transaction;
-- DROP TABLE IF EXISTS orderedItem;


CREATE TABLE menu (
	itemID SERIAL PRIMARY KEY,
	name VARCHAR(256),
	price INTEGER,
	calories INTEGER,
	allergens VARCHAR(256)
);


-- These are all schemas for the ARMS system that have yet to be tested

-- CREATE TABLE customer (
-- 	customerID SERIAL PRIMARY KEY,
-- 	name VARCHAR(256)
-- );
--
-- CREATE TABLE transaction (
-- 	transactionID SERIAL PRIMARY KEY,
-- 	customerID SERIAL PRIMARY KEY,
--     tableNumber INTEGER,
--     total INTEGER
-- );
--
-- CREATE TABLE orderedItem (
-- 	orderedItemID SERIAL PRIMARY KEY,
-- 	ItemID SERIAL PRIMARY KEY,
-- 	orderID SERIAL PRIMARY KEY,
-- 	name VARCHAR(256),
-- 	price INTEGER,
-- 	calories INTEGER,
-- 	allergens VARCHAR(256)
-- );


