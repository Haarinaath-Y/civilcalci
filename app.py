import streamlit as st

st.set_page_config(page_title="Civil Material Calculator", page_icon=":material/calculate:", layout="wide")


def func():
    a = length * breadth * thickness * width
    return a


st.title("Civil Material Calculator")

item_name = st.text_input("Enter item name")

col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
with col1:
    length = st.number_input("Enter the length", value=1)
with col2:
    breadth = st.number_input("Enter the breadth", value=1)
with col3:
    thickness = st.number_input("Enter the thickness", value=1)
with col4:
    width = st.number_input("Enter the width", value=1)
with col5:
    st.write(func())

