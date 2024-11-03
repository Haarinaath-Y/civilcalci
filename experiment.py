import streamlit as st
from pandas import DataFrame
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas

st.set_page_config(page_title="MS Weight Calculator", page_icon=":material/measuring_tape:", layout='wide',
                   initial_sidebar_state='collapsed')
st.sidebar.success("Navigate yourself")

st.title("📏 MS Weight Calculator")

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


# Function to create PDF
def create_pdf(dataframe):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Title
    p.setFont("Helvetica-Bold", 14)
    p.drawString(30, height - 40, "DataFrame Report")

    # Set font for content
    p.setFont("Helvetica", 10)

    # Layout for columns
    x_offset = 30
    y_offset = height - 70
    line_height = 20
    max_cols = min(len(dataframe.columns), 8)  # Fit up to 8 columns

    # Column width calculation to fit all columns
    col_width = (width - 2 * x_offset) / max_cols

    # Header
    for i, col in enumerate(dataframe.columns[:max_cols]):
        p.drawString(x_offset + i * col_width, y_offset, str(col))
    y_offset -= line_height

    # Rows
    for _, row in dataframe.iterrows():
        for i, col in enumerate(dataframe.columns[:max_cols]):
            p.drawString(x_offset + i * col_width, y_offset, str(row[col]))
        y_offset -= line_height

    p.save()
    buffer.seek(0)
    return buffer


# Add a new empty add items row
def add_item_row():
    st.session_state.add_items.append(default_values.copy())  # Use copy to avoid reference issues


def remove_item_row(index):
    if 0 <= index < len(st.session_state.add_items):
        del st.session_state.add_items[index]  # Remove the specific row by index


def rec_hollow_func():

    # Function to calculate the Weight
    def calculate_weight(l, b, t, d):
        return ((b*d) - ((b-(2*t))*(d-(2*t))))*l/1000000*7850

    total_bar_sum = 0

    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 0.5, 0.15, 0.15])

    with col1:
        breadth = st.number_input("Enter the breadth (mm)", value=0.0, min_value=0.0, key=f'breadth_{i}')
        st.session_state.add_items[i]['breadth'] = breadth

    with col2:
        depth = st.number_input("Enter the depth (mm)", value=0.0, min_value=0.0, key=f'depth_{i}')
        st.session_state.add_items[i]['depth'] = depth

    with col3:
        thickness = st.number_input("Enter the thickness (mm)", value=0.0, min_value=0.0,
                                    key=f'thickness_{i}')
        st.session_state.add_items[i]['thickness'] = thickness

    with col4:
        length = st.number_input("Enter the length (m)", value=0.0, min_value=0.0, key=f'length_{i}')
        st.session_state.add_items[i]['length'] = length

    with col5:
        st.write(f'Weight of item {i + 1}')
        weight = calculate_weight(length, breadth, thickness, depth)
        weight = round(weight, 2)
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


def cir_hollow_func():

    # Function to calculate the Weight
    def calculate_weight(l, d, t):
        R = d/2
        r = R-t
        return 3.1416 * ((R*R)-(r*r))*l*7850/1000000

    total_bar_sum = 0
    col1, col2, col3, col4, col5, col6 = st.columns([1.33, 1.33, 1.33, 0.5, 0.15, 0.15])

    with col1:
        diameter = st.number_input("Enter the diameter (mm)", value=0.0, min_value=0.0,
                                   key=f'diameter_{i}')
        st.session_state.add_items[i]['diameter'] = diameter

    with col2:
        thickness = st.number_input("Enter the thickness (mm)", value=0.0, min_value=0.0,
                                    key=f'thickness_{i}')
        st.session_state.add_items[i]['thickness'] = thickness

    with col3:
        length = st.number_input("Enter the length (m)", value=0.0, min_value=0.0, key=f'length_{i}')
        st.session_state.add_items[i]['length'] = length

    with col4:
        st.write(f'Weight of item {i + 1}')
        weight = calculate_weight(length, diameter, thickness)
        weight = round(weight, 2)
        st.session_state.add_items[i]['weight'] = weight
        st.text(weight)
        total_bar_sum += weight

    with col5:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button(":material/add:", key=f"add_{i}"):
            add_item_row()
            st.rerun()  # Rerun to refresh the UI after addition

    with col6:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button(":material/delete:", key=f"remove_{i}"):
            remove_item_row(i)
            st.rerun()  # Rerun to refresh the UI after deletion


def round_steel_bar():

    # Function to calculate the Weight
    def calculate_weight(l, d):
        return d*d*l/162

    total_bar_sum = 0
    col1, col2, col3, col4, col5 = st.columns([2, 2, 0.5, 0.15, 0.15])

    with col1:
        diameter = st.number_input("Enter the diameter (mm)", value=0.0, min_value=0.0,
                                   key=f'diameter_{i}')
        st.session_state.add_items[i]['diameter'] = diameter

    with col2:
        length = st.number_input("Enter the length (m)", value=0.0, min_value=0.0, key=f'length_{i}')
        st.session_state.add_items[i]['length'] = length

    with col3:
        st.write(f'Weight of item {i + 1}')
        weight = calculate_weight(length, diameter)
        weight = round(weight, 2)
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


