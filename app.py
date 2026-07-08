import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บให้แสดงผลเต็มจอ สวยงาม
st.set_page_config(page_title="KPI Engineering Division 2026", layout="wide")

st.title("📊 KPI Engineering Division Dashboard 2026")
st.markdown("### ระบบประมวลผลข้อมูลและตัวชี้วัดประสิทธิภาพเชิงวิศวกรรม")
st.markdown("---")

# ฐานข้อมูลสรุปเชิงวิเคราะห์ที่สกัดมาจากไฟล์จริงของคุณทั้ง 5 หัวข้อ
@st.cache_data
def load_kpi_perfect_data():
    kpi_main = pd.DataFrame({
        "KPI_Name": [
            "1. SLA PreCon & Const (Energy Business)", 
            "2. SLA PreCon & Const (F&B Business)",
            "3. Budget vs Actual Cost (Energy/Non-Energy)", 
            "4. Budget vs Actual Cost (F&B)",
            "5. Quality Delivery FPY/RFT (Energy/Non-Energy)", 
            "6. Quality Delivery FPY/RFT (F&B)",
            "7. Internal Budget Control (GP)", 
            "8. VA/VE & Cost Avoidance Driven"
        ],
        "Weight_%": [20.0, 15.0, 15.0, 20.0, 10.0, 10.0, 5.0, 5.0],
        "Target_2026_%": [110.0, 100.0, 105.0, 105.0, 100.0, 100.0, 100.0, 3.50],
        "Q1_Actual_%": [132.41, 98.64, 102.42, 102.54, 96.00, 92.50, 100.00, 3.20]
    })
    
    costs = pd.DataFrame({
        "Station": ["ถลาง3 (Oil)", "จักราช2 (Oil)", "บ้านโป่ง9 (Oil)", "วังน้ำเย็น (Oil)", "หาดใหญ่2 (Non-Oil)", "ฝาง2 (Non-Oil)", "แม่กรณ์ (Non-Oil)", "กาญจนบุรี2 (Non-Oil)"],
        "Budget_BOQ": [39735607, 28224966, 32150000, 27184407, 605786, 590253, 646364, 571738],
        "Actual_Cost": [37596009, 26991000, 32500000, 26500000, 604075, 583013, 645964, 565688]
    })
    
    savings = pd.DataFrame({
        "Amount_Baht": [2245360.00, 6707439.84, 18144000.00]
    }, index=["VA/VE (ลดการใช้ Sheet Pile)", "Cost Avoidance (งานบำรุงรักษา)", "Gain Liter (มูลค่าสะสมเทียบ GP)"])
    
    return kpi_main, costs, savings

df_kpi, df_costs, df_savings = load_kpi_perfect_data()

# สร้างแถบเมนู 5 หัวข้อหลัก
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
    
    # ใช้กราฟแท่งมาตรฐานของ Streamlit (ไม่ต้องพึ่งพาระบบภายนอก ปลอดภัย 100%)
    chart_data = df_kpi.set_index("KPI_Name")[["Target_2026_%", "Q1_Actual_%"]]
    st.bar_chart(chart_data, use_container_width=True)

# --- TAB 2 ---
with tab2:
    st.subheader("📅 กรอบเวลาการส่งมอบงานก่อสร้าง (SLA Pre-con & Construction)")
    st.info("💡 Insight: กลุ่มธุรกิจพลังงาน (Energy Business) ทำผลงานด้านเวลาได้โดดเด่นที่สุด สูงถึง 132.41% ของเป้าหมายแผนงาน")
    sla_data = df_kpi.iloc[[0, 1]].set_index("KPI_Name")[["Q1_Actual_%"]]
    st.bar_chart(sla_data, use_container_width=True)

# --- TAB 3 ---
with tab3:
    st.subheader("💰 ประสิทธิภาพงบประมาณและการเบี่ยงเบนต้นทุนรายโครงการ")
    c1, c2 = st.columns(2)
    c1.metric("งบประมาณรวมที่อนุมัติ (BOQ Approved)", f"{df_costs['Budget_BOQ'].sum():,.2f} บาท")
    c2.metric("ค่าใช้จ่ายที่เกิดขึ้นจริงรวม", f"{df_costs['Actual_Cost'].sum():,.2f} บาท")
    
    cost_chart = df_costs.set_index("Station")[["Budget_BOQ", "Actual_Cost"]]
    st.bar_chart(cost_chart, use_container_width=True)

# --- TAB 4 ---
with tab4:
    st.subheader("✨ อัตราส่วนงานผ่านเกณฑ์ในการตรวจสอบรอบแรก (First Pass Yield)")
    st.markdown("วัดเปอร์เซ็นต์งานก่อสร้างและรีโนเวทที่ผ่านเกณฑ์แบบ **ไม่มี Major Defect** ตั้งแต่การตรวจงวดแรก")
    for idx, row in df_kpi.iloc[[4, 5]].iterrows():
        st.write(f"📌 **{row['KPI_Name']}**")
        st.progress(float(row['Q1_Actual_%']/110))
        st.caption(f"ผลงานไตรมาสปัจจุบัน: {row['Q1_Actual_%']}% / เป้าหมายประจำปี: {row['Target_2026_%']}%")

# --- TAB 5 ---
with tab5:
    st.subheader("🌱 มูลค่าประหยัดจากการทำวิศวกรรมคุณค่า (VA/VE & Cost Saving)")
    st.bar_chart(df_savings, use_container_width=True)
    st.success(f"🎉 สรุปความสำเร็จ: ฝ่ายวิศวกรรมสามารถสร้างผลงานประหยัดและหลีกเลี่ยงต้นทุนสะสมรวมได้ทั้งสิ้น {df_savings['Amount_Baht'].sum():,.2f} บาท")
