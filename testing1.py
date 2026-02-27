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