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
CREATE TABLE routes (
    route_id VARCHAR(20) PRIMARY KEY,
    origin VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    distance_km DECIMAL(8,2) NOT NULL,
    avg_time_hours DECIMAL(5,2) NOT NULL
);
CREATE TABLE warehouses (
    warehouse_id VARCHAR(20) PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    capacity INT NOT NULL
);
CREATE TABLE shipment_tracking (
    tracking_id INT AUTO_INCREMENT PRIMARY KEY,
    shipment_id VARCHAR(20) NOT NULL,
    status VARCHAR(50) NOT NULL,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (shipment_id) 
        REFERENCES shipments(shipment_id)
        ON DELETE CASCADE
);
USE logistics_db;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE costs;
TRUNCATE TABLE shipments;
SET FOREIGN_KEY_CHECKS = 1;
SHOW databases:
DESCRIBE warehouses;

