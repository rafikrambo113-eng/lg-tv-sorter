import streamlit as st
import xml.etree.ElementTree as ET
import json
from datetime import datetime

# (هذا الكود هو "رامبو 2" - النسخة الداعمة للموديلين)

def parse_tll_file(file_bytes):
    root = ET.fromstring(file_bytes)
    channels = []
    
    # 1. محاولة القراءة بطريقة الـ 32 بوصة (عن طريق البحث عن ITEMS)
    items = root.findall(".//ITEM")
    if items:
        for item in items:
            name_node = item.find("vchName") # في الموديل اللي رفعته الاسم في vchName
            freq_node = item.find("frequency")
            if name_node is not None:
                channels.append({
                    "channelName": name_node.text,
                    "frequency": freq_node.text if freq_node is not None else "0",
                    "polarization": "H" # افتراضي للموديلات الجديدة
                })
        return channels, root, "NEW_MODEL"

    # 2. القراءة بالطريقة القديمة (JSON) للموديلات الكبيرة
    legacy_tag = root.find(".//legacybroadcast")
    if legacy_tag is not None:
        broadcast_data = json.loads(legacy_tag.text)
        return broadcast_data.get("channelList", []), root, "OLD_MODEL"
        
    return [], root, "UNKNOWN"

# --- الواجهة ---
st.title("📺 RAMBO - LG Futuristic AI Sorter (Dual-Mode)")
uploaded_file = st.file_uploader("ارفع ملف القنوات (يعمل مع كل الموديلات):", type=["TLL"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    channels, root, mode = parse_tll_file(file_bytes)
    
    if mode == "UNKNOWN":
        st.error("⚠️ صيغة الملف غير معروفة، يرجى التأكد من أن الملف سليم.")
    else:
        st.success(f"🛸 تم فك تشفير الملف بنجاح! (الوضع: {mode})")
        st.write(f"عدد القنوات المكتشفة: {len(channels)}")
        
        # هنا تكمل منطق الترتيب والفلترة الخاص بك...
        # الكود السابق كان يعتمد على `channels` كقائمة، وهذا التحديث يوحدها للموديلين.

# (ضع هنا باقي كود الفلترة، الترتيب، وزر التحميل كما كان في برنامجك)

# الفوتر الموحد
whatsapp_url = "https://wa.me/201280339779?text=Hello%20Developer%20Rafik%20Rambo"
st.markdown(f"""
    <div class="futuristic-cyber-footer">
        <h3>🛠️ DEVELOPER ENG: RAFIK RAMBO</h3>
        <a href="{whatsapp_url}" target="_blank" class="cyber-whatsapp-btn">💬 Open WhatsApp Now</a>
    </div>
""", unsafe_allow_html=True)
