import streamlit as st
import xml.etree.ElementTree as ET
import json
import re
import os
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="RAMBO 5 - Satellite Engine", page_icon="📡", layout="wide")

# تهيئة المتغيرات الأساسية (عشان الكود ما يضربش)
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
if 'theme' not in st.session_state: st.session_state.theme = 'dark'
if 'file_processed' not in st.session_state: st.session_state.file_processed = False
if 'unique_channels_map' not in st.session_state: st.session_state.unique_channels_map = {}

# النصوص (نفس اللي بعتهولي)
UI_TEXT = {
    'ar': {
        'title': "📺 RAMBO 5 - رادار الترددات الحية",
        'ready_msg': "🌌 تمت المعالجة بنجاح! الملفات جاهزة للتحميل:",
        'btn_download_tll': "📥 تحميل ملف الشاشة (.TLL)",
        'lg_trick_title': "💡 ملحوظة فنية:",
        'lg_trick_text': "بعد التنزيل، ادخل مدير القنوات واختار 'استعادة' (Restore)."
    }
}
t = UI_TEXT[st.session_state.lang]

# --- (هنا الكود الخاص بك بالكامل من البداية وحتى مرحلة المعالجة) ---
# ملحوظة: في الكود بتاعك، استبدل كل تعريف للمتغيرات (file_processed = False) 
# بـ (st.session_state.file_processed = False) عشان الموقع يفتكرها.

# --- الجزء الخاص بالتحميل (النسخة النهائية) ---
if st.session_state.file_processed and st.session_state.unique_channels_map:
    st.markdown(f"""<div class="lg-trick-box"><h4>{t['lg_trick_title']}</h4><p>{t['lg_trick_text']}</p></div>""", unsafe_allow_html=True)
    
    # تجهيز التقرير
    txt_report = f"📄 تقرير RAMBO 5 - {datetime.now().strftime('%Y-%m-%d')}\n========================================\n\n"
    for ch in st.session_state.unique_channels_map.values():
        txt_report += f"📺 القناة: {ch['name']} | التردد: {ch['freq']} MHz\n"
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(t['btn_download_tll'], st.session_state.file_bytes_out, "GlobalClone00001.TLL")
    with col2:
        st.download_button("📄 تحميل تقرير الترتيب (.txt)", txt_report, "Channels_List.txt")
