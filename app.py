import streamlit as st
import xml.etree.ElementTree as ET
import json
import re
import pandas as pd
from io import BytesIO
from fuzzywuzzy import process

# --- إعدادات الصفحة ---
st.set_page_config(page_title="RAMBO - LG AI Sorter", page_icon="⚡", layout="wide")

# --- دالة التصنيف الذكي ---
def ai_classify(channel_name):
    categories = {
        "⛪ قنوات مسيحية": ["CTV", "AGHAPY", "MESAT", "KARMA", "NOURSAT"],
        "🕌 قنوات إسلامية": ["QURAN", "RAHMA", "MAJD", "MAKKA", "HAYAT"],
        "🎬 مسلسلات ودراما": ["DRAMA", "SERIES", "MOSALSALAT"],
        "🍿 أفلام": ["CINEMA", "ROTANA", "AFLAM", "MBC2", "ACTION"],
        "⚽ رياضة": ["SPORT", "ONTIME", "KASS", "AD_SPORTS"]
    }
    name = channel_name.upper()
    for cat, keywords in categories.items():
        match, score = process.extractOne(name, keywords)
        if score > 70: return cat
    return "📺 قنوات عامة"

# --- دالة تصدير الإكسيل ---
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Channels')
    return output.getvalue()

# --- واجهة المستخدم ---
st.title("📺 RAMBO - المنسق الذكي لشاشات LG")
uploaded_file = st.file_uploader("🚀 اختر ملف القنوات (GlobalClone00001.TLL):", type=["TLL"])

if uploaded_file is not None:
    try:
        # قراءة الملف ومعالجة الأخطاء
        file_bytes = uploaded_file.read()
        try:
            root = ET.fromstring(file_bytes)
        except Exception:
            st.error("⚠️ الملف تالف أو غير مدعوم!")
            st.stop()

        # استخراج القنوات (المنطق الأصلي لك)
        legacy_broadcast_tag = root.find(".//legacybroadcast")
        if legacy_broadcast_tag is not None:
            broadcast_data = json.loads(legacy_broadcast_tag.text)
            channels_list = broadcast_data.get("channelList", [])
            
            # تجهيز البيانات للعرض وللإكسيل
            export_data = []
            for ch in channels_list:
                name = ch.get("channelName", "Unknown")
                export_data.append({
                    "اسم القناة": name,
                    "الفئة": ai_classify(name),
                    "التردد": ch.get("frequency", "N/A")
                })
            
            # عرض النتائج في جدول
            st.success("🛸 تمت المعالجة بنجاح!")
            df = pd.DataFrame(export_data)
            st.dataframe(df)

            # زر تحميل الإكسيل
            excel_data = to_excel(df)
            st.download_button(
                label="📥 تحميل القائمة بصيغة Excel",
                data=excel_data,
                file_name="Channels_List.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("⚠️ لم يتم العثور على بيانات قنوات في الملف.")

    except Exception as e:
        st.error(f"⚠️ حدث خطأ: {e}")

st.markdown("---")
st.write("🛠️ DEVELOPER ENG: RAFIK NATHAN")
