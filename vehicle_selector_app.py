import streamlit as st
import pandas as pd
import altair as alt
import math

# ----------------------------
# Vehicle master data
# ----------------------------

vehicle_types = [
    {"name": "LCV Truck", "max_length": 4.2, "max_width": 2.0, "max_height": 2.2, "max_weight": 3000, "cost_per_km": 18, "cost_per_tkm": 5.5, "has_sidewalls": True},
    {"name": "DCM Truck (7 Ton)", "max_length": 5.5, "max_width": 2.2, "max_height": 2.4, "max_weight": 7000, "cost_per_km": 24, "cost_per_tkm": 5.2, "has_sidewalls": True},
    {"name": "14 ft Truck", "max_length": 6, "max_width": 2.5, "max_height": 2.5, "max_weight": 10000, "cost_per_km": 28, "cost_per_tkm": 5, "has_sidewalls": True},
    {"name": "22 ft Truck", "max_length": 12, "max_width": 2.6, "max_height": 3, "max_weight": 20000, "cost_per_km": 38, "cost_per_tkm": 4.3, "has_sidewalls": True},
    {"name": "Flatbed Trailer (40 ft)", "max_length": 18, "max_width": 2.6, "max_height": 3.5, "max_weight": 30000, "cost_per_km": 55, "cost_per_tkm": 3.8, "has_sidewalls": False},
    {"name": "Flatbed Trailer (60 ft)", "max_length": 25, "max_width": 2.6, "max_height": 3.5, "max_weight": 35000, "cost_per_km": 65, "cost_per_tkm": 3.5, "has_sidewalls": False},
    {"name": "Semi Low Bed", "max_length": 18, "max_width": 3.0, "max_height": 3.5, "max_weight": 40000, "cost_per_km": 75, "cost_per_tkm": 3.2, "has_sidewalls": False},
    {"name": "Low Bed Trailer", "max_length": 18, "max_width": 3.5, "max_height": 4.2, "max_weight": 80000, "cost_per_km": 90, "cost_per_tkm": 3, "has_sidewalls": False},
    {"name": "Multi-Axle Modular Trailer", "max_length": 30, "max_width": 5.0, "max_height": 5.5, "max_weight": 500000, "cost_per_km": 180, "cost_per_tkm": 2.5, "has_sidewalls": False},
    {"name": "Container Trailer (40 ft)", "max_length": 12.2, "max_width": 2.6, "max_height": 2.9, "max_weight": 28000, "cost_per_km": 42, "cost_per_tkm": 3.8, "has_sidewalls": True}
]

# vehicle_types = [
#     {"name": "LCV Truck", "max_length": 4.2, "max_width": 2.0, "max_height": 2.2, "max_weight": 3000, "cost_per_km": 18, "cost_per_tkm": 5.5, "has_sidewalls": True},
#     {"name": "14 ft Truck", "max_length": 6, "max_width": 2.5, "max_height": 2.5, "max_weight": 10000, "cost_per_km": 28, "cost_per_tkm": 5, "has_sidewalls": True},
#     {"name": "22 ft Truck", "max_length": 12, "max_width": 2.6, "max_height": 3, "max_weight": 20000, "cost_per_km": 38, "cost_per_tkm": 4.3, "has_sidewalls": True},
#     {"name": "Flatbed Trailer (40 ft)", "max_length": 18, "max_width": 2.6, "max_height": 3.5, "max_weight": 30000, "cost_per_km": 55, "cost_per_tkm": 3.8, "has_sidewalls": False},
#     {"name": "Flatbed Trailer (60 ft)", "max_length": 25, "max_width": 2.6, "max_height": 3.5, "max_weight": 35000, "cost_per_km": 65, "cost_per_tkm": 3.5, "has_sidewalls": False},
#     {"name": "Semi Low Bed", "max_length": 18, "max_width": 3.0, "max_height": 3.5, "max_weight": 40000, "cost_per_km": 75, "cost_per_tkm": 3.2, "has_sidewalls": False},
#     {"name": "Low Bed Trailer", "max_length": 18, "max_width": 3.5, "max_height": 4.2, "max_weight": 80000, "cost_per_km": 90, "cost_per_tkm": 3, "has_sidewalls": False},
#     {"name": "Multi-Axle Modular Trailer", "max_length": 30, "max_width": 5.0, "max_height": 5.5, "max_weight": 500000, "cost_per_km": 180, "cost_per_tkm": 2.5, "has_sidewalls": False},
#     {"name": "Container Trailer (40 ft)", "max_length": 12.2, "max_width": 2.6, "max_height": 2.9, "max_weight": 28000, "cost_per_km": 42, "cost_per_tkm": 3.8, "has_sidewalls": True}
# ]

