import streamlit as st
import xml.etree.ElementTree as ET
import json
import urllib.parse
from datetime import datetime

# --- الدوال المساعدة (هنا تمت إضافة ذكاء كشف الموديل) ---
def ai_classify(channel_name):
    name = channel_name.upper()
    if any(w in name for w in ["CTV", "AGHAPY", "MESAT", "KARMA", "NOURSAT"]): return "⛪ قنوات مسيحية"
    if any(w in name for w in ["QURAN", "RAHMA", "MAJD", "MAKKA"]): return "🕌 قنوات إسلامية"
    if any(w in name for w in ["MOSALSALAT", "DRAMA", "SERIES", "KHOLASA"]): return "🎬 مسلسلات ودراما"
    if any(w in name for w in ["CINEMA", "ROTANA", "AFLAM", "MIX", "MBC2", "ACTION", "RAMBO", "MISHMISH"]): return "🍿 أفلام عربية وأجنبية"
    if any(w in name for w in ["SPACE TOON", "CN", "MAJID", "KIDS", "TOM"]): return "👶 أطفال وكرتون"
    if any(w in name for w in ["SPORT", "ONTIME", "KASS", "AD_SPORTS"]): return "⚽ رياضة"
    if any(w in name for w in ["NEWS", "JAZEERA", "ARABIYA", "HADATH", "CAIRO"]): return "📰 أخبار وسياسة"
    return "📺 قنوات عامة ومنوعات"

def parse_tll_file(file_bytes):
    root = ET.fromstring(file_bytes)
    channels = []
    
    # 1. محاولة القراءة لموديلات 32 بوصة (عن طريق ITEM و vchName)
    items = root.findall(".//ITEM")
    if items:
        for item in items:
            name_node = item.find("vchName") # التعديل الجوهري هنا
            if name_node is not None:
                channels.append({
                    "channelName": name_node.text,
                    "frequency": item.find("frequency").text if item.find("frequency") is not None else "0"
                })
        return channels, root
    
    # 2. القراءة التقليدية (JSON) للموديلات الكبيرة
    legacy_tag = root.find(".//legacybroadcast")
    if legacy_tag is not None:
        broadcast_data = json.loads(legacy_tag.text)
        return broadcast_data.get("channelList", []), root
        
    return [], root

# --- استكمال الكود ---
# (استخدم نفس كودك السابق تماماً، لكن بدلاً من قراءة channels من JSON مباشرة، استخدم الدالة parse_tll_file)
# مثال:
uploaded_file = st.file_uploader("🚀 ارفع ملف القنوات (يعمل مع كل الموديلات):", type=["TLL"])

if uploaded_file is not None:
    channels, root = parse_tll_file(uploaded_file.read())
    
    # الآن المتغير channels جاهز ويحتوي على البيانات من أي موديل (32 أو 55)
    # أكمل باقي كودك (الترتيب، العرض، التحميل) كما هو
    st.write(f"تم اكتشاف {len(channels)} قناة بنجاح!")
    
    # [باقي الكود الخاص بك يوضع هنا...]
