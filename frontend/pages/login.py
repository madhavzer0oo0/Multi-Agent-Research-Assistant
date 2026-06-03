import streamlit as st
from api import login

st.title("Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):

    response = login(email, password)

    st.write("Status Code:", response.status_code)
    st.write("Response:", response.text)

    if response.status_code == 200:

        token = response.json()["access_token"]

        st.session_state.token = token

        st.success("Login successful!")

        st.switch_page("pages/dashboard.py")

    else:
        st.error("Invalid credentials")