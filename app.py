import streamlit as st
import xml.etree.ElementTree as ET
import json
import re
import pandas as pd
from io import BytesIO
from fuzzywuzzy import process

st.set_page_config(page_title="RAMBO - LG AI Sorter", layout="wide")

# --- دالة التصنيف الذكي ---
def ai_classify(channel_name):
    categories = {
        "⛪ قنوات مسيحية": ["CTV", "AGHAPY", "MESAT", "KARMA"],
        "🕌 قنوات إسلامية": ["QURAN", "RAHMA", "MAJD", "MAKKA"],
        "🎬 مسلسلات ودراما": ["DRAMA", "SERIES", "MOSALSALAT"],
        "🍿 أفلام": ["CINEMA", "ROTANA", "AFLAM", "MBC2", "ACTION"],
        "⚽ رياضة": ["SPORT", "ONTIME", "KASS"]
    }
    name = channel_name.upper()
    for cat, keywords in categories.items():
        match, score = process.extractOne(name, keywords)
        if score > 70: return cat
    return "📺 قنوات عامة"

# --- الواجهة ---
st.title("📺 RAMBO - المنسق الذكي لشاشات LG")
uploaded_file = st.file_uploader("🚀 اختر ملف القنوات (GlobalClone00001.TLL):", type=["TLL"])

if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.read()
        file_text = file_bytes.decode('utf-8', errors='ignore')
        
        # محاولة قراءة كـ XML
        try:
            root = ET.fromstring(file_bytes)
            # الموديلات الحديثة
            if root.find(".//legacybroadcast") is not None:
                data = json.loads(root.find(".//legacybroadcast").text)
                channels = data.get("channelList", [])
            else:
                # الموديلات القديمة (البحث بالنصوص)
                channels = []
                for match in re.finditer(r'<vchName>(.*?)</vchName>.*?<frequency>(\d+)</frequency>', file_text, re.DOTALL):
                    channels.append({"channelName": match.group(1), "frequency": match.group(2)})
        except:
            st.error("⚠️ فشل قراءة هيكل الملف.")
            st.stop()

        # تجهيز البيانات
        if channels:
            df = pd.DataFrame([{
                "الاسم": ch.get("channelName"),
                "التردد": ch.get("frequency"),
                "التصنيف": ai_classify(ch.get("channelName", ""))
            } for ch in channels])
            
            st.success(f"✅ تم العثور على {len(df)} قناة!")
            st.dataframe(df)

            # زر الإكسيل
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            
            st.download_button("📥 تحميل القائمة بصيغة Excel", output.getvalue(), "Channels_List.xlsx", "application/vnd.ms-excel")
        else:
            st.warning("⚠️ الملف فارغ أو غير متوافق.")

    except Exception as e:
        st.error(f"⚠️ حدث خطأ: {e}")
