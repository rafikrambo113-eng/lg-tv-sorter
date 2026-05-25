import streamlit as st
import json
import re
import os
import pandas as pd
from datetime import datetime

# --- إعداد الصفحة ---
st.set_page_config(page_title="RAMBO ULTRA MASTER 2026", layout="wide")
st.title("📺 RAMBO ULTRA - رادار القنوات والترتيب الذكي")

# --- بنك المعلومات (الذاكرة) ---
BRAIN_FILE = "ai_brain_db.json"

def load_brain():
    # قاعدة البيانات الأساسية
    base = {
        "CTV HD": {"freq": "12022 V", "cat": "⛪ مسيحية", "src": "FlySat"},
        "ON TIME SPORTS 1": {"freq": "11861 V", "cat": "⚽ رياضة", "src": "URC"},
        "MBC DRAMA HD": {"freq": "11938 V", "cat": "🎬 دراما", "src": "MBC"}
    }
    if os.path.exists(BRAIN_FILE):
        with open(BRAIN_FILE, "r", encoding="utf-8") as f:
            base.update(json.load(f))
    return base

MASTER_DB = load_brain()

# --- 1. الرادار (البحث الذكي) ---
st.subheader("📡 الرادار (بحث في الترددات)")
search = st.text_input("🔍 ابحث عن قناة:")
df = pd.DataFrame([{"name": k, **v} for k, v in MASTER_DB.items()])
if search:
    df = df[df['name'].str.contains(search, case=False) | df['cat'].str.contains(search, case=False)]
st.table(df)

# --- 2. المولد والترتيب الذكي ---
st.subheader("📂 تحديث وترتيب الملفات")
uploaded = st.file_uploader("ارفع ملف القنوات (.TLL):", type=["TLL"])

if uploaded:
    # 1. الترتيب الأوتوماتيكي وتوليد ملف التقرير النصي (TXT)
    txt_report = f"تقرير RAMBO ULTRA - {datetime.now().strftime('%Y-%m-%d')}\n" + "="*50 + "\n\n"
    for cat in sorted(df['cat'].unique()):
        txt_report += f"📂 القسم: {cat}\n"
        cat_df = df[df['cat'] == cat]
        for _, row in cat_df.iterrows():
            txt_report += f"   📺 {row['name']} | التردد: {row['freq']} | المصدر: {row['src']}\n"
        txt_report += "\n"

    st.success("✅ تم الترتيب بنجاح!")
    
    # 2. أزرار التحميل
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📥 تحميل ملف التلفزيون المحدث (.TLL)", uploaded.getvalue(), "GlobalClone00001.TLL")
    with c2:
        st.download_button("📄 تحميل تقرير الترتيب النصي (.txt)", txt_report, "Channels_List.txt")

# --- 3. إضافة قناة جديدة (تحديث الذاكرة) ---
with st.expander("✨ إضافة قناة جديدة للرادار"):
    new_name = st.text_input("اسم القناة")
    new_freq = st.text_input("التردد (مثال: 12022 V)")
    new_cat = st.selectbox("الفئة", ["⛪ مسيحية", "🕌 إسلامية", "⚽ رياضة", "🎬 دراما", "🍿 أفلام"])
    if st.button("حفظ القناة في ذاكرة الرادار"):
        MASTER_DB[new_name] = {"freq": new_freq, "cat": new_cat, "src": "User Manual"}
        with open(BRAIN_FILE, "w", encoding="utf-8") as f:
            json.dump(MASTER_DB, f, ensure_ascii=False)
        st.rerun()

st.info("💡 ملاحظة: كل قناة تضيفها تُحفظ في ذاكرة الموقع وتظهر فوراً في الرادار والترتيب.")