ODC_LIMITS = {"length": 12.0, "width": 2.6, "height": 3.8, "weight": 40000}  # weight in kg

fragile_items = {
    "Precision Instrument": "Bubble Wrap + Custom Crating",
    "Glass Equipment": "Wooden Crate + Shock Absorbers",
    "Control Panel": "Shrink Wrap + Cushioning",
    "Rotating Machinery": "Custom Industrial Packing",
    "Fragile Custom Assembly": "Bubble Wrap + Wooden Crate"
}

def classify_vehicle(name):
    if "LCV" in name or "14 ft" in name:
        return "🟢 Light Commercial"
    elif "22 ft" in name or "Container" in name or "Tanker" in name:
        return "🟡 Medium Duty"
    elif "Flatbed" in name or "Low Bed" in name:
        return "🟠 Heavy Duty"
    elif "Multi-Axle" in name:
        return "🔴 Oversize Modular"
    else:
        return "🔧 Custom Haulage"

def check_odc(length, width, height, weight):
    exceeded = {}
    if length > ODC_LIMITS["length"]:
        exceeded["Length"] = f"{length} m > {ODC_LIMITS['length']} m"
    if width > ODC_LIMITS["width"]:
        exceeded["Width"] = f"{width} m > {ODC_LIMITS['width']} m"
    if height > ODC_LIMITS["height"]:
        exceeded["Height"] = f"{height} m > {ODC_LIMITS['height']} m"
    if weight > ODC_LIMITS["weight"]:
        exceeded["Weight"] = f"{weight} kg > {ODC_LIMITS['weight']} kg"
    return exceeded

def compute_best_vehicle(length, width, height, weight, quantity, distance_km, allow_stacking, cargo_type):
    volume = length * width * height
    total_weight = weight * quantity  # in kg
    results = []

    for v in vehicle_types:
        if not v["has_sidewalls"] and cargo_type in fragile_items:
            continue
        
        # Skip if cargo does not physically fit
        if length > v["max_length"] or width > v["max_width"] or height > v["max_height"] or weight > v["max_weight"]:
            continue

        # Calculate how many cargo units can physically fit
        fit_length = math.floor(v["max_length"] / length)
        fit_width = math.floor(v["max_width"] / width)
        fit_height = math.floor(v["max_height"] / height)

        if allow_stacking:
            max_units_vol = max(1, fit_length * fit_width * fit_height)
        else:
            max_units_vol = max(1, fit_length * fit_width)

        # Calculate how many units fit by weight
        max_units_wt = math.floor(v["max_weight"] / weight) if weight > 0 else quantity


        max_units = max(1, min(max_units_vol, max_units_wt))
        trucks_needed = math.ceil(quantity / max_units)
        avg_weight_per_truck_tonnes = (total_weight / trucks_needed) / 1000

        total_cost = trucks_needed * (
            v["cost_per_km"] * distance_km +
            v["cost_per_tkm"] * avg_weight_per_truck_tonnes * distance_km
        )

        results.append({
            "vehicle": v["name"],
            "class": classify_vehicle(v["name"]),
            "num_trucks": trucks_needed,
            "total_cost": round(total_cost, 2),
            "max_units_per_truck": max_units
        })

    return sorted(results, key=lambda x: x["total_cost"])

# ----------------------------
# Streamlit App Starts
# ----------------------------
st.set_page_config(page_title="Vehicle Selector – Artson", layout="centered")
st.title("🚛 Vehicle Recommendation Tool – Artson Logistics")
st.caption("Built for SCM use-cases. Made by Pushkin Dugam.")
st.markdown("---")

# Inputs
col1, col2 = st.columns(2)
with col1:
    length = st.number_input("Cargo Length (m)", value=2.2, min_value=0.1)
    width = st.number_input("Cargo Width (m)", value=1.2, min_value=0.1)
    height = st.number_input("Cargo Height (m)", value=1.8, min_value=0.1)
    weight = st.number_input("Cargo Weight (kg)", value=1200.0, min_value=0.01)
