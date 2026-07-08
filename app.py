import streamlit as st
import pandas as pd

# ฟังก์ชันจัดการติดตั้งและการเรียกใช้งาน Plotly เพื่อป้องกันการ Error บน Cloud
try:
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError:
    import os
    os.system('pip install plotly openpyxl')
    import plotly.express as px
    import plotly.graph_objects as go

# ตั้งค่าหน้าเว็บให้แสดงผลเต็มตา สวยงามสไตล์ Data Analyst
st.set_page_config(page_title="KPI Engineering Division 2026", layout="wide")

st.title("📊 KPI Engineering Division Dashboard 2026")
st.markdown("### ระบบประมวลผลข้อมูลและตัวชี้วัดประสิทธิภาพเชิงวิศวกรรมแบบโต้ตอบ (Interactive)")
st.markdown("---")

# ฐานข้อมูลสรุปเชิงวิเคราะห์ที่สกัดมาจากไฟล์จริงของคุณทั้ง 5 หัวข้อ
@st.cache_data
def load_kpi_perfect_data():
    # 1. ข้อมูลจาก Strategic KPI (Oil&Non-oil)
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
        "Q1_Actual": [132.41, 98.64, 102.42, 102.54, 96.00, 92.50, 100.00, 3.20]
    })
    
    # 2. ข้อมูลสรุปงบประมาณเปรียบเทียบจากไฟล์ Budget vs Actual Cost
    costs = pd.DataFrame({
        "Station": ["ถลาง3 (Oil)", "จักราช2 (Oil)", "บ้านโป่ง9 (Oil)", "วังน้ำเย็น (Oil)", "หาดใหญ่2 (Non-Oil)", "ฝาง2 (Non-Oil)", "แม่กรณ์ (Non-Oil)", "กาญจนบุรี2 (Non-Oil)"],
        "Budget_BOQ": [39735607, 28224966, 32150000, 27184407, 605786, 590253, 646364, 571738],
        "Actual_Cost": [37596009, 26991000, 32500000, 26500000, 604075, 583013, 645964, 565688]
    })
    costs["Variation"] = costs["Budget_BOQ"] - costs["Actual_Cost"]
    
    # 3. มูลค่าการประหยัดเงินจากไฟล์ VA/VE และ Cost Avoidance
    savings = pd.DataFrame({
        "Category": ["VA/VE (ลดการใช้ Sheet Pile)", "Cost Avoidance (งานบำรุงรักษา)", "Gain Liter (มูลค่าสะสมเทียบ GP)"],
        "Amount": [2245360.00, 6707439.84, 18144000.00]
    })
    return kpi_main, costs, savings

df_kpi, df_costs, df_savings = load_kpi_perfect_data()

# สร้างแถบเมนู 5 หัวข้อหลักด้วยระบบจำแนกข้อมูลอัจฉริยะ
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 1. Overview & Strategic Scorecard",
    "📅 2. Timeline & SLA Performance",
    "💰 3. Financial & Cost Management",
    "✨ 4. Quality Assurance (FPY & RFT)",
    "🌱 5. Value Engineering & Saving"
])

# --- TAB 1 ---
with tab1:
    st.subheader("📋 สรุปผลคะแนนตัวชี้วัดกลยุทธ์ภาพรวม")
    st.dataframe(df_kpi, use_container_width=True)
    fig1 = px.bar(df_kpi, x="KPI_Name", y=["Target_2026", "Q1_Actual"], barmode="group", title="เปรียบเทียบเป้าหมาย Target vs ผลงานจริง Q1 Actual (%)")
    st.plotly_chart(fig1, use_container_width=True)

# --- TAB 2 ---
with tab2:
    st.subheader("📅 กรอบเวลาการส่งมอบงานก่อสร้าง (SLA Pre-con & Construction)")
    st.info("💡 Insight: กลุ่มธุรกิจพลังงาน (Energy Business) ทำผลงานด้านเวลาได้โดดเด่นที่สุด สูงถึง 132.41% ของเป้าหมายแผนงาน")
    fig2 = px.bar(df_kpi.iloc[[0, 1]], x="KPI_Name", y="Q1_Actual", color="KPI_Name", text_auto=True)
    st.plotly_chart(fig2, use_container_width=True)

# --- TAB 3 ---
with tab3:
    st.subheader("💰 ประสิทธิภาพงบประมาณและการเบี่ยงเบนต้นทุนรายโครงการ")
    c1, c2 = st.columns(2)
    c1.metric("งบประมาณรวมที่อนุมัติ (BOQ Approved)", f"{df_costs['Budget_BOQ'].sum():,.2f} บาท")
    c2.metric("งบประมาณที่เซฟได้รวม (Positive Variance)", f"{df_costs['Variation'].sum():,.2f} บาท")
    fig3 = px.bar(df_costs, x="Station", y=["Budget_BOQ", "Actual_Cost"], barmode="group", title="งบประมาณเปรียบเทียบค่าใช้จ่ายจริงรายสถานี")
    st.plotly_chart(fig3, use_container_width=True)

# --- TAB 4 ---
with tab4:
    st.subheader("✨ อัตราส่วนงานผ่านเกณฑ์ในการตรวจสอบรอบแรก (First Pass Yield)")
    st.markdown("วัดเปอร์เซ็นต์งานก่อสร้างและรีโนเวทที่ผ่านเกณฑ์แบบ **ไม่มี Major Defect** ตั้งแต่การตรวจงวดแรก")
    for idx, row in df_kpi.iloc[[4, 5]].iterrows():
        st.write(f"📌 **{row['KPI_Name']}**")
        st.progress(float(row['Q1_Actual']/110))
        st.caption(f"ผลงานไตรมาสปัจจุบัน: {row['Q1_Actual']}% / เป้าหมายประจำปี: {row['Target_2026']}%")

# --- TAB 5 ---
with tab5:
    st.subheader("🌱 มูลค่าประหยัดจากการทำวิศวกรรมคุณค่า (VA/VE & Cost Saving)")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.plotly_chart(px.pie(df_savings, values="Amount", names="Category", title="สัดส่วนโครงสร้างการลดต้นทุน"), use_container_width=True)
    with col2:
        st.plotly_chart(px.bar(df_savings, x="Category", y="Amount", color="Category", text_auto=',.2f', title="มูลค่าตัวเงินสุทธิที่ประหยัดได้ (บาท)"), use_container_width=True)
    st.success(f"🎉 สรุปความสำเร็จ: ฝ่ายวิศวกรรมสามารถสร้างผลงานประหยัดและหลีกเลี่ยงต้นทุนสะสมรวมได้ทั้งสิ้น {df_savings['Amount'].sum():,.2f} บาท")
