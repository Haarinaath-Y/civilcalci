import streamlit as st

st.set_page_config(page_title="Civil Material Calculator", page_icon=":material/calculate:", layout="wide")

st.title("Civil Material Calculator")

# Function to calculate the volume
def calculate_volume(length, breadth, thickness, width):
    return length * breadth * thickness * width

# Update default values to floats
default_values = {
    "item_name": None,
    "length": 1.0,  # Changed to float
    "breadth": 1.0,  # Changed to float
    "thickness": 1.0,  # Changed to float
    "width": 1.0  # Changed to float
}

# Initialize session state for add items list if not already done
if 'add_items' not in st.session_state:
    st.session_state.add_items = [default_values]  # List to store add items

# Add a new empty add items row
def add_item_row():
    st.session_state.add_items.append(default_values.copy())  # Use copy to avoid reference issues

# Function to remove an item row by index with specific handling for index 0
def remove_item_row(index):
    # If trying to delete index 0, and it's the only item, reset to default
    if index == 0 and len(st.session_state.add_items) == 1:
        st.session_state.add_items[0] = default_values.copy()  # Reset to default values
    elif index < len(st.session_state.add_items):
        del st.session_state.add_items[index]

total_sum = 0

# Display current add items
for i, items in enumerate(st.session_state.add_items):
    item_name = st.text_input(f"Enter item {i+1}", value=items['item_name'], key=f"item_name_{i}")

    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 0.5, 0.15, 0.15])
    with col1:
        length = st.number_input("Enter the length", value=float(items['length']), min_value=0.0, key=f'length_{i}')
    with col2:
        breadth = st.number_input("Enter the breadth", value=float(items['breadth']), min_value=0.0, key=f'breadth_{i}')
    with col3:
        thickness = st.number_input("Enter the thickness", value=float(items['thickness']), min_value=0.0, key=f'thickness_{i}')
    with col4:
        width = st.number_input("Enter the width", value=float(items['width']), min_value=0.0, key=f'width_{i}')
    with col5:
        st.write(f'Volume of item {i+1}')
        volume = calculate_volume(length, breadth, thickness, width)
        st.text(volume)
        total_sum += volume
    with col6:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button(":material/add:", key=f"add_{i}"):
            add_item_row()
            st.rerun()  # Rerun to refresh the UI after addition
    with col7:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button(":material/delete:", key=f"remove_{i}"):
            remove_item_row(i)
            st.rerun()  # Rerun to refresh the UI after deletion

st.success(f"Total Volume of all items: **{total_sum}**")
