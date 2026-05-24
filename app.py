import streamlit as st
import xml.etree.ElementTree as ET
import json
from datetime import datetime

# --- دوال المعالجة والذكاء الاصطناعي ---
def ai_classify(channel_name):
    name = channel_name.upper()
    if any(w in name for w in ["CTV", "AGHAPY", "MESAT"]): return "⛪ قنوات مسيحية"
    if any(w in name for w in ["QURAN", "RAHMA", "MAJD"]): return "🕌 قنوات إسلامية"
    if any(w in name for w in ["DRAMA", "SERIES", "MOSALSALAT"]): return "🎬 مسلسلات ودراما"
    if any(w in name for w in ["CINEMA", "AFLAM", "MBC2", "ACTION"]): return "🍿 أفلام"
    return "📺 قنوات عامة"

def parse_tll_file(file_bytes):
    root = ET.fromstring(file_bytes)
    channels = []
    
    # 1. الموديل الجديد (32LH604U) - استخراج الأسماء من vchName
    items = root.findall(".//ITEM")
    if items:
        for item in items:
            name_node = item.find("vchName")
            if name_node is not None:
                ch_name = name_node.text
                channels.append({
                    "channelName": ch_name,
                    "category": ai_classify(ch_name), # هنا التصنيف
                    "frequency": item.find("frequency").text if item.find("frequency") is not None else "0"
                })
        return channels, root, "NEW_MODEL"

    # 2. الموديل القديم
    legacy_tag = root.find(".//legacybroadcast")
    if legacy_tag is not None:
        broadcast_data = json.loads(legacy_tag.text)
        ch_list = broadcast_data.get("channelList", [])
        for ch in ch_list:
            ch["category"] = ai_classify(ch.get("channelName", ""))
        return ch_list, root, "OLD_MODEL"
        
    return [], root, "UNKNOWN"

# --- الواجهة ---
st.title("📺 RAMBO - LG AI Sorter")
uploaded_file = st.file_uploader("ارفع ملف القنوات:", type=["TLL"])

if uploaded_file is not None:
    channels, root, mode = parse_tll_file(uploaded_file.read())
    
    if channels:
        st.success(f"تم فك التشفير وتصنيف القنوات! (الوضع: {mode})")
        
        # عرض القنوات مع التصنيف
        st.write("### 📊 القنوات المكتشفة")
        for ch in channels[:20]: # عرض أول 20 كمثال
            st.write(f"**{ch['channelName']}** | الفئة: *{ch['category']}*")
            
        # هنا ستظهر باقي اختياراتك (الترتيب، البحث، التحميل) 
        # لأن قائمة channels الآن تحتوي على مفتاح "category" لكل قناة
