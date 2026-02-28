import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="logistics_db"
)

# Query 1: Shipments per Warehouse
query1 = """
SELECT warehouse_id, COUNT(*) as total_shipments
FROM shipments
GROUP BY warehouse_id;
"""

df1 = pd.read_sql(query1, conn)

plt.figure()
plt.bar(df1['warehouse_id'], df1['total_shipments'])
plt.xlabel("Warehouse ID")
plt.ylabel("Total Shipments")
plt.title("Shipments per Warehouse")
plt.show()


# Query 2: Total Cost per Warehouse
query2 = """
SELECT warehouse_id, SUM(cost) as total_cost
FROM costs
GROUP BY warehouse_id;
"""

df2 = pd.read_sql(query2, conn)

plt.figure()
plt.bar(df2['warehouse_id'], df2['total_cost'])
plt.xlabel("Warehouse ID")
plt.ylabel("Total Cost")
plt.title("Total Cost per Warehouse")
plt.show()

conn.close()