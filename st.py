import streamlit as st

col1, col2 = st.columns(2)

with col1:
    st.header("Left Side")
    st.write("This is the left column")

with col2:
    st.header("Right Side")
    st.write("This is the right column")