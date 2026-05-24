import streamlit as st
import xml.etree.ElementTree as ET
import json

st.set_page_config(page_title="RAMBO - Universal LG Sorter", layout="wide")
st.title("📺 RAMBO - المنسق العالمي الشامل")

# 1. تعريف الفئات
CATEGORIES = ["دينية", "أفلام ودراما", "رياضة", "أخبار", "أطفال", "عامة"]

def get_category(name):
    name = name.upper()
    if any(x in name for x in ["ALMAJD", "SAT", "AGHAPY", "KARMA", "MESAT"]): return "دينية"
    if any(x in name for x in ["CINEMA", "DRAMA", "MBC", "MOVIE"]): return "أفلام ودراما"
    if any(x in name for x in ["SPORT", "ONTIME"]): return "رياضة"
    if any(x in name for x in ["NEWS", "JAZEERA"]): return "أخبار"
    if any(x in name for x in ["KIDS", "TOON"]): return "أطفال"
    return "عامة"

uploaded_file = st.file_uploader("🚀 ارفع ملف القنوات (TLL):", type=["TLL"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    root = ET.fromstring(file_bytes)
    
    st.success(f"✅ تم التعرف على ملف: {root.find('.//ModelName').text}")

    # 2. أداة الترتيب الذكي
    st.write("### 🎛️ أدوات التحكم في الترتيب")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✨ ترتيب القنوات حسب الفئة (AI)"):
            items = root.findall(".//ITEM")
            # ترتيب القنوات بناءً على الفئات
            sorted_items = sorted(items, key=lambda x: get_category(x.find("vchName").text if x.find("vchName") is not None else ""))
            
            # إعادة تعيين الأرقام بعد الترتيب
            for i, item in enumerate(sorted_items, start=1):
                item.find("prNum").text = str(i)
            st.success("تم إعادة ترتيب القنوات بنجاح حسب التصنيفات!")

    with col2:
        if st.button("🔄 إعادة الترقيم التسلسلي (1, 2, 3...)"):
            items = root.findall(".//ITEM")
            for i, item in enumerate(items, start=1):
                item.find("prNum").text = str(i)
            st.success("تم الترقيم المتسلسل!")

    # 3. تحميل الملف
    st.write("---")
    final_xml = ET.tostring(root, encoding="utf-8")
    st.download_button("📥 تحميل الملف النهائي المعدل", data=final_xml, file_name="RAMBO_FINAL.TLL")

else:
    st.info("💡 بانتظار رفع الملف للبدء.")
