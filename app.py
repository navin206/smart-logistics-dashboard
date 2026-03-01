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
    ["Shipment Tracking","Order Trends", "Route Efficiency", "Cost Analysis", "Courier Performance"]
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
            COALESCE(c.fuel_cost,0) +
            COALESCE(c.labor_cost,0) +
            COALESCE(c.misc_cost,0) AS total_cost
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

            st.write("📍 Origin:", df.loc[0, "origin"])
            st.write("🏁 Destination:", df.loc[0, "destination"])
            st.write("🚦 Status:", df.loc[0, "status"])
            st.write("💰 Total Cost:", df.loc[0, "total_cost"])
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
    LIMIT 20;
    """

    df = pd.read_sql(query, conn)

    st.subheader("📉 Slowest Routes")
    st.dataframe(df)

    st.subheader("📊 Speed Chart")
    st.bar_chart(df.set_index("origin")["speed_kmph"])

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
# -----------------------
# COURIER PERFORMANCE
# -----------------------
elif page == "Courier Performance":

    st.header("👨‍✈️ Courier Workload")

    query = """
    SELECT 
        c.name AS courier_name,
        c.rating,
        c.vehicle_type,
        COUNT(s.shipment_id) AS total_shipments
    FROM shipments s
    JOIN courier_staff c 
        ON s.courier_id = c.courier_id
    GROUP BY c.name, c.rating, c.vehicle_type
    ORDER BY total_shipments DESC
    LIMIT 20;
    """

    df = pd.read_sql(query, conn)

    st.dataframe(df)
    st.bar_chart(df.set_index("courier_name")["total_shipments"])
elif page == "Order Trends":

    st.header("📈 Monthly Order Trend")

    query = """
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') AS order_month,
        COUNT(*) AS total_orders
    FROM shipments
    GROUP BY order_month
    ORDER BY order_month;
    """

    df = pd.read_sql(query, conn)

    st.dataframe(df)

    st.line_chart(df.set_index("order_month")["total_orders"])
    df2 = pd.read_sql(query, conn)