with col2:
    quantity = st.number_input("Quantity of Cargo Units", value=4, min_value=1, step=1)
    distance_km = st.number_input("Transport Distance (km)", value=800, min_value=1)
    cargo_type = st.selectbox("Cargo Type", [
        "Standard Steel Fabrication", "Precision Instrument", "Glass Equipment",
        "Control Panel", "Pipeline", "Rotating Machinery", "Fragile Custom Assembly"
    ], index=3)
    stacking = st.checkbox("Allow Vertical Stacking (if feasible)", value=False)

st.markdown("---")

if st.button("🔍 Recommend Vehicle"):
    results = compute_best_vehicle(length, width, height, weight, quantity, distance_km, stacking, cargo_type)

    if not results:
        st.error("❌ No suitable vehicle found.")
    else:
        best = results[0]
        st.success(f"✅ **Recommended Vehicle:** {best['vehicle']}")
        st.markdown(f"- **Class:** {best['class']}")
        st.markdown(f"- **Number of Vehicles Required:** {best['num_trucks']}")
        st.markdown(f"- **Estimated Transport Cost:** ₹ {best['total_cost']}")
        st.markdown(f"- **Max Units per Vehicle:** {best['max_units_per_truck']}")

        odc_exceeded = check_odc(length, width, height, weight)
        if odc_exceeded:
            st.warning("⚠️ **ODC Alert:** This cargo exceeds standard transport limits and qualifies as **Over Dimensional Cargo (ODC)**.")
            st.markdown("### ❌ Dimensions Exceeding Limits:")
            for key, msg in odc_exceeded.items():
                st.markdown(f"- **{key}**: {msg}")
            st.markdown("🔧 Please arrange for **special permits**, route clearance, and escort vehicles.")
        else:
            st.info("📦 This cargo is **within standard CMVR transport limits** and does **not** qualify as ODC.")

        if cargo_type in fragile_items:
            st.info(f"📦 Fragile Cargo – Suggested Packaging: **{fragile_items[cargo_type]}**")

        st.subheader("📊 Cost Comparison by Vehicle Type")
        df = pd.DataFrame(results)
        chart = alt.Chart(df).mark_bar().encode(
            y=alt.Y("vehicle:N", title="Vehicle Type", sort="-x"),
            x=alt.X("total_cost:Q", title="Estimated Cost ₹"),
            color="class:N",
            tooltip=["vehicle", "total_cost", "num_trucks"]
        ).properties(height=400)
        st.altair_chart(chart, use_container_width=True)

        st.subheader("🔄 Alternate Vehicle Options")
        st.dataframe(df.style.highlight_min(subset=["total_cost"], color="lightgreen", axis=0))

# Sidebar
with st.sidebar:
    st.image(
        "https://github.com/Pushkindugam/Artson-Vehicle-Selector/blob/main/artson_logo.png?raw=true",
        use_container_width=True,
        caption="Artson Engineering Ltd."
    )
    st.markdown("## 🚛 ODC Guidelines")
    st.markdown("""
    **ODC (Over Dimensional Cargo)** refers to cargo exceeding standard  
    dimensions. This tool helps ensure **safe & compliant** transport.
    """)
    st.markdown("### 📏 Standard ODC Limits")
    st.markdown("""
    - **Max Length:** 12.0 m  
    - **Max Width:** 2.6 m  
    - **Max Height:** 3.8 m  
    - **Max Weight:** 40,000 kg
    """)
    st.markdown("---")
    st.markdown("### 🛠️ Artson SCM Team – 2025")
    st.markdown("*by **Pushkin Dugam***")
    st.markdown("[🔗 GitHub](https://github.com/Pushkindugam/Artson-Vehicle-Selector)")








# import streamlit as st
# import pandas as pd
# import altair as alt

# st.set_page_config(
#     layout="centered",
#     initial_sidebar_state="expanded",
#     page_title="Vehicle Selector – Artson",
#     page_icon="🚚"
# )

