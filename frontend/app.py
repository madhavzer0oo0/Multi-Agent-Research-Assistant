import streamlit as st

if "token" not in st.session_state:
    st.session_state.token = None

if st.session_state.token:
    st.switch_page("pages/dashboard.py")

st.title("Multi-Agent Research Assistant")

col1, col2 = st.columns(2)

with col1:
    if st.button("Login"):
        st.switch_page("pages/login.py")

with col2:
    if st.button("Register"):
        st.switch_page("pages/register.py")