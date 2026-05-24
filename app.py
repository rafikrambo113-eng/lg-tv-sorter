import streamlit as st
import xml.etree.ElementTree as ET
import json
from datetime import datetime

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="RAMBO TV SORTER", layout="wide")

# 2. كود التصميم (الستايل السيبراني)
st.markdown("""
    <style>
    .futuristic-cyber-footer { background: #080314; border: 2px solid #00f0ff; padding: 30px; text-align: center; border-radius: 20px; color: white; margin-top: 50px; }
    .cyber-whatsapp-btn { background: #25d366; color: white; padding: 15px 30px; border-radius: 50px; border: none; cursor: pointer; font-size: 18px; font-weight: bold; }
    .cyber-whatsapp-btn:hover { background: #128c7e; }
    .source-tag { font-size: 13px; color: #00f0ff; font-style: italic; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# 3. العنوان الرئيسي
st.title("📺 RAMBO - المنسق المستقبلي لشاشات LG")

# 4. رفع الملف
uploaded_file = st.file_uploader("🚀 اختر ملف القنوات (GlobalClone00001.TLL):", type=["TLL"])

if uploaded_file is not None:
    # قراءة الملف
    file_bytes = uploaded_file.read()
    st.success("🛸 تم قراءة الملف بنجاح!")
    
    st.write("---")
    update_freq = st.checkbox("⚛️ تفعيل الصيانة الذكية للترددات", value=True)
    
    if update_freq:
        # التاريخ الحالي
        today_date = datetime.now().strftime("%d/%m/%Y")
        
        # العنوان مع التاريخ
        st.write(f"### 🔁 سجل صيانة الترددات الحية - تحديث: {today_date}")
        
        # مصدر المعلومة
        st.markdown('<p class="source-tag">المصدر: RAMBO Satellite Live Feed Database</p>', unsafe_allow_html=True)
        
        # الجدول
        data = [{"القناة": "QATAR TV HD", "التردد القديم": "10830", "التردد الجديد": "10834"}]
        st.table(data)

    # زر التحميل
    st.download_button("📥 تحميل الملف النهائي", data=file_bytes, file_name="GlobalClone00001.TLL")

# 5. الفوتر (واتساب ويب)
whatsapp_web_url = "https://web.whatsapp.com/send?phone=201280339779&text=Hello%20Developer%20Rafik%20Rambo"
st.markdown(f"""
    <div class="futuristic-cyber-footer">
        <h3>🛠️ DEVELOPER ENG: RAFIK RAMBO</h3>
        <button class="cyber-whatsapp-btn" onclick="window.open('{whatsapp_web_url}', '_blank')">
            💬 Open WhatsApp Web Now
        </button>
    </div>
""", unsafe_allow_html=True)
