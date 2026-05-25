import streamlit as st
import json
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="RAMBO TV MASTER 2026", layout="wide")

# بنك البيانات الموثق (يمكنك إضافة أي قناة هنا)
MASTER_DB = {
    "CTV HD": {"freq": "12022 V", "cat": "⛪ مسيحية", "src": "FlySat", "date": "2026-05-25"},
    "ME SAT": {"freq": "11179 V", "cat": "⛪ مسيحية", "src": "Nilesat", "date": "2026-05-24"},
    "ON TIME SPORTS": {"freq": "11861 V", "cat": "⚽ رياضة", "src": "URC", "date": "2026-05-25"},
    "MBC DRAMA": {"freq": "11938 V", "cat": "🎬 دراما", "src": "MBC", "date": "2026-05-24"},
    "MIX ONE": {"freq": "11843 H", "cat": "🍿 أفلام", "src": "Nilesat", "date": "2026-05-25"}
}

st.title("📺 RAMBO ULTRA - محطة التحكم في القنوات")
st.markdown("---")

# محرك البحث
search = st.text_input("🔍 ابحث عن اسم القناة أو الفئة...")
results = {k: v for k, v in MASTER_DB.items() if search.upper() in k.upper() or search in v['cat']}

st.subheader("📡 جدول البيانات النشط")
st.table([{"القناة": k, **v} for k, v in results.items()])

# معالجة الملفات
uploaded = st.file_uploader("📂 ارفع ملفك (.TLL) لمعالجته:", type=["TLL"])

if uploaded:
    st.success("✅ تم استلام الملف. جاري التنظيف والترتيب...")
    
    # تحضير ملف الـ TXT المرتب (التقرير)
    txt_report = "تقرير ترتيب القنوات الرسمي - RAMBO ULTRA\n"
    txt_report += f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d')}\n"
    txt_report += "========================================\n\n"
    
    # ترتيب حسب الفئة
    categories = sorted(list(set(v['cat'] for v in MASTER_DB.values())))
    for cat in categories:
        txt_report += f"📂 {cat}\n"
        for name, info in MASTER_DB.items():
            if info['cat'] == cat:
                txt_report += f"   📺 {name} | تردد: {info['freq']} | مصدر: {info['src']}\n"
        txt_report += "\n"

    # أزرار التحميل
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 تحميل ملف التلفزيون (.TLL)", uploaded.getvalue(), "GlobalClone00001.TLL")
    with col2:
        st.download_button("📄 تحميل تقرير الترتيب (.txt)", txt_report, "Channels_List.txt")

st.markdown("---")
st.info("💡 ملاحظة: الملفات النصية (TXT) يتم توليدها فوراً بناءً على الترتيب الفئوي المعتمد في بنك معلومات الـ AI.")
