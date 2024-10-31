import streamlit as st
from pandas import DataFrame

st.set_page_config(page_title="Civil Material Calculator", page_icon=":material/calculate:", layout='wide')
st.sidebar.success("Navigate yourself")

st.title("Civil Material Calculator")

total_sum = 0


# Update default values to floats
default_values = {
    "item_name": None,
    "length": 0.0,  # Changed to float
    "diameter": 0.0,  # Changed to float
    "breadth": 0.0,  # Changed to float
    "thickness": 0.0,  # Changed to float
    "width": 0.0  # Changed to float
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


def hollow_bar_func():

    # Function to calculate the Weight
    def calculate_weight(ln, br, thick, wid):
        return ln * br * thick * wid

    total_bar_sum = 0

    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 0.5, 0.15, 0.15])

    with col1:
        length = st.number_input("Enter the length (mm)", value=float(items['length']), min_value=0.0, key=f'length_{i}')
        st.session_state.add_items[i]['length'] = length

    with col2:
        breadth = st.number_input("Enter the breadth (mm)", value=float(items['breadth']), min_value=0.0, key=f'breadth_{i}')
        st.session_state.add_items[i]['breadth'] = breadth

    with col3:
        thickness = st.number_input("Enter the thickness (mm)", value=float(items['thickness']), min_value=0.0,
                                    key=f'thickness_{i}')
        st.session_state.add_items[i]['thickness'] = thickness

    with col4:
        width = st.number_input("Enter the width (mm)", value=float(items['width']), min_value=0.0, key=f'width_{i}')
        st.session_state.add_items[i]['width'] = width

    with col5:
        st.write(f'Weight of item {i + 1}')
        weight = calculate_weight(length, breadth, thickness, width)
        st.session_state.add_items[i]['weight'] = weight
        st.text(weight)
        total_bar_sum += weight

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

    return total_bar_sum


def round_bar_func():

    # Function to calculate the Weight
    def calculate_weight(ln, dia):
        return ln * dia

    total_bar_sum = 0
    col1, col2, col3, col4, col5 = st.columns([2, 2, 0.5, 0.15, 0.15])

    with col1:
        length = st.number_input("Enter the length (mm)", value=float(items['length']), min_value=0.0, key=f'length_{i}')
        st.session_state.add_items[i]['length'] = length

    with col2:
        diameter = st.number_input("Enter the diameter (mm)", value=float(items['diameter']), min_value=0.0,
                                   key=f'diameter_{i}')
        st.session_state.add_items[i]['diameter'] = diameter

    with col3:
        st.write(f'Weight of item {i + 1}')
        weight = calculate_weight(length, diameter)
        st.session_state.add_items[i]['weight'] = weight
        st.text(weight)
        total_bar_sum += weight

    with col4:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button(":material/add:", key=f"add_{i}"):
            add_item_row()
            st.rerun()  # Rerun to refresh the UI after addition

    with col5:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button(":material/delete:", key=f"remove_{i}"):
            remove_item_row(i)
            st.rerun()  # Rerun to refresh the UI after deletion

    return total_bar_sum


item_types = ['Hollow Bar', 'Round Bar']

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

    if st.session_state.add_items[i]['item_type'] == 'Hollow Bar':
        hollow_bar_func()

    if st.session_state.add_items[i]['item_type'] == 'Round Bar':
        round_bar_func()

    st.divider()



# for item in st.session_state.add_items:
#     st.write(f"The Weight of {item['item_name']} is {item['Weight']}")


# Convert list of dictionaries to DataFrame with additional columns
df = DataFrame({
    "Item Name": [item["item_name"] for item in st.session_state.add_items],
    "Item Type": [item["item_type"] for item in st.session_state.add_items],
    "Length": [item["length"] for item in st.session_state.add_items],
    "Breadth": [item["breadth"] for item in st.session_state.add_items],
    "Diameter": [item["diameter"] for item in st.session_state.add_items],
    "Thickness": [item["thickness"] for item in st.session_state.add_items],
    "Width": [item["width"] for item in st.session_state.add_items],
    "Weight": [item["weight"] for item in st.session_state.add_items]
})

st.subheader('MS Steel Calculation Details', divider=True)
# Display the DataFrame in Streamlit
st.dataframe(df, hide_index=True)

st.success(f"Total Weight of all items: **{total_sum}**")