# # 🚚 Full vehicle reference table (EPC)
# vehicle_types = [
#     {"name": "LCV Truck (Light Commercial Vehicle)", "max_length": 4.2, "max_width": 2.0, "max_height": 2.2, "max_weight": 3},
#     {"name": "14 ft Truck (Standard)", "max_length": 6, "max_width": 2.5, "max_height": 2.5, "max_weight": 10},
#     {"name": "22 ft Truck / Semi Trailer", "max_length": 12, "max_width": 2.6, "max_height": 3, "max_weight": 20},
#     {"name": "Flatbed Trailer (40 ft)", "max_length": 18, "max_width": 2.6, "max_height": 3.5, "max_weight": 30},
#     {"name": "Flatbed Trailer (60 ft)", "max_length": 25, "max_width": 2.6, "max_height": 3.5, "max_weight": 35},
#     {"name": "Semi Low Bed Trailer", "max_length": 18, "max_width": 3.0, "max_height": 3.5, "max_weight": 40},
#     {"name": "Low Bed Trailer", "max_length": 18, "max_width": 3.5, "max_height": 4.2, "max_weight": 80},
#     {"name": "Multi-Axle Modular Hydraulic Trailer", "max_length": 30, "max_width": 5.0, "max_height": 5.5, "max_weight": 500},
#     {"name": "Container Trailer (40 ft)", "max_length": 12.2, "max_width": 2.6, "max_height": 2.9, "max_weight": 28},
#     {"name": "Tanker Truck", "max_length": 12, "max_width": 2.5, "max_height": 3.0, "max_weight": 25}
# ]

# ODC_LIMITS = {
#     "length": 12.0,
#     "width": 2.6,
#     "height": 3.8,
#     "weight": 40
# }

# def check_odc(length, width, height, weight):
#     exceeded = {}
#     if length > ODC_LIMITS["length"]:
#         exceeded["Length"] = f"{length} m > {ODC_LIMITS['length']} m"
#     if width > ODC_LIMITS["width"]:
#         exceeded["Width"] = f"{width} m > {ODC_LIMITS['width']} m"
#     if height > ODC_LIMITS["height"]:
#         exceeded["Height"] = f"{height} m > {ODC_LIMITS['height']} m"
#     if weight > ODC_LIMITS["weight"]:
#         exceeded["Weight"] = f"{weight} t > {ODC_LIMITS['weight']} t"
#     return exceeded

# def select_vehicle_type(length_m, width_m, height_m, weight_tonnes):
#     for vehicle in vehicle_types:
#         if (length_m <= vehicle["max_length"] and
#             width_m <= vehicle["max_width"] and
#             height_m <= vehicle["max_height"] and
#             weight_tonnes <= vehicle["max_weight"]):
#             return vehicle["name"]
#     return "Custom/Heavy Haulage Required (Contact Transport Planner)"

# def get_vehicle_specs(name):
#     for v in vehicle_types:
#         if v["name"] == name:
#             return v
#     return None

# def classify_vehicle(name):
#     if "LCV" in name or "14 ft" in name:
#         return "🟢 Light Commercial"
#     elif "22 ft" in name or "Container" in name or "Tanker" in name:
#         return "🟡 Medium Duty"
#     elif "Flatbed" in name or "Low Bed" in name:
#         return "🟠 Heavy Duty"
#     elif "Multi-Axle" in name:
#         return "🔴 Oversize Modular"
#     else:
#         return "🔧 Custom Haulage"

# # ----------------------------
# # 🧱 Streamlit UI
# # ----------------------------

# st.title("🚚 Vehicle Recommendation Tool – Artson Logistics")

# st.markdown("""
# This tool helps select the **most suitable vehicle** for transporting project cargo based on:
# - Length × Width × Height (in meters)
# - Weight (in tonnes)
# - Cargo characteristics (fragility, packaging, etc.)
# """)

# # 📥 Dimension Inputs
# length = st.number_input("📏 Cargo Length (m)", value=6.0, step=0.1)
# width = st.number_input("📐 Cargo Width (m)", value=2.5, step=0.1)
# height = st.number_input("📦 Cargo Height (m)", value=2.5, step=0.1)
# weight = st.number_input("⚖️ Cargo Weight (tonnes)", value=10.0, step=0.1)

# # 📦 Cargo Type & Handling Requirements
# cargo_type = st.selectbox("📦 Cargo Type", [
#     "Standard Steel Fabrication",
#     "Precision Instrument",
#     "Glass Equipment",
#     "Control Panel",
#     "Pipeline",
#     "Rotating Machinery",
#     "Fragile Custom Assembly"
# ])

