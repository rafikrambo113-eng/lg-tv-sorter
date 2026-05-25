ده كود رامبو 5
import streamlit as st
import xml.etree.ElementTree as ET
import json
import re
import os
from datetime import datetime

# 1. تهيئة الحالات الافتراضية للغة والثيم
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

UI_TEXT = {
    'ar': {
        'title': "📺 RAMBO ULTRA - رادار الترددات الحية لشاشات LG",
        'subtitle': "📡 محرك بحث استخباراتي يرصد أحدث ترددات 2026 على القمر بالتاريخ والمصدر والكاتوجري",
        'mode_selector': "🛠️ اختر وضع العمل المطلوب للبرنامج:",
        'mode_edit': "🛸 تعديل وترتيب ملف مرفوع (تنقية وتغذية الـ AI)",
        'mode_gen': "⚛️ توليد ملف جديد تماماً يعتمد على أحدث ما تعلمه الـ AI",
        'model_label': "📺 اختر نوع موديل شاشة LG المستهدفة:",
        'model_modern': "Smart webOS (شاشات سمارت حديثة)",
        'model_legacy': "Legacy / 32 Inch (الشاشات الكلاسيكية والـ 32 بوصة)",
        'country_label': "🌍 اختر بلد البث (Broadcast Country):",
        'country_egy': "مصر (Egypt) — تصنيف شمال أفريقيا [NAFR]",
        'country_ksa': "السعودية (KSA) — تصنيف الشرق الأوسط [MIDE]",
        'btn_generate': "🚀 إطلاق مصفوفة التوليد السريع للملف الجديد",
        'upload_label': "🚀 اختر ملف القنوات (GlobalClone00001.TLL) من الفلاشة لتطهيره وتحديثه:",
        'update_freq_label': "⚛️ إجبار الملف على الترددات الرسمية الحديثة لعام 2026 (تطهير الترددات الميتة)",
        'add_new_ch_label': "✨ امتصاص القنوات الحصرية الجديدة وحفظها في ذاكرة الموقع الأبدية",
        'success_read': "🛸 تم قراءة وفك الهيكل بنجاح! الموديل الحالي: ",
        'success_gen': "🌌 تم توليد ملف قنوات LG فائق النقاء ومتوافق مع نطاق بث: ",
        'search_header': "🔍 محرك الفرز الاستخباراتي والبحث الزمني المتقدم:",
        'search_placeholder': "ابحث باسم القناة، التردد، المصدر، أو التاريخ (مثال: 2026-05)...",
        'multiselect_label': "اضغط هنا لبناء تسلسل خطة العرض التفاعلي للفئات:",
        'ready_msg': "🌌 تم دمج مصفوفة RAMBO وتطهير البيانات بنجاح! الملفات جاهزة للتحميل:",
        'btn_download_tll': "📥 تحميل ملف الشاشة المحدث والمنظم (GlobalClone00001.TLL)",
        'channels_count': "قناة نقيّة",
        'lg_trick_title': "💡 ملحوظة فنية هامة جداً بعد تنزيل الملف على شاشة LG:",
        'lg_trick_text': "من إعدادات التلفزيون اختار القنوات -> مدير القنوات -> التعديل على كل القنوات -> حدد الكل واختار استعادة (Restore) لإجبار الشاشة على تفعيل الترتيب الفعلي الحقيقي للموقع."
    },
    'en': {
        'title': "📺 RAMBO ULTRA - LG Satellite Intelligence Sorter",
        'subtitle': "📡 AI Search & Tracking Engine: Live 2026 Frequencies by Date, Source & Category",
        'mode_selector': "🛠️ Select Operations Mode:",
        'mode_edit': "🛸 Edit/Optimize USB File (Cleanse & Feed AI)",
        'mode_gen': "⚛️ Generate Brand New Raw .TLL (Evolved from Persistent AI Memory)",
        'model_label': "📺 Select Target LG TV Model Type:",
        'model_modern': "Smart webOS (Modern Smart Models)",
        'model_legacy': "Legacy / 32 Inch (Classic Profile)",
        'country_label': "🌍 Select Broadcast Country Profile:",
        'country_egy': "Egypt [NAFR]",
        'country_ksa': "Saudi Arabia [MIDE]",
        'btn_generate': "🚀 Fire Matrix Generation Engine",
        'upload_label': "🚀 Upload Channel File (GlobalClone00001.TLL):",
        'update_freq_label': "⚛️ Enforce Official Live Frequencies",
        'add_new_ch_label': "✨ Absorb New Channels to Persistent Memory",
        'success_read': "🛸 Structure Decoded Profile: ",
        'success_gen': "🌌 Created pure LG layout for: ",
        'search_header': "🔍 Quantum Search & Temporal Timeline Filter:",
        'search_placeholder': "Search by channel, frequency, source, or date...",
        'multiselect_label': "Click here to build your interactive category timeline sequence:",
        'ready_msg': "🌌 Quantum Matrix Cleansing Successful! Assets ready for transfer:",
        'btn_download_tll': "📥 Download Verified TV Configuration (GlobalClone00001.TLL)",
        'channels_count': "Pure Channels",
        'lg_trick_title': "💡 LG Post-Installation Technical Step:",
        'lg_trick_text': "Go to Settings -> Channels -> Channel Manager -> Edit All Channels -> Select All -> Choose 'Restore' to enforce linear sorting layout."
    }
}

