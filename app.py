import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. ตั้งค่าหน้าเว็บหน้า Dashboard ให้กว้างและสวยงาม
st.set_page_config(page_title="KPI Engineering Division 2026", layout="wide")

st.title("📊 KPI Engineering Division Dashboard 2026")
st.markdown("### ระบบวิเคราะห์ข้อมูลและตัวชี้วัดประสิทธิภาพเชิงวิศวกรรม (Data Analytics Expert)")
st.markdown("---")

# 2. ฟังก์ชันจำลองการดึงและประมวลผลข้อมูลจากโครงสร้างไฟล์จริงของคุณ
@st.cache_data
def load_expert_data():
    # ข้อมูลจากโครงสร้าง Strategic KPI (Oil & Non-Oil)
    kpi_summary = pd.DataFrame({
        "No": [1, 2, 3, 4, 5, 6, 7, 8],
        "KPI_Name": [
            "SLA PreCon & Const (Energy)", "SLA PreCon & Const (Non-Oil)",
            "Budget vs Actual Cost (Oil)", "Budget vs Actual Cost (Non-Oil)",
            "Quality Delivery FPY/RFT (Oil)", "Quality Delivery FPY/RFT (Non-Oil)",
            "Internal Budget Control (GP)", "VA/VE and Cost Avoidance"
        ],
        "Weight": [20.0, 15.0, 15.0, 20.0, 10.0, 10.0, 5.0, 5.0],
        "Target_2026": [110.0, 100.0, 105.0, 105.0, 100.0, 100.0, 100.0, 3.5],
        "Q1_Actual": [132.41, 98.64, 102.42, 102.54, 96.00, 92.50, 100.00, 3.20],
        "Status": ["Beyond Achieved", "Achieved", "Over Achieved", "Over Achieved", "Achieved", "Achieved", "Achieved", "Achieved"]
    })
    
    # ข้อมูลจากโครงสร้างงบประมาณจริง (Budget vs Actual Cost)
    branch_costs = pd.DataFrame({
        "Station": ["ถลาง3 (Oil)", "จักราช2 (Oil)", "บ้านโป่ง9 (Oil)", "วังน้ำเย็น (Oil)", "หาดใหญ่2 (Non-Oil)", "ฝาง2 (Non-Oil)", "แม่กรณ์ (Non-Oil)", "กาญจนบุรี2 (Non-Oil)"],
        "Budget_BOQ": [39735607, 28224966, 32150000, 27184407, 605786, 590253, 646364, 571738],
        "Actual_Cost": [37596009, 26991000, 32500000, 26500000, 604075, 583013, 645964, 565688]
    })
    branch_costs["Variation"] = branch_costs["Budget_BOQ"] - branch_costs["Actual_Cost"]
    
    # ข้อมูลการเซฟคอสจริง (VA/VE & Cost Avoidance)
    savings = pd.DataFrame({
        "Category": ["VA/VE (ลดการใช้ Sheet Pile)", "Cost Avoidance (งานซ่อมบำรุง)", "Gain Liter (มูลค่าเทียบเท่า GP)"],
        "Amount": [2245360.00, 6707439.84, 18144000.00]
    })
    
    return kpi_summary, branch_costs, savings

kpi_summary, branch_costs, savings = load_expert_data()

# 3. แถบเมนูด้านซ้ายสำหรับกรองข้อมูล (Sidebar Filter)
st.sidebar.header("📌 ตัวกรองแดชบอร์ด")
selected_status = st.sidebar.multiselect(
    "กรองตามสถานะความสำเร็จ:",
    options=kpi_summary["Status"].unique(),
    default=kpi_summary["Status"].unique()
)
filtered_kpi = kpi_summary[kpi_summary["Status"].isin(selected_status)]

# 4. แบ่งหน้าจอเป็น 5 หัวข้อหลักแบบ Interactive Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 1. Overview & Strategic KPIs",
    "📅 2. Timeline & SLA Performance",
    "💰 3. Financial & Cost Management",
    "✨ 4. Quality Assurance (FPY & RFT)",
    "🌱 5. Value Engineering (VA/VE)"
])

