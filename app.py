import streamlit as st
from pandas import DataFrame
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
import uuid
from datetime import datetime

now = datetime.now()
date_time = now.strftime("%m-%d-%Y_%H:%M:%S")


st.set_page_config(page_title="MS Weight Calculator", page_icon=":material/measuring_tape:", layout='wide',
                   initial_sidebar_state='collapsed')
st.sidebar.success("Navigate yourself")

st.title("📏 MS Weight Calculator")

total_sum = 0

# Define default item values with a unique id
def create_item():
    return {
        "id": str(uuid.uuid4()),  # Unique identifier for each item
        "item_name": None,
        "item_type": None,
        "length": 0.0,
        "diameter": 0.0,
        "breadth": 0.0,
        "thickness": 0.0,
        "depth": 0.0,
        "weight": 0.0
    }


# Initialize session state for add_items list
if 'add_items' not in st.session_state:
    st.session_state.add_items = [create_item()]


# Function to add a new item
def add_item():
    st.session_state.add_items.append(create_item())


# Function to remove an item by its unique id
def remove_item(item_id):
    st.session_state.add_items = [item for item in st.session_state.add_items if item["id"] != item_id]


def create_pdf(dataframe, total_sum):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Title
    p.setFont("Helvetica-Bold", 14)
    p.drawString(30, height - 40, "MS Weight Calculation Report")

    # Set font for regular content
    p.setFont("Helvetica", 9)

    # Layout for columns
    x_offset = 30
    y_offset = height - 70
    line_height = 20
    max_cols = min(len(dataframe.columns), 8)  # Fit up to 8 columns

    # Adjusted column widths
    special_col_width = 1.5 * ((width - 2 * x_offset) / max_cols)  # Wider for "Item Type" and "Item Name"
    remaining_col_width = (width - 2 * x_offset - 2 * special_col_width) / (max_cols - 2)  # Other columns

    # Header with bold text and borders
    p.setFont("Helvetica-Bold", 9)  # Bold font for headers
    x_position = x_offset
    for i, col in enumerate(dataframe.columns[:max_cols]):
        # Determine column width: apply special width for "Item Type" and "Item Name"
        col_width = special_col_width if col in ["Item Type", "Item Name"] else remaining_col_width

        # Draw header cell border
        p.rect(x_position, y_offset - line_height, col_width, line_height)

        # Center the header text
        text_x = x_position + col_width / 2
        p.drawCentredString(text_x, y_offset - line_height / 2 - 3, str(col))

        # Update x_position for the next cell
        x_position += col_width

    # Reset x_position and move y_offset down for the rows
    y_offset -= line_height

    # Rows with borders
    p.setFont("Helvetica", 9)  # Regular font for row content
    for _, row in dataframe.iterrows():
        x_position = x_offset
        for i, col in enumerate(dataframe.columns[:max_cols]):
            # Determine column width
            col_width = special_col_width if col in ["Item Type", "Item Name"] else remaining_col_width

            # Draw cell border
            p.rect(x_position, y_offset - line_height, col_width, line_height)

            # Center the row text
            text_x = x_position + col_width / 2
            text_y = y_offset - line_height / 2 - 3  # Adjust for vertical centering
            p.drawCentredString(text_x, text_y, str(row[col]))

            # Update x_position for the next cell
            x_position += col_width

        # Move to the next row
        y_offset -= line_height

    p.drawString(30, y_offset, f"Total Weight: {total_sum}")

    p.save()
    buffer.seek(0)
    return buffer


# Redefine each type function to accept an `index` parameter
def rec_hollow_func(index):
    def calculate_weight(l, b, t, d):
        return ((b * d) - ((b - (2 * t)) * (d - (2 * t)))) * l / 1000000 * 7850

    item = st.session_state.add_items[index]
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 0.5, 0.15])

    with col1:
        item['breadth'] = st.number_input("Enter the breadth (mm)", value=item['breadth'], min_value=0.0,
                                          key=f'breadth_{index}')

    with col2:
        item['depth'] = st.number_input("Enter the depth (mm)", value=item['depth'], min_value=0.0,
                                        key=f'depth_{index}')

    with col3:
        item['thickness'] = st.number_input("Enter the thickness (mm)", value=item['thickness'], min_value=0.0,
                                            key=f'thickness_{index}')

    with col4:
        item['length'] = st.number_input("Enter the length (m)", value=item['length'], min_value=0.0,
                                         key=f'length_{index}', format="%.3f")

    with col5:
        st.write(f'Weight of item {index + 1}')
        item['weight'] = round(calculate_weight(item['length'], item['breadth'], item['thickness'], item['depth']), 2)
        st.text(item['weight'])

    with col6:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button(":material/delete:", key=f"remove_{index}"):
            remove_item(item["id"])
            st.rerun()


def cir_hollow_func(index):
    # Function to calculate the Weight
    def calculate_weight(l, d, t):
        R = d / 2
        r = R - t
        return 3.1416 * ((R * R) - (r * r)) * l * 7850 / 1000000

    item = st.session_state.add_items[index]

    col1, col2, col3, col4, col5 = st.columns([1.33, 1.33, 1.33, 0.5, 0.15])

    with col1:
        item['diameter'] = st.number_input("Enter the diameter (mm)", value=item['diameter'], min_value=0.0,
                                           key=f'diameter_{index}')

    with col2:
        item['thickness'] = st.number_input("Enter the thickness (mm)", value=item['thickness'], min_value=0.0,
                                            key=f'thickness_{index}')

    with col3:
        item['length'] = st.number_input("Enter the length (m)", value=item['length'], min_value=0.0,
                                         key=f'length_{index}', format="%.3f")

    with col4:
        st.write(f'Weight of item {index + 1}')
        item['weight'] = round(calculate_weight(item['length'], item['diameter'], item['thickness']), 2)
        st.text(item['weight'])

    with col5:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button(":material/delete:", key=f"remove_{index}"):
            remove_item(item["id"])
            st.rerun()  # Rerun to refresh the UI after deletion


