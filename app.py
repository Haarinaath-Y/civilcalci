import streamlit as st

st.set_page_config(page_title="Civil Material Calculator", page_icon=":material/calculate:", layout="wide")

st.title("Civil Material Calculator")


def func():
    a = length * breadth * thickness * width
    return a


# Initialize session state for add items list if not already done
if 'add_items' not in st.session_state:
    st.session_state.add_items = []  # List to store add items


# Add a new empty add items row
def add_item_row():
    st.session_state.add_items.append({"month": None, "amount": 0})


# Remove an add items row by index
def remove_item_row(index):
    if index < len(st.session_state.add_items):
        del st.session_state.add_items[index]  # Delete entry at the specified index


item_name = st.text_input("Enter item name")
# Display current add items
for i, items in enumerate(st.session_state.add_items):
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 0.2, 0.2, 0.2])
    with col1:
        length = st.number_input("Enter the length", value=1, key=f'length_{i}')
    with col2:
        breadth = st.number_input("Enter the breadth", value=1, key=f'breadth_{i}')
    with col3:
        thickness = st.number_input("Enter the thickness", value=1, key=f'thickness_{i}')
    with col4:
        width = st.number_input("Enter the width", value=1, key=f'width_{i}')
    with col5:
        st.write('Area')
        st.text(func())
    with col6:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)  # Adjust 'height' as needed
        if st.button(":material/add:", key=f"add_{i}"):
            add_item_row()
            st.rerun()  # Rerun to refresh the UI after addition
    with col7:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)  # Adjust 'height' as needed
        if st.button(":material/delete:", key=f"remove_{i}"):
            remove_item_row(i)
            st.rerun()  # Rerun to refresh the UI after deletion


# Add new extra payment row button
if st.button("👉 Click here to Add Extra Payments"):
    add_item_row()
    st.rerun()

