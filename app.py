import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="KPI Engineering Dashboard 2026", layout="wide")

st.title("📊 KPI Engineering Division Interactive Dashboard")
st.markdown("### ระบบวิเคราะห์ข้อมูลผลการดำเนินงานและตัวชี้วัดประสิทธิภาพเชิงวิศวกรรม")

# ระบบจำลองข้อมูลผู้เชี่ยวชาญ (Data Analysis) จากไฟล์จริงของคุณ
@st.cache_data
def load_data():
    # โครงสร้างอ้างอิงจากไฟล์ KPI (Oil&Non-oil).csv ของคุณ
    kpi_data = {
        "KPI_Name": [
            "SLA PreCon & Const (Energy)", 
            "SLA PreCon & Const (Non-Oil)",
            "Budget vs Actual Cost (Oil)", 
            "Budget vs Actual Cost (Non-Oil)",
            "Quality Delivery FPY/RFT (Oil)", 
            "Quality Delivery FPY/RFT (Non-Oil)",
            "Internal Budget Control", 
            "VA/VE & Cost Avoidance"
        ],
        "Weight": [20, 15, 15, 20, 10, 10, 5, 5],
        "Target_2026": [110.0, 100.0, 105.0, 105.0, 100.0, 100.0, 100.0, 3.5],
        "Q1_Actual": [132.41, 98.64, 102.42, 102.54, 96.00, 92.50, 100.00, 3.20],
        "Score_Q1": [5.0, 4.0, 4.0, 4.0, 4.0, 3.0, 5.0, 4.0]
    }
    return pd.DataFrame(kpi_data)

df = load_data()

# สร้างแถบเมนู 5 หัวข้อหลัก
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 1. Overview & Scorecard",
    "📅 2. SLA & Timeline Performance",
    "💰 3. Budget & Cost Management",
    "✨ 4. Quality Assurance (FPY/RFT)",
    "🌱 5. VA/VE & Cost Saving"
])

with tab1:
    st.subheader("📋 ภาพรวมตัวชี้วัดผลงานเชิงกลยุทธ์ (Strategic Scorecard)")
    col1, col2, col3 = st.columns(3)
    col1.metric("น้ำหนักคะแนนรวม", "100%", "ครบถ้วนตามเกณฑ์")
    col2.metric("อัตรา FPY เฉลี่ย", "94.25%", "เป้าหมาย > 90%")
    col3.metric("มูลค่าประหยัดสะสม (Saving)", "27.09 ลบ.", "ทะลุเป้าหมายปี 2026")
    
    st.dataframe(df, use_container_width=True)
    
    fig = px.bar(df, x="KPI_Name", y=["Target_2026", "Q1_Actual"], barmode="group",
                 title="กราฟเปรียบเทียบเป้าหมายปี 2026 และผลงานจริงไตรมาส 1")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("📅 วิเคราะห์ระยะเวลาดำเนินงาน Pre-construction & Construction")
    st.info("💡 ข้อมูลจากชีตวิเคราะห์เวลา: โครงการ Oil ส่วนใหญ่เสร็จสิ้นเร็วกว่าแผน (Ahead) เฉลี่ย 9-12 วัน")
    df_sla = df.iloc[[0, 1]]
    fig_sla = px.bar(df_sla, x="KPI_Name", y="Q1_Actual", color="KPI_Name", text_auto=True)
    st.plotly_chart(fig_sla, use_container_width=True)

with tab3:
    st.subheader("💰 ประสิทธิภาพการบริหารงบประมาณและการควบคุมต้นทุน")
    df_cost = df.iloc[[2, 3]]
    fig_cost = px.line(df_cost, x="KPI_Name", y="Q1_Actual", markers=True, title="อัตราส่วน Budget / Actual (ยิ่งสูงกว่า 100% ยิ่งประหยัด)")
    st.plotly_chart(fig_cost, use_container_width=True)

with tab4:
    st.subheader("✨ ดัชนีคุณภาพการส่งมอบงานในครั้งแรก (First Pass Yield)")
    st.markdown("วัดเปอร์เซ็นต์งานก่อสร้างและปรับปรุงสาขาที่ผ่านเกณฑ์แบบ **No Major Defect** ตั้งแต่งวดแรก")
    df_q = df.iloc[[4, 5]]
    for idx, row in df_q.iterrows():
        st.write(f"**{row['KPI_Name']}**")
        st.progress(float(row['Q1_Actual']/110))

with tab5:
    st.subheader("🌱 งานวิศวกรรมคุณค่าและการหลีกเลี่ยงต้นทุน (VA/VE)")
    st.markdown("### สรุปความสำเร็จเชิงตัวเลข:")
    st.success("1. ปรับกระบวนการไม่ใช้ Sheet Pile ที่สาขาวังน้ำเย็น, ขอนแก่น13, และจักราช2 ประหยัดเงินรวม **2,245,360 บาท**")
    st.success("2. นวัตกรรมซ่อมบำรุงสร้างค่า Cost Avoidance ได้รวม **6,707,439.84 บาท**")
    st.success("3. โครงการ Gain Liter สร้างมูลค่าเทียบเท่า GP เป็นเงิน **18,144,000.00 บาท**")
