import streamlit as st
from api import register

st.title("Register")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Register"):

    response = register(email, password)

    if response.status_code in [200, 201]:
        st.success("Registered successfully!")
        st.switch_page("pages/login.py")
    else:
        st.error(response.text)