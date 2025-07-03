# 🚛 Artson Vehicle Selector – EPC Transport Planner

An intelligent transport logistics assistant for **Artson Engineering Ltd.**, built to assist EPC project teams in selecting the **right vehicle** for cargo transport based on size, weight, and packaging needs.

🔗 **Live App:**  
👉 [https://artson-vehicle-selector-xewufqpfkn32dzkeqlguk5.streamlit.app/](https://artson-vehicle-selector-xewufqpfkn32dzkeqlguk5.streamlit.app/)

---

## 📦 What This Tool Does

This Streamlit-powered tool enables **project engineers**, **site planners**, and **SCM professionals** to:

- Input **cargo dimensions** (Length × Width × Height) and **weight**
- Get an **instant recommendation** for the most suitable transport vehicle
- Check whether the cargo is **ODC (Over Dimensional Cargo)** as per CMVR limits
- Receive **packaging advice** for fragile items
- See a **cost comparison chart** across eligible vehicles
- Refer to an **expandable transport table** for all vehicle specs

---

## 📸 Screenshots

<!-- Screenshots will be added here -->

<!--
| 🔧 Input Interface | 📦 Output Recommendations |
|--------------------|---------------------------|
| ![Input](https://github.com/Pushkindugam/Artson-Vehicle-Selector/blob/main/V-S-input-screenshot.png?raw=true) | ![Output](https://github.com/Pushkindugam/Artson-Vehicle-Selector/blob/main/V-S-output-screenshot.png?raw=true) |
-->

---

## 🛠️ Key Features

| Feature                          | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| 📐 Dimension & weight input       | Easy-to-use input in meters and kilograms                                   |
| ⚙️ Intelligent vehicle selection | Picks optimal vehicle (LCV, 14-ft, 22-ft, 40-ft, LBT, MAHT, etc.)           |
| 🚨 ODC alert                      | Warns if cargo exceeds CMVR legal limits; flags need for permits            |
| 🧊 Fragile cargo packaging        | Suggests suitable packaging (Bubble Wrap, Wooden Crate, etc.)               |
| 📊 Cost comparison chart          | Visualizes estimated cost by vehicle type using Altair                      |
| 📋 Expandable vehicle table       | Browse specs of all supported transport types                               |
| 🌐 Streamlit-based UI             | No login required; accessible on any device                                 |

---

## 🧭 Use Cases

This tool supports EPC transport planning decisions related to:

- Route planning for large equipment  
- ODC and permit requirement identification  
- Packaging recommendations for delicate cargo  
- Vendor selection and vehicle capacity forecasting

---

## 🏗️ Built For

> **Artson Engineering Ltd. (A Tata Enterprise)**  
> *By Pushkin Dugam (B.Tech Mechanical, IIT Jodhpur)*

---

## 📤 Local Run Instructions

To run this tool on your local system:

```bash
git clone https://github.com/Pushkindugam/Artson-Vehicle-Selector.git
cd Artson-Vehicle-Selector
pip install -r requirements.txt
streamlit run streamlit_app.py
