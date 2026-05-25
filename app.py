import streamlit as st
import xml.etree.ElementTree as ET
import json
import re
import os
import csv
from io import StringIO
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════
# التهيئة
# ═══════════════════════════════════════════════════════════════════════
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# ═══════════════════════════════════════════════════════════════════════
# نصوص الواجهة
# ═══════════════════════════════════════════════════════════════════════
UI_TEXT = {
    'ar': {
        'title': "📺 RAMBO ULTRA - رادار الترددات الحية لشاشات LG",
        'subtitle': "📡 محرك بحث استخباراتي يرصد أحدث ترددات 2026",
        'mode_selector': "🛠️ اختر وضع العمل:",
        'mode_edit': "🛸 تعديل وترتيب ملف مرفوع",
        'mode_gen': "⚛️ توليد ملف جديد تماماً",
        'btn_download_tll': "📥 تحميل ملف الشاشة (TLL)",
        'btn_download_sort': "📥 تحميل ترتيب القنوات (CSV)",
        'lg_trick_title': "💡 خطوة هامة بعد تركيب الملف:",
        'lg_trick_text': "إعدادات ← القنوات ← مدير القنوات ← حدد الكل ← استعادة",
    },
    'en': {
        'title': "📺 RAMBO ULTRA - LG TV Sorter",
        'subtitle': "📡 Live 2026 Frequencies Intelligence",
        'mode_selector': "🛠️ Select Mode:",
        'mode_edit': "🛸 Edit USB File",
        'mode_gen': "⚛️ Generate New .TLL",
        'btn_download_tll': "📥 Download TV File (TLL)",
        'btn_download_sort': "📥 Download Sort Order (CSV)",
        'lg_trick_title': "💡 LG Post-Install Step:",
        'lg_trick_text': "Settings → Channels → Select All → Restore",
    }
}

st.set_page_config(page_title="RAMBO ULTRA", page_icon="📡", layout="wide")
t = UI_TEXT[st.session_state.lang]

# ═══════════════════════════════════════════════════════════════════════════════
# CSS احترافي
# ═══════════════════════════════════════════════════════════════════════
if st.session_state.theme == 'dark':
    BG, BG2, CYAN, PINK, GREEN, TEXT, MUTED, BORDER = "#06020f", "#0d0520", "#00e5ff", "#ff0066", "#00ff99", "#c8f0ff", "#7090aa", "rgba(0,229,255,0.22)"
else:
    BG, BG2, CYAN, PINK, GREEN, TEXT, MUTED, BORDER = "#f0f4f8", "#ffffff", "#0077aa", "#cc0044", "#007744", "#0d1a26", "#556677", "rgba(0,119,170,0.25)"

FONT = "'Cairo'" if st.session_state.lang == 'ar' else "'Orbitron'"
DIR = "rtl" if st.session_state.lang == 'ar' else "ltr"

