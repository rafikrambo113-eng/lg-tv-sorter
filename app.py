import streamlit as st
import xml.etree.ElementTree as ET
import json
import re
import os
from datetime import datetime

# [تأكد من وجود تعريفات الإعدادات والـ UI_TEXT في الأعلى كما هي في كودك]
# (تم اختصارها هنا للتركيز على الجزء المُصلح)

# --- تعريف المتغيرات الافتراضية لمنع الـ NameError ---
if 'file_processed' not in locals():
    file_processed = False
if 'unique_channels_map' not in locals():
    unique_channels_map = {}

# --- [هنا تضع باقي الكود والوظائف: get_base_2026_db, load_persistent_brain, ai_classify] ---

# --- لوحة العمل (التي تحتوي على الخطأ سابقاً) ---
# تم وضع التعريفات في مكانها الصحيح قبل استدعاء هذا الجزء
if file_processed and unique_channels_map:
    st.markdown(f"""<div class="lg-trick-box"><h4>{t['lg_trick_title']}</h4><p style="white-space: pre-line;">{t['lg_trick_text']}</p></div>""", unsafe_allow_html=True)
    
    cleaned_channels_list = list(unique_channels_map.values())
    
    user_priority = st.multiselect(t['multiselect_label'], options=ALL_AVAILABLE_CATEGORIES, default=[])
    final_priority = list(user_priority)
    for cat in ALL_AVAILABLE_CATEGORIES:
        if cat not in final_priority: final_priority.append(cat)
        
    channels_sorted = sorted(cleaned_channels_list, key=lambda x: final_priority.index(ai_classify(x["name"])))
    
    # تحضير ملف الـ TLL
    if 'is_modern' in locals() and is_modern:
        final_list_modern = []
        for index, ch in enumerate(channels_sorted, start=1):
            node = ch["raw_node"]
            node["majorNumber"] = index
            final_list_modern.append(node)
        broadcast_data["channelList"] = final_list_modern
        legacy_broadcast_tag.text = json.dumps(broadcast_data, ensure_ascii=False)
        file_bytes_out = ET.tostring(root, encoding="utf-8")
    else:
        item_strings_sorted = []
        for index, ch in enumerate(channels_sorted, start=1):
            s = ch.get("raw_str", "")
            s = re.sub(r'<prNum>\d+</prNum>', f'<prNum>{index}</prNum>', s) if "<prNum>" in s else s.replace("<ITEM>", f"<ITEM>\r\n<prNum>{index}</prNum>")
            item_strings_sorted.append(s)
        file_bytes_out = "\r\n".join(item_strings_sorted).encode('utf-8')

    # --- الجزء المدمج للتقرير النصي ---
    st.success(t['ready_msg'])
    
    txt_report = f"📄 تقرير RAMBO 5 - الترتيب الرسمي - {datetime.now().strftime('%Y-%m-%d')}\n"
    txt_report += "==================================================\n\n"
    for index, ch in enumerate(channels_sorted, start=1):
        txt_report += f"{index:03d} | القناة: {ch['name']} | التردد: {ch['freq']} MHz\n"
    
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(label=t['btn_download_tll'], data=file_bytes_out, file_name="GlobalClone00001.TLL", mime="application/octet-stream")
    with col_dl2:
        st.download_button(label="📄 تحميل تقرير الترتيب (Channels_List.txt)", data=txt_report, file_name="Channels_List.txt", mime="text/plain")

# [الفوتر السيبراني هنا]
