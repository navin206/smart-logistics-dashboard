import streamlit as st
import mysql.connector
import pandas as pd

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
    cursor.execute("SELECT COUNT(*) FROM courier_staff")
    result3 = cursor.fetchone()

    st.success("Database Connected Successfully")
    st.write("📦 Total Shipments:", result[0])
    st.write("🏢 Total Warehouses:", result2[0])
    st.write("👨‍✈️ Courier Staff:", result3[0])

except Exception as e:
    st.error("Error occurred:")
    st.write(e)

# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Shipment Tracking", "Route Efficiency", "Cost Analysis", "Courier Performance"]
)
if page == "Shipment Tracking":

    st.header("📦 Shipment Tracking System")

    shipment_id = st.text_input("Enter Shipment ID")

    if shipment_id:

        query = """
SELECT 
    s.shipment_id,
    s.origin,
    s.destination,
    s.status,
    s.courier_id,
    r.distance_km,
    r.avg_time_hours,
    (c.fuel_cost + c.labor_cost + c.misc_cost) AS total_cost
FROM shipments s
LEFT JOIN routes r 
    ON s.origin = r.origin 
    AND s.destination = r.destination
LEFT JOIN costs c 
    ON s.shipment_id = c.shipment_id
WHERE s.shipment_id = %s
"""

        df = pd.read_sql(query, conn, params=(shipment_id,))

        if df.empty:
            st.error("❌ Shipment ID not found")
        else:
            st.success("✅ Shipment Found")
            st.dataframe(df)

            st.subheader("📊 Shipment Summary")

            st.write("📍 Origin:", df["origin"][0])
            st.write("🏁 Destination:", df["destination"][0])
            st.write("🚦 Status:", df["status"][0])
            st.write("💰 Total Cost:", df["total_cost"][0])
# -----------------------
# ROUTE EFFICIENCY
# -----------------------
elif page == "Route Efficiency":

    st.header("🚦 Route Efficiency Analysis")

    query = """
    SELECT 
        route_id,
        origin,
        destination,
        distance_km,
        avg_time_hours,
        (distance_km / avg_time_hours) AS speed_kmph
    FROM routes
    ORDER BY speed_kmph ASC
    LIMIT 5;
    """

    df = pd.read_sql(query, conn)

    st.subheader("📉 Slowest Routes")
    st.dataframe(df)

    st.subheader("📊 Speed Chart")
    st.bar_chart(df.set_index("route_id")["speed_kmph"])

# -----------------------
# COST ANALYSIS
# -----------------------
elif page == "Cost Analysis":

    st.header("💰 Shipment Cost Analysis")

    query = """
    SELECT 
        shipment_id,
        (fuel_cost + labor_cost + misc_cost) AS total_cost
    FROM costs
    ORDER BY total_cost DESC
    LIMIT 5;
    """

    df = pd.read_sql(query, conn)

    st.dataframe(df)
    st.bar_chart(df.set_index("shipment_id")["total_cost"])

# -----------------------
# COURIER PERFORMANCE
# -----------------------
elif page == "Courier Performance":

    st.header("👨‍✈️ Courier Workload")

    query = """
SELECT 
    c.name AS courier_name,
    COUNT(s.shipment_id) AS total_shipments
FROM shipments s
JOIN courier_staff c 
    ON s.courier_id = c.courier_id
GROUP BY c.name
ORDER BY total_shipments DESC
LIMIT 20;
"""
df = pd.read_sql(query, conn)

st.dataframe(df)
st.bar_chart(df.set_index("courier_name")["total_shipments"])