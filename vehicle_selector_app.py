import streamlit as st

# 🚚 Full vehicle reference table (EPC)
vehicle_types = [
    {"name": "LCV Truck (Light Commercial Vehicle)", "max_length": 4.2, "max_width": 2.0, "max_height": 2.2, "max_weight": 3},
    {"name": "14 ft Truck (Standard)", "max_length": 6, "max_width": 2.5, "max_height": 2.5, "max_weight": 10},
    {"name": "22 ft Truck / Semi Trailer", "max_length": 12, "max_width": 2.6, "max_height": 3, "max_weight": 20},
    {"name": "Flatbed Trailer (40 ft)", "max_length": 18, "max_width": 2.6, "max_height": 3.5, "max_weight": 30},
    {"name": "Flatbed Trailer (60 ft)", "max_length": 25, "max_width": 2.6, "max_height": 3.5, "max_weight": 35},
    {"name": "Semi Low Bed Trailer", "max_length": 18, "max_width": 3.0, "max_height": 3.5, "max_weight": 40},
    {"name": "Low Bed Trailer", "max_length": 18, "max_width": 3.5, "max_height": 4.2, "max_weight": 80},
    {"name": "Multi-Axle Modular Hydraulic Trailer", "max_length": 30, "max_width": 5.0, "max_height": 5.5, "max_weight": 500},
    {"name": "Container Trailer (40 ft)", "max_length": 12.2, "max_width": 2.6, "max_height": 2.9, "max_weight": 28},
    {"name": "Tanker Truck", "max_length": 12, "max_width": 2.5, "max_height": 3.0, "max_weight": 25}
]

def select_vehicle_type(length_m, width_m, height_m, weight_tonnes):
    for vehicle in vehicle_types:
        if (length_m <= vehicle["max_length"] and
            width_m <= vehicle["max_width"] and
            height_m <= vehicle["max_height"] and
            weight_tonnes <= vehicle["max_weight"]):
            return vehicle["name"]
    return "Custom/Heavy Haulage Required (Contact Transport Planner)"

# 🧱 UI
st.title("🚚 Vehicle Recommendation Tool – Artson Logistics")
st.markdown("""
This tool helps select the **most suitable vehicle** for transporting project cargo based on:
- Length × Width × Height (in meters)
- Weight (in tonnes)
""")

# 📥 Inputs
length = st.number_input("📏 Cargo Length (m)", value=6.0, step=0.1)
width = st.number_input("📐 Cargo Width (m)", value=2.5, step=0.1)
height = st.number_input("📦 Cargo Height (m)", value=2.5, step=0.1)
weight = st.number_input("⚖️ Cargo Weight (tonnes)", value=10.0, step=0.1)

# 🔍 Run matching
if st.button("🔍 Recommend Vehicle"):
    vehicle = select_vehicle_type(length, width, height, weight)
    st.success(f"✅ **Recommended Vehicle Type:** {vehicle}")
