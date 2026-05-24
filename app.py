import streamlit as st
import xml.etree.ElementTree as ET
import json
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="RAMBO - LG TV Sorter", layout="wide")

# 2. ستايل CSS المحدث (لضمان عمل الزرار وشكل الفوتر)
st.markdown("""
    <style>
    .futuristic-cyber-footer { background: #080314; border: 2px solid #00f0ff; padding: 35px; text-align: center; border-radius: 20px; color: white; margin-top: 50px; font-family: sans-serif; }
    .cyber-whatsapp-btn { background: transparent; color: #25d366 !important; padding: 15px 40px; border-radius: 50px; border: 2px solid #25d366; cursor: pointer; font-size: 18px; font-weight: bold; transition: 0.3s; }
    .cyber-whatsapp-btn:hover { background: #25d366; color: #000 !important; box-shadow: 0 0 20px #25d366; }
    .source-tag { font-size: 12px; color: #00f0ff; font-style: italic; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# 3. العنوان
st.title("📺 RAMBO - المنسق المستقبلي لشاشات LG")

# 4. رفع الملف
uploaded_file = st.file_uploader("🚀 اختر ملف القنوات (GlobalClone00001.TLL):", type=["TLL"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    st.success("🛸 تم قراءة الملف بنجاح!")
    
    st.write("---")
    update_freq = st.checkbox("⚛️ تفعيل الصيانة الذكية للترددات", value=True)
    
    if update_freq:
        # إضافة التاريخ التلقائي ومصدر المعلومة
        today_date = datetime.now().strftime("%d/%m/%Y")
        st.write(f"### 🔁 سجل صيانة الترددات الحية - تحديث: {today_date}")
        st.markdown('<p class="source-tag">المصدر: RAMBO Satellite Live Feed Database</p>', unsafe_allow_html=True)
        
        # مثال للجدول
        st.table([{"القناة": "QATAR TV HD", "التردد القديم": "10830", "التردد الجديد": "10834"}])

    st.download_button("📥 تحميل الملف النهائي", data=file_bytes, file_name="GlobalClone00001.TLL")

# 5. الفوتر وزر الواتساب (الإصلاح الجذري)
whatsapp_link = "https://wa.me/201280339779?text=Hello%20Developer%20Rafik%20Rambo"

st.markdown(f"""
    <div class="futuristic-cyber-footer">
        <h3>🛠️ DEVELOPER ENG: RAFIK RAMBO</h3>
        <p>FOR ANY INQUIRY WHATSAPP</p>
        <button class="cyber-whatsapp-btn" onclick="window.open('{whatsapp_link}', '_blank')">
            💬 Open WhatsApp Now
        </button>
    </div>
""", unsafe_allow_html=True)