# # Define rules for fragility and packaging
# fragile_items = {
#     "Precision Instrument": "Bubble Wrap + Custom Crating",
#     "Glass Equipment": "Wooden Crate + Shock Absorbers",
#     "Control Panel": "Shrink Wrap + Cushioning",
#     "Rotating Machinery": "Custom Industrial Packing",
#     "Fragile Custom Assembly": "Bubble Wrap + Wooden Crate"
# }

# is_fragile = cargo_type in fragile_items
# packaging_suggestion = fragile_items.get(cargo_type, "Not Needed")

# # 🔍 Main Recommendation Section
# if st.button("🔍 Recommend Vehicle"):

#     # 1. Vehicle Type & Class
#     vehicle = select_vehicle_type(length, width, height, weight)
#     st.success(f"✅ **Recommended Vehicle Type:** {vehicle}")
#     st.markdown(f"**Class:** {classify_vehicle(vehicle)}")

#     # 2. ODC Alert
#     odc_exceeded = check_odc(length, width, height, weight)
#     if odc_exceeded:
#         st.warning("⚠️ **ODC Alert:** This cargo exceeds standard transport limits and qualifies as **Over Dimensional Cargo (ODC)**.")
#         st.markdown("### ❌ Dimensions Exceeding Limits:")
#         for key, msg in odc_exceeded.items():
#             st.markdown(f"- **{key}**: {msg}")
#         st.markdown("🔧 Please arrange for **special permits**, route clearance, and escort vehicles.")
#     else:
#         st.info("📦 This cargo is **within standard CMVR transport limits** and does **not** qualify as ODC.")

#     # 3. Packaging Suggestion
#     if is_fragile:
#         st.warning("⚠️ This cargo is **fragile** and requires **special packaging**.")
#         st.markdown(f"**📦 Suggested Packaging:** `{packaging_suggestion}`")
#     else:
#         st.info("✅ This cargo is **non-fragile** and does **not** require special packaging.")

#     # 4. Vehicle Utility Chart
#     specs = get_vehicle_specs(vehicle)
#     if specs:
#         st.markdown("### 🚛 Vehicle Capacity Utilization")

#         utilization_data = pd.DataFrame({
#             'Parameter': ['Length', 'Width', 'Height', 'Weight'],
#             'Cargo': [length, width, height, weight],
#             'Capacity': [specs["max_length"], specs["max_width"], specs["max_height"], specs["max_weight"]]
#         })

#         utilization_data["Utilization (%)"] = (utilization_data["Cargo"] / utilization_data["Capacity"] * 100).round(1)
#         utilization_data["Remaining (%)"] = 100 - utilization_data["Utilization (%)"]

#         bar_data = utilization_data.melt(
#             id_vars="Parameter",
#             value_vars=["Utilization (%)", "Remaining (%)"],
#             var_name="Type",
#             value_name="Percentage"
#         )

#         chart = alt.Chart(bar_data).mark_bar().encode(
#             y=alt.Y("Parameter:N", sort=None),
#             x=alt.X("Percentage:Q", stack="normalize"),
#             color=alt.Color("Type:N",
#                             scale=alt.Scale(
#                                 domain=["Utilization (%)", "Remaining (%)"],
#                                 range=["#1f77b4", "#d3d3d3"]),
#                             sort=["Utilization (%)", "Remaining (%)"]),
#             tooltip=["Type", "Percentage"]
#         ).properties(
#             width=600,
#             height=200,
#             title="🚛 Cargo Fill % of Vehicle Capacity"
#         )

#         st.altair_chart(chart)

# # 5. Vehicle Reference Table
# with st.expander("📚 View All Vehicle Types"):
#     st.table(pd.DataFrame(vehicle_types))

# with st.sidebar:
#     st.image(
#         "https://github.com/Pushkindugam/Artson-Vehicle-Selector/blob/main/artson_logo.png?raw=true",
#         use_container_width=True,
#         caption="Artson Engineering Ltd."
#     )

#     st.markdown("## 🚛 ODC Guidelines")
#     st.markdown("""
#     **ODC (Over Dimensional Cargo)** refers to cargo exceeding standard  
#     dimensions. This tool helps ensure **safe & compliant** transport.
#     """)

