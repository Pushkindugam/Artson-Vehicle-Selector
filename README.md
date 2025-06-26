# 🚛 Artson Vehicle Selector – EPC Transport Planner

An intelligent transport logistics assistant for **Artson Engineering Ltd.**, built to assist EPC project teams in selecting the **right vehicle** for cargo transport.

🔗 **Live App:**  
👉 [https://artson-vehicle-selector-xewufqpfkn32dzkeqlguk5.streamlit.app/](https://artson-vehicle-selector-xewufqpfkn32dzkeqlguk5.streamlit.app/)

---

## 📦 What This Tool Does

This Streamlit-powered tool allows **project engineers**, **site planners**, and **SCM professionals** to:

- Enter **cargo dimensions (Length × Width × Height)** and **weight**
- Instantly get a **vehicle recommendation** from real EPC transport options
- Check if the cargo qualifies as **ODC (Over Dimensional Cargo)** under CMVR
- Get **packaging suggestions** for fragile cargo types
- Visualize **vehicle capacity utilization**

---

## 🛠️ Features

| Feature                          | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| 📐 Dimension & weight input       | Easy-to-use interface in meters and tonnes                                  |
| ⚙️ Intelligent vehicle selection | Chooses from real-world vehicles (LCV, 14-ft, 22-ft, 40-ft, LBT, MAHT, etc.)|
| 🚨 ODC alert                      | Flags cargo that exceeds CMVR limits and advises on permits/escorts         |
| 🧊 Fragile cargo packaging        | Suggests protective packaging (Bubble wrap, Wooden crate, etc.)             |
| 📊 Capacity utilization chart     | Bar chart showing % fill of recommended vehicle                             |
| 📋 Expandable vehicle reference  | View full table of all supported vehicle types                              |
| 🌐 Streamlit UI                   | Deployed online; works instantly without login                              |

---

## 📸 Screenshots

### 🔧 Input Interface  
![Input Screenshot](V-S-input-screenshot.png)

### 📦 Output Recommendations  
![Output Screenshot](V-S-output-screenshot.png)

---

## 📘 Vehicle Logic

The app contains a curated reference table of commonly used EPC transport vehicles, including:

| Vehicle Type                             | Max Length | Max Width | Max Height | Max Weight |
|------------------------------------------|------------|-----------|------------|------------|
| LCV Truck (Light Commercial Vehicle)      | 4.2 m      | 2.0 m     | 2.2 m      | 3 T        |
| 14 ft Truck (Standard)                   | 6.0 m      | 2.5 m     | 2.5 m      | 10 T       |
| 22 ft Truck / Semi Trailer               | 12.0 m     | 2.6 m     | 3.0 m      | 20 T       |
| Flatbed Trailer (40 ft)                  | 18.0 m     | 2.6 m     | 3.5 m      | 30 T       |
| Flatbed Trailer (60 ft)                  | 25.0 m     | 2.6 m     | 3.5 m      | 35 T       |
| Semi Low Bed Trailer                     | 18.0 m     | 3.0 m     | 3.5 m      | 40 T       |
| Low Bed Trailer                          | 18.0 m     | 3.5 m     | 4.2 m      | 80 T       |
| Multi-Axle Modular Hydraulic Trailer     | 30.0 m     | 5.0 m     | 5.5 m      | 500 T      |
| Container Trailer (40 ft)                | 12.2 m     | 2.6 m     | 2.9 m      | 28 T       |
| Tanker Truck                             | 12.0 m     | 2.5 m     | 3.0 m      | 25 T       |

---

## 📘 ODC Limits (as per CMVR)

```json
{
  "length": 12,
  "width": 2.6,
  "height": 3.8,
  "weight": 40
}

