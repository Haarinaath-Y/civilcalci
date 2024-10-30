import streamlit as st

st.set_page_config(page_title="Civil Material Calculator", page_icon=":material/calculate:", layout="wide")

st.title("Civil Material Calculator")

item_name = st.text_input("Enter item name")
length = st.number_input("Enter the length", value=1)
breadth = st.number_input("Enter the breadth", value=1)
thickness = st.number_input("Enter the thickness", value=1)
width = st.number_input("Enter the width", value=1)


def func():
    a = length * breadth * thickness * width
    return a


st.write(func())
