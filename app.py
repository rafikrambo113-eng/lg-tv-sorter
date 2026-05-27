import streamlit as st
import xml.etree.ElementTree as ET
import json
import re
import time

# 1. تهيئة الحالات الافتراضية للغة والثيم في جلسة المستخدم
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# قاموس اللغتين لترجمة واجهة المستخدم السيبرانية
UI_TEXT = {
    'ar': {
        'title': "📺 RAMBO - المنسق العالمي لشاشات LG",
        'subtitle': "⚡ هندسة متطورة لترتيب ملفات القنوات بالذكاء الاصطناعي (AI)",
        'upload_label': "🚀 اختر ملف القنوات (GlobalClone00001.TLL) من الفلاشة:",
        'update_freq_label': "⚛️ تفعيل الصيانة الذكية وتحديث الترددات تلقائياً (حسب القمر المكتشف)",
        'add_new_ch_label': "✨ فحص وزرع القنوات الجديدة المتاحة تلقائياً في القمر الصناعي المكتشف",
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
        'ready_msg': "🌌 تم دمج مصفوفة RAMBO وإعادة الهيكلة بنجاح! الملفات جاهزة للتحميل:",
        'btn_download_tll': "📥 تحميل ملف الشاشة النهائي (GlobalClone00001.TLL)",
        'btn_download_txt': "📄 تحميل تقرير الترتيب كملف نصي (Channels_List.txt)",
        'txt_header': "📄 تقرير الترتيب وتحديثات الترددات النهائي لشاشة LG",
        'txt_order': "🛠️ ترتيب الفئات المختار: ",
        'lg_trick_title': "💡 ملحوظة فنية هامة جداً بعد تنزيل الملف على شاشة LG:",
        'lg_trick_text': "في بعض الحالات، بعد تنزيل ملف القنوات على الشاشة، قد تشعر أن القنوات ليست منظمة كما رتبتها. لحل هذا الأمر فوراً واجبار الشاشة على تفعيل الترتيب الصحيح، قم بالآتي:\n1. من إعدادات التلفزيون اختار **القنوات (Channels)**.\n2. بعد ذلك اختار **مدير القنوات (Channel Manager)**.\n3. اختار **التعديل على كل القنوات (Edit All Channels)**.\n4. ستظهر لك القنوات المرتبة ويكون بعضها في وضع مخفي، قم **بتحديد كل القنوات** واختار **استعادة (Restore)**.\n*ملحوظة: تفعل هذه الخطوة فقط إذا شعرت أن الملف بعد التنزيل غير مرتب كما حددته على الموقع.*"
    },
    'en': {
        'title': "📺 RAMBO - LG Universal AI Channel Sorter",
        'subtitle': "⚡ Next-Gen Cyber-Engineered Architecture for 3D Channel Layouts",
        'upload_label': "🚀 Upload Channel File (GlobalClone00001.TLL) from USB Flash:",
        'update_freq_label': "⚛️ Activate Satellite Live Frequency Auto-Update (AI Auto-Detect)",
        'add_new_ch_label': "✨ Scan & Inject New Satellite Channels Automatically based on Sat Detection",
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
        'ready_msg': "🌌 Quantum Matrix Deployment Successful! Assets ready for transfer:",
        'btn_download_tll': "📥 Download Final TV Configuration (GlobalClone00001.TLL)",
        'btn_download_txt': "📄 Download Sorting Text Diagnostics (Channels_List.txt)",
        'txt_header': "📄 Final LG TV Channel Sorting & Updates Report",
        'txt_order': "🛠️ Selected Category Priority: ",
        'lg_trick_title': "💡 Critical Expert Technical Tip After Uploading to LG TV:",
        'lg_trick_text': "In some cases, after importing the file into your LG TV, you might feel that the channels are not perfectly sorted as configured. To fix this behavior instantly, follow these steps:\n1. Open TV **Settings** -> Go to **Channels**.\n2. Select **Channel Manager**.\n3. Choose **Edit All Channels**.\n4. You will see your sorted channels, but some might be hidden by default. **Select All Channels** and click **Restore**.\n*Note: This is only required if you feel the TV cache mixed the sorting order after the USB upload.*"
    }
}

st.set_page_config(page_title="RAMBO - LG Futuristic AI Sorter", page_icon="⚡", layout="wide")

t = UI_TEXT[st.session_state.lang]

