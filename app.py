import streamlit as st
import xml.etree.ElementTree as ET
import json
import urllib.parse

# 1. تهيئة الحالة الافتراضية للغة (عربي كديفولت)
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'

# قاموس اللغتين (عربي وإنجليزي) لترجمة واجهة الموقع
UI_TEXT = {
    'ar': {
        'title': "📺 RAMBO - المنسق المستقبلي لشاشات LG",
        'subtitle': "⚡ الجيل القادم من هندسة وترتيب ملفات القنوات ثلاثية الأبعاد",
        'upload_label': "🚀 ارفع ملف القنوات (GlobalClone00001.TLL) من الفلاشة:",
        'update_freq_label': "⚛️ تفعيل الصيانة الحية وتحديث الترددات تلقائياً عبر الأقمار",
        'success_read': "🛸 تم اختراق وقراءة الهيكل بنجاح! بلد البث الحالي: ",
        'config_title': "🎛️ مصفوفة ترتيب الفئات المخصصة:",
        'config_tip': "💡 تلميح: اضغط على الفئات بالترتيب الذي تريده. الفئة الأولى ستكون في صدارة التلفزيون.",
        'multiselect_label': "اختر الفئات واحدة تلو الأخرى لبناء خطتك:",
        'preview_title': "📊 مجسم استعراض القنوات الحالي:",
        'channels_count': "قناة",
        'freq_table_title': "🔁 سجل الترددات التي تمت صيانته وتحديثها:",
        'ready_msg': "🌌 تم دمج المصفوفة وإعادة الهيكلة بنجاح! الملفات جاهزة للتحميل:",
        'btn_download_tll': "📥 تحميل ملف الشاشة النهائي (TLL)",
        'btn_download_txt': "📄 تحميل تقرير الترتيب النصي (TXT)",
        'txt_header': "📄 تقرير الترتيب النهائي لقنوات شاشة LG",
        'txt_order': "🛠️ ترتيب الفئات المختار: "
    },
    'en': {
        'title': "📺 RAMBO - LG Futuristic AI Sorter",
        'subtitle': "⚡ Next-Gen 3D Architecture for Channel Management",
        'upload_label': "🚀 Upload Channel File (GlobalClone00001.TLL) from USB:",
        'update_freq_label': "⚛️ Enable Live Satellite Frequency Auto-Update & Maintenance",
        'success_read': "🛸 Structure Decoded Successfully! Broadcast Country: ",
        'config_title': "🎛️ Custom Category Priority Matrix:",
        'config_tip': "💡 Hint: Click categories in order. The first chosen will be on top of your TV list.",
        'multiselect_label': "Select categories one by one to build your layout:",
        'preview_title': "📊 Current Channel Live 3D Matrix:",
        'channels_count': "Channels",
        'freq_table_title': "🔁 Maintained & Updated Frequency Log:",
        'ready_msg': "🌌 Matrix Integrated Successfully! Assets ready for deployment:",
        'btn_download_tll': "📥 Download Final TV File (TLL)",
        'btn_download_txt': "📄 Download Order Text Report (TXT)",
        'txt_header': "📄 Final LG TV Channel Sorting Report",
        'txt_order': "🛠️ Selected Category Priority: "
    }
}

t = UI_TEXT[st.session_state.lang]

# إعدادات الصفحة
st.set_page_config(page_title="RAMBO 3D Sorter", page_icon="⚡", layout="wide")

# زر تغيير اللغة
col_lang, _ = st.columns([1, 10])
with col_lang:
    if st.button("🌐 English" if st.session_state.lang == 'ar' else "🌐 العربية"):
        st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
        st.rerun()