#     st.markdown("### 📏 Standard ODC Limits")
#     st.markdown("""
#     - **Max Length:** 12.0 m  
#     - **Max Width:** 2.6 m  
#     - **Max Height:** 3.8 m  
#     - **Max Weight:** 40,000 kg
#     """)

#     st.markdown("---")
#     st.markdown("### 🛠️ Artson SCM Team – 2025")
#     st.markdown("*by **Pushkin Dugam***")
#     st.markdown("[🔗 GitHub](https://github.com/Pushkindugam/Artson-Vehicle-Selector)")














# with st.sidebar:
#     st.markdown("## 📘 ODC Transport Guidelines")
#     st.json(ODC_LIMITS)

#     st.markdown("---")
#     st.markdown("### 🛠️ Built by Artson SCM Team – 2025")
#     st.markdown("*by **Pushkin Dugam***")

#     st.image("artson_logo.png", use_container_width=True, caption="Artson Engineering Ltd.")





# import streamlit as st
# import pandas as pd
# import altair as alt

# # 🚚 Full vehicle reference table (EPC)
# vehicle_types = [
#     {"name": "LCV Truck (Light Commercial Vehicle)", "max_length": 4.2, "max_width": 2.0, "max_height": 2.2, "max_weight": 3},
#     {"name": "14 ft Truck (Standard)", "max_length": 6, "max_width": 2.5, "max_height": 2.5, "max_weight": 10},
#     {"name": "22 ft Truck / Semi Trailer", "max_length": 12, "max_width": 2.6, "max_height": 3, "max_weight": 20},
#     {"name": "Flatbed Trailer (40 ft)", "max_length": 18, "max_width": 2.6, "max_height": 3.5, "max_weight": 30},
#     {"name": "Flatbed Trailer (60 ft)", "max_length": 25, "max_width": 2.6, "max_height": 3.5, "max_weight": 35},
#     {"name": "Semi Low Bed Trailer", "max_length": 18, "max_width": 3.0, "max_height": 3.5, "max_weight": 40},
#     {"name": "Low Bed Trailer", "max_length": 18, "max_width": 3.5, "max_height": 4.2, "max_weight": 80},
#     {"name": "Multi-Axle Modular Hydraulic Trailer", "max_length": 30, "max_width": 5.0, "max_height": 5.5, "max_weight": 500},
#     {"name": "Container Trailer (40 ft)", "max_length": 12.2, "max_width": 2.6, "max_height": 2.9, "max_weight": 28},
#     {"name": "Tanker Truck", "max_length": 12, "max_width": 2.5, "max_height": 3.0, "max_weight": 25}
# ]

# # 🚨 Standard limits as per CMVR (Beyond this = ODC)
# ODC_LIMITS = {
#     "length": 12.0,
#     "width": 2.6,
#     "height": 3.8,
#     "weight": 40
# }

# def check_odc(length, width, height, weight):
#     exceeded = {}
#     if length > ODC_LIMITS["length"]:
#         exceeded["Length"] = f"{length} m > {ODC_LIMITS['length']} m"
#     if width > ODC_LIMITS["width"]:
#         exceeded["Width"] = f"{width} m > {ODC_LIMITS['width']} m"
#     if height > ODC_LIMITS["height"]:
#         exceeded["Height"] = f"{height} m > {ODC_LIMITS['height']} m"
#     if weight > ODC_LIMITS["weight"]:
#         exceeded["Weight"] = f"{weight} t > {ODC_LIMITS['weight']} t"
#     return exceeded

# def select_vehicle_type(length_m, width_m, height_m, weight_tonnes):
#     for vehicle in vehicle_types:
#         if (length_m <= vehicle["max_length"] and
#             width_m <= vehicle["max_width"] and
#             height_m <= vehicle["max_height"] and
#             weight_tonnes <= vehicle["max_weight"]):
#             return vehicle["name"]
#     return "Custom/Heavy Haulage Required (Contact Transport Planner)"

# def get_vehicle_specs(name):
#     for v in vehicle_types:
#         if v["name"] == name:
#             return v
#     return None

# def classify_vehicle(name):
#     if "LCV" in name or "14 ft" in name:
#         return "🟢 Light Commercial"
#     elif "22 ft" in name or "Container" in name or "Tanker" in name:
#         return "🟡 Medium Duty"
#     elif "Flatbed" in name or "Low Bed" in name:
#         return "🟠 Heavy Duty"
#     elif "Multi-Axle" in name:
#         return "🔴 Oversize Modular"
#     else:
#         return "🔧 Custom Haulage"

