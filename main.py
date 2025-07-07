import streamlit as st
from datetime import datetime
from can_module import show_can_dashboard
from san_module import show_san_dashboard

# إعداد الصفحة
st.set_page_config(page_title="EGYPTAIR M&E Dashboard", layout="wide")

# رأس الصفحة الرسمي
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"""
        <div style='text-align: left; font-size: 22px; font-weight: bold; line-height: 1.6;'>
            EGYPTAIR M&E<br>
            Technical Services Directorate<br>
            Reliability Department<br>
            Date: <span style='font-weight: normal;'>{datetime.today().strftime('%Y-%m-%d')}</span>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.image("egyptair_logo.png", width=180)

st.markdown("---")
st.title("📊 Fleet Reliability Dashboard")

# اختيار الموديول
selected_module = st.selectbox(
    "اختر الموديول الذي تريد عرضه:",
    ["-- اختر --", "CAN - Component Alert Notice", "SAN - System Alert Notice", "MP - Maintenance Program", "Events"]
)

# عرض الموديول المختار
if selected_module.startswith("CAN"):
    show_can_dashboard()
elif selected_module.startswith("SAN"):
    show_san_dashboard()
elif selected_module.startswith("MP"):
    st.info("📋 Module MP تحت التطوير. سيتم إضافته قريبًا.")
elif selected_module.startswith("Events"):
    st.info("📊 Module Events تحت التطوير. سيتم إضافته قريبًا.")

# ✅ الإمضاء في نهاية الصفحة
st.markdown("---")
st.markdown("""
### ✨ Project Credits  
**Developed by:**  
- Eng. Mennat Allah Mostafa  
- Eng. Osama Ibrahim Beela  

**Supervised by:**  
- Eng. Hazem Fahmi El-Shafei  
Reliability Dept. Manager  
EGYPTAIR M&E
""")
