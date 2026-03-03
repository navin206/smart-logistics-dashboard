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
    
    cursor.execute("SELECT SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END) AS delivered_count FROM shipments")
    result4 = cursor.fetchone()

    cursor.execute("SELECT SUM(CASE WHEN status = 'In Transit' THEN 1 ELSE 0 END) AS in_transit_count FROM shipments")
    result5 = cursor.fetchone()

    cursor.execute("SELECT SUM(CASE WHEN status = 'Out for Delivery' THEN 1 ELSE 0 END) AS out_for_delivery_count FROM shipment_tracking")
    result6 = cursor.fetchone()

    cursor.execute("SELECT SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_count FROM shipment_tracking")
    result7 = cursor.fetchone()

    cursor.execute("SELECT SUM(CASE WHEN status = 'Order Placed' THEN 1 ELSE 0 END) AS order_placed_count FROM shipment_tracking")
    result8 = cursor.fetchone()
    col1, col2 = st.columns(2)
    with col1:
         st.metric("📦 Total Shipments", result[0])
    with col2:
         st.metric("🏢 Total Warehouses", result2[0])

    # Row 2
    col3, col4 = st.columns(2)
    with col3:
        st.metric("👨‍✈️ Courier Staff", result3[0])
    with col4:
        st.metric("✅ Delivered Shipments", result4[0])

    # Row 3
    col5, col6 = st.columns(2)
    with col5:
        st.metric("🚚 In Transit Shipments", result5[0])
    with col6:
        st.metric("📍 Out for Delivery", result6[0])

    # Row 4
    col7, col8 = st.columns(2)
    with col7:
        st.metric("❌ Cancelled Shipments", result7[0])
    with col8:
        st.metric("🛒 Orders Placed", result8[0]) 
    

except Exception as e:
    st.error("Error occurred:")
    st.write(e)

# SIDEBAR
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #14577D;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] * {
        color: #F4F1F1 !important;   /* Change this color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Shipment Tracking","Order Trends", "Route Efficiency", "Cost Analysis", "Courier Performance","Logistics Overview"]
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
        
        
# ROUTE EFFICIENCY

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
    LIMIT 10;
    """
    
    df = pd.read_sql(query, conn)

    st.subheader("📉 Slowest Routes")
    st.dataframe(df)
    st.bar_chart(df.set_index("origin")["speed_kmph"])

# COST ANALYSIS

elif page == "Cost Analysis":

    st.header("💰 Shipment Cost Analysis")
    st.header("Highly Expensive Shipments")


    query = """
    SELECT 
        shipment_id,
        (fuel_cost + labor_cost + misc_cost) AS total_cost
    FROM costs
    ORDER BY total_cost DESC
    LIMIT 20;
    """

    df = pd.read_sql(query, conn)

    st.dataframe(df)
    st.bar_chart(df.set_index("shipment_id")["total_cost"])


# COURIER PERFORMANCE

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

    # Order Trends

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
    
    query2 = """
    SELECT
        destination,
        COUNT(shipment_id) AS total_orders
    FROM shipments
    GROUP BY destination
    ORDER BY total_orders DESC
    LIMIT 10;
    """
    df2 = pd.read_sql(query2, conn)

    st.subheader("📊 Top Destinations by Order Count")
    st.dataframe(df2)
    st.bar_chart(df2.set_index("destination")["total_orders"])

elif page == "Logistics Overview":
    st.header("📊 Logistics Overview")
    st.subheader("📈 Total Vehicles")

    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(*) 
        FROM courier_staff 
        WHERE vehicle_type = 'car'
    """)
    
    result = cursor.fetchone()
    cursor.execute("""
        SELECT COUNT(*) 
        FROM courier_staff 
        WHERE vehicle_type = 'van'
    """)
    
    result1 = cursor.fetchone()
    cursor.execute("""
        SELECT COUNT(*) 
        FROM courier_staff 
        WHERE vehicle_type = 'bike'
    """)

    result2 = cursor.fetchone()
    cursor.execute("""
        SELECT COUNT(*) 
        FROM courier_staff 
        WHERE vehicle_type = 'truck'
    """)
    result3 = cursor.fetchone()
    col1, col2 = st.columns(2)
    with col1:
         st.metric("🚗 Car Count", result[0])
    with col2:
         st.metric("🚙 Van Count", result1[0])
    col3, col4 = st.columns(2)
    with col3:
         st.metric("🚛 Truck Count", result3[0])
    with col4:
         st.metric("🚲 Bike Count", result2[0])