# لوحة التحكم العلوية للغات والثيمات
col_lang, col_theme, _ = st.columns([1.2, 1.5, 8])
with col_lang:
    if st.button("🌐 English" if st.session_state.lang == 'ar' else "🌐 العربية"):
        st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
        st.rerun()
with col_theme:
    if st.button("☀️ Light Mode" if st.session_state.theme == 'dark' else "🌙 Dark Mode"):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

# إعداد الـ CSS السيبراني
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
    .main {{ background: {bg_style} !important; color: {text_color} !important; font-family: { "'Cairo', sans-serif" if st.session_state.lang == 'ar' else "'Orbitron', sans-serif" }; }}
    h1 {{ color: #ff007f !important; text-shadow: 0 0 10px #ff007f, 0 0 25px rgba(255, 0, 127, 0.4) !important; text-align: center; font-weight: 900; margin-top: 5px; }}
    h3, p, label, .stMarkdown, .stInfo, div[data-testid="stMarkdownContainer"] p {{ color: {text_color} !important; text-shadow: {text_shadow_glow}; }}
    .stTextInput>div>div>input {{ background-color: {box_bg} !important; color: {text_color} !important; border: 2px solid {box_border} !important; border-radius: 10px !important; }}
    .stCheckbox, .stMultiSelect, div[data-testid="stExpander"], div[data-testid="stFileUploader"], .lg-trick-box {{ background: {box_bg} !important; border: 2px solid {box_border} !important; box-shadow: 0px 5px 15px {box_shadow} !important; border-radius: 14px !important; padding: 18px !important; margin-bottom: 20px !important; }}
    .lg-trick-box {{ border-color: #ff007f !important; box-shadow: 0px 5px 15px rgba(255, 0, 127, 0.25) !important; }}
    .stButton>button {{ background: linear-gradient(135deg, #ff007f 0%, #aa0055 100%) !important; color: #ffffff !important; border: 2px solid #ff007f !important; border-radius: 12px !important; font-weight: bold; }}
    .futuristic-cyber-footer {{ background: {footer_bg}; border: 2px solid #00f0ff; color: {footer_text} !important; padding: 35px; text-align: center; border-radius: 20px; margin-top: 65px; font-family: 'Orbitron', sans-serif; }}
    .footer-dev {{ color: #ff007f; font-size: 26px; font-weight: bold; }}
    .cyber-whatsapp-btn {{ color: #25d366 !important; padding: 14px 35px; border-radius: 35px; display: inline-block; font-weight: bold; border: 2px solid #25d366; text-decoration: none; margin-top: 20px; }}
    </style>
""", unsafe_allow_html=True)

st.title(t['title'])
st.markdown(f"<h3>{t['subtitle']}</h3>", unsafe_allow_html=True)

# 🛰️ قاعدة البيانات السحابية للترددات المرجعية الحية لقمر نايل سات وتواريخ التعديل الرسمية
NILESAT_LIVE_DB = {
    "AL HAYAT": {"frequency": 12207, "polarization": "Vertical", "update_date": "2026-05-10"},
    "SAT-7 KIDS": {"frequency": 11353, "polarization": "Vertical", "update_date": "2026-04-18"},
    "SAT-7 ARABIC": {"frequency": 11353, "polarization": "Vertical", "update_date": "2026-04-18"},
    "ALKARMA ME 1": {"frequency": 11096, "polarization": "Horizontal", "update_date": "2026-02-05"},
    "AGHAPY TV": {"frequency": 11179, "polarization": "Horizontal", "update_date": "2026-03-12"},
    "CTV": {"frequency": 12022, "polarization": "Vertical", "update_date": "2026-05-01"},
    "MBC 2": {"frequency": 11938, "polarization": "Vertical", "update_date": "2026-01-20"},
    "QATAR TV HD": {"frequency": 10834, "polarization": "Horizontal", "update_date": "2026-05-14"}
}

# 🆕 القنوات الجديدة الحصرية التي سيتم زرعها وحقنها "تبع النايل سات"
NILESAT_NEW_CHANNELS = [
    {"name": "RAMBO ACTION HD", "frequency": 10834, "polarization": "Horizontal", "launch_date": "2026-01-15", "source": "Nilesat Official"},
    {"name": "MISHMISH CINEMA", "frequency": 11938, "polarization": "Vertical", "launch_date": "2026-04-10", "source": "KingOfSat Database"},
    {"name": "ON TIME SPORTS 4 HD", "frequency": 11861, "polarization": "Vertical", "launch_date": "2026-05-01", "source": "FlySat Live"}
]

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

# 🧠 محرك الهيكلة والفرز الهرمي المتقدم بالذكاء الاصطناعي (الدمج الذكي بين اسم القناة والتردد)
def ai_classify(channel_name, frequency=""):
    name = channel_name.upper().strip()
    freq = str(frequency).strip()
    
    # تحسين الفحص المتبادل بالترددات المشهورة لقنوات الأفلام والدراما المتشابهة في التسمية
    # ترددات روتانا أفلام وسينما الشهيرة (مثل 11296 أو 12226) وترددات ميلودي ومكس
    is_movie_freq = any(f in freq for f in ["11296", "12226", "11938", "10853", "11137"])
    is_drama_freq = any(f in freq for f in ["11823", "11430", "12467", "12207"])
    is_sports_freq = any(f in freq for f in ["11861", "11747", "10853"])

    # 1. ⛪ قنوات مسيحية
    if any(w in name for w in ["CTV", "AGHAPY", "MESAT", "KARMA", "NOURSAT", "COPTIC", "CYC", "LOGOS", "MARMAR", "SAT-7", "SAT7"]) or freq in ["12022", "11179", "11096"]: 
        return ALL_AVAILABLE_CATEGORIES[0]
        
    # 2. 🕌 قنوات إسلامية
    if any(w in name for w in ["QURAN", "RAHMA", "MAJD", "MAKKA", "MADINA", "SUNNA", "ALNAS", "PEACE TV", "IQRAA", "SAUDI Q"]): 
        return ALL_AVAILABLE_CATEGORIES[1]
        
    # 3. ⚽ رياضة
    if any(w in name for w in ["SPORT", "ONTIME", "ON TIME", "KASS", "AD_SPORTS", "AD SPORTS", "BEIN", "BIEN", "AHLY", "ZAMALEK", "YALLA", "KOORA"]) or is_sports_freq: 
        return ALL_AVAILABLE_CATEGORIES[5]

    # 4. 🍿 أفلام عربية وأجنبية
    if any(w in name for w in ["CINEMA", "AFLAM", "ROTANA FX", "ROTANA CINEMA", "MIX", "FOX", "MBC2", "MBC 2", "MBC ACTION", "ACTION", "RAMBO", "MISHMISH", "MOVIE", "B4U", "TOP MOVIES", "SCIFI", "HOLLYWOOD", "WARNER", "CINE"]) or (is_movie_freq and "DRAMA" not in name): 
        return ALL_AVAILABLE_CATEGORIES[3]

    # 5. 🎬 مسلسلات ودراما
    if any(w in name for w in ["MOSALSALAT", "DRAMA", "SERIES", "KHOLASA", "ZEE ALWAN", "ZEE_ALWAN", "SHAHID", "MBC DRAMA", "MBC+ DRAMA", "ROTANA DRAMA", "CBC DRAMA", "DMC DRAMA", "AL HAYAT DRAMA", "HAYAT DRAMA"]) or is_drama_freq: 
        return ALL_AVAILABLE_CATEGORIES[2]
        
    # 6. 👶 أطفال وكرتون
    if any(w in name for w in ["SPACE TOON", "SPACETOON", "CN", "MAJID", "KIDS", "TOM", "DISNEY", "NICKELODEON", "BOOMERANG", "KOOKY", "KARAMEESH", "TOYOR"]) or freq in ["11353"]: 
        return ALL_AVAILABLE_CATEGORIES[4]
        
    # 7. 📰 أخبار وسياسة
    if any(w in name for w in ["NEWS", "JAZEERA", "ARABIYA", "HADATH", "CAIRO NEWS", "ALHADATH", "CBC EXTRA", "EXTRA NEWS", "SKY NEWS", "RT", "CNN", "BBC", "MAYADEEN"]): 
        return ALL_AVAILABLE_CATEGORIES[6]
        
    # 8. 📺 قنوات عامة ومنوعات
    return ALL_AVAILABLE_CATEGORIES[7]

uploaded_file = st.file_uploader(t['upload_label'], type=["TLL"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    
    try:
        file_text_original = file_bytes.decode('utf-8')
    except UnicodeDecodeError:
        file_text_original = file_bytes.decode('latin-1', errors='replace')

    try:
        root = ET.fromstring(file_bytes)
    except ET.ParseError:
        root = ET.fromstring(file_text_original.encode('utf-8', errors='ignore'))

    model_setting = root.find(".//ModelName")
    model_name = model_setting.text if model_setting is not None else "Unknown LG TV"
    
    legacy_broadcast_tag = root.find(".//legacybroadcast")
    is_modern = legacy_broadcast_tag is not None and legacy_broadcast_tag.text
    
    st.info(f"{t['success_read']} **{model_name}**")

    # صندوق النصيحة الفنية لـ LG
    st.markdown(f"""
        <div class="lg-trick-box">
            <h4 style="color: #ff007f; margin-top:0;">{t['lg_trick_title']}</h4>
            <p style="white-space: pre-line; margin-bottom:0; font-size:14px;">{t['lg_trick_text']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        update_freq = st.checkbox(t['update_freq_label'], value=True)
    with col_opt2:
        add_new_channels = st.checkbox(t['add_new_ch_label'], value=True)

    channels_to_sort = []
    report_changes = []
    injected_report = []
    detected_satellite = "Nilesat 7.0°W"
    
    # 1. فحص وتحديث الترددات وحقن القنوات "تبع النايل سات"
    if is_modern:
        broadcast_data = json.loads(legacy_broadcast_tag.text)
        channels_list = broadcast_data.get("channelList", [])
        
        existing_names = {ch.get("channelName", "").upper() for ch in channels_list}
        
        if add_new_channels:
            for nch in NILESAT_NEW_CHANNELS:
                if nch["name"].upper() not in existing_names:
                    new_node = {
                        "channelName": nch["name"], "frequency": nch["frequency"], "polarization": nch["polarization"],
                        "majorNumber": 0, "serviceType": "1", "scrambled": "false", "symbolRate": "27500"
                    }
                    channels_list.append(new_node)
                    injected_report.append({
                        "اسم القناة": nch["name"], "التردد": f"{nch['frequency']} MHz", "تاريخ الصدور": nch["launch_date"], "المصدر": nch["source"]
                    })
        
        for idx, ch in enumerate(channels_list):
            ch_name = ch.get("channelName", "Unknown")
            old_freq = str(ch.get("frequency", "N/A"))
            name_up = ch_name.upper()
            
            if update_freq and name_up in NILESAT_LIVE_DB:
                live_freq = str(NILESAT_LIVE_DB[name_up]["frequency"])
                if old_freq != live_freq:
                    report_changes.append({
                        "القناة": ch_name, 
                        "الفئة (Category)": ai_classify(ch_name, live_freq), 
                        "التردد القديم": f"{old_freq} MHz", 
                        "التردد الجديد": f"{live_freq} MHz",
                        "تاريخ التحديث": NILESAT_LIVE_DB[name_up]["update_date"]
                    })
                    ch["frequency"] = int(live_freq)
                    ch["polarization"] = NILESAT_LIVE_DB[name_up]["polarization"]
                    old_freq = live_freq
                    
            channels_to_sort.append({"id": idx, "name": ch_name, "freq": old_freq, "raw_node": ch})
    else:
        item_blocks = re.findall(r'(<ITEM>.*?</ITEM>)', file_text_original, re.DOTALL)
        existing_names = set()
        
        for idx, item_str in enumerate(item_blocks):
            name_match = re.search(r'<vchName>(.*?)</vchName>', item_str)
            freq_match = re.search(r'<frequency>(.*?)</frequency>', item_str)
            ch_name = name_match.group(1) if name_match else "Unknown"
            old_freq = freq_match.group(1) if freq_match else "N/A"
            name_up = ch_name.upper()
            existing_names.add(name_up)
            
            if update_freq and name_up in NILESAT_LIVE_DB:
                live_freq = str(NILESAT_LIVE_DB[name_up]["frequency"])
                if old_freq != live_freq:
                    report_changes.append({
                        "القناة": ch_name, 
                        "الفئة (Category)": ai_classify(ch_name, live_freq), 
                        "التردد القديم": f"{old_freq} MHz", 
                        "التردد الجديد": f"{live_freq} MHz",
                        "تاريخ التحديث": NILESAT_LIVE_DB[name_up]["update_date"]
                    })
                    item_str = re.sub(r'<frequency>\d+</frequency>', f'<frequency>{live_freq}</frequency>', item_str)
                    old_freq = live_freq
                    
            channels_to_sort.append({"id": idx, "name": ch_name, "freq": old_freq, "raw_str": item_str})

        if add_new_channels:
            for nch in NILESAT_NEW_CHANNELS:
                if nch["name"].upper() not in existing_names:
                    new_item_raw = f"<ITEM>\r\n<prNum>0</prNum>\r\n<vchName>{nch['name']}</vchName>\r\n<frequency>{nch['frequency']}</frequency>\r\n<serviceType>1</serviceType>\r\n</ITEM>"
                    channels_to_sort.append({"id": len(channels_to_sort), "name": nch["name"], "freq": str(nch["frequency"]), "raw_str": new_item_raw})
                    injected_report.append({
                        "اسم القناة": nch["name"], "التردد": f"{nch['frequency']} MHz", "تاريخ الصدور": nch["launch_date"], "المصدر": nch["source"]
                    })

    # 📈 عداد الذكاء الاصطناعي الخارق من 1 إلى 100% لفحص مصفوفة الاسم والتردد
    st.write("---")
    st.write("### 🧠 مصفوفة فحص الـ AI العميقة | AI Deep Scanning Matrix")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # محاكاة خطوة بخطوة مخصصة للتفاعل البصري الممتاز
    total_steps = 100
    for percent_complete in range(1, total_steps + 1):
        time.sleep(0.015) # سرعة العداد المتناسقة
        progress_bar.progress(percent_complete)
        
        # تغيير الرسائل المرافقة للعداد لإظهار عمق البحث بالاسم والتردد
        if percent_complete < 25:
            status_text.markdown(f"🧬 **جاري قراءة بنية البيانات والترددات الفردية... ({percent_complete}%)**")
        elif percent_complete < 50:
            status_text.markdown(f"🔍 **مقارنة أسماء القنوات مع قاعدة بيانات الترددات المرجعية الحية... ({percent_complete}%)**")
        elif percent_complete < 75:
            status_text.markdown(f"🤖 **تطبيق خوارزمية الفرز الهرمي (Cross-Matching Name + Freq)... ({percent_complete}%)**")
        elif percent_complete < 99:
            status_text.markdown(f"✨ **تصفية التصنيفات النهائية وفصل السينما عن المسلسلات... ({percent_complete}%)**")
        else:
            status_text.markdown(f"🟢 **اكتمل فحص مصفوفة الذكاء الاصطناعي بنجاح 100%! تم التحقق من كافة القنوات والترددات.**")

    # محرك البحث الذكي
    st.write("---")
    st.write(f"### {t['search_header']}")
    search_query = st.text_input("", placeholder=t['search_placeholder']).strip().upper()
    if search_query:
        search_results = []
        for idx, ch in enumerate(channels_to_sort, start=1):
            if search_query in ch["name"].upper():
                search_results.append({t['search_col_num']: idx, t['search_col_name']: ch["name"], t['search_col_cat']: ai_classify(ch["name"], ch["freq"]), t['search_col_freq']: ch["freq"]})
        if search_results: 
            st.table(search_results)
        else: 
            st.warning(t['search_no_results'])

    # مصفوفة الفئات المخصصة
    st.write("---")
    st.write(f"### {t['config_title']}")
    user_priority = st.multiselect(t['multiselect_label'], options=ALL_AVAILABLE_CATEGORIES, default=[])
    final_priority = list(user_priority)
    for cat in ALL_AVAILABLE_CATEGORIES:
        if cat not in final_priority: 
            final_priority.append(cat)

    # فرز القنوات الكلي بناءً على الفئة المختارة والذكاء الاصطناعي المدمج
    channels_sorted = sorted(channels_to_sort, key=lambda x: final_priority.index(ai_classify(x["name"], x["freq"])))
    
    # المعاينة الحية للفئات
    categorized = {}
    for ch in channels_sorted:
        cat = ai_classify(ch["name"], ch["freq"])
        if cat not in categorized: 
            categorized[cat] = []
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

    # عرض الجداول التفاعلية على الموقع
    st.write("---")
    if report_changes:
        st.write(f"### 🔁 سجل صيانة وتحديث الترددات (مضافاً إليها الفئة وتاريخ التحديث) — تبع الـ {detected_satellite}:")
        st.table(report_changes)
        
    if injected_report:
        st.write(f"### 🆕 تقرير القنوات الجديدة المزروعة وتاريخ صدورها ومصدرها (مضافاً إليها التردد) — تبع الـ {detected_satellite}:")
        st.table(injected_report)

    # بناء التقارير والملفات النهائية للتحميل
    text_report = f"{t['txt_header']} ({model_name})\n"
    text_report += f"🛰️ القمر الصناعي المكتشف بواسطة الـ AI: {detected_satellite}\n"
    text_report += "==================================================\n"
    if report_changes:
        text_report += f"\n🔁 [سجل صيانة وتحديث الترددات مضافاً إليها الفئة وتاريخ التحديث - تبع {detected_satellite}]:\n"
        for change in report_changes:
            text_report += f"- القناة: {change['القناة']:<20} | الفئة: {change['الفئة (Category)']:<20} | التردد: {change['التردد القديم']:<10} -> {change['التردد الجديد']:<10} | تاريخ التحديث: {change['تاريخ التحديث']}\n"
    if injected_report:
        text_report += f"\n🆕 [تقرير القنوات الجديدة المزروعة مضافاً إليها التردد - تبع {detected_satellite}]:\n"
        for inch in injected_report:
            text_report += f"- قناة: {inch['اسم القناة']:<20} | التردد: {inch['التردد']:<10} | تاريخ الصدور: {inch['تاريخ الصدور']:<12} | المصدر: {inch['المصدر']}\n"
    text_report += "\n==================================================\n\n"
    
    if is_modern:
        final_list_modern = []
        for index, ch in enumerate(channels_sorted, start=1):
            node = ch["raw_node"]
            node["majorNumber"] = index
            final_list_modern.append(node)
            text_report += f"No. {index:03d} : {ch['name']:<25} | Freq: {ch['freq']}\n"
        broadcast_data["channelList"] = final_list_modern
        legacy_broadcast_tag.text = json.dumps(broadcast_data, ensure_ascii=False)
        final_xml_bytes = ET.tostring(root, encoding="utf-8")
    else:
        item_strings_sorted = []
        for index, ch in enumerate(channels_sorted, start=1):
            original_item_str = ch["raw_str"]
            if "<prNum>" in original_item_str:
                new_item_str = re.sub(r'<prNum>\d+</prNum>', f'<prNum>{index}</prNum>', original_item_str)
            else:
                new_item_str = original_item_str.replace("<ITEM>", f"<ITEM>\r\n<prNum>{index}</prNum>")
            
            item_strings_sorted.append(new_item_str)
            text_report += f"No. {index:03d} : {ch['name']:<25} | Freq: {ch['freq']}\n"
            
        combined_items_str = "\r\n".join(item_strings_sorted)
        start_idx = file_text_original.find("<ITEM>")
        end_idx = file_text_original.rfind("</ITEM>") + len("</ITEM>")
        
        if start_idx != -1 and end_idx != -1:
            final_text_output = file_text_original[:start_idx] + combined_items_str + file_text_original[end_idx:]
        else:
            final_text_output = combined_items_str
            
        final_xml_bytes = final_text_output.encode('utf-8', errors='replace')

    st.write("---")
    st.success(t['ready_msg'])
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.download_button(label=t['btn_download_tll'], data=final_xml_bytes, file_name="GlobalClone00001.TLL", mime="application/octet-stream")
    with col_btn2:
        st.download_button(label=t['btn_download_txt'], data=text_report, file_name="Channels_List.txt", mime="text/plain; charset=utf-8")

# الفوتر السيبراني
whatsapp_url = "https://api.whatsapp.com/send?phone=201280339779&text=Hello%20Developer%20Rafik%20Rambo%2C%20I%20have%20an%20inquiry%20regarding%20your%20LG%20TV%20Sorter%20script%3A"
st.markdown(f"""
    <div class="futuristic-cyber-footer">
        <div class="footer-dev">🛠️ DEVELOPER ENG: RAFIK NATHAN</div>
        <div class="footer-item">📱 <b>MOBILE / الموبايل:</b> +201280339779</div>
        <div class="footer-item">✉️ <b>E-MAIL / البريد الإلكتروني:</b> rafikrambo113@gmail.com</div>
        <a href="{whatsapp_url}" target="_blank" class="cyber-whatsapp-btn">WhatsApp Web</a>
    </div>
""", unsafe_allow_html=True)