st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Cairo:wght@700&display=swap" rel="stylesheet">
<style>
html{{direction:{DIR};font-family:{FONT};background:{BG};color:{TEXT}}}
h1{{font-family:'Orbitron';font-weight:900;text-align:center;background:linear-gradient(90deg,{CYAN},{PINK});-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.scan-line{{height:2px;background:linear-gradient(90deg,transparent,{CYAN},{PINK});margin:10px auto 20px;width:70%;animation:scan 3s infinite alternate}}
@keyframes scan{{from{{opacity:.3}}to{{opacity:1}}}}
.stButton>button{{background:linear-gradient(135deg,{PINK},#990033);color:#fff;border-radius:12px;font-weight:700;width:100%;padding:10px}}
.stDownloadButton>button{{background:linear-gradient(135deg,{CYAN},#005577);color:{BG};border-radius:12px;font-weight:700;width:100%;padding:10px}}
.lg-tip-box{{background:rgba(255,204,0,.07);border:1px solid rgba(255,204,0,.35);border-radius:14px;padding:14px;color:#ffcc00;font-size:13px}}
.cyber-footer{{background:rgba(0,229,255,.04);border:1px solid {BORDER};border-radius:16px;padding:22px;text-align:center;margin-top:50px;font-family:'Orbitron'}}
</style>
<div class="scan-line"></div>
""", unsafe_allow_html=True)

st.title(t['title'])
st.caption(t['subtitle'])

# ═══════════════════════════════════════════════════════════════════════
# بنك الترددات 2026
# ═══════════════════════════════════════════════════════════════════════
def get_base_2026_db():
    return {
        "CTV HD": {"frequency": 12022, "polarization": "Vertical", "date": "2026-05-25", "source": "FlySat", "category": "⛪ مسيحية"},
        "ME SAT HD": {"frequency": 11179, "polarization": "Vertical", "date": "2026-05-24", "source": "Nilesat", "category": "⛪ مسيحية"},
        "EGYPT QURAN": {"frequency": 11179, "polarization": "Vertical", "date": "2026-05-25", "source": "Nilesat", "category": "🕌 إسلامية"},
        "SAUDI QURAN HD": {"frequency": 12149, "polarization": "Horizontal", "date": "2026-05-22", "source": "Arabsat", "category": "🕌 إسلامية"},
        "AL MAJD QURAN": {"frequency": 12054, "polarization": "Horizontal", "date": "2026-05-10", "source": "Almajd", "category": "🕌 إسلامية"},
        "MBC DRAMA HD": {"frequency": 11938, "polarization": "Vertical", "date": "2026-05-12", "source": "MBC", "category": "🎬 دراما"},
        "ROTANA DRAMA": {"frequency": 11843, "polarization": "Horizontal", "date": "2026-05-05", "source": "Rotana", "category": "🎬 دراما"},
        "MIX ONE HD": {"frequency": 11843, "polarization": "Horizontal", "date": "2026-05-25", "source": "Nilesat", "category": "🍿 أفلام"},
        "MBC2 HD": {"frequency": 11938, "polarization": "Vertical", "date": "2026-05-14", "source": "MBC", "category": "🍿 أفلام"},
        "ROTANA CINEMA": {"frequency": 11843, "polarization": "Horizontal", "date": "2026-05-03", "source": "Rotana", "category": "🍿 أفلام"},
        "ON TIME SPORTS 1 HD": {"frequency": 11861, "polarization": "Vertical", "date": "2026-05-18", "source": "URC Egypt", "category": "⚽ رياضة"},
        "ON TIME SPORTS 2 HD": {"frequency": 11843, "polarization": "Vertical", "date": "2026-05-18", "source": "URC Egypt", "category": "⚽ رياضة"},
        "BEIN SPORTS HD1": {"frequency": 12226, "polarization": "Horizontal", "date": "2026-05-15", "source": "beIN", "category": "⚽ رياضة"},
        "WANNASAH HD": {"frequency": 11938, "polarization": "Vertical", "date": "2026-05-24", "source": "Nilesat", "category": "👶 أطفال"},
        "SPACE TOON": {"frequency": 11977, "polarization": "Horizontal", "date": "2026-04-20", "source": "FlySat", "category": "👶 أطفال"},
        "MBC3 HD": {"frequency": 11938, "polarization": "Vertical", "date": "2026-05-10", "source": "MBC", "category": "👶 أطفال"},
        "NILE NEWS": {"frequency": 11179, "polarization": "Vertical", "date": "2026-05-22", "source": "Nilesat", "category": "📰 أخبار"},
        "AL JAZEERA HD": {"frequency": 11938, "polarization": "Horizontal", "date": "2026-05-20", "source": "Arabsat", "category": "📰 أخبار"},
        "CAIRO NEWS": {"frequency": 11843, "polarization": "Horizontal", "date": "2026-05-16", "source": "Nilesat", "category": "📰 أخبار"},
        "MBC1 HD": {"frequency": 11938, "polarization": "Vertical", "date": "2026-05-11", "source": "MBC", "category": "📺 عامة"},
        "NILE TV HD": {"frequency": 11179, "polarization": "Vertical", "date": "2026-05-09", "source": "Nilesat", "category": "📺 عامة"},
        "DREAM TV HD": {"frequency": 11843, "polarization": "Horizontal", "date": "2026-05-07", "source": "FlySat", "category": "📺 عامة"},
    }

BRAIN_FILE = "ai_brain_db.json"

def load_persistent_brain():
    db = get_base_2026_db()
    if os.path.exists(BRAIN_FILE):
        try:
            with open(BRAIN_FILE, "r", encoding="utf-8") as f:
                db.update(json.load(f))
        except:
            pass
    return db

def save_persistent_brain(db):
    try:
        with open(BRAIN_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
    except:
        pass

MASTER_2026_DB = load_persistent_brain()
TODAY_STR = "2026-05-25"

def ai_classify(name):
    n = name.upper().strip()
    if n in MASTER_2026_DB and "category" in MASTER_2026_DB[n]:
        return MASTER_2026_DB[n]["category"]
    checks = [
        (["CTV","AGHAPY","ME SAT","SAT-7"], "⛪ مسيحية"),
        (["QURAN","MAJD","RAHMA"], "🕌 إسلامية"),
        (["DRAMA","SERIES","ALWAN"], "🎬 دراما"),
        (["CINEMA","MBC2","MIX ONE","AFLAM"], "🍿 أفلام"),
        (["SPACE TOON","MBC3","WANNASAH"], "👶 أطفال"),
        (["SPORT","ONTIME","BEIN"], "⚽ رياضة"),
        (["NEWS","JAZEERA","CAIRO"], "📰 أخبار"),
    ]
    for kw, cat in checks:
        if any(w in n for w in kw):
            return cat
    return "📺 عامة"

ALL_CATEGORIES = ["⛪ مسيحية","🕌 إسلامية","🎬 دراما","🍿 أفلام","👶 أطفال","⚽ رياضة","📰 أخبار","📺 عامة"]

# ═══════════════════════════════════════════════════════════════════════
# Sidebar
# ═══════════════════════════════════════════════════════════════════════
st.sidebar.title(t['mode_selector'])
app_mode = st.sidebar.radio("", [t['mode_edit'], t['mode_gen']])

file_processed = False
file_bytes_out = b""
unique_channels_map = {}
database_needs_save = False

# ═══════════════════════════════════════════════════════════════════════
# وضع التعديل
# ═══════════════════════════════════════════════════════════════════════
if app_mode == t['mode_edit']:
    uploaded_file = st.file_uploader("🚀 ارفع ملف القنوات:", type=["TLL"])
    if uploaded_file:
        file_bytes = uploaded_file.read()
        root = ET.fromstring(file_bytes)
        legacy_tag = root.find(".//legacybroadcast")
        is_modern = legacy_tag is not None and legacy_tag.text
        
        enforce_2026 = st.checkbox("⚛️ تطبيق الترددات 2026", value=True)
        inject_excl = st.checkbox("✨ امتصاص قنوات جديدة", value=True)
        
        if is_modern:
            broadcast_data = json.loads(legacy_tag.text)
            uploaded_list = broadcast_data.get("channelList", [])
            for c in uploaded_list:
                name_up = c.get("channelName", "").strip().upper()
                freq_up = c.get("frequency", 0)
                pol_up = c.get("polarization", "Horizontal")
                if name_up and freq_up > 0:
                    if name_up not in MASTER_2026_DB or MASTER_2026_DB[name_up]["frequency"] != int(freq_up):
                        MASTER_2026_DB[name_up] = {
                            "frequency": int(freq_up), "polarization": pol_up,
                            "date": TODAY_STR, "source": "User Inject", "category": ai_classify(name_up)
                        }
                        database_needs_save = True
            
            for idx, ch in enumerate(uploaded_list):
                ch_name = ch.get("channelName", "").strip()
                name_up = ch_name.upper()
                if not name_up: continue
                if enforce_2026 and name_up in MASTER_2026_DB:
                    ch["frequency"] = int(MASTER_2026_DB[name_up]["frequency"])
                    ch["polarization"] = MASTER_2026_DB[name_up]["polarization"]
                unique_channels_map[name_up] = {"id": idx, "name": ch_name, "freq": str(ch["frequency"]), "raw_node": ch}
        else:
            file_text = file_bytes.decode('utf-8', errors='ignore')
            item_blocks = re.findall(r'(<ITEM>.*?</ITEM>)', file_text, re.DOTALL)
            for item_str in item_blocks:
                nm = re.search(r'<vchName>(.*?)</vchName>', item_str)
                fr = re.search(r'<frequency>(.*?)</frequency>', item_str)
                if nm and fr:
                    name_up = nm.group(1).strip().upper()
                    freq_up = fr.group(1).strip()
                    if name_up and freq_up.isdigit():
                        if name_up not in MASTER_2026_DB or MASTER_2026_DB[name_up]["frequency"] != int(freq_up):
                            MASTER_2026_DB[name_up] = {
                                "frequency": int(freq_up), "polarization": "Vertical",
                                "date": TODAY_STR, "source": "Legacy Inject", "category": ai_classify(name_up)
                            }
                            database_needs_save = True
            
            for idx, item_str in enumerate(item_blocks):
                nm = re.search(r'<vchName>(.*?)</vchName>', item_str)
                fr = re.search(r'<frequency>(.*?)</frequency>', item_str)
                if not nm: continue
                ch_name = nm.group(1).strip()
                name_up = ch_name.upper()
                old_freq = fr.group(1).strip() if fr else "0"
                if enforce_2026 and name_up in MASTER_2026_DB:
                    vf = MASTER_2026_DB[name_up]["frequency"]
                    item_str = re.sub(r'<frequency>\d+</frequency>', f'<frequency>{vf}</frequency>', item_str)
                    old_freq = str(vf)
                unique_channels_map[name_up] = {"id": idx, "name": ch_name, "freq": old_freq, "raw_str": item_str}
        
        if database_needs_save:
            save_persistent_brain(MASTER_2026_DB)
            st.toast("📡 تم حفظ الترددات الجديدة!", icon="🧠")
        
        st.success("🛸 تم قراءة الملف! الموديل: " + ("Smart webOS" if is_modern else "Legacy"))
        file_processed = True

# ═══════════════════════════════════════════════════════════════════════
# وضع التوليد
# ═══════════════════════════════════════════════════════════════════════
else:
    col_m, col_c = st.columns(2)
    with col_m:
        model_choice = st.selectbox("📺 اختر الموديل:", ["Smart webOS", "Legacy"])
    with col_c:
        country_choice = st.selectbox("🌍 اختر الدولة:", ["مصر [NAFR]", "السعودية [MIDE]"])
    
    if st.button("🚀 إطلاق التوليد"):
        for idx, (ch_name, data) in enumerate(MASTER_2026_DB.items()):
            unique_channels_map[ch_name] = {
                "id": idx, "name": ch_name, "freq": str(data["frequency"]),
                "raw_node": {
                    "channelName": ch_name, "frequency": data["frequency"],
                    "polarization": data["polarization"], "majorNumber": 0,
                    "serviceType": "1", "scrambled": "false", "symbolRate": "27500",
                },
            }
        file_processed = True
        st.success("🌌 تم توليد الملف!")

# ═══════════════════════════════════════════════════════════════════════
# بناء الملفات والتحميل
# ═══════════════════════════════════════════════════════════════════════
if file_processed and unique_channels_map