# --- TAB 1: OVERVIEW ---
with tab1:
    st.subheader("📋 ตารางสรุปคะแนนเชิงกลยุทธ์ (Strategic Scorecard)")
    st.dataframe(filtered_kpi.style.background_gradient(cmap="Blues", subset=["Q1_Actual"]), use_container_width=True)
    
    fig_ov = px.bar(filtered_kpi, x="KPI_Name", y=["Target_2026", "Q1_Actual"], barmode="group",
                    title="กราฟเปรียบเทียบเป้าหมายปี 2026 กับผลงานจริงไตรมาส 1",
                    labels={"value": "เปอร์เซ็นต์ (%)", "variable": "ประเภทข้อมูล"})
    st.plotly_chart(fig_ov, use_container_width=True)

# --- TAB 2: TIMELINE & SLA ---
with tab2:
    st.subheader("📅 การวิเคราะห์ระยะเวลาการดำเนินงาน (Pre-con & Construction)")
    st.info("💡 ข้อมูลเชิงวิเคราะห์: จากไฟล์ข้อมูล Pre-con พบว่างานจัดทำผังและ BOQ ส่วนใหญ่ทำได้เร็วกว่ากรอบ SLA เฉลี่ย 8-15 วัน")
    
    df_sla = filtered_kpi[filtered_kpi["KPI_Name"].str.contains("SLA")]
    fig_sla = px.bar(df_sla, x="KPI_Name", y="Q1_Actual", color="Status", text_auto=True,
                     title="ประสิทธิภาพความเร็วการส่งมอบโครงการแยกตามประเภทธุรกิจ")
    st.plotly_chart(fig_sla, use_container_width=True)

# --- TAB 3: FINANCIAL & COST ---
with tab3:
    st.subheader("💰 การบริหารงบประมาณและควบคุมต้นทุนโครงการ")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("งบประมาณ BOQ รวม", f"{branch_costs['Budget_BOQ'].sum():,.2f} บาท")
    c2.metric("ค่าใช้จ่ายจริงรวม", f"{branch_costs['Actual_Cost'].sum():,.2f} บาท")
    c3.metric("งบประมาณคงเหลือ (เซฟได้)", f"{branch_costs['Variation'].sum():,.2f} บาท", delta="Positive Variance")
    
    st.markdown("---")
    fig_cost = px.bar(branch_costs, x="Station", y=["Budget_BOQ", "Actual_Cost"], barmode="group",
                      title="วิเคราะห์งบประมาณเปรียบเทียบค่าใช้จ่ายจริงรายสถานี (BOQ vs Actual Cost)")
    st.plotly_chart(fig_cost, use_container_width=True)

# --- TAB 4: QUALITY ASSURANCE ---
with tab4:
    st.subheader("✨ ดัชนีคุณภาพการส่งมอบงานในครั้งแรก (First Pass Yield)")
    st.markdown("สัดส่วนงานที่ผ่านเกณฑ์แบบ **No Major Defect** ทันทีหลังจากการเข้าตรวจสอบงวดแรก")
    
    df_q = filtered_kpi[filtered_kpi["KPI_Name"].str.contains("Quality")]
    for idx, row in df_q.iterrows():
        st.write(f"📊 **{row['KPI_Name']}**")
        st.progress(min(float(row["Q1_Actual"] / 110), 1.0))
        st.caption(f"ผลงานไตรมาส 1 ทำได้: **{row['Q1_Actual']}%** (เป้าหมายปี 2026 คือ {row['Target_2026']}%)")

# --- TAB 5: VALUE ENGINEERING ---
with tab5:
    st.subheader("🌱 การเพิ่มมูลค่าและการหลีกเลี่ยงต้นทุนสะสม (VA/VE)")
    
    col_v1, col_v2 = st.columns([1, 2])
    with col_v1:
        fig_pie = px.pie(savings, values="Amount", names="Category", title="สัดส่วนมูลค่าการเซฟคอสสะสม")
        st.plotly_chart(fig_pie, use_container_width=True)
    with col_v2:
        fig_save = px.bar(savings, x="Category", y="Amount", text_auto=',.2f', color="Category",
                          title="มูลค่าตัวเงินสุทธิที่ฝ่ายวิศวกรรมประหยัดได้จริง (บาท)")
        st.plotly_chart(fig_save, use_container_width=True)
        
    st.success(f"🎉 สรุปมูลค่าการประหยัดต้นทุนของฝ่ายวิศวกรรมสะสมรวมทั้งสิ้น: **{savings['Amount'].sum():,.2f}** บาท")
