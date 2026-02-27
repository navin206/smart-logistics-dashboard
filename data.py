print("RUNNING NAVIN DATA SCRIPT VERSION 2")
import mysql.connector
import json
import csv

print("Starting script...")

# Connect to database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root", 
    database="logistics_db"
)

cursor = connection.cursor()
print("Database is connected!")
# Courier staff  
print("Loading courier_staff.csv...")

with open("courier_staff.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute("""
            INSERT IGNORE INTO courier_staff (courier_id, name, rating, vehicle_type)
            VALUES (%s, %s, %s, %s)
        """, (
            row["courier_id"],
            row["name"],
            row["rating"],
            row["vehicle_type"]
        ))

print("Courier staff inserted")

# Shipments.json file
print("Loading shipments.json...")

with open("shipments.json", "r", encoding="utf-8") as file:
    shipments = json.load(file)

for i, row in enumerate(shipments):
    if i % 1000 == 0:
        print(f"Inserting shipment row: {i}")

    cursor.execute("""
        INSERT IGNORE INTO shipments (
            shipment_id, order_date, origin, destination,
            weight, courier_id, status, delivery_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row["shipment_id"],
        row["order_date"],
        row["origin"],
        row["destination"],
        row["weight"],
        row["courier_id"],
        row["status"],
        row["delivery_date"]
    ))

print("Shipments inserted!")

# Costs.csv file
print("Loading costs.csv...")

with open("costs.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute("""
            INSERT IGNORE INTO costs (shipment_id, fuel_cost, labor_cost, misc_cost)
    VALUES (%s, %s, %s, %s)
        """, (
            row["shipment_id"],
            row["fuel_cost"],
            row["labor_cost"],
            row["misc_cost"]
        ))
print("Costs inserted!")

#Warehouses.json file
# Warehouses.json file
print("Loading warehouses.json...")

with open("warehouses.json", "r", encoding="utf-8") as file:
    warehouses = json.load(file)

for i, row in enumerate(warehouses):
    if i % 1000 == 0:
        print(f"Inserting warehouse row: {i}")

    cursor.execute("""
        INSERT IGNORE INTO warehouses (
            warehouse_id, city, state, capacity
        )
        VALUES (%s, %s, %s, %s)
    """, (
        row["warehouse_id"],
        row["city"],
        row["state"],
        row["capacity"]
    ))

print("Warehouses inserted!")
                           
            
# ---------------------------------------------------
# COMMIT & CLOSE
# ---------------------------------------------------
connection.commit()
cursor.close()
connection.close()

print("All data inserted successfully!")