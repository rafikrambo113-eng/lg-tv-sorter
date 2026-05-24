import streamlit as st
import xml.etree.ElementTree as ET
import json
import urllib.parse

# 1. تهيئة الحالة الافتراضية للغة (عربي كديفولت)
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'

# قاموس اللغتين (عربي وإنجليزي) لترجمة الموقع بالكامل
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
        'footer_title': "🛸 تكنولوجيا وتطوير بواسطة: RAFIK RAMBO",
        'footer_contact': "📱 الموبايل: +201280339779 | ✉️ الإيميل: rafikrambo113@gmail.com",
        'whatsapp_btn': "💬 اتصال فوري عبر WhatsApp Web",
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
        'footer_title': "🛸 Cyber-Engineered By: RAFIK RAMBO",
        'footer_contact': "📱 Mobile: +201280339779 | ✉️ Email: rafikrambo113@gmail.com",
        'whatsapp_btn': "💬 Instant Liaison via WhatsApp Web",
        'txt_header': "📄 Final LG TV Channel Sorting Report",
        'txt_order': "🛠️ Selected Category Priority: "
    }
}

t = UI_TEXT[st.session_state.lang]

# إعدادات الصفحة
st.set_page_config(page_title="RAMBO 3D Sorter", page_icon="⚡", layout="wide")

# زر تغيير اللغة في أعلى اليمين بتصميم نيون مستقبلي متناسق
col_lang, _ = st.columns([1, 10])
with col_lang:
    if st.button("🌐 English" if st.session_state.lang == 'ar' else "🌐 العربية"):
        st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
        st.rerun()

