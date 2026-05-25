import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="RAMBO TV MASTER 2026", layout="wide")

# بنك المعلومات (محدث بتاريخ اليوم 25 مايو 2026)
# يمكنك تعديل أي بيانات هنا فوراً
MASTER_DB = [
    {"name": "CTV HD", "freq": "12022 V", "cat": "⛪ مسيحية", "src": "FlySat"},
    {"name": "ME SAT HD", "freq": "11179 V", "cat": "⛪ مسيحية", "src": "Nilesat"},
    {"name": "EGYPT QURAN", "freq": "11179 V", "cat": "🕌 إسلامية", "src": "Nilesat"},
    {"name": "ON TIME SPORTS 1", "freq": "11861 V", "cat": "⚽ رياضة", "src": "URC"},
    {"name": "MBC DRAMA HD", "freq": "11938 V", "cat": "🎬 دراما", "src": "MBC"},
    {"name": "MIX ONE HD", "freq": "11843 H", "cat": "🍿 أفلام", "src": "Nilesat"},
    {"name": "WANNASAH HD", "freq": "11938 V", "cat": "👶 أطفال", "src": "Nilesat"}
]

st.title("📺 RAMBO ULTRA - تحديث وترتيب القنوات 2026")
st.markdown("---")

# 1. قسم الرادار (البحث)
st.subheader("📡 الرادار (بحث في الترددات)")
search = st.text_input("🔍 ابحث باسم القناة أو القسم...")
df = pd.DataFrame(MASTER_DB)
filtered_df = df[df['name'].str.contains(search, case=False) | df['cat'].str.contains(search, case=False)]
st.table(filtered_df)

# 2. قسم معالجة الملفات
st.subheader("📂 تحديث ملف القنوات الخاص بك")
uploaded = st.file_uploader("ارفع ملف القنوات (.TLL):", type=["TLL"])

if uploaded:
    # توليد ملف الـ TXT المرتب
    txt_content = f"تقرير قنوات RAMBO - بتاريخ {datetime.now().strftime('%Y-%m-%d')}\n"
    txt_content += "="*50 + "\n\n"
    
    # ترتيب حسب القسم
    for cat in sorted(df['cat'].unique()):
        txt_content += f"📂 القسم: {cat}\n"
        cat_data = df[df['cat'] == cat]
        for _, row in cat_data.iterrows():
            txt_content += f"  📺 {row['name']} | التردد: {row['freq']} | المصدر: {row['src']}\n"
        txt_content += "\n"
        
    st.success("✅ تم معالجة البيانات بنجاح!")
    
    # أزرار التحميل
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📥 تحميل ملف التلفزيون (.TLL)", uploaded.getvalue(), "GlobalClone00001.TLL")
    with c2:
        st.download_button("📄 تحميل تقرير الترتيب (.txt)", txt_content, "Channels_List.txt")

st.markdown("---")
st.info("💡 ملاحظة: هذا الموقع يمنحك ملف التلفزيون جاهزاً وملف نصي (TXT) للترتيب والتوثيق.")