def flat_bar():

    # Function to calculate the Weight
    def calculate_weight(l, t, b):
        return b*t*l/1000000*7850

    total_bar_sum = 0
    col1, col2, col3, col4, col5, col6 = st.columns([1.33, 1.33, 1.33, 0.5, 0.15, 0.15])

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

    with col5:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button(":material/add:", key=f"add_{i}"):
            add_item_row()
            st.rerun()  # Rerun to refresh the UI after addition

    with col6:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button(":material/delete:", key=f"remove_{i}"):
            remove_item_row(i)
            st.rerun()  # Rerun to refresh the UI after deletion


def square_steel_bar():

    # Function to calculate the Weight
    def calculate_weight(l, b):
        return b*b*l/1000000*7850

    total_bar_sum = 0
    col1, col2, col3, col4, col5 = st.columns([2, 2, 0.5, 0.15, 0.15])

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


item_types = ['Rectangular Hollow Section', 'Circular Hollow Section', 'Round Steel Bars', 'Flat Bars',
              'Square Steel Bars']

# Display current add items
for i in range(len(st.session_state.add_items)):
    # Ensure a unique key for each item row
    item_key = f"item_{i}"

    items = st.session_state.add_items[i]  # Get the item at the current index
    col_item, col_type, col_delete = st.columns([1, 1, 1])
    with col_item:
        item_name = st.text_input(f"Enter item {i + 1}", value=items['item_name'], key=f"item_name_{item_key}")
        st.session_state.add_items[i]['item_name'] = item_name

    with col_type:
        item_type = st.selectbox('Select the item type', options=item_types, key=f"item_type_{item_key}")
        st.session_state.add_items[i]['item_type'] = item_type

    with col_delete:
        if st.button("Delete", key=f"delete_{item_key}", icon=':material/delete:'):
            remove_item_row(i)
            st.rerun()  # Rerun to refresh the UI after deletion

    if st.session_state.add_items[i]['item_type'] == 'Rectangular Hollow Section':
        rec_hollow_func()

    if st.session_state.add_items[i]['item_type'] == 'Circular Hollow Section':
        cir_hollow_func()

    if st.session_state.add_items[i]['item_type'] == 'Round Steel Bars':
        round_steel_bar()

    if st.session_state.add_items[i]['item_type'] == 'Flat Bars':
        flat_bar()

    if st.session_state.add_items[i]['item_type'] == 'Square Steel Bars':
        square_steel_bar()

    st.divider()


if st.button("Add a new item", key=f"add", icon=':material/add:'):
    add_item_row()
    st.rerun()  # Rerun to refresh the UI after addition


# if st.button("Delete the last row", key=f"remove", icon=':material/delete:'):
#     remove_item_row(-1)
#     st.rerun()  # Rerun to refresh the UI after deletion


# for item in st.session_state.add_items:
#     st.write(f"The Weight of {item['item_name']} is {item['Weight']}")


# Convert list of dictionaries to DataFrame with additional columns
df = DataFrame({
    "Item Name": [item["item_name"] for item in st.session_state.add_items],
    "Item Type": [item["item_type"] for item in st.session_state.add_items],
    "Breadth (mm)": [item["breadth"] for item in st.session_state.add_items],
    "Depth (mm)": [item["depth"] for item in st.session_state.add_items],
    "Thickness (mm)": [item["thickness"] for item in st.session_state.add_items],
    "Diameter (mm)": [item["diameter"] for item in st.session_state.add_items],
    "Length (m)": [item["length"] for item in st.session_state.add_items],
    "Weight (kg)": [item["weight"] for item in st.session_state.add_items]
})

# Apply rules for Item Type Selection
df.loc[df["Item Type"] == "Rectangular Hollow Section", ["Diameter (mm)"]] = 0
df.loc[df["Item Type"] == "Circular Hollow Section", ["Breadth (mm)", "Depth (mm)"]] = 0
df.loc[df["Item Type"] == "Round Steel Bars", ["Breadth (mm)", "Depth (mm)", "Thickness (mm)"]] = 0
df.loc[df["Item Type"] == "Flat Bars", ["Depth (mm)", "Diameter (mm)"]] = 0
df.loc[df["Item Type"] == "Square Steel Bars", ["Depth (mm)", "Diameter (mm)", "Thickness (mm)"]] = 0


# Total weight calculation
total_sum = df.iloc[:, -1].sum()
total_sum = round(total_sum, 2)

# Replacing zero values with hyphen
df.replace(0, '-', inplace=True)

st.subheader('MS Steel Calculation Details', divider=True)
st.dataframe(df, hide_index=True)
st.success(f"Total Weight of all items: **{total_sum} kg**")

# Button to generate and download PDF
pdf_buffer = create_pdf(df)
st.download_button(
    label="Download PDF",
    data=pdf_buffer,
    file_name="dataframe_report.pdf",
    mime="application/pdf"
)