# # 🧱 UI
# st.title("🚚 Vehicle Recommendation Tool – Artson Logistics")
# st.markdown("""
# This tool helps select the **most suitable vehicle** for transporting project cargo based on:
# - Length × Width × Height (in meters)
# - Weight (in tonnes)

# It also checks if the cargo qualifies as **ODC (Over Dimensional Cargo)** as per CMVR rules.
# """)

# # 📥 Inputs
# length = st.number_input("📏 Cargo Length (m)", value=6.0, step=0.1)
# width = st.number_input("📐 Cargo Width (m)", value=2.5, step=0.1)
# height = st.number_input("📦 Cargo Height (m)", value=2.5, step=0.1)
# weight = st.number_input("⚖️ Cargo Weight (tonnes)", value=10.0, step=0.1)

# # 🔍 Run matching
# if st.button("🔍 Recommend Vehicle"):
#     vehicle = select_vehicle_type(length, width, height, weight)
#     st.success(f"✅ **Recommended Vehicle Type:** {vehicle}")
#     st.markdown(f"**Class:** {classify_vehicle(vehicle)}")

#     specs = get_vehicle_specs(vehicle)
#     if specs:
#         st.markdown("### 📊 Vehicle Specifications:")
#         st.table({
#             "Max Length (m)": [specs["max_length"]],
#             "Max Width (m)": [specs["max_width"]],
#             "Max Height (m)": [specs["max_height"]],
#             "Max Weight (t)": [specs["max_weight"]]
#         })

#         # 📊 Utilization Bar Chart: Cargo as % of Vehicle Capacity
#         utilization_data = pd.DataFrame({
#             'Parameter': ['Length', 'Width', 'Height', 'Weight'],
#             'Cargo': [length, width, height, weight],
#             'Capacity': [specs["max_length"], specs["max_width"], specs["max_height"], specs["max_weight"]]
#         })

#         # Calculate % utilization
#         utilization_data["Utilization (%)"] = (utilization_data["Cargo"] / utilization_data["Capacity"] * 100).round(1)
#         utilization_data["Remaining (%)"] = 100 - utilization_data["Utilization (%)"]

#         # Prepare long-form for stacked bar
#         bar_data = utilization_data.melt(
#             id_vars="Parameter",
#             value_vars=["Utilization (%)", "Remaining (%)"],
#             var_name="Type",
#             value_name="Percentage"
#         )

#         chart = alt.Chart(bar_data).mark_bar().encode(
#         y=alt.Y("Parameter:N", sort=None),
#         x=alt.X("Percentage:Q", stack="normalize"),
#         color=alt.Color("Type:N",
#         scale=alt.Scale(
#             domain=["Utilization (%)", "Remaining (%)"],
#             range=["#1f77b4", "#d3d3d3"]
#         )
#         ),
#         tooltip=["Type", "Percentage"]
#         ).properties(
#         width=600,
#         height=200,
#         title="🚛 Cargo Fill % of Vehicle Capacity"
#         )

#         st.altair_chart(chart)

#     # ODC Alert
#     odc_exceeded = check_odc(length, width, height, weight)
#     if odc_exceeded:
#         st.warning("⚠️ **ODC Alert:** This cargo exceeds standard transport limits and qualifies as **Over Dimensional Cargo (ODC)**.")
#         st.markdown("### ❌ Dimensions Exceeding Limits:")
#         for key, msg in odc_exceeded.items():
#             st.markdown(f"- **{key}**: {msg}")
#         st.markdown("🔧 Please arrange for **special permits**, route clearance, and escort vehicles.")
#     else:
#         st.info("📦 This cargo is **within standard CMVR transport limits** and does **not** qualify as ODC.")

# # Optional Expandable Reference
# with st.expander("📚 View All Vehicle Types"):
#     st.table(pd.DataFrame(vehicle_types))

# # Sidebar
# with st.sidebar:
#     st.markdown("### 📘 ODC Limits (as per CMVR)")
#     st.write(ODC_LIMITS)
#     st.markdown("---")
#     st.markdown("🛠️ Built by Artson SCM Team – 2025")





























