DROP DATABASE IF EXISTS logistics_db;
CREATE DATABASE logistics_db;
USE logistics_db;
CREATE TABLE courier_staff (
    courier_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    rating DECIMAL(2,1),
    vehicle_type VARCHAR(50)
);

CREATE TABLE shipments (
    shipment_id VARCHAR(20) PRIMARY KEY,
    order_date DATE,
    origin VARCHAR(100),
    destination VARCHAR(100),
    weight DECIMAL(10,2),
    courier_id VARCHAR(20),
    status VARCHAR(50),
    delivery_date DATE,
    FOREIGN KEY (courier_id)
    REFERENCES courier_staff(courier_id)
);

CREATE TABLE costs (
    shipment_id VARCHAR(20) PRIMARY KEY,
    fuel_cost DECIMAL(10,2),
    labor_cost DECIMAL(10,2),
    misc_cost DECIMAL(10,2),
    FOREIGN KEY (shipment_id)
    REFERENCES shipments(shipment_id)
);
USE logistics_db;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE costs;
TRUNCATE TABLE shipments;
SET FOREIGN_KEY_CHECKS = 1;