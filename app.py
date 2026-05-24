import streamlit as st
import xml.etree.ElementTree as ET
import json
from datetime import datetime

# --- الإعدادات والستايل ---
st.set_page_config(page_title="RAMBO - LG Futuristic AI Sorter", layout="wide")
# [ضع هنا كود الـ CSS الخاص بك كما هو]

# --- دالة القراءة الذكية للملفين ---
def parse_tll_file(file_bytes):
    root = ET.fromstring(file_bytes)
    channels = []
    
    # 1. الموديل الجديد (32LH604U)
    items = root.findall(".//ITEM")
    if items:
        for item in items:
            name_node = item.find("vchName")
            freq_node = item.find("frequency")
            if name_node is not None:
                channels.append({
                    "channelName": name_node.text,
                    "frequency": freq_node.text if freq_node is not None else "0"
                })
        return channels, root, "NEW_MODEL"

    # 2. الموديل القديم (JSON)
    legacy_tag = root.find(".//legacybroadcast")
    if legacy_tag is not None:
        broadcast_data = json.loads(legacy_tag.text)
        return broadcast_data.get("channelList", []), root, "OLD_MODEL"
        
    return [], root, "UNKNOWN"

# --- الواجهة الرئيسية ---
st.title("📺 RAMBO - LG Futuristic AI Sorter")
uploaded_file = st.file_uploader("🚀 ارفع ملف القنوات (TLL):", type=["TLL"])

if uploaded_file is not None:
    channels, root, mode = parse_tll_file(uploaded_file.read())
    
    if mode == "UNKNOWN":
        st.error("⚠️ صيغة الملف غير معروفة.")
    else:
        st.success(f"🛸 تم فك التشفير بنجاح! (الوضع: {mode}) - القنوات: {len(channels)}")
        
        # --- هنا باقي اختياراتك اللي كانت مختفية ---
        st.write("---")
        
        # اختيارات التحديث
        col1, col2 = st.columns(2)
        with col1:
            update_freq = st.checkbox("⚛️ تفعيل تحديث الترددات", value=True)
        with col2:
            add_new_ch = st.checkbox("✨ إضافة قنوات جديدة تلقائياً", value=False)
            
        # محرك البحث
        st.write("### 🔍 محرك البحث")
        search = st.text_input("اكتب اسم القناة للبحث...")
        
        # منطقة الجدول والترتيب (هنا تضع منطقك القديم الذي كان يعرض الجداول والترتيب)
        # بما أن المتغير channels الآن موحد للموديلين، سيعمل الكود القديم الخاص بك معهما
        
        # زر التحميل
        st.download_button("📥 تحميل الملف النهائي", data=ET.tostring(root), file_name="GlobalClone00001.TLL")

# الفوتر وزر الواتساب
whatsapp_url = "https://wa.me/201280339779?text=Hello%20Developer%20Rafik%20Rambo"
st.markdown(f"""
    <div class="futuristic-cyber-footer">
        <h3>🛠️ DEVELOPER ENG: RAFIK RAMBO</h3>
        <a href="{whatsapp_url}" target="_blank" class="cyber-whatsapp-btn">💬 Open WhatsApp Now</a>
    </div>
""", unsafe_allow_html=True)