# استايلات الـ 3D والألوان المستقبلية (أزرق سيبراني + بنفسجي نيوني + أحمر LG متوهج)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;900&family=Cairo:wght@400;700&display=swap');
    
    .main {{
        background: radial-gradient(circle at 50% 50%, #0d1117 0%, #070a0f 100%);
        color: #00f0ff;
        font-family: { "'Cairo', sans-serif" if st.session_state.lang == 'ar' else "'Orbitron', sans-serif" };
    }}
    
    /* عنوان رئيسي ثلاثي الأبعاد ومتوهج النيون */
    h1 {{
        color: #ff0055;
        text-shadow: 0 0 10px #ff0055, 0 0 30px #ff0055, 0 0 50px #ff0055;
        text-align: center;
        font-weight: 900;
        transform: perspective(500px) rotateX(10deg);
        margin-bottom: 10px;
    }}
    h3, p, label, .stMarkdown {{
        color: #00f0ff;
        text-shadow: 0 0 2px #00f0ff;
    }}
    
    /* صناديق اختيار ورفوف ثلاثية الأبعاد 3D Glassmorphism Box */
    .stCheckbox, .stRadio, .stMultiSelect, div[data-testid="stExpander"] {{
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 240, 255, 0.1), inset 0 0 15px rgba(0, 240, 255, 0.05) !important;
        backdrop-filter: blur(4px) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
        transform: translateY(0px);
        transition: all 0.3s ease;
    }}
    div[data-testid="stExpander"]:hover {{
        transform: translateY(-5px) scale(1.01);
        border-color: #ff0055 !important;
        box-shadow: 0 15px 35px 0 rgba(255, 0, 85, 0.2) !important;
    }}
    
    /* أزرار التحميل المجسمة بارزة 3D */
    .stButton>button {{
        background: linear-gradient(135deg, #ff0055 0%, #a50034 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: 0 5px 0 #660022, 0 10px 20px rgba(255, 0, 85, 0.3) !important;
        transform: translateY(0px);
        transition: all 0.1s ease-size;
        font-weight: bold;
    }}
    .stButton>button:active {{
        transform: translateY(4px) !important;
        box-shadow: 0 1px 0 #660022, 0 5px 10px rgba(255, 0, 85, 0.3) !important;
    }}
    
    /* الفوتر السايبر الرائع */
    .footer {{
        background: linear-gradient(180deg, rgba(255, 0, 85, 0.1) 0%, rgba(13, 17, 23, 0.9) 100%);
        border: 2px solid #ff0055;
        box-shadow: 0 0 25px rgba(255, 0, 85, 0.2);
        color: white;
        padding: 30px;
        text-align: center;
        border-radius: 20px;
        margin-top: 50px;
    }}
    .whatsapp-btn {{
        background: linear-gradient(135deg, #25d366 0%, #075e54 100%);
        color: white !important;
        padding: 12px 25px;
        text-align: center;
        border-radius: 10px;
        display: inline-block;
        font-weight: bold;
        text-decoration: none;
        margin-top: 15px;
        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4);
    }}
    </style>
""", unsafe_allow_html=True)

st.title(t['title'])
st.markdown(f"<h3>{t['subtitle']}</h3>", unsafe_allow_html=True)

# قاعدة البيانات الحية للترددات
LIVE_SATELLITE_DB = {
    "QATAR TV HD": {"frequency": 10834, "polarization": "Horizontal", "symbolRate": 27500},
    "AL RAHMA": {"frequency": 10873, "polarization": "Vertical", "symbolRate": 27500},
    "ELKHOLASA MOSALSALAT": {"frequency": 10873, "polarization": "Vertical", "symbolRate": 27500},
    "MBC 2": {"frequency": 11938, "polarization": "Vertical", "symbolRate": 27500}, 
    "CTV": {"frequency": 12022, "polarization": "Vertical", "symbolRate": 27500}
}

# تصنيفات القنوات المترجمة
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
    is_en = st.session_state.lang == 'en'
    if any(w in name for w in ["CTV", "AGHAPY", "MESAT", "KARMA", "NOURSAT"]): return ALL_AVAILABLE_CATEGORIES[0]
    if any(w in name for w in ["QURAN", "RAHMA", "MAJD", "MAKKA"]): return ALL_AVAILABLE_CATEGORIES[1]
    if any(w in name for w in ["MOSALSALAT", "DRAMA", "SERIES", "KHOLASA"]): return ALL_AVAILABLE_CATEGORIES[2]
    if any(w in name for w in ["CINEMA", "ROTANA", "AFLAM", "MIX", "FOX", "MBC2", "ACTION"]): return ALL_AVAILABLE_CATEGORIES[3]
    if any(w in name for w in ["SPACE TOON", "CN", "MAJID", "KIDS", "TOM"]): return ALL_AVAILABLE_CATEGORIES[4]
    if any(w in name for w in ["SPORT", "ONTIME", "KASS", "AD_SPORTS"]): return ALL_AVAILABLE_CATEGORIES[5]
    if any(w in name for w in ["NEWS", "JAZEERA", "ARABIYA", "HADATH", "CAIRO"]): return ALL_AVAILABLE_CATEGORIES[6]
    return ALL_AVAILABLE_CATEGORIES[7]

# منطقة رفع الملف
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

    # مصفوفة الترتيب المعتمدة على ضغط التشيك بوكس/الاختيار اليدوي الذكي
    st.write("---")
    st.write(f"### {t['config_title']}")
    st.write(t['config_tip'])
    
    user_priority = st.multiselect(
        t['multiselect_label'],
        options=ALL_AVAILABLE_CATEGORIES,
        default=[]
    )
    
    final_priority = list(user_priority)
    for cat in ALL_AVAILABLE_CATEGORIES:
        if cat not in final_priority:
            final_priority.append(cat)

    # معالجة الفرز
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

    # عرض المجسمات ثلاثية الأبعاد للفئات
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

    # الترتيب والعد التنازلي والبناء
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

# الفوتر السيبراني الاحترافي لـ رفيق رامبو بالبيانات وزر الواتساب المتطور
whatsapp_msg = urllib.parse.quote("Hello Rambo, I just deployed your futuristic 3D LG Sorter app and have an inquiry:")
whatsapp_url = f"https://web.whatsapp.com/send?phone=201280339779&text={whatsapp_msg}"

st.markdown(f"""
    <div class="footer">
        <h3>🛸 {t['footer_title']}</h3>
        <p dir="ltr"><b>{t['footer_contact']}</b></p>
        <a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">{t['whatsapp_btn']}</a>
    </div>
""", unsafe_allow_html=True)
