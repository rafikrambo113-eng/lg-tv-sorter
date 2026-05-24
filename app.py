import streamlit as st
import xml.etree.ElementTree as ET
import json

st.set_page_config(page_title="RAMBO - Universal LG Sorter", layout="wide")
st.title("📺 RAMBO - المنسق العالمي الشامل")

uploaded_file = st.file_uploader("🚀 ارفع ملف القنوات (TLL):", type=["TLL"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    root = ET.fromstring(file_bytes)
    
    # 1. تحديد نوع النظام
    legacy_broadcast_tag = root.find(".//legacybroadcast")
    is_modern = legacy_broadcast_tag is not None and legacy_broadcast_tag.text
    
    st.success(f"✅ تم التعرف على الملف: {root.find('.//ModelName').text}")
    
    # 2. منطقة البحث والترتيب
    search_query = st.text_input("🔍 ابحث عن قناة في الملف:")
    
    if is_modern:
        # --- معالجة WebOS (الحديث) ---
        broadcast_data = json.loads(legacy_broadcast_tag.text)
        channels = broadcast_data.get("channelList", [])
        
        # فلترة القنوات
        filtered = [ch for ch in channels if search_query.lower() in ch.get("channelName", "").lower()]
        st.write(f"عرض {len(filtered)} قناة:")
        st.table([{"الاسم": ch["channelName"], "التردد": ch["frequency"]} for ch in filtered[:10]])
        
        # هنا يمكنك إضافة زر "ترتيب" ليقوم بتعديل broadcast_data
        
    else:
        # --- معالجة LH Series (القديم) ---
        items = root.findall(".//ITEM")
        filtered = [item for item in items if search_query.lower() in (item.find("vchName").text.lower() if item.find("vchName") is not None else "")]
        
        st.write(f"عرض {len(filtered)} قناة (نظام قديم):")
        data = []
        for item in filtered[:10]:
            data.append({
                "رقم": item.find("prNum").text,
                "الاسم": item.find("vchName").text if item.find("vchName") is not None else "N/A"
            })
        st.table(data)
        
        # ميزة الترتيب للموديل القديم:
        if st.button("🛠️ إعادة ترتيب القنوات (تلقائي)"):
            for i, item in enumerate(items, start=1):
                item.find("prNum").text = str(i)
            st.success("تم إعادة ترتيب جميع القنوات رقمياً (1, 2, 3...)")

    # 3. زر التحميل الموحد
    final_xml = ET.tostring(root, encoding="utf-8")
    st.download_button("📥 تحميل الملف النهائي المنسق", data=final_xml, file_name="RAMBO_Sorted.TLL")

else:
    st.info("💡 بانتظار رفع ملف القنوات للبدء في التنسيق.")
