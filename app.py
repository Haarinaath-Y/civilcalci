import streamlit as st

st.set_page_config(page_title="Civil Material Calculator", page_icon=":material/calculate:", layout="wide")

st.title("Civil Material Calculator")


def func():
    a = length * breadth * thickness * width
    return a


default_values = {"item_name": None, "length": 1, "breadth": 1, "thickness": 1, "width": 1}


# Initialize session state for add items list if not already done
if 'add_items' not in st.session_state:
    st.session_state.add_items = [default_values.copy()]  # List to store add items


# Add a new empty add items row
def add_item_row():
    st.session_state.add_items.append(default_values)


# Function to remove an item row by index with specific handling for index 0
def remove_item_row(index):
    # Delete entry if it's not the first or only entry
    if index < len(st.session_state.add_items):
        del st.session_state.add_items[index]


# Function to reset session state to default values
def reset_session_state():
    st.session_state.add_items = [default_values.copy()]


total_sum = 0
# Display current add items
for i, items in enumerate(st.session_state.add_items):
    item_name = st.text_input(f"Enter item {i+1}", key=f"item_name_{i}")

    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 0.5, 0.15, 0.15])
    with col1:
        length = st.number_input("Enter the length", value=1, key=f'length_{i}')
    with col2:
        breadth = st.number_input("Enter the breadth", value=1, key=f'breadth_{i}')
    with col3:
        thickness = st.number_input("Enter the thickness", value=1, key=f'thickness_{i}')
    with col4:
        width = st.number_input("Enter the width", value=1, key=f'width_{i}')
    with col5:
        st.write(f'Volume of item {i+1}')
        volume = func()
        st.text(volume)
        total_sum += volume
    with col6:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)  # Adjust 'height' as needed
        if st.button(":material/add:", key=f"add_{i}"):
            add_item_row()
            st.rerun()  # Rerun to refresh the UI after addition
    with col7:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)  # Adjust 'height' as needed
        if st.button(":material/delete:", key=f"remove_{i}"):
            if i < 1:
                remove_item_row(i)
                st.rerun()  # Rerun to refresh the UI after deletion
            else:
                reset_session_state()


st.success(f"Total Volume of all items: **{total_sum}**")
