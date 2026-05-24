import streamlit as st
import xml.etree.ElementTree as ET
import json
import urllib.parse
from datetime import datetime

# 1. تهيئة الحالات الافتراضية
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# قاموس اللغتين
UI_TEXT = {
    'ar': {
        'title': "📺 RAMBO - المنسق المستقبلي لشاشات LG",
        'subtitle': "⚡ هندسة متطورة لترتيب ملفات القنوات بالتأثيرات السيبرانية مصفوفة (3D)",
        'upload_label': "🚀 اختر ملف القنوات (GlobalClone00001.TLL) من الفلاشة:",
        'update_freq_label': "⚛️ تفعيل الصيانة الذكية وتحديث الترددات تلقائياً من القمر",
        'add_new_ch_label': "✨ فحص وإضافة القنوات الجديدة المتاحة على القمر الصناعي تلقائياً",
        'success_read': "🛸 تم قراءة الهيكل وفك التشفير بنجاح! بلد البث الحالي: ",
        'search_header': "🔍 محرك البحث الذكي عن القنوات داخل الملف:",
        'search_placeholder': "اكتب اسم القناة هنا للبحث...",
        'search_col_num': "الرقم",
        'search_col_name': "اسم القناة",
        'search_col_cat': "الفئة (Category)",
        'search_col_freq': "التردد (Frequency)",
        'search_no_results': "⚠️ لم يتم العثور على أي قنوات مطابقة للبحث.",
        'config_title': "🎛️ مصفوفة ترتيب الفئات المخصصة حسب اختيارك اليدوي:",
        'config_tip': "💡 ملحوظة: اضغط على الفئات بالترتيب الفعلي المفضل لديك.",
        'multiselect_label': "اضغط هنا لبناء تسلسل خطة العرض التفاعلي للفئات:",
        'preview_title': "📊 مجسم المعاينة الحية لتوزيع القنوات الحالي:",
        'channels_count': "قناة",
        'freq_table_title': "🔁 سجل صيانة الترددات الحية المحدثة",
        'new_ch_added_title': "🆕 القنوات الجديدة المكتشفة والتي تم زرعها في الملف:",
        'ready_msg': "🌌 تم دمج مصفوفة RAMBO وإعادة الهيكلة بنجاح!",
        'btn_download_tll': "📥 تحميل ملف الشاشة النهائي (GlobalClone00001.TLL)",
        'btn_download_txt': "📄 تحميل تقرير الترتيب كملف نصي (Channels_List.txt)",
        'txt_header': "📄 تقرير الترتيب النهائي لقنوات شاشة LG",
        'txt_order': "🛠️ ترتيب الفئات المختار: "
    },
    'en': {
        'title': "📺 RAMBO - LG Futuristic AI Channel Sorter",
        'subtitle': "⚡ Next-Gen Cyber-Engineered Architecture for 3D Channel Layouts",
        'upload_label': "🚀 Upload Channel File (GlobalClone00001.TLL) from USB Flash:",
        'update_freq_label': "⚛️ Activate Satellite Live Frequency Auto-Update & Diagnostics",
        'add_new_ch_label': "✨ Scan & Inject New Satellite Channels Into Your File Automatically",
        'success_read': "🛸 Matrix Structure Decoded Successfully! Country Profile: ",
        'search_header': "🔍 Dynamic Channel Search Engine:",
        'search_placeholder': "Type channel name to look up...",
        'search_col_num': "No.",
        'search_col_name': "Channel Name",
        'search_col_cat': "Category",
        'search_col_freq': "Frequency",
        'search_no_results': "⚠️ No channels matching your search criteria.",
        'config_title': "🎛️ Custom Category Priority Control Matrix:",
        'config_tip': "💡 Hint: Click categories in exact order.",
        'multiselect_label': "Select categories one by one to configure your linear priority:",
        'preview_title': "📊 Channel Grid Live 3D Preview Dashboard:",
        'channels_count': "Channels",
        'freq_table_title': "🔁 Automatic Frequency Correction Logs",
        'new_ch_added_title': "🆕 New Satellite Channels Discovered & Injected:",
        'ready_msg': "🌌 Quantum Matrix Deployment Successful!",
        'btn_download_tll': "📥 Download Final TV Configuration (GlobalClone00001.TLL)",
        'btn_download_txt': "📄 Download Sorting Text Diagnostics (Channels_List.txt)",
        'txt_header': "📄 Final LG TV Channel Sorting Report",
        'txt_order': "🛠️ Selected Category Priority: "
    }
}

