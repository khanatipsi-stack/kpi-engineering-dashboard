import os
import sys

# --- ส่วนพิเศษ: ตรวจสอบและติดตั้ง Library อัตโนมัติในระบบ Cloud ---
try:
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "plotly", "openpyxl"])
    import pandas as pd
    import px = px
    import plotly.graph_objects as go

import streamlit as st

# ตั้งค่าหน้า Dashboard เชิงลึก
st.set_page_config(page_title="KPI Engineering Division 2026", layout="wide")

st.title("📊 KPI Engineering Division Dashboard 2026")
st.markdown("### Interactive Data Analytics Dashboard (Expert Version)")
st.markdown("---")

# --- โหลดข้อมูลระดับผู้เชี่ยวชาญ (Data Analysis) จากไฟล์จริงของคุณ ---
@st.cache_data
def load_kpi_static_data():
    # โครงสร้างชุดข้อมูลอ้างอิงตรงจากไฟล์ New 4.Func Strategic KPI (ENG).csv และ KPI (Oil&Non-oil).csv ของคุณ
    kpi_main = pd.DataFrame({
        "No": [1, 2, 3, 4, 5, 6, 7, 8],
        "KPI_Name": [
            "SLA PreCon & Const (Energy Business)", 
            "SLA PreCon & Const (F&B Business)",
            "Budget vs Actual Cost (Energy/Non-Energy)", 
            "Budget vs Actual Cost (F&B)",
            "Quality Delivery FPY/RFT (Energy/Non-Energy)", 
            "Quality Delivery FPY/RFT (F&B)",
            "Internal Budget Control (GP)", 
            "VA/VE & Cost Avoidance Driven"
        ],
        "Weight": [20.0, 15.0, 15.0, 20.0, 10.0, 10.0, 5.0, 5.0],
        "Target_2026": [110.0, 100.0, 105.0, 105.0, 100.0, 100.0, 100.0, 3.50],
        "Q1_Actual": [132.41, 98.64, 102.42, 102.54, 96.00, 92.50, 100.00, 3.20],
        "Score_Q1": [5.0, 4.0, 4.0, 4.0, 4.0, 3.0, 5.0, 4.0]
    })
    
    # ข้อมูลสถิติเชิงลึก Budget vs Actual Cost
    costs = pd.DataFrame({
        "Station": ["ถลาง3 (Oil)", "จักราช2 (Oil)", "บ้านโป่ง9 (Oil)", "วังน้ำเย็น (Oil)", "หาดใหญ่2 (Non-Oil)", "ฝาง2 (Non-Oil)", "แม่กรณ์ (Non-Oil)", "กาญจนบุรี2 (Non-Oil)"],
        "Budget_BOQ": [39735607, 28224966, 32150000, 27184407, 605786, 590253, 646364, 571738],
        "Actual_Cost": [37596009, 26991000, 32500000, 26500000, 604075, 583013, 645964, 565688]
    })
    costs["Variation"] = costs["Budget_BOQ"] - costs["Actual_Cost"]
    
    # ข้อมูลการเซฟต้นทุนจากไฟล์ Oil&Non-oil VA/VE.csv และ Cost Avoidance.csv
    savings = pd.DataFrame({
        "Category": ["VA/VE (ลดการใช้ Sheet Pile)", "Cost Avoidance (งานซ่อมบำรุง)", "Gain Liter (มูลค่าเทียบเท่า GP)"],
        "Amount": [2245360.00, 6707439.84, 18144000.00]
    })
    return kpi_main, costs, savings

df_kpi, df_costs, df_savings = load_kpi_static_data()

# --- ส่วนจัดแสดงผลลัพธ์แยกตาม 5 หัวข้อหลัก ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 1. Overview & Strategic KPIs",
    "📅 2. Timeline & SLA Performance",
    "💰 3. Financial & Cost Management",
    "✨ 4. Quality Assurance (FPY & RFT)",
    "🌱 5. Value Engineering (VA/VE)"
])

# TAB 1
with tab1:
    st.subheader("📋 ภาพรวมผลงานตามตัวชี้วัดกลยุทธ์ประจำไตรมาส")
    st.dataframe(df_kpi, use_container_width=True)
    fig1 = px.bar(df_kpi, x="KPI_Name", y=["Target_2026", "Q1_Actual"], barmode="group", title="เปรียบเทียบ Target vs Q1 Actual (%)")
    st.plotly_chart(fig1, use_container_width=True)

# TAB 2
with tab2:
    st.subheader("📅 ประสิทธิภาพกรอบเวลา (SLA Pre-construction & Construction)")
    st.info("💡 ข้อมูลเชิงวิเคราะห์: โครงการส่วนใหญ่ทำเวลาได้ดีกว่าแผน (Ahead Days) โดยเฉพาะกลุ่ม Energy Business ที่ทำผลงานได้ถึง 132.41%")
    fig2 = px.bar(df_kpi.iloc[[0, 1]], x="KPI_Name", y="Q1_Actual", color="KPI_Name", text_auto=True)
    st.plotly_chart(fig2, use_container_width=True)

# TAB 3
with tab3:
    st.subheader("💰 ประสิทธิภาพการบริหารงบประมาณ (Budget vs Actual)")
    c1, c2 = st.columns(2)
    c1.metric("งบประมาณรวมตาม BOQ Approved", f"{df_costs['Budget_BOQ'].sum():,.2f} บาท")
    c2.metric("งบประมาณคงเหลือหลังจบโครงการ (Variance)", f"{df_costs['Variation'].sum():,.2f} บาท", delta="ประหยัดงบได้ตามเป้า")
    fig3 = px.bar(df_costs, x="Station", y=["Budget_BOQ", "Actual_Cost"], barmode="group", title="เปรียบเทียบรายสาขา")
    st.plotly_chart(fig3, use_container_width=True)

# TAB 4
with tab4:
    st.subheader("✨ คุณภาพการส่งมอบงานครั้งแรก (First Pass Yield / Right First Time)")
    st.markdown("ดัชนีวัดผลงานที่เสร็จสมบูรณ์โดยไม่มี **Major Defect** ในรอบการตรวจงวดแรก")
    for idx, row in df_kpi.iloc[[4, 5]].iterrows():
        st.write(f"📌 {row['KPI_Name']}")
        st.progress(float(row['Q1_Actual']/110))
        st.caption(f"ผลงานที่ทำได้จริง: {row['Q1_Actual']}% (เป้าหมาย 100%)")

# TAB 5
with tab5:
    st.subheader("🌱 นวัตกรรมคุณค่าและการลดต้นทุน (VA/VE & Cost Avoidance)")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.plotly_chart(px.pie(df_savings, values="Amount", names="Category"), use_container_width=True)
    with col2:
        st.plotly_chart(px.bar(df_savings, x="Category", y="Amount", color="Category", text_auto=',.2f'), use_container_width=True)
    st.success(f"🎉 สรุปมูลค่าที่ฝ่ายวิศวกรรมเซฟงบประมาณและ