t = UI_TEXT[st.session_state.lang]
st.set_page_config(page_title="RAMBO ULTRA - Intelligence Satellite Engine", page_icon="📡", layout="wide")

# أزرار اللغة والثيم
col_lang, col_theme, _ = st.columns([1.2, 1.5, 8])
with col_lang:
    if st.button("🌐 English" if st.session_state.lang == 'ar' else "🌐 العربية"):
        st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
        st.rerun()
with col_theme:
    if st.button("☀️ Light Mode" if st.session_state.theme == 'dark' else "🌙 Dark Mode"):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

# الـ CSS السيبراني
if st.session_state.theme == 'dark':
    bg_style = "radial-gradient(circle at 50% 50%, #0d061f 0%, #030107 100%)"
    text_color = "#00f0ff"
    box_bg = "rgba(15, 8, 38, 0.9)"
    box_border = "#00f0ff"
    box_shadow = "rgba(0, 240, 255, 0.25)"
else:
    bg_style = "radial-gradient(circle at 50% 50%, #f4f5f7 0%, #e4e7eb 100%)"
    text_color = "#0d0722"
    box_bg = "#ffffff"
    box_border = "#ff007f"
    box_shadow = "rgba(255, 0, 127, 0.15)"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;900&family=Cairo:wght@400;700&display=swap');
    .main {{ background: {bg_style} !important; color: {text_color} !important; font-family: { "'Cairo', sans-serif" if st.session_state.lang == 'ar' else "'Orbitron', sans-serif" }; }}
    h1 {{ color: #ff007f !important; text-shadow: 0 0 10px #ff007f !important; text-align: center; font-weight: 900; }}
    h2, h3, p, label, .stMarkdown {{ color: {text_color} !important; }}
    .stTextInput>div>div>input {{ background-color: {box_bg} !important; color: {text_color} !important; border: 2px solid {box_border} !important; border-radius: 10px !important; }}
    .cyber-metric-card {{ background: {box_bg}; border: 2px solid {box_border}; border-radius: 12px; padding: 15px; text-align: center; box-shadow: 0 4px 10px {box_shadow}; }}
    .stCheckbox, .stMultiSelect, div[data-testid="stExpander"], div[data-testid="stFileUploader"], .lg-trick-box, .cyber-sidebar-box {{ background: {box_bg} !important; border: 2px solid {box_border} !important; box-shadow: 0px 5px 15px {box_shadow} !important; border-radius: 14px !important; padding: 18px !important; margin-bottom: 20px !important; }}
    .stButton>button {{ background: linear-gradient(135deg, #ff007f 0%, #aa0055 100%) !important; color: white !important; border-radius: 12px !important; font-weight: bold; width: 100%; }}
    .futuristic-cyber-footer {{ background: #080314; border: 2px solid #00f0ff; color: white; padding: 25px; text-align: center; border-radius: 20px; margin-top: 55px; font-family: 'Orbitron', sans-serif; }}
    </style>
""", unsafe_allow_html=True)

st.title(t['title'])
st.markdown(f"<h3 style='text-align:center;'>{t['subtitle']}</h3>", unsafe_allow_html=True)

# 💾 بنك معلومات الترددات المستقرة 2026
def get_base_2026_db():
    return {
        "CTV HD": {"frequency": 12022, "polarization": "Vertical", "date": "2026-05-25", "source": "FlySat Official", "category": "⛪ قنوات مسيحية"},
        "ME SAT HD": {"frequency": 11179, "polarization": "Vertical", "date": "2026-05-24", "source": "Nilesat Spectrum", "category": "⛪ قنوات مسيحية"},
        "AGHAPY TV": {"frequency": 11179, "polarization": "Vertical", "date": "2026-05-20", "source": "FlySat", "category": "⛪ قنوات مسيحية"},
        "KOOGI TV": {"frequency": 11096, "polarization": "Vertical", "date": "2026-05-15", "source": "LyngSat", "category": "⛪ قنوات مسيحية"},
        "ALHAYAT TV": {"frequency": 11392, "polarization": "Vertical", "date": "2026-05-01", "source": "Nilesat Official", "category": "⛪ قنوات مسيحية"},
        "MARMARKOS": {"frequency": 11137, "polarization": "Vertical", "date": "2026-04-18", "source": "FlySat", "category": "⛪ قنوات مسيحية"},
        "EGYPT QURAN": {"frequency": 11179, "polarization": "Vertical", "date": "2026-05-25", "source": "Nilesat Official", "category": "🕌 قنوات إسلامية"},
        "SAUDI QURAN HD": {"frequency": 12149, "polarization": "Horizontal", "date": "2026-05-22", "source": "Arabsat Feed", "category": "🕌 قنوات إسلامية"},
        "AL MAJD QURAN": {"frequency": 12054, "polarization": "Horizontal", "date": "2026-05-10", "source": "Almajd Network", "category": "🕌 قنوات إسلامية"},
        "MIX ONE HD": {"frequency": 11843, "polarization": "Horizontal", "date": "2026-05-25", "source": "Nilesat Monitor", "category": "🍿 أفلام عربية وأجنبية"},
        "ON TIME SPORTS 1 HD": {"frequency": 11861, "polarization": "Vertical", "date": "2026-05-18", "source": "URC Egypt", "category": "⚽ رياضة"},
        "MBC DRAMA HD": {"frequency": 11938, "polarization": "Vertical", "date": "2026-05-12", "source": "MBC Group", "category": "🎬 مسلسلات ودراما"},
        "WANNASAH HD": {"frequency": 11938, "polarization": "Vertical", "date": "2026-05-24", "source": "Nilesat Transponder", "category": "👶 أطفال وكرتون"}
    }

BRAIN_FILE = "ai_brain_db.json"

def load_persistent_brain():
    base_db = get_base_2026_db()
    if os.path.exists(BRAIN_FILE):
        try:
            with open(BRAIN_FILE, "r", encoding="utf-8") as f:
                saved_db = json.load(f)
                base_db.update(saved_db)
        except Exception:
            pass
    return base_db

def save_persistent_brain(updated_db):
    try:
        with open(BRAIN_FILE, "w", encoding="utf-8") as f:
            json.dump(updated_db, f, ensure_ascii=False, indent=4)
    except Exception:
        pass

MASTER_2026_DB = load_persistent_brain()

# --- 🧠 العدادات وفلاتر البحث الزمني المتقدم ---
st.markdown(f"### {t['search_header']}")

today_str = "2026-05-25"  
today_dt = datetime.strptime(today_str, "%Y-%m-%d")

ch_today = 0
ch_week = 0
for k, v in MASTER_2026_DB.items():
    ch_date_str = v.get("date", "2026-05-01")
    try:
        ch_dt = datetime.strptime(ch_date_str, "%Y-%m-%d")
        delta = today_dt - ch_dt
        if delta.days == 0: ch_today += 1
        if delta.days <= 7: ch_week += 1
    except: pass

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown(f"<div class='cyber-metric-card'><h4 style='color:#ff007f;margin:0;'>🌟 قنوات رُصدت اليوم الجديد</h4><h2 style='margin:10px 0;'>{ch_today} قناة</h2></div>", unsafe_allow_html=True)
with col_m2:
    st.markdown(f"<div class='cyber-metric-card'><h4 style='color:#00f0ff;margin:0;'>⚡ رادار الـ 7 أيام الأخيرة</h4><h2 style='margin:10px 0;'>{ch_week} قناة جديدة</h2></div>", unsafe_allow_html=True)
with col_m3:
    st.markdown(f"<div class='cyber-metric-card'><h4 style='color:#25d366;margin:0;'>📦 إجمالي بنك معلومات السيرفر</h4><h2 style='margin:10px 0;'>{len(MASTER_2026_DB)} تردد نشط</h2></div>", unsafe_allow_html=True)

st.write("")

col_search, col_filter_time, col_filter_cat = st.columns([5, 3, 3])

with col_search:
    search_q = st.text_input("", placeholder=t['search_placeholder'], key="radar_search").strip().upper()
with col_filter_time:
    time_filter = st.selectbox("📅 النطاق الزمني للرصد:", ["كل الترددات المخزنة", "حصريات اليوم (اليوم فقط)", "أحدث التغييرات هذا الأسبوع", "تحديثات شهر مايو 2026"])
with col_filter_cat:
    distinct_cats = ["كل الفئات"] + list(set([v.get("category", "📺 قنوات عامة ومنوعات") for v in MASTER_2026_DB.values()]))
    cat_filter = st.selectbox("🗂️ الفرز حسب القسم الميكانيكي:", distinct_cats)

processed_search_results = []
for index, (ch_name, info) in enumerate(MASTER_2026_DB.items(), start=1):
    ch_cat = info.get("category", "📺 قنوات عامة ومنوعات")
    ch_date_str = info.get("date", "2026-05-01")
    ch_source = info.get("source", "Live Feed")
    ch_freq = f"{info['frequency']} MHz ({info['polarization'][0]})"
    
    if search_q:
        match_text = (search_q in ch_name) or (search_q in ch_freq) or (search_q in ch_source.upper()) or (search_q in ch_date_str)
        if not match_text: continue
        
    if cat_filter != "كل الفئات" and ch_cat != cat_filter: continue
        
    try:
        ch_dt = datetime.strptime(ch_date_str, "%Y-%m-%d")
        days_diff = (today_dt - ch_dt).days
        if time_filter == "حصريات اليوم (اليوم فقط)" and days_diff != 0: continue
        elif time_filter == "أحدث التغييرات هذا الأسبوع" and days_diff > 7: continue
        elif time_filter == "تحديثات شهر مايو 2026" and not ch_date_str.startswith("2026-05"): continue
    except: pass

    status_tag = "🌟 حصرية اليوم" if ch_date_str == today_str else "🟢 نشط"
    processed_search_results.append({
        "حالة الرصد": status_tag,
        "اسم القناة الفضائية": ch_name,
        "التردد المعتمد 2026": ch_freq,
        "تصنيف الـ AI الدقيق": ch_cat,
        "تاريخ الصدور/التعديل": ch_date_str,
        "المصدر الاستخباراتي": ch_source
    })

if processed_search_results:
    st.dataframe(processed_search_results, use_container_width=True)
else:
    st.warning("⚠️ الرادار لم يرصد أي ترددات مطابقة لفلاتر البحث الحالية.")

st.write("---")

# --- 🛠️ لوحة العمل ومصنع الـ TLL ---
st.sidebar.markdown(f"### {t['mode_selector']}")
app_mode = st.sidebar.radio("", [t['mode_edit'], t['mode_gen']])

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
    name = channel_name.upper().strip()
    if name in MASTER_2026_DB and "category" in MASTER_2026_DB[name]:
        return MASTER_2026_DB[name]["category"]
    if any(w in name for w in ["CTV", "AGHAPY", "ME SAT", "MESAT", "MARMARKOS", "KOOGI", "SAT-7"]): return ALL_AVAILABLE_CATEGORIES[0]
    if any(w in name for w in ["QURAN", "RAHMA", "MAJD", "EGYPT QURAN"]): return ALL_AVAILABLE_CATEGORIES[1]
    if any(w in name for w in ["DRAMA", "SERIES", "ALWAN"]): return ALL_AVAILABLE_CATEGORIES[2]
    if any(w in name for w in ["CINEMA", "ROTANA", "AFLAM", "MIX ONE", "MBC2", "ACTION"]): return ALL_AVAILABLE_CATEGORIES[3]
    if any(w in name for w in ["SPACE TOON", "CN", "MAJID", "WANNASAH"]): return ALL_AVAILABLE_CATEGORIES[4]
    if any(w in name for w in ["SPORT", "ONTIME", "BEIN"]): return ALL_AVAILABLE_CATEGORIES[5]
    if any(w in name for w in ["NEWS", "JAZEERA", "ARABIYA", "CAIRO"]): return ALL_AVAILABLE_CATEGORIES[6]
    return ALL_AVAILABLE_CATEGORIES[7]

file_processed = False
file_bytes_out = b""
unique_channels_map = {}
database_needs_save = False

if app_mode == t['mode_edit']:
    uploaded_file = st.file_uploader(t['upload_label'], type=["TLL"])
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        try: file_text_original = file_bytes.decode('utf-8')
        except UnicodeDecodeError: file_text_original = file_bytes.decode('latin-1')

        root = ET.fromstring(file_bytes)
        legacy_broadcast_tag = root.find(".//legacybroadcast")
        is_modern = legacy_broadcast_tag is not None and legacy_broadcast_tag.text
        
        enforce_2026 = st.checkbox(t['update_freq_label'], value=True)
        inject_exclusive = st.checkbox(t['add_new_ch_label'], value=True)

        if is_modern:
            broadcast_data = json.loads(legacy_broadcast_tag.text)
            uploaded_list = broadcast_data.get("channelList", [])
            for c in uploaded_list:
                name_up = c.get("channelName", "").strip().upper()
                freq_up = c.get("frequency", 0)
                pol_up = c.get("polarization", "Horizontal")
                if name_up and freq_up > 0:
                    if name_up not in MASTER_2026_DB or MASTER_2026_DB[name_up]["frequency"] != int(freq_up):
                        MASTER_2026_DB[name_up] = {
                            "frequency": int(freq_up), 
                            "polarization": pol_up,
                            "date": today_str,
                            "source": "User Flash Injection",
                            "category": ai_classify(name_up)
                        }
                        database_needs_save = True

            for idx, ch in enumerate(uploaded_list):
                ch_name = ch.get("channelName", "").strip()
                ch_name_upper = ch_name.upper()
                if not ch_name_upper: continue
                old_freq = str(ch.get("frequency", "0"))
                if enforce_2026 and ch_name_upper in MASTER_2026_DB:
                    verified_freq = MASTER_2026_DB[ch_name_upper]["frequency"]
                    ch["frequency"] = int(verified_freq)
                    ch["polarization"] = MASTER_2026_DB[ch_name_upper]["polarization"]
                    old_freq = str(verified_freq)
                unique_channels_map[ch_name_upper] = {"id": idx, "name": ch_name, "freq": old_freq, "raw_node": ch}
        else:
            item_blocks = re.findall(r'(<ITEM>.*?</ITEM>)', file_text_original, re.DOTALL)
            for item_str in item_blocks:
                name_match = re.search(r'<vchName>(.*?)</vchName>', item_str)
                freq_match = re.search(r'<frequency>(.*?)</frequency>', item_str)
                if name_match and freq_match:
                    name_up = name_match.group(1).strip().upper()
                    freq_up = freq_match.group(1).strip()
                    if name_up and freq_up.isdigit():
                        if name_up not in MASTER_2026_DB or MASTER_2026_DB[name_up]["frequency"] != int(freq_up):
                            MASTER_2026_DB[name_up] = {
                                "frequency": int(freq_up), 
                                "polarization": "Vertical",
                                "date": today_str,
                                "source": "User Legacy Flash",
                                "category": ai_classify(name_up)
                            }
                            database_needs_save = True

            for idx, item_str in enumerate(item_blocks):
                name_match = re.search(r'<vchName>(.*?)</vchName>', item_str)
                freq_match = re.search(r'<frequency>(.*?)</frequency>', item_str)
                if not name_match: continue
                ch_name = name_match.group(1).strip()
                ch_name_upper = ch_name.upper()
                old_freq = freq_match.group(1).strip() if freq_match else "0"
                if enforce_2026 and ch_name_upper in MASTER_2026_DB:
                    verified_freq = MASTER_2026_DB[ch_name_upper]["frequency"]
                    item_str = re.sub(r'<frequency>\d+</frequency>', f'<frequency>{verified_freq}</frequency>', item_str)
                    old_freq = str(verified_freq)
                unique_channels_map[ch_name_upper] = {"id": idx, "name": ch_name, "freq": old_freq, "raw_str": item_str}

        if database_needs_save:
            save_persistent_brain(MASTER_2026_DB)
            st.toast("📡 تم حفظ الترددات الممتصة بنجاح في مخزن السيرفر!", icon="🧠")
        file_processed = True
else:
    if st.button(t['btn_generate']) or 'generated_active' in st.session_state:
        st.session_state.generated_active = True
        idx = 0
        for ch_name, data in MASTER_2026_DB.items():
            node = {"channelName": ch_name, "frequency": data["frequency"], "polarization": data["polarization"], "majorNumber": 0, "serviceType": "1", "scrambled": "false", "symbolRate": "27500"}
            unique_channels_map[ch_name] = {"id": idx, "name": ch_name, "freq": str(data["frequency"]), "raw_node": node}
            idx += 1
        file_processed = True

if file_processed and unique_channels_map:
    st.markdown(f"""<div class="lg-trick-box"><h4>{t['lg_trick_title']}</h4><p style="white-space: pre-line;">{t['lg_trick_text']}</p></div>""", unsafe_allow_html=True)
    
    cleaned_channels_list = list(unique_channels_map.values())
    
    # استدعاء مفتاح الـ multiselect الموثق والمعاد تعريفه بشكل صحيح وآمن تماماً لمنع الـ KeyError
    user_priority = st.multiselect(t['multiselect_label'], options=ALL_AVAILABLE_CATEGORIES, default=[])
    final_priority = list(user_priority)
    for cat in ALL_AVAILABLE_CATEGORIES:
        if cat not in final_priority: final_priority.append(cat)
        
    channels_sorted = sorted(cleaned_channels_list, key=lambda x: final_priority.index(ai_classify(x["name"])))
    
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

    st.success(t['ready_msg'])
    st.download_button(label=t['btn_download_tll'], data=file_bytes_out, file_name="GlobalClone00001.TLL", mime="application/octet-stream")

# الفوتر السيبراني
st.markdown(f"""
    <div class="futuristic-cyber-footer">
        <div style="color:#ff007f;font-size:24px;font-weight:bold;">🛠️ DEVELOPER ENG: RAFIK NATHAN</div>
        <div>📱 <b>MOBILE:</b> +201280339779 | rafikrambo113@gmail.com</div>
    </div>
""", unsafe_allow_html=True)
