import streamlit as st

st.set_page_config(page_title="MS Weight Calculator", page_icon=":material/measuring_tape:", layout='wide',
                   initial_sidebar_state='collapsed')
st.sidebar.success("Navigate yourself")

st.title("📏 Experiment")

total_sum = 0


# Update default values to floats
default_values = {
    "item_name": None,
    "length": 0.0,  # Changed to float
    "diameter": 0.0,  # Changed to float
    "breadth": 0.0,  # Changed to float
    "thickness": 0.0,  # Changed to float
    "depth": 0.0  # Changed to float
}

# Initialize session state for add items list if not already done
if 'add_items' not in st.session_state:
    st.session_state.add_items = [default_values.copy()]  # Use copy to avoid reference issues


# Add a new empty add items row
def add_item_row():
    st.session_state.add_items.append(default_values.copy())  # Use copy to avoid reference issues


# Function to remove an item row by index with specific handling for index 0
def remove_item_row(index):
    # If trying to delete index 0, and it's the only item, reset to default
    if index == 0 and len(st.session_state.add_items) == 1:
        # Reset the first item to default values
        st.session_state.add_items[0] = default_values.copy()  # Reset to default values
    elif index < len(st.session_state.add_items):
        del st.session_state.add_items[index]


def flat_bar():

    # Function to calculate the Weight
    def calculate_weight(l, t, b):
        return b*t*l/1000000*7850

    total_bar_sum = 0
    col1, col2, col3, col4 = st.columns([1.33, 1.33, 1.33, 0.5])

    with col1:
        breadth = st.number_input("Enter the breadth (mm)", value=0.0, min_value=0.0, key=f'breadth_{i}')
        st.session_state.add_items[i]['breadth'] = breadth

    with col2:
        thickness = st.number_input("Enter the thickness (mm)", value=0.0, min_value=0.0,
                                    key=f'thickness_{i}')
        st.session_state.add_items[i]['thickness'] = thickness

    with col3:
        length = st.number_input("Enter the length (m)", value=0.0, min_value=0.0, key=f'length_{i}')
        st.session_state.add_items[i]['length'] = length

    with col4:
        st.write(f'Weight of item {i + 1}')
        weight = calculate_weight(length, thickness, breadth)
        weight = round(weight, 2)
        st.session_state.add_items[i]['weight'] = weight
        st.text(weight)
        total_bar_sum += weight


def square_steel_bar():

    # Function to calculate the Weight
    def calculate_weight(l, b):
        return b*b*l/1000000*7850

    total_bar_sum = 0
    col1, col2, col3 = st.columns([2, 2, 0.5])

    with col1:
        breadth = st.number_input("Enter the breadth (mm)", value=0.0, min_value=0.0, key=f'breadth_{i}')
        st.session_state.add_items[i]['breadth'] = breadth

    with col2:
        length = st.number_input("Enter the length (m)", value=0.0, min_value=0.0, key=f'length_{i}')
        st.session_state.add_items[i]['length'] = length

    with col3:
        st.write(f'Weight of item {i + 1}')
        weight = calculate_weight(length, breadth)
        weight = round(weight, 2)
        st.session_state.add_items[i]['weight'] = weight
        st.text(weight)
        total_bar_sum += weight


item_types = ['Flat Bars', 'Square Steel Bars']

# Display current add items
for i in range(len(st.session_state.add_items)):
    items = st.session_state.add_items[i]  # Get the item at the current index
    col_item, col_type = st.columns([1, 1])
    with col_item:
        item_name = st.text_input(f"Enter item {i + 1}", value=items['item_name'], key=f"item_name_{i}")
        st.session_state.add_items[i]['item_name'] = item_name

    with col_type:
        item_type = st.selectbox('Select the item type', options=item_types, key=f"item_type_{i}")
        st.session_state.add_items[i]['item_type'] = item_type

    if st.session_state.add_items[i]['item_type'] == 'Flat Bars':
        flat_bar()

    if st.session_state.add_items[i]['item_type'] == 'Square Steel Bars':
        square_steel_bar()

    st.divider()


if st.button("Add a new item", key=f"add", icon=':material/add:'):
    add_item_row()
    st.rerun()  # Rerun to refresh the UI after addition


if st.button("Delete the last row", key=f"remove", icon=':material/delete:'):
    remove_item_row(-1)
    st.rerun()  # Rerun to refresh the UI after deletion

