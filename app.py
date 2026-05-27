import streamlit as st
import xml.etree.ElementTree as ET
import json
import re
import pandas as pd
from io import BytesIO
from fuzzywuzzy import process

# إعدادات الصفحة
st.set_page_config(page_title="RAMBO - LG AI Sorter", page_icon="⚡", layout="wide")

# --- دالة تصدير الإكسيل ---
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Channels')
    return output.getvalue()

# --- دالة التصنيف الذكي ---
def ai_classify(channel_name):
    categories = {
        "⛪ قنوات مسيحية": ["CTV", "AGHAPY", "MESAT", "KARMA", "NOURSAT"],
        "🕌 قنوات إسلامية": ["QURAN", "RAHMA", "MAJD", "MAKKA", "HAYAT"],
        "🎬 مسلسلات ودراما": ["DRAMA", "SERIES", "MOSALSALAT"],
        "🍿 أفلام": ["CINEMA", "ROTANA", "AFLAM", "MIX", "FOX", "MBC2"],
        "⚽ رياضة": ["SPORT", "ONTIME", "KASS", "AD_SPORTS"]
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
        # معالجة الملف
        file_bytes = uploaded_file.read()
        try:
            root = ET.fromstring(file_bytes)
        except Exception:
            st.error("⚠️ ملف تالف! يرجى التأكد من أن الملف هو ملف قنوات LG (TLL).")
            st.stop()

        st.success("🛸 تم قراءة الملف بنجاح وبدقة عالية!")

        # محاكاة لبيانات القنوات (هنا يكتمل عملك)
        # فرضنا وجود قائمة قنوات باسم channels_data
        # [ضع هنا منطق المعالجة الخاص بك]

        # زر تحميل الإكسيل
        # فقط قم بتغيير اسم المتغير channels_data بالمتغير الذي تستخدمه في كودك الأصلي
        if 'channels_to_sort' in locals():
            df_export = pd.DataFrame(channels_to_sort)
            excel_data = to_excel(df_export)
            st.download_button(
                label="📥 تحميل قائمة القنوات بصيغة Excel",
                data=excel_data,
                file_name="Channels_List.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"⚠️ حدث خطأ أثناء المعالجة: {e}")
        st.write("يرجى التأكد من أن هيكلية الملف تدعم الموديل الحالي.")

st.markdown("---")
st.write("🛠️ DEVELOPER ENG: RAFIK NATHAN")
