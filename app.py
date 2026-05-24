import streamlit as st
import xml.etree.ElementTree as ET
import json

# إعدادات الصفحة
st.set_page_config(page_title="RAMBO - Universal LG Sorter", layout="wide")
st.title("📺 RAMBO - المنسق العالمي لشاشات LG")

uploaded_file = st.file_uploader("🚀 ارفع ملف القنوات (TLL):", type=["TLL"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    root = ET.fromstring(file_bytes)
    
    # 1. كشف نوع الملف (هل هو موديل حديث أم قديم؟)
    legacy_broadcast_tag = root.find(".//legacybroadcast")
    
    if legacy_broadcast_tag is not None and legacy_broadcast_tag.text:
        # --- هذا للموديلات الحديثة (مثل الـ 55 بوصة) ---
        st.info("نظام الملف: WebOS الحديث - تم التعرف على هيكل JSON")
        broadcast_data = json.loads(legacy_broadcast_tag.text)
        channels = broadcast_data.get("channelList", [])
        st.success(f"تم تحميل {len(channels)} قناة.")
        # هنا يكمل باقي كود الترتيب الخاص بك...
        
    else:
        # --- هذا للموديلات القديمة (مثل الـ 32 بوصة) ---
        st.warning("نظام الملف: كلاسيكي (LH Series) - يتم معالجة وسوم ITEM")
        items = root.findall(".//ITEM")
        st.write(f"تم العثور على {len(items)} قناة.")
        
        # عرض سريع للقنوات في الموديل القديم
        for item in items[:5]:
            ch_name = item.find("vchName").text if item.find("vchName") is not None else "Unknown"
            pr_num = item.find("prNum").text if item.find("prNum") is not None else "N/A"
            st.write(f"رقم {pr_num}: {ch_name}")
            
    st.success("الملف جاهز للمعالجة!")
    
    # زر التحميل
    final_xml = ET.tostring(root, encoding="utf-8")
    st.download_button("📥 تحميل الملف النهائي", data=final_xml, file_name="Modified_Channels.TLL")

else:
    st.write("يرجى رفع ملف الـ TLL للبدء.")