def round_steel_bar(index):
    # Function to calculate the Weight
    def calculate_weight(l, d):
        return d * d * l / 162

    item = st.session_state.add_items[index]
    col1, col2, col3, col4 = st.columns([2, 2, 0.5, 0.15])

    with col1:
        item['diameter'] = st.number_input("Enter the diameter (mm)", value=item['diameter'], min_value=0.0,
                                           key=f'diameter_{index}')

    with col2:
        item['length'] = st.number_input("Enter the length (m)", value=item['length'], min_value=0.0,
                                         key=f'length_{index}', format="%.3f")

    with col3:
        st.write(f'Weight of item {index + 1}')
        item['weight'] = round(calculate_weight(item['length'], item['diameter']), 2)
        st.text(item['weight'])

    with col4:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button(":material/delete:", key=f"remove_{index}"):
            remove_item(item["id"])
            st.rerun()  # Rerun to refresh the UI after deletion


def flat_bar(index):
    # Function to calculate the Weight
    def calculate_weight(l, t, b):
        return b * t * l / 1000000 * 7850

    item = st.session_state.add_items[index]
    col1, col2, col3, col4, col5 = st.columns([1.33, 1.33, 1.33, 0.5, 0.15])

    with col1:
        item['breadth'] = st.number_input("Enter the breadth (mm)", value=item['breadth'], min_value=0.0,
                                          key=f'breadth_{index}')

    with col2:
        item['thickness'] = st.number_input("Enter the thickness (mm)", value=item['thickness'], min_value=0.0,
                                            key=f'thickness_{index}')

    with col3:
        item['length'] = st.number_input("Enter the length (m)", value=item['length'], min_value=0.0,
                                         key=f'length_{index}', format="%.3f")

    with col4:
        st.write(f'Weight of item {index + 1}')
        item['weight'] = round(calculate_weight(item['length'], item['thickness'], item['breadth']), 2)
        st.text(item['weight'])

    with col5:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button(":material/delete:", key=f"remove_{index}"):
            remove_item(item["id"])
            st.rerun()  # Rerun to refresh the UI after deletion


def square_steel_bar(index):
    # Function to calculate the Weight
    def calculate_weight(l, b):
        return b * b * l / 1000000 * 7850

    item = st.session_state.add_items[index]

    col1, col2, col3, col4 = st.columns([2, 2, 0.5, 0.15])

    with col1:
        item['breadth'] = st.number_input("Enter the breadth (mm)", value=item['breadth'], min_value=0.0,
                                          key=f'breadth_{index}')

    with col2:
        item['length'] = st.number_input("Enter the length (m)", value=item['length'], min_value=0.0,
                                         key=f'length_{index}', format="%.3f")

    with col3:
        st.write(f'Weight of item {index + 1}')
        item['weight'] = round(calculate_weight(item['length'], item['breadth']), 2)
        st.text(item['weight'])

    with col4:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button(":material/delete:", key=f"remove_{index}"):
            remove_item(item["id"])
            st.rerun()  # Rerun to refresh the UI after deletion


item_types = ['Rectangular Hollow Section', 'Circular Hollow Section', 'Round Steel Bars', 'Flat Bars',
              'Square Steel Bars']

# Display current add items
for i, item in enumerate(st.session_state.add_items):
    item_key = item["id"]

    col_item, col_type = st.columns([1, 1])

    with col_item:
        item['item_name'] = st.text_input(f"Enter item {i + 1}", value=item['item_name'], key=f"item_name_{item_key}")

    with col_type:
        item_type = st.selectbox("Select item type", options=item_types,
                                 index=item_types.index(item["item_type"]) if item["item_type"] in item_types else 0,
                                 key=f"item_type_{item_key}")
        item["item_type"] = item_type

    if item_type == 'Rectangular Hollow Section':
        rec_hollow_func(i)

    elif item_type == 'Circular Hollow Section':
        cir_hollow_func(i)

    elif item_type == 'Round Steel Bars':
        round_steel_bar(i)

    elif item_type == 'Flat Bars':
        flat_bar(i)

    elif item_type == 'Square Steel Bars':
        square_steel_bar(i)

    st.divider()

if st.button("Add a new item", key=f"add", icon=':material/add:'):
    add_item()
    st.rerun()  # Rerun to refresh the UI after addition

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
total_sum = round(df.iloc[:, -1].sum(), 2)

# Replacing zero values with hyphen
df.replace(0, '-', inplace=True)

st.subheader('MS Steel Calculation Details', divider=True)
st.dataframe(df, hide_index=True, use_container_width=True)
st.success(f"Total Weight of all items: **{total_sum} kg**")

# Button to generate and download PDF
pdf_buffer = create_pdf(df, total_sum)
st.download_button(
    label="Download as PDF",
    data=pdf_buffer,
    file_name=f"ms_weight_report_{date_time}.pdf",
    mime="application/pdf",
    icon=':material/download_for_offline:'
)
