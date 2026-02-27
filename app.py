import streamlit as st
import mysql.connector

st.title("🚚 Smart Logistics Dashboard")

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="logistics_db"
    )

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM shipments")
    result = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) FROM warehouses")
    result2 = cursor.fetchone()
    st.success("Database Connected Successfully")
    st.write("📦Total Shipments in Database:", result[0])
    st.write("Total Warehouses in Database:", result2[0])
except Exception as e:
    st.error("Error occurred:")
    st.write(e)