# استايلات الـ 3D والألوان المستقبلية المعدلة (السيبرانية المظلمة مع توهج نيون متطور)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;900&family=Cairo:wght@400;700&display=swap');
    
    .main {{
        background: radial-gradient(circle at 50% 50%, #050508 0%, #020203 100%);
        color: #00f0ff;
        font-family: { "'Cairo', sans-serif" if st.session_state.lang == 'ar' else "'Orbitron', sans-serif" };
    }}
    
    h1 {{
        color: #ff0055;
        text-shadow: 0 0 10px #ff0055, 0 0 25px #ff0055;
        text-align: center;
        font-weight: 900;
    }}
    h3, p, label, .stMarkdown {{
        color: #00f0ff;
        text-shadow: 0 0 2px rgba(0, 240, 255, 0.5);
    }}
    
    /* صناديق ثلاثية الأبعاد */
    .stCheckbox, .stRadio, .stMultiSelect, div[data-testid="stExpander"] {{
        background: rgba(10, 15, 30, 0.7) !important;
        border: 1px solid #00f0ff !important;
        box-shadow: 0px 0px 15px rgba(0, 240, 255, 0.2), inset 0px 0px 10px rgba(0, 240, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
    }}
    div[data-testid="stExpander"]:hover {{
        border-color: #ff0055 !important;
        box-shadow: 0px 0px 25px rgba(255, 0, 85, 0.4) !important;
    }}
    
    /* أزرار التحميل البارزة */
    .stButton>button {{
        background: linear-gradient(135deg, #ff0055 0%, #a50034 100%) !important;
        color: white !important;
        border: 1px solid #ff0055 !important;
        border-radius: 10px !important;
        box-shadow: 0 5px 0 #55001a, 0 10px 20px rgba(255, 0, 85, 0.4) !important;
        font-weight: bold;
    }}
    .stButton>button:active {{
        transform: translateY(4px) !important;
        box-shadow: 0 1px 0 #55001a, 0 5px 10px rgba(255, 0, 85, 0.4) !important;
    }}
    
    /* الفوتر المستقبلي الجديد المطور لرامبو باللغتين */
    .futuristic-footer {{
        background: #060913;
        border: 2px solid #00f0ff;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.3), inset 0 0 20px rgba(255, 0, 85, 0.2);
        color: #ffffff;
        padding: 35px;
        text-align: center;
        border-radius: 20px;
        margin-top: 60px;
        font-family: 'Orbitron', 'Cairo', sans-serif;
    }}
    .footer-title-ar {{ color: #ff0055; font-size: 24px; font-weight: bold; text-shadow: 0 0 10px #ff0055; margin-bottom: 2px; }}
    .footer-title-en {{ color: #00f0ff; font-size: 20px; font-weight: bold; text-shadow: 0 0 10px #00f0ff; margin-bottom: 15px; letter-spacing: 2px; }}
    .footer-info {{ color: #e0e0e0; font-size: 16px; margin: 5px 0; line-spacing: 1.5; }}
    
    .cyber-whatsapp-btn {{
        background: transparent;
        color: #25d366 !important;
        padding: 12px 30px;
        text-align: center;
        border-radius: 30px;
        display: inline-block;
        font-weight: bold;
        text-decoration: none;
        margin-top: 20px;
        border: 2px solid #25d366;
        box-shadow: 0 0 15px rgba(37, 211, 102, 0.2);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .cyber-whatsapp-btn:hover {{
        background: #25d366;
        color: #000000 !important;
        box-shadow: 0 0 30px #25d366;
        transform: scale(1.05);
    }}
    </style>
""", unsafe_allow_html=True)

st.title(t['title'])
st.markdown(f"<h3>{t['subtitle']}</h3>", unsafe_allow_html=True)

# قاعدة بيانات الترددات
LIVE_SATELLITE_DB = {
    "QATAR TV HD": {"frequency": 10834, "polarization": "Horizontal", "symbolRate": 27500},
    "AL RAHMA": {"frequency": 10873, "polarization": "Vertical", "symbolRate": 27500},
    "ELKHOLASA MOSALSALAT": {"frequency": 10873, "polarization": "Vertical", "symbolRate": 27500},
    "MBC 2": {"frequency": 11938, "polarization": "Vertical", "symbolRate": 27500}, 
    "CTV": {"frequency": 12022, "polarization": "Vertical", "symbolRate": 27500}
}

# تصنيفات القنوات
ALL_AVAILABLE_CATEGORIES = [
    "⛪ Christian Channels" if st.session_state.lang == 'en' else "⛪ قنوات مسيحية",
    "🕌 Islamic Channels" if st.session_state.lang == 'en' else "🕌 قنوات إسلامية",
    "🎬 Drama & Series" if st.session_state.lang == 'en' else "🎬 مسلسلات ودراما",
    "🍿 Movies (Ar/En)" if st.session_state.lang == 'en' else "🍿 أفلام عربية وأجنبية",
    "👶 Kids & Cartoon" if st.session_state.lang == 'en' else "👶 أطفال وكرتون",
    "⚽ Sports" if st.session_state.lang == 'en' else "⚽ رياضة",
    "📰 News & Politics" if st.session_state.lang == 'en' else "📰 أخبار وسياسة",
    "📺 General Channels" if st.session_state.lang == 'en' else "📺 قنوات عامة ومنوعات"
]

def ai_classify(channel_name):
    name = channel_name.upper()
    if any(w in name for w in ["CTV", "AGHAPY", "MESAT", "KARMA", "NOURSAT"]): return ALL_AVAILABLE_CATEGORIES[0]
    if any(w in name for w in ["QURAN", "RAHMA", "MAJD", "MAKKA"]): return ALL_AVAILABLE_CATEGORIES[1]
    if any(w in name for w in ["MOSALSALAT", "DRAMA", "SERIES", "KHOLASA"]): return ALL_AVAILABLE_CATEGORIES[2]
    if any(w in name for w in ["CINEMA", "ROTANA", "AFLAM", "MIX", "FOX", "MBC2", "ACTION"]): return ALL_AVAILABLE_CATEGORIES[3]
    if any(w in name for w in ["SPACE TOON", "CN", "MAJID", "KIDS", "TOM"]): return ALL_AVAILABLE_CATEGORIES[4]
    if any(w in name for w in ["SPORT", "ONTIME", "KASS", "AD_SPORTS"]): return ALL_AVAILABLE_CATEGORIES[5]
    if any(w in name for w in ["NEWS", "JAZEERA", "ARABIYA", "HADATH", "CAIRO"]): return ALL_AVAILABLE_CATEGORIES[6]
    return ALL_AVAILABLE_CATEGORIES[7]

uploaded_file = st.file_uploader(t['upload_label'], type=["TLL"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    update_freq = st.checkbox(t['update_freq_label'])
    
    root = ET.fromstring(file_bytes)
    country_setting = root.find(".//BroadcastCountrySetting").text
    legacy_broadcast_tag = root.find(".//legacybroadcast")
    broadcast_data = json.loads(legacy_broadcast_tag.text)
    channels = broadcast_data.get("channelList", [])
    
    st.info(f"{t['success_read']} **{country_setting}**")

    st.write("---")
    st.write(f"### {t['config_title']}")
    st.write(t['config_tip'])
    
    user_priority = st.multiselect(t['multiselect_label'], options=ALL_AVAILABLE_CATEGORIES, default=[])
    
    final_priority = list(user_priority)
    for cat in ALL_AVAILABLE_CATEGORIES:
        if cat not in final_priority:
            final_priority.append(cat)

    categorized = {}
    report_changes = []
    for ch in channels:
        name = ch.get("channelName", "")
        cat = ai_classify(name)
        if cat not in categorized: categorized[cat] = []
        categorized[cat].append(name)
        
        if update_freq and name.upper() in LIVE_SATELLITE_DB:
            live = LIVE_SATELLITE_DB[name.upper()]
            if ch.get("frequency") != live["frequency"]:
                report_changes.append({
                    "Channel" if st.session_state.lang == 'en' else "القناة": name, 
                    "Old Freq" if st.session_state.lang == 'en' else "التردد القديم": ch.get("frequency"), 
                    "New Freq" if st.session_state.lang == 'en' else "التردد الجديد": live["frequency"]
                })
                ch["frequency"] = live["frequency"]
                ch["polarization"] = live["polarization"]
                ch["symbolRate"] = live["symbolRate"]

    st.write("---")
    st.write(f"### {t['preview_title']}")
    col1, col2 = st.columns(2)
    for i, cat_name in enumerate(final_priority):
        if cat_name in categorized:
            ch_list = categorized[cat_name]
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                is_user_chosen = "⭐ " if cat_name in user_priority else ""
                with st.expander(f"{is_user_chosen}{cat_name} — ({len(ch_list)} {t['channels_count']})"):
                    st.write(", ".join(ch_list))
                    
    if update_freq and report_changes:
        st.write(f"### {t['freq_table_title']}")
        st.table(report_changes)

    channels_sorted = sorted(channels, key=lambda x: final_priority.index(ai_classify(x.get("channelName", ""))))
    
    text_report = f"{t['txt_header']} ({country_setting})\n"
    text_report += t['txt_order'] + " -> ".join([c.split()[-1] for c in final_priority]) + "\n"
    text_report += "==================================================\n\n"
    
    for index, ch in enumerate(channels_sorted, start=1):
        ch["majorNumber"] = index
        ch_name = ch.get("channelName", "Unknown")
        ch_cat = ai_classify(ch_name)
        text_report += f"No. {index:03d} : {ch_name:<25} | Matrix Group: {ch_cat}\n"
        
    broadcast_data["channelList"] = channels_sorted
    legacy_broadcast_tag.text = json.dumps(broadcast_data, ensure_ascii=False)
    final_xml = ET.tostring(root, encoding="utf-8")
    
    st.write("---")
    st.success(t['ready_msg'])
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.download_button(label=t['btn_download_tll'], data=final_xml, file_name="GlobalClone00001.TLL", mime="application/octet-stream")
    with col_btn2:
        st.download_button(label=t['btn_download_txt'], data=text_report, file_name="Channels_List.txt", mime="text/plain; charset=utf-8")

# الفوتر السيبراني الاحترافي باللغتين (تحت بعض) مع ألوان مستقبلية نيون متوهجة وربط بالواتساب ويب
whatsapp_msg = urllib.parse.quote("Hello Rambo, I just deployed your futuristic 3D LG Sorter app and have an inquiry:")
whatsapp_url = f"https://web.whatsapp.com/send?phone=201280339779&text={whatsapp_msg}"

st.markdown(f"""
    <div class="futuristic-footer">
        <div class="footer-title-ar">🛸 تم العمل بواسطة RAFIK RAMBO</div>
        <div class="footer-title-en">🛸 CYBER-ENGINEERED BY: RAFIK RAMBO</div>
        
        <div class="footer-info">📱 <b>Mobile / الموبايل:</b> +201280339779</div>
        <div class="footer-info">✉️ <b>Email / البريد الإلكتروني:</b> rafikrambo113@gmail.com</div>
        
        <a href="{whatsapp_url}" target="_blank" class="cyber-whatsapp-btn">
            💬 اتصال فوري عبر WhatsApp Web | INSTANT LIAISON
        </a>
    </div>
""", unsafe_allow_html=True)
