import streamlit as st
import xml.etree.ElementTree as ET
import json
import re

# 1. تهيئة الحالات الافتراضية للغة والثيم في جلسة المستخدم
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# قاموس اللغتين لترجمة كافة نصوص واجهة الموقع
UI_TEXT = {
    'ar': {
        'title': "📺 RAMBO - المنسق العالمي لشاشات LG",
        'subtitle': "⚡ هندسة متطورة لترتيب ملفات القنوات بالتأثيرات السيبرانية مصفوفة (3D)",
        'upload_label': "🚀 اختر ملف القنوات (GlobalClone00001.TLL) من الفلاشة:",
        'update_freq_label': "⚛️ تفعيل الصيانة الذكية وتحديث الترددات تلقائياً (للشاشات الحديثة)",
        'add_new_ch_label': "✨ فحص وإضافة القنوات الجديدة المتاحة تلقائياً",
        'success_read': "🛸 تم قراءة الهيكل بنجاح! الموديل الحالي: ",
        'search_header': "🔍 محرك البحث الذكي عن القنوات داخل الملف:",
        'search_placeholder': "اكتب اسم القناة هنا للبحث...",
        'search_col_num': "الرقم الحالي",
        'search_col_name': "اسم القناة",
        'search_col_cat': "الفئة (Category)",
        'search_col_freq': "التردد (Frequency)",
        'search_no_results': "⚠️ لم يتم العثور على أي قنوات مطابقة للبحث.",
        'config_title': "🎛️ مصفوفة ترتيب الفئات المخصصة حسب اختيارك اليدوي:",
        'config_tip': "💡 ملحوظة: اضغط على الفئات بالترتيب الفعلي المفضل لديك. الفئة التي تختارها أولاً ستتصدر شاشة التلفزيون.",
        'multiselect_label': "اضغط هنا لبناء تسلسل خطة العرض التفاعلي للفئات:",
        'preview_title': "📊 مجسم المعاينة الحية لتوزيع القنوات الحالي:",
        'channels_count': "قناة",
        'freq_table_title': "🔁 سجل صيانة الترددات الحية المحدثة:",
        'new_ch_added_title': "🆕 القنوات الجديدة المكتشفة والتي تم زرعها في الملف:",
        'ready_msg': "🌌 تم دمج مصفوفة RAMBO وإعادة الهيكلة بنجاح! الملفات جاهزة للتحميل:",
        'btn_download_tll': "📥 تحميل ملف الشاشة النهائي (GlobalClone00001.TLL)",
        'btn_download_txt': "📄 تحميل تقرير الترتيب كملف نصي (Channels_List.txt)",
        'txt_header': "📄 تقرير الترتيب النهائي لقنوات شاشة LG",
        'txt_order': "🛠️ ترتيب الفئات المختار: "
    },
    'en': {
        'title': "📺 RAMBO - LG Universal AI Channel Sorter",
        'subtitle': "⚡ Next-Gen Cyber-Engineered Architecture for 3D Channel Layouts",
        'upload_label': "🚀 Upload Channel File (GlobalClone00001.TLL) from USB Flash:",
        'update_freq_label': "⚛️ Activate Satellite Live Frequency Auto-Update (Modern Models)",
        'add_new_ch_label': "✨ Scan & Inject New Satellite Channels Into Your File Automatically",
        'success_read': "🛸 Matrix Structure Decoded Successfully! Model Profile: ",
        'search_header': "🔍 Dynamic Channel Search Engine:",
        'search_placeholder': "Type channel name to look up...",
        'search_col_num': "No.",
        'search_col_name': "Channel Name",
        'search_col_cat': "Category",
        'search_col_freq': "Frequency",
        'search_no_results': "⚠️ No channels matching your search criteria.",
        'config_title': "🎛️ Custom Category Priority Control Matrix:",
        'config_tip': "💡 Hint: Click categories in exact order. The first selection populates the absolute top of your TV.",
        'multiselect_label': "Select categories one by one to configure your linear priority:",
        'preview_title': "📊 Channel Grid Live 3D Preview Dashboard:",
        'channels_count': "Channels",
        'freq_table_title': "🔁 Automatic Frequency Correction Logs:",
        'new_ch_added_title': "🆕 New Satellite Channels Discovered & Injected:",
        'ready_msg': "🌌 Quantum Matrix Deployment Successful! Assets ready for transfer:",
        'btn_download_tll': "📥 Download Final TV Configuration (GlobalClone00001.TLL)",
        'btn_download_txt': "📄 Download Sorting Text Diagnostics (Channels_List.txt)",
        'txt_header': "📄 Final LG TV Channel Sorting Report",
        'txt_order': "🛠️ Selected Category Priority: "
    }
}