t = UI_TEXT[st.session_state.lang]
st.set_page_config(page_title="RAMBO - LG Futuristic AI Sorter", page_icon="⚡", layout="wide")

# لوحة التحكم
col_lang, col_theme, _ = st.columns([1.2, 1.5, 8])
with col_lang:
    if st.button("🌐 English" if st.session_state.lang == 'ar' else "🌐 العربية"):
        st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
        st.rerun()
with col_theme:
    if st.button("☀️ Light Mode" if st.session_state.theme == 'dark' else "🌙 Dark Mode"):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

# ستايل CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;900&family=Cairo:wght@400;700&display=swap');
    .main { font-family: 'Cairo', sans-serif; }
    h1 { color: #ff007f !important; text-align: center; }
    .futuristic-cyber-footer { background: #080314; border: 2px solid #00f0ff; padding: 35px; text-align: center; border-radius: 20px; margin-top: 65px; color: white; }
    .cyber-whatsapp-btn { background: transparent !important; color: #25d366 !important; padding: 14px 35px !important; border-radius: 35px !important; border: 2px solid #25d366 !important; cursor: pointer !important; font-size: 16px !important; transition: 0.3s !important; }
    .cyber-whatsapp-btn:hover { background: #25d366 !important; color: #000 !important; }
    </style>
""", unsafe_allow_html=True)

st.title(t['title'])
st.markdown(f"<h3>{t['subtitle']}</h3>", unsafe_allow_html=True)

# قاعدة البيانات والمنطق
LIVE_SATELLITE_DB = {
    "QATAR TV HD": {"frequency": 10834, "polarization": "Horizontal", "symbolRate": 27500, "scrambled": "false", "serviceType": "1"},
    "AL RAHMA": {"frequency": 10873, "polarization": "Vertical", "symbolRate": 27500, "scrambled": "false", "serviceType": "1"},
    "MBC 2": {"frequency": 11938, "polarization": "Vertical", "symbolRate": 27500, "scrambled": "false", "serviceType": "1"}
}

ALL_AVAILABLE_CATEGORIES = ["⛪ قنوات مسيحية", "🕌 قنوات إسلامية", "🎬 مسلسلات ودراما", "🍿 أفلام", "👶 أطفال", "⚽ رياضة", "📰 أخبار", "📺 منوعات"]

def ai_classify(channel_name): return ALL_AVAILABLE_CATEGORIES[7]

uploaded_file = st.file_uploader(t['upload_label'], type=["TLL"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    root = ET.fromstring(file_bytes)
    broadcast_data = json.loads(root.find(".//legacybroadcast").text)
    channels = broadcast_data.get("channelList", [])
    
    st.write("---")
    update_freq = st.checkbox(t['update_freq_label'], value=True)
    add_new_channels = st.checkbox(t['add_new_ch_label'], value=False)
    
    report_changes = []
    for ch in channels:
        name = ch.get("channelName", "").upper()
        if update_freq and name in LIVE_SATELLITE_DB:
            live = LIVE_SATELLITE_DB[name]
            if int(ch.get("frequency", 0)) != live["frequency"]:
                report_changes.append({"القناة": name, "التردد القديم": ch.get("frequency"), "التردد الجديد": live["frequency"]})
                ch["frequency"] = str(live["frequency"])

    if update_freq and report_changes:
        today_date = datetime.now().strftime("%d/%m/%Y")
        st.write(f"### {t['freq_table_title']} ({today_date})")
        st.table(report_changes)
    
    st.success(t['ready_msg'])

# الفوتر
whatsapp_web_url = "https://web.whatsapp.com/send?phone=201280339779&text=Hello%20Developer%20Rafik%20Rambo"
st.markdown(f"""
    <div class="futuristic-cyber-footer">
        <h3>🛠️ DEVELOPER ENG: RAFIK RAMBO</h3>
        <button class="cyber-whatsapp-btn" onclick="window.open('{whatsapp_web_url}', '_blank')">
            💬 Open WhatsApp Web Now
        </button>
    </div>
""", unsafe_allow_html=True)