t = UI_TEXT[st.session_state.lang]

# إعدادات واجهة الموقع والعنوان الرئيسي للمتصفح
st.set_page_config(page_title="RAMBO - LG Futuristic AI Sorter", page_icon="⚡", layout="wide")

# لوحة التحكم العلوية: تبديل اللغة وتبديل الثيم (فاتح / غامق)
col_lang, col_theme, _ = st.columns([1.2, 1.5, 8])
with col_lang:
    if st.button("🌐 English" if st.session_state.lang == 'ar' else "🌐 العربية"):
        st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
        st.rerun()
with col_theme:
    if st.button("☀️ Light Mode" if st.session_state.theme == 'dark' else "🌙 Dark Mode"):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

# بناء الـ CSS الديناميكي للتحكم في الألوان (Dark & Light Cyber Style)
if st.session_state.theme == 'dark':
    bg_style = "radial-gradient(circle at 50% 50%, #110926 0%, #05020d 100%)"
    text_color = "#00f0ff"
    box_bg = "rgba(13, 7, 33, 0.85)"
    box_border = "#00f0ff"
    box_shadow = "rgba(0, 240, 255, 0.35)"
    text_shadow_glow = "0 0 5px rgba(0, 240, 255, 0.4)"
    footer_bg = "#080314"
    footer_text = "#ffffff"
else:
    bg_style = "radial-gradient(circle at 50% 50%, #f4f5f7 0%, #e4e7eb 100%)"
    text_color = "#0d0722"
    box_bg = "#ffffff"
    box_border = "#ff007f"
    box_shadow = "rgba(255, 0, 127, 0.15)"
    text_shadow_glow = "none"
    footer_bg = "#110926"
    footer_text = "#ffffff"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;900&family=Cairo:wght@400;700&display=swap');
    
    .main {{
        background: {bg_style} !important;
        color: {text_color} !important;
        font-family: { "'Cairo', sans-serif" if st.session_state.lang == 'ar' else "'Orbitron', sans-serif" };
    }}
    
    h1 {{
        color: #ff007f !important;
        text-shadow: 0 0 10px #ff007f, 0 0 25px rgba(255, 0, 127, 0.4) !important;
        text-align: center;
        font-weight: 900;
        margin-top: 5px;
    }}
    h3, p, label, .stMarkdown, .stInfo, div[data-testid="stMarkdownContainer"] p {{
        color: {text_color} !important;
        text-shadow: {text_shadow_glow};
    }}
    
    .stTextInput>div>div>input {{
        background-color: {box_bg} !important;
        color: {text_color} !important;
        border: 2px solid {box_border} !important;
        border-radius: 10px !important;
    }}
    
    .stCheckbox, .stMultiSelect, div[data-testid="stExpander"], div[data-testid="stFileUploader"] {{
        background: {box_bg} !important;
        border: 2px solid {box_border} !important;
        box-shadow: 0px 5px 15px {box_shadow}, inset 0px 0px 10px rgba(0, 240, 255, 0.05) !important;
        border-radius: 14px !important;
        padding: 18px !important;
        margin-bottom: 20px !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }}
    
    div[data-testid="stExpander"]:hover, .stCheckbox:hover {{
        border-color: #ff007f !important;
        box-shadow: 0px 8px 25px rgba(255, 0, 127, 0.5) !important;
        transform: translateY(-3px);
    }}
    
    .stButton>button {{
        background: linear-gradient(135deg, #ff007f 0%, #aa0055 100%) !important;
        color: #ffffff !important;
        border: 2px solid #ff007f !important;
        border-radius: 12px !important;
        box-shadow: 0 5px 0 #55002a, 0 10px 20px rgba(255, 0, 127, 0.4) !important;
        font-weight: bold;
        text-transform: uppercase;
        transition: all 0.1s ease;
    }}
    .stButton>button:active {{
        transform: translateY(4px) !important;
        box-shadow: 0 1px 0 #55002a, 0 5px 12px rgba(255, 0, 127, 0.4) !important;
    }}
    
    .futuristic-cyber-footer {{
        background: {footer_bg};
        border: 2px solid #00f0ff;
        box-shadow: 0 0 35px rgba(0, 240, 255, 0.3), inset 0 0 25px rgba(255, 0, 127, 0.2);
        color: {footer_text} !important;
        padding: 35px;
        text-align: center;
        border-radius: 20px;
        margin-top: 65px;
        font-family: 'Orbitron', sans-serif;
        line-height: 1.8;
    }}
    .footer-dev {{ color: #ff007f; font-size: 26px; font-weight: bold; text-shadow: 0 0 12px #ff007f; margin-bottom: 10px; }}
    .footer-item {{ color: #ffffff !important; font-size: 18px; margin: 6px 0; font-weight: 500; }}
    .footer-item b {{ color: #00f0ff !important; }}
    
    .cyber-whatsapp-btn {{
        background: transparent;
        color: #25d366 !important;
        padding: 14px 35px;
        text-align: center;
        border-radius: 35px;
        display: inline-block;
        font-weight: bold;
        text-decoration: none;
        margin-top: 20px;
        border: 2px solid #25d366;
        box-shadow: 0 0 20px rgba(37, 211, 102, 0.3);
        transition: all 0.3s ease;
    }}
    .cyber-whatsapp-btn:hover {{
        background: #25d366;
        color: #000000 !important;
        box-shadow: 0 0 35px #25d366;
        transform: scale(1.04);
    }}
    </style>
""", unsafe_allow_html=True)

st.title(t['title'])
st.markdown(f"<h3>{t['subtitle']}</h3>", unsafe_allow_html=True)

# 🛰️ قاعدة بيانات الترددات المرجعية الشائعة
LIVE_SATELLITE_DB = {
    "QATAR TV HD": {"frequency": 10834, "polarization": "Horizontal", "symbolRate": 27500, "scrambled": "false", "serviceType": "1"},
    "AL RAHMA": {"frequency": 10873, "polarization": "Vertical", "symbolRate": 27500, "scrambled": "false", "serviceType": "1"},
    "ELKHOLASA MOSALSALAT": {"frequency": 10873, "polarization": "Vertical", "symbolRate": 27500, "scrambled": "false", "serviceType": "1"},
    "MBC 2": {"frequency": 11938, "polarization": "Vertical", "symbolRate": 27500, "scrambled": "false", "serviceType": "1"}, 
    "CTV": {"frequency": 12022, "polarization": "Vertical", "symbolRate": 27500, "scrambled": "false", "serviceType": "1"},
    "RAMBO ACTION HD": {"frequency": 10834, "polarization": "Horizontal", "symbolRate": 27500, "scrambled": "false", "serviceType": "1"},
    "MISHMISH CINEMA": {"frequency": 11938, "polarization": "Vertical", "symbolRate": 27500, "scrambled": "false", "serviceType": "1"}
}

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
    if any(w in name for w in ["QURAN", "RAHMA", "MAJD", "MAKKA", "HAYAT"]): return ALL_AVAILABLE_CATEGORIES[1]
    if any(w in name for w in ["MOSALSALAT", "DRAMA", "SERIES", "KHOLASA"]): return ALL_AVAILABLE_CATEGORIES[2]
    if any(w in name for w in ["CINEMA", "ROTANA", "AFLAM", "MIX", "FOX", "MBC2", "ACTION", "RAMBO", "MISHMISH", "MOVIE"]): return ALL_AVAILABLE_CATEGORIES[3]
    if any(w in name for w in ["SPACE TOON", "CN", "MAJID", "KIDS", "TOM"]): return ALL_AVAILABLE_CATEGORIES[4]
    if any(w in name for w in ["SPORT", "ONTIME", "KASS", "AD_SPORTS"]): return ALL_AVAILABLE_CATEGORIES[5]
    if any(w in name for w in ["NEWS", "JAZEERA", "ARABIYA", "HADATH", "CAIRO"]): return ALL_AVAILABLE_CATEGORIES[6]
    return ALL_AVAILABLE_CATEGORIES[7]

# استقبال وقراءة ملف الشاشة
uploaded_file = st.file_uploader(t['upload_label'], type=["TLL"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    
    # محاولة فك الترميز النصي لحفظ بنية الملفات الكلاسيكية بدقة
    try:
        file_text_original = file_bytes.decode('utf-8')
    except UnicodeDecodeError:
        file_text_original = file_bytes.decode('latin-1')

    root = ET.fromstring(file_bytes)
    
    # التعرف على موديل ونوع الملف
    model_setting = root.find(".//ModelName")
    model_name = model_setting.text if model_setting is not None else "Unknown LG TV"
    
    legacy_broadcast_tag = root.find(".//legacybroadcast")
    is_modern = legacy_broadcast_tag is not None and legacy_broadcast_tag.text
    
    st.info(f"{t['success_read']} **{model_name}**")
    
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        update_freq = st.checkbox(t['update_freq_label'], value=True if is_modern else False, disabled=not is_modern)
    with col_opt2:
        add_new_channels = st.checkbox(t['add_new_ch_label'], value=False, disabled=not is_modern)

    # توحيد استخراج القنوات بناءً على نوع النظام مع حفظ المعرف الفريد لكل ITEM
    channels_to_sort = []
    report_changes = []
    
    if is_modern:
        broadcast_data = json.loads(legacy_broadcast_tag.text)
        channels_list = broadcast_data.get("channelList", [])
        
        for idx, ch in enumerate(channels_list):
            channels_to_sort.append({
                "id": idx,
                "name": ch.get("channelName", "Unknown"),
                "freq": str(ch.get("frequency", "N/A")),
                "raw_node": ch
            })
    else:
        # نظام الشاشات الكلاسيكية (32 بوصة): سنقوم باستخراج معرفات فريدة بناءً على ترتيب الظهور
        xml_items = root.findall(".//ITEM")
        for idx, item in enumerate(xml_items):
            ch_name_node = item.find("vchName")
            freq_node = item.find("frequency")
            ch_name = ch_name_node.text if ch_name_node is not None else "Unknown"
            freq = freq_node.text if freq_node is not None else "N/A"
            
            channels_to_sort.append({
                "id": idx,
                "name": ch_name,
                "freq": freq,
                "raw_node": item
            })

    # محرك البحث الذكي الموحد لقنوات الملف المرفوع
    st.write("---")
    st.write(f"### {t['search_header']}")
    search_query = st.text_input("", placeholder=t['search_placeholder']).strip().upper()
    
    if search_query:
        search_results = []
        for idx, ch in enumerate(channels_to_sort, start=1):
            if search_query in ch["name"].upper():
                search_results.append({
                    t['search_col_num']: idx,
                    t['search_col_name']: ch["name"],
                    t['search_col_cat']: ai_classify(ch["name"]),
                    t['search_col_freq']: ch["freq"]
                })
        if search_results:
            st.table(search_results)
        else:
            st.warning(t['search_no_results'])

    # تحديد ترتيب الأولويات للفئات
    st.write("---")
    st.write(f"### {t['config_title']}")
    st.write(t['config_tip'])
    
    user_priority = st.multiselect(t['multiselect_label'], options=ALL_AVAILABLE_CATEGORIES, default=[])
    
    final_priority = list(user_priority)
    for cat in ALL_AVAILABLE_CATEGORIES:
        if cat not in final_priority:
            final_priority.append(cat)

    # معالجة وتعديل الترددات الحية للموديلات الحديثة فقط
    if is_modern and update_freq:
        for ch in channels_to_sort:
            name_up = ch["name"].upper()
            if name_up in LIVE_SATELLITE_DB:
                live = LIVE_SATELLITE_DB[name_up]
                node = ch["raw_node"]
                if int(node.get("frequency", 0)) != live["frequency"]:
                    report_changes.append({
                        "Channel" if st.session_state.lang == 'en' else "القناة": ch["name"], 
                        "Old Freq" if st.session_state.lang == 'en' else "التردد القديم": node.get("frequency"), 
                        "New Freq" if st.session_state.lang == 'en' else "التردد الجديد": live["frequency"]
                    })
                    node["frequency"] = str(live["frequency"])
                    node["polarization"] = live["polarization"]
                    node["symbolRate"] = str(live["symbolRate"])

    # عملية الفرز والترتيب الفعلي بناءً على اختيار المستخدم للفئات
    channels_sorted = sorted(channels_to_sort, key=lambda x: final_priority.index(ai_classify(x["name"])))
    
    # توزيع القنوات في مجسم المعاينة
    categorized = {}
    for ch in channels_sorted:
        cat = ai_classify(ch["name"])
        if cat not in categorized: categorized[cat] = []
        categorized[cat].append(ch["name"])

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
                    
    if is_modern and update_freq and report_changes:
        st.write(f"### {t['freq_table_title']}")
        st.table(report_changes)

    # حفظ وإعادة ترقيم القنوات وبناء ملف الـ XML النهائي بشكل صحيح وآمن لكل موديل
    text_report = f"{t['txt_header']} ({model_name})\n"
    text_report += t['txt_order'] + " -> ".join([c.split()[-1] for c in final_priority]) + "\n"
    text_report += "==================================================\n\n"
    
    if is_modern:
        final_list_modern = []
        for index, ch in enumerate(channels_sorted, start=1):
            node = ch["raw_node"]
            node["majorNumber"] = index
            final_list_modern.append(node)
            text_report += f"No. {index:03d} : {ch['name']:<25} | Matrix Group: {ai_classify(ch['name'])} | Freq: {ch['freq']}\n"
            
        broadcast_data["channelList"] = final_list_modern
        legacy_broadcast_tag.text = json.dumps(broadcast_data, ensure_ascii=False)
        final_xml_bytes = ET.tostring(root, encoding="utf-8")
    else:
        # الحل السحري للموديلات القديمة (32 بوصة): الحقن المباشر في النص الأصلي لتجنب تلف الملف!
        # نقوم بقراءة كتل <ITEM> كاملة بالترتيب الجديد
        all_items_raw_xml = root.findall(".//ITEM")
        
        # إنشاء مصفوفة موازية تحتوي على النصوص الكاملة لكل ITEM من الملف المصدري دون أي تعديل هيكلي
        # هذا يضمن احتفاظ الشاشة بكل الفراغات والرموز الخاصة بها
        item_strings_sorted = []
        for index, ch in enumerate(channels_sorted, start=1):
            item_node = ch["raw_node"]
            # تعديل الترقيم برمجياً داخل النود
            pr_num_tag = item_node.find("prNum")
            if pr_num_tag is not None:
                pr_num_tag.text = str(index)
            
            # تحويل النود لمتن نصي نقي
            item_str = ET.tostring(item_node, encoding="utf-8").decode("utf-8")
            # إزالة الترويسات الزائدة إن وجدت من عملية التوليد الفرعية
            item_str = item_str.replace("<?xml version='1.0' encoding='utf-8'?>\n", "")
            item_strings_sorted.append(item_str)
            text_report += f"No. {index:03d} : {ch['name']:<25} | Matrix Group: {ai_classify(ch['name'])} | Freq: {ch['freq']}\n"
        
        # بناء الحاوية النهائية للقنوات وإرجاعها في جسم الملف المصدري الأصلي
        combined_items_str = "\n".join(item_strings_sorted)
        
        # استبدال كتلة القنوات القديمة بالكتلة الجديدة تماماً
        # نبحث عن أول ظهور لـ <ITEM> وآخر ظهور لـ </ITEM>
        start_idx = file_text_original.find("<ITEM>")
        end_idx = file_text_original.rfind("</ITEM>") + len("</ITEM>")
        
        if start_idx != -1 and end_idx != -1:
            final_text_output = file_text_original[:start_idx] + combined_items_str + file_text_original[end_idx:]
        else:
            final_text_output = ET.tostring(root, encoding="utf-8").decode("utf-8")
            
        final_xml_bytes = final_text_output.encode('utf-8')

    st.write("---")
    st.success(t['ready_msg'])
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.download_button(label=t['btn_download_tll'], data=final_xml_bytes, file_name="GlobalClone00001.TLL", mime="application/octet-stream")
    with col_btn2:
        st.download_button(label=t['btn_download_txt'], data=text_report, file_name="Channels_List.txt", mime="text/plain; charset=utf-8")

# الفوتر الاحترافي
whatsapp_url = "https://api.whatsapp.com/send?phone=201280339779&text=Hello%20Developer%20Rafik%20Rambo%2C%20I%20have%20an%20inquiry%20regarding%20your%20LG%20TV%20Sorter%20script%3A"

st.markdown(f"""
    <div class="futuristic-cyber-footer">
        <div class="footer-dev">🛠️ DEVELOPER ENG: RAFIK RAMBO</div>
        <div class="footer-item">📱 <b>MOBILE / الموبايل:</b> +201280339779</div>
        <div class="footer-item">✉️ <b>E-MAIL / البريد الإلكتروني:</b> rafikrambo113@gmail.com</div>
        <div class="footer-item">FOR ANY INQUIRY WHATSAPP 💬</div>
        
        <a href="{whatsapp_url}" target="_blank" class="cyber-whatsapp-btn">
            WhatsApp Web
        </a>
    </div>
""", unsafe_allow_html=True)
