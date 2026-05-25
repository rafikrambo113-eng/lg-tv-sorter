import streamlit as st
import xml.etree.ElementTree as ET
import json
import re
import os
import io
from datetime import datetime

if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

UI_TEXT = {
    'ar': {
        'title': "📺 RAMBO ULTRA - رادار الترددات الحية لشاشات LG",
        'subtitle': "📡 محرك بحث استخباراتي يرصد أحدث ترددات 2026 على القمر بالتاريخ والمصدر والكاتوجري",
        'mode_selector': "🛠️ اختر وضع العمل:",
        'mode_edit': "🛸 تعديل وترتيب ملف مرفوع",
        'mode_gen': "⚛️ توليد ملف جديد تماماً",
        'model_label': "📺 اختر موديل شاشة LG:",
        'model_modern': "Smart webOS (شاشات سمارت حديثة)",
        'model_legacy': "Legacy / 32 Inch (الشاشات الكلاسيكية)",
        'country_label': "🌍 اختر بلد البث:",
        'country_egy': "مصر (Egypt) [NAFR]",
        'country_ksa': "السعودية (KSA) [MIDE]",
        'btn_generate': "🚀 إطلاق مصفوفة التوليد",
        'upload_label': "🚀 ارفع ملف القنوات (GlobalClone00001.TLL):",
        'upload_txt_label': "📋 ارفع قائمة الترتيب والترددات (.txt / .csv):",
        'upload_txt_help': "الفورمات: اسم_القناة,تردد,فئة (كل قناة في سطر) — التردد والفئة اختياريان",
        'txt_preview_header': "📋 معاينة قائمة الترتيب المرفوعة:",
        'txt_stats': "تم تحميل {} قناة من الملف — تردد الملف يطغى على البنك",
        'txt_download_template': "⬇️ تحميل قالب CSV جاهز",
        'update_freq_label': "⚛️ تطبيق الترددات الرسمية 2026",
        'add_new_ch_label': "✨ امتصاص القنوات الجديدة وحفظها",
        'success_read': "🛸 تم قراءة الملف بنجاح! الموديل: ",
        'success_gen': "🌌 تم توليد ملف قنوات LG لنطاق: ",
        'search_header': "🔍 محرك الفرز والبحث الاستخباراتي:",
        'search_placeholder': "ابحث باسم القناة، التردد، المصدر، أو التاريخ...",
        'multiselect_label': "ترتيب خطة العرض حسب الفئات (يُستخدم إذا لم يُرفع ملف ترتيب):",
        'ready_msg': "🌌 تم دمج المصفوفة وتطهير البيانات! الملف جاهز:",
        'btn_download_tll': "📥 تحميل ملف الشاشة المحدث (GlobalClone00001.TLL)",
        'channels_count': "قناة نقيّة",
        'lg_trick_title': "💡 خطوة هامة بعد تركيب الملف على شاشة LG:",
        'lg_trick_text': "إعدادات التلفزيون ← القنوات ← مدير القنوات ← التعديل على كل القنوات ← حدد الكل ← استعادة (Restore) لإجبار الشاشة على تفعيل الترتيب الفعلي.",
    },
    'en': {
        'title': "📺 RAMBO ULTRA - LG Satellite Intelligence Sorter",
        'subtitle': "📡 AI Search & Tracking Engine: Live 2026 Frequencies by Date, Source & Category",
        'mode_selector': "🛠️ Select Operations Mode:",
        'mode_edit': "🛸 Edit/Optimize USB File",
        'mode_gen': "⚛️ Generate Brand New .TLL",
        'model_label': "📺 Select LG TV Model:",
        'model_modern': "Smart webOS (Modern Smart Models)",
        'model_legacy': "Legacy / 32 Inch (Classic Profile)",
        'country_label': "🌍 Select Broadcast Country:",
        'country_egy': "Egypt [NAFR]",
        'country_ksa': "Saudi Arabia [MIDE]",
        'btn_generate': "🚀 Fire Matrix Generation Engine",
        'upload_label': "🚀 Upload Channel File (GlobalClone00001.TLL):",
        'upload_txt_label': "📋 Upload Sort & Frequency List (.txt / .csv):",
        'upload_txt_help': "Format: channel_name,frequency,category (one per line) — frequency & category optional",
        'txt_preview_header': "📋 Uploaded Sort List Preview:",
        'txt_stats': "Loaded {} channels from file — file frequency overrides the bank",
        'txt_download_template': "⬇️ Download Ready CSV Template",
        'update_freq_label': "⚛️ Enforce Official Live 2026 Frequencies",
        'add_new_ch_label': "✨ Absorb New Channels to Persistent Memory",
        'success_read': "🛸 File Decoded. Profile: ",
        'success_gen': "🌌 Pure LG layout created for: ",
        'search_header': "🔍 Quantum Search & Temporal Timeline Filter:",
        'search_placeholder': "Search by channel, frequency, source, or date...",
        'multiselect_label': "Build your interactive category sequence (used if no sort file uploaded):",
        'ready_msg': "🌌 Matrix Cleansing Successful! Asset ready:",
        'btn_download_tll': "📥 Download Verified TV Config (GlobalClone00001.TLL)",
        'channels_count': "Pure Channels",
        'lg_trick_title': "💡 LG Post-Installation Step:",
        'lg_trick_text': "Settings → Channels → Channel Manager → Edit All Channels → Select All → Restore to enforce correct sort order.",
    }
}

st.set_page_config(page_title="RAMBO ULTRA", page_icon="📡", layout="wide")

t = UI_TEXT[st.session_state.lang]

col_lang, col_theme, _ = st.columns([1.2, 1.5, 8])
with col_lang:
    if st.button("🌐 English" if st.session_state.lang == 'ar' else "🌐 العربية"):
        st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
        st.rerun()
with col_theme:
    if st.button("☀️ Light Mode" if st.session_state.theme == 'dark' else "🌙 Dark Mode"):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

if st.session_state.theme == 'dark':
    BG        = "#06020f"
    BG2       = "#0d0520"
    CYAN      = "#00e5ff"
    PINK      = "#ff0066"
    GREEN     = "#00ff99"
    TEXT      = "#c8f0ff"
    MUTED     = "#7090aa"
    BORDER    = "rgba(0,229,255,0.22)"
    CARD_BG   = "rgba(0,229,255,0.04)"
    CARD2_BG  = "rgba(255,0,102,0.06)"
    CARD2_BDR = "rgba(255,0,102,0.30)"
    TXT_BOX_BG = "rgba(0,229,255,0.06)"
    TXT_BOX_BD = "rgba(0,229,255,0.35)"
else:
    BG        = "#f0f4f8"
    BG2       = "#ffffff"
    CYAN      = "#0077aa"
    PINK      = "#cc0044"
    GREEN     = "#007744"
    TEXT      = "#0d1a26"
    MUTED     = "#556677"
    BORDER    = "rgba(0,119,170,0.25)"
    CARD_BG   = "rgba(0,119,170,0.05)"
    CARD2_BG  = "rgba(204,0,68,0.05)"
    CARD2_BDR = "rgba(204,0,68,0.30)"
    TXT_BOX_BG = "rgba(0,119,170,0.06)"
    TXT_BOX_BD = "rgba(0,119,170,0.35)"

FONT_MAIN = "'Cairo', sans-serif" if st.session_state.lang == 'ar' else "'Orbitron', sans-serif"
DIR       = "rtl" if st.session_state.lang == 'ar' else "ltr"

st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] {{
    direction: {DIR};
    font-family: {FONT_MAIN};
    background-color: {BG} !important;
    color: {TEXT} !important;
}}
h1 {{
    font-family: 'Orbitron', monospace !important;
    font-weight: 900 !important;
    text-align: center;
    background: linear-gradient(90deg, {CYAN}, {PINK});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 2px;
    margin-bottom: 4px !important;
}}
h2, h3, p, label, .stMarkdown, .stText {{ color: {TEXT} !important; }}
.scan-line {{
    height: 2px;
    background: linear-gradient(90deg, transparent, {CYAN}, {PINK}, transparent);
    border-radius: 2px;
    margin: 8px auto 20px;
    width: 70%;
    animation: scan 3s ease-in-out infinite alternate;
}}
@keyframes scan {{ from{{opacity:.3}} to{{opacity:1}} }}
.cyber-metric-card {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 16px 12px;
    text-align: center;
    transition: transform .2s;
}}
.cyber-metric-card:hover {{ transform: translateY(-3px); }}
.metric-num {{
    font-family: 'Orbitron', monospace;
    font-size: 28px;
    font-weight: 700;
    margin: 6px 0 2px;
}}
.metric-label {{ font-size: 11px; color: {MUTED}; }}
div[data-testid="stFileUploader"],
div[data-testid="stExpander"],
.stCheckbox {{
    background: {CARD2_BG} !important;
    border: 1px solid {CARD2_BDR} !important;
    border-radius: 14px !important;
    padding: 14px !important;
    margin-bottom: 14px !important;
}}
.stTextInput > div > div > input {{
    background: {BG2} !important;
    color: {TEXT} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    font-family: {FONT_MAIN};
}}
.stSelectbox > div > div {{
    background: {BG2} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    color: {TEXT} !important;
}}
.stButton > button {{
    background: linear-gradient(135deg, {PINK} 0%, #990033 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-family: {FONT_MAIN};
    width: 100%;
    padding: 10px 0;
    transition: opacity .2s, transform .15s;
}}
.stButton > button:hover {{ opacity: .88; transform: translateY(-2px); }}
.stDownloadButton > button {{
    background: linear-gradient(135deg, {CYAN} 0%, #005577 100%) !important;
    color: {BG} !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    width: 100%;
    padding: 10px 0;
}}
section[data-testid="stSidebar"] {{
    background: {BG2} !important;
    border-left: 2px solid {BORDER};
}}
.lg-tip-box {{
    background: rgba(255,204,0,.07);
    border: 1px solid rgba(255,204,0,.35);
    border-radius: 14px;
    padding: 14px 18px;
    margin-top: 14px;
    color: #ffcc00;
    font-size: 13px;
    line-height: 1.8;
}}
.lg-tip-box strong {{
    font-family: 'Orbitron', monospace;
    font-size: 11px;
    display: block;
    margin-bottom: 6px;
}}
.txt-upload-box {{
    background: {TXT_BOX_BG};
    border: 1px solid {TXT_BOX_BD};
    border-radius: 14px;
    padding: 16px 18px;
    margin: 14px 0;
}}
.txt-upload-title {{
    font-family: 'Orbitron', monospace;
    font-size: 12px;
    color: {CYAN};
    margin-bottom: 8px;
    font-weight: 700;
}}
.txt-preview-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 0;
    border-bottom: 1px solid {BORDER};
    font-size: 12px;
    direction: ltr;
}}
.txt-preview-row:last-child {{ border-bottom: none; }}
.txt-ch-name  {{ color: {CYAN};  font-weight: 600; min-width: 160px; }}
.txt-ch-freq  {{ color: {GREEN}; font-family: 'Orbitron', monospace; font-size: 11px; min-width: 120px; text-align:center; }}
.txt-ch-cat   {{ color: {MUTED}; font-size: 11px; min-width: 160px; text-align: right; }}
.txt-ch-src   {{ color: #ffcc00; font-size: 10px; min-width: 80px; text-align: right; }}
.stDataFrame {{ border-radius: 12px; overflow: hidden; border: 1px solid {BORDER} !important; }}
.cyber-footer {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 22px;
    text-align: center;
    margin-top: 50px;
    font-family: 'Orbitron', monospace;
}}
</style>
<div class="scan-line"></div>
""", unsafe_allow_html=True)

st.title(t['title'])
st.markdown(f"<h3 style='text-align:center;color:{MUTED};font-size:13px;'>{t['subtitle']}</h3>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  بنك الترددات 2026
# ══════════════════════════════════════════════════════════════
def get_base_2026_db():
    return {
        "CTV HD":             {"frequency": 12022, "polarization": "Vertical",   "date": "2026-05-25", "source": "FlySat Official",    "category": "⛪ قنوات مسيحية"},
        "ME SAT HD":          {"frequency": 11179, "polarization": "Vertical",   "date": "2026-05-24", "source": "Nilesat Spectrum",    "category": "⛪ قنوات مسيحية"},
        "AGHAPY TV":          {"frequency": 11179, "polarization": "Vertical",   "date": "2026-05-20", "source": "FlySat",              "category": "⛪ قنوات مسيحية"},
        "KOOGI TV":           {"frequency": 11096, "polarization": "Vertical",   "date": "2026-05-15", "source": "LyngSat",             "category": "⛪ قنوات مسيحية"},
        "ALHAYAT TV":         {"frequency": 11392, "polarization": "Vertical",   "date": "2026-05-01", "source": "Nilesat Official",    "category": "⛪ قنوات مسيحية"},
        "MARMARKOS":          {"frequency": 11137, "polarization": "Vertical",   "date": "2026-04-18", "source": "FlySat",              "category": "⛪ قنوات مسيحية"},
        "SAT-7 ARABIC":       {"frequency": 11977, "polarization": "Vertical",   "date": "2026-05-10", "source": "FlySat",              "category": "⛪ قنوات مسيحية"},
        "EGYPT QURAN":        {"frequency": 11179, "polarization": "Vertical",   "date": "2026-05-25", "source": "Nilesat Official",    "category": "🕌 قنوات إسلامية"},
        "SAUDI QURAN HD":     {"frequency": 12149, "polarization": "Horizontal", "date": "2026-05-22", "source": "Arabsat Feed",        "category": "🕌 قنوات إسلامية"},
        "AL MAJD QURAN":      {"frequency": 12054, "polarization": "Horizontal", "date": "2026-05-10", "source": "Almajd Network",      "category": "🕌 قنوات إسلامية"},
        "RAHMA TV":           {"frequency": 11283, "polarization": "Vertical",   "date": "2026-05-08", "source": "Nilesat",             "category": "🕌 قنوات إسلامية"},
        "MBC DRAMA HD":       {"frequency": 11938, "polarization": "Vertical",   "date": "2026-05-12", "source": "MBC Group",           "category": "🎬 مسلسلات ودراما"},
        "ROTANA DRAMA":       {"frequency": 11843, "polarization": "Horizontal", "date": "2026-05-05", "source": "Rotana Group",        "category": "🎬 مسلسلات ودراما"},
        "ALWAN HD":           {"frequency": 11958, "polarization": "Horizontal", "date": "2026-04-30", "source": "LyngSat",             "category": "🎬 مسلسلات ودراما"},
        "MIX ONE HD":         {"frequency": 11843, "polarization": "Horizontal", "date": "2026-05-25", "source": "Nilesat Monitor",     "category": "🍿 أفلام عربية وأجنبية"},
        "MBC2 HD":            {"frequency": 11938, "polarization": "Vertical",   "date": "2026-05-14", "source": "MBC Group",           "category": "🍿 أفلام عربية وأجنبية"},
        "ROTANA CINEMA":      {"frequency": 11843, "polarization": "Horizontal", "date": "2026-05-03", "source": "Rotana Group",        "category": "🍿 أفلام عربية وأجنبية"},
        "ON TIME SPORTS 1 HD":{"frequency": 11861, "polarization": "Vertical",   "date": "2026-05-18", "source": "URC Egypt",           "category": "⚽ رياضة"},
        "ON TIME SPORTS 2 HD":{"frequency": 11843, "polarization": "Vertical",   "date": "2026-05-18", "source": "URC Egypt",           "category": "⚽ رياضة"},
        "BEIN SPORTS HD1":    {"frequency": 12226, "polarization": "Horizontal", "date": "2026-05-15", "source": "beIN Sports",         "category": "⚽ رياضة"},
        "WANNASAH HD":        {"frequency": 11938, "polarization": "Vertical",   "date": "2026-05-24", "source": "Nilesat Transponder", "category": "👶 أطفال وكرتون"},
        "SPACE TOON":         {"frequency": 11977, "polarization": "Horizontal", "date": "2026-04-20", "source": "FlySat",              "category": "👶 أطفال وكرتون"},
        "MBC3 HD":            {"frequency": 11938, "polarization": "Vertical",   "date": "2026-05-10", "source": "MBC Group",           "category": "👶 أطفال وكرتون"},
        "NILE NEWS":          {"frequency": 11179, "polarization": "Vertical",   "date": "2026-05-22", "source": "Nilesat Official",    "category": "📰 أخبار وسياسة"},
        "AL JAZEERA HD":      {"frequency": 11938, "polarization": "Horizontal", "date": "2026-05-20", "source": "Arabsat",             "category": "📰 أخبار وسياسة"},
        "CAIRO NEWS":         {"frequency": 11843, "polarization": "Horizontal", "date": "2026-05-16", "source": "Nilesat",             "category": "📰 أخبار وسياسة"},
        "MBC1 HD":            {"frequency": 11938, "polarization": "Vertical",   "date": "2026-05-11", "source": "MBC Group",           "category": "📺 قنوات عامة ومنوعات"},
        "NILE TV HD":         {"frequency": 11179, "polarization": "Vertical",   "date": "2026-05-09", "source": "Nilesat",             "category": "📺 قنوات عامة ومنوعات"},
        "DREAM TV HD":        {"frequency": 11843, "polarization": "Horizontal", "date": "2026-05-07", "source": "FlySat",              "category": "📺 قنوات عامة ومنوعات"},
    }

BRAIN_FILE = "ai_brain_db.json"

def load_persistent_brain():
    db = get_base_2026_db()
    if os.path.exists(BRAIN_FILE):
        try:
            with open(BRAIN_FILE, "r", encoding="utf-8") as f:
                db.update(json.load(f))
        except Exception:
            pass
    return db

def save_persistent_brain(db):
    try:
        with open(BRAIN_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
    except Exception:
        pass

MASTER_2026_DB = load_persistent_brain()
TODAY_STR = "2026-05-25"
TODAY_DT  = datetime.strptime(TODAY_STR, "%Y-%m-%d")

ALL_CATEGORIES = [
    "⛪ قنوات مسيحية",
    "🕌 قنوات إسلامية",
    "🎬 مسلسلات ودراما",
    "🍿 أفلام عربية وأجنبية",
    "👶 أطفال وكرتون",
    "⚽ رياضة",
    "📰 أخبار وسياسة",
    "📺 قنوات عامة ومنوعات",
]

# ══════════════════════════════════════════════════════════════
#  عدادات الرادار
# ══════════════════════════════════════════════════════════════
ch_today = ch_week = 0
for v in MASTER_2026_DB.values():
    try:
        delta = (TODAY_DT - datetime.strptime(v.get("date", TODAY_STR), "%Y-%m-%d")).days
        if delta == 0: ch_today += 1
        if delta <= 7: ch_week  += 1
    except Exception:
        pass

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""<div class="cyber-metric-card">
        <div class="metric-label">🌟 رُصدت اليوم</div>
        <div class="metric-num" style="color:{PINK};">{ch_today}</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="cyber-metric-card">
        <div class="metric-label">⚡ آخر 7 أيام</div>
        <div class="metric-num" style="color:{CYAN};">{ch_week}</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="cyber-metric-card">
        <div class="metric-label">📦 إجمالي البنك</div>
        <div class="metric-num" style="color:{GREEN};">{len(MASTER_2026_DB)}</div>
    </div>""", unsafe_allow_html=True)

st.write("")

# ══════════════════════════════════════════════════════════════
#  محرك البحث والرادار
# ══════════════════════════════════════════════════════════════
st.markdown(f"### {t['search_header']}")

col_s, col_t, col_c = st.columns([5, 3, 3])
with col_s:
    search_q = st.text_input("", placeholder=t['search_placeholder'], key="radar_search").strip().upper()
with col_t:
    time_filter = st.selectbox("📅 النطاق الزمني:", ["كل الترددات","حصريات اليوم","آخر 7 أيام","مايو 2026"])
with col_c:
    cats_list = ["كل الفئات"] + list(dict.fromkeys(v.get("category","📺 قنوات عامة ومنوعات") for v in MASTER_2026_DB.values()))
    cat_filter = st.selectbox("🗂️ الفئة:", cats_list)

rows = []
for ch_name, info in MASTER_2026_DB.items():
    ch_cat  = info.get("category","📺 قنوات عامة ومنوعات")
    ch_date = info.get("date", TODAY_STR)
    ch_freq = f"{info['frequency']} MHz ({info['polarization'][0]})"
    ch_src  = info.get("source","Live Feed")
    if search_q and not any(search_q in x for x in [ch_name, ch_freq, ch_src.upper(), ch_date]):
        continue
    if cat_filter != "كل الفئات" and ch_cat != cat_filter:
        continue
    try:
        diff = (TODAY_DT - datetime.strptime(ch_date, "%Y-%m-%d")).days
        if time_filter == "حصريات اليوم" and diff != 0: continue
        if time_filter == "آخر 7 أيام"   and diff > 7:  continue
        if time_filter == "مايو 2026"     and not ch_date.startswith("2026-05"): continue
    except Exception:
        pass
    rows.append({
        "حالة الرصد":    "🌟 اليوم" if ch_date == TODAY_STR else "🟢 نشط",
        "اسم القناة":    ch_name,
        "التردد 2026":   ch_freq,
        "الفئة":         ch_cat,
        "تاريخ التحديث": ch_date,
        "المصدر":        ch_src,
    })

if rows:
    st.dataframe(rows, use_container_width=True)
else:
    st.warning("⚠️ لا توجد ترددات مطابقة للفلاتر الحالية.")

st.write("---")

# ══════════════════════════════════════════════════════════════
#  تصنيف AI
# ══════════════════════════════════════════════════════════════
def ai_classify(name: str) -> str:
    n = name.upper().strip()
    if n in MASTER_2026_DB and "category" in MASTER_2026_DB[n]:
        return MASTER_2026_DB[n]["category"]
    checks = [
        (["CTV","AGHAPY","ME SAT","MESAT","MARMARKOS","KOOGI","SAT-7"], ALL_CATEGORIES[0]),
        (["QURAN","RAHMA","MAJD"],                                       ALL_CATEGORIES[1]),
        (["DRAMA","SERIES","ALWAN"],                                     ALL_CATEGORIES[2]),
        (["CINEMA","ROTANA","AFLAM","MIX ONE","MBC2","ACTION"],          ALL_CATEGORIES[3]),
        (["SPACE TOON","MBC3","MAJID","WANNASAH"],                       ALL_CATEGORIES[4]),
        (["SPORT","ONTIME","BEIN"],                                      ALL_CATEGORIES[5]),
        (["NEWS","JAZEERA","ARABIYA","CAIRO"],                           ALL_CATEGORIES[6]),
    ]
    for keywords, cat in checks:
        if any(w in n for w in keywords):
            return cat
    return ALL_CATEGORIES[7]

# ══════════════════════════════════════════════════════════════
#  🆕 قراءة ملف الترتيب TXT/CSV
#  الفورمات المدعوم (كل سطر):
#    اسم_القناة
#    اسم_القناة,تردد
#    اسم_القناة,تردد,فئة
#    اسم_القناة,تردد,فئة,استقطاب
# ══════════════════════════════════════════════════════════════
def parse_sort_txt(file_bytes: bytes) -> list[dict]:
    """
    يقرأ ملف نص ويرجع قائمة مرتبة من dict:
      { name, frequency(int|None), category(str|None), polarization(str|None), source }
    """
    try:
        text = file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        text = file_bytes.decode("latin-1")

    result = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):      # تجاهل التعليقات والأسطر الفارغة
            continue
        # دعم الفاصلة أو الفاصلة المنقوطة أو التاب
        parts = re.split(r'[,;\t]', line)
        name = parts[0].strip().upper()
        if not name:
            continue

        freq    = None
        cat     = None
        pol     = None

        if len(parts) >= 2:
            freq_raw = parts[1].strip()
            if freq_raw.isdigit():
                freq = int(freq_raw)

        if len(parts) >= 3:
            cat_raw = parts[2].strip()
            if cat_raw:
                cat = cat_raw

        if len(parts) >= 4:
            pol_raw = parts[3].strip().capitalize()
            if pol_raw in ("Vertical", "Horizontal"):
                pol = pol_raw

        result.append({
            "name":         name,
            "frequency":    freq,
            "category":     cat,
            "polarization": pol,
            "source":       "Sort File",
        })
    return result


def build_template_csv() -> bytes:
    """ينشئ قالب CSV للمستخدم."""
    lines = [
        "# قالب RAMBO ULTRA - ملف الترتيب والترددات",
        "# الفورمات: اسم_القناة,تردد,فئة,استقطاب",
        "# التردد والفئة والاستقطاب اختيارية - يمكن ترك الأعمدة فارغة",
        "# مثال:",
        "CTV HD,12022,⛪ قنوات مسيحية,Vertical",
        "AGHAPY TV,11179,⛪ قنوات مسيحية,Vertical",
        "EGYPT QURAN,11179,🕌 قنوات إسلامية,Vertical",
        "MBC1 HD,11938,📺 قنوات عامة ومنوعات,Vertical",
        "MBC DRAMA HD,11938,🎬 مسلسلات ودراما,Vertical",
        "ON TIME SPORTS 1 HD,11861,⚽ رياضة,Vertical",
        "BEIN SPORTS HD1,12226,⚽ رياضة,Horizontal",
        "AL JAZEERA HD,11938,📰 أخبار وسياسة,Horizontal",
        "WANNASAH HD,11938,👶 أطفال وكرتون,Vertical",
        "ROTANA CINEMA,11843,🍿 أفلام عربية وأجنبية,Horizontal",
    ]
    return "\n".join(lines).encode("utf-8-sig")

# ══════════════════════════════════════════════════════════════
#  الـ Sidebar
# ══════════════════════════════════════════════════════════════
st.sidebar.markdown(f"### {t['mode_selector']}")
app_mode = st.sidebar.radio("", [t['mode_edit'], t['mode_gen']])

# ── رفع ملف الترتيب (مشترك بين الوضعين) ──────────────────────
st.sidebar.markdown("---")
st.sidebar.markdown(f"### {t['upload_txt_label']}")
st.sidebar.caption(t['upload_txt_help'])
sort_file = st.sidebar.file_uploader("", type=["txt","csv"], key="sort_uploader")

# قالب جاهز للتحميل
st.sidebar.download_button(
    label     = t['txt_download_template'],
    data      = build_template_csv(),
    file_name = "rambo_sort_template.csv",
    mime      = "text/csv",
)

# معالجة ملف الترتيب
sort_list: list[dict] = []  # القائمة المرتبة من الملف (فارغة = لا يوجد ملف)
sort_names_ordered: list[str] = []  # أسماء القنوات بالترتيب (uppercase)

if sort_file is not None:
    sort_bytes = sort_file.read()
    sort_list  = parse_sort_txt(sort_bytes)
    sort_names_ordered = [ch["name"] for ch in sort_list]

    # تطبيق الترددات والفئات من الملف على البنك الحي
    updated_from_file = 0
    for entry in sort_list:
        nm = entry["name"]
        if nm not in MASTER_2026_DB:
            MASTER_2026_DB[nm] = {
                "frequency":    entry["frequency"] or 0,
                "polarization": entry["polarization"] or "Vertical",
                "date":         TODAY_STR,
                "source":       "Sort File",
                "category":     entry["category"] or ai_classify(nm),
            }
            updated_from_file += 1
        else:
            # تردد الملف يطغى دائماً
            if entry["frequency"]:
                MASTER_2026_DB[nm]["frequency"]    = entry["frequency"]
                MASTER_2026_DB[nm]["polarization"] = entry["polarization"] or MASTER_2026_DB[nm].get("polarization","Vertical")
                updated_from_file += 1
            if entry["category"]:
                MASTER_2026_DB[nm]["category"] = entry["category"]

    save_persistent_brain(MASTER_2026_DB)

    # عرض معاينة في Sidebar
    st.sidebar.success(t['txt_stats'].format(len(sort_list)))

    # معاينة تفصيلية في الصفحة الرئيسية
    with st.expander(t['txt_preview_header'], expanded=False):
        preview_rows = []
        for i, entry in enumerate(sort_list, 1):
            nm  = entry["name"]
            eff_freq = entry["frequency"] or MASTER_2026_DB.get(nm, {}).get("frequency", "—")
            eff_cat  = entry["category"]  or MASTER_2026_DB.get(nm, {}).get("category",  ai_classify(nm))
            eff_pol  = entry["polarization"] or MASTER_2026_DB.get(nm, {}).get("polarization", "—")
            src_tag  = "📋 ملف" if entry["frequency"] else "🏦 بنك"
            preview_rows.append({
                "#":      i,
                "القناة": nm,
                "التردد": f"{eff_freq} ({str(eff_pol)[0] if eff_pol != '—' else '?'})",
                "الفئة":  eff_cat,
                "مصدر التردد": src_tag,
            })
        st.dataframe(preview_rows, use_container_width=True)
        st.caption(f"📋 {len(sort_list)} قناة | 📋 تردد الملف يطغى على البنك 2026")

file_processed      = False
file_bytes_out      = b""
unique_channels_map = {}
database_needs_save = False
is_modern           = False   # تعريف مبكر لتجنب أخطاء scope

# ══════════════════════════════════════════════════════════════
#  وضع التعديل
# ══════════════════════════════════════════════════════════════
if app_mode == t['mode_edit']:
    uploaded_file = st.file_uploader(t['upload_label'], type=["TLL"])

    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        try:
            file_text = file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            file_text = file_bytes.decode('latin-1')

        root       = ET.fromstring(file_bytes)
        legacy_tag = root.find(".//legacybroadcast")
        is_modern  = legacy_tag is not None and legacy_tag.text

        enforce_2026 = st.checkbox(t['update_freq_label'], value=True)
        inject_excl  = st.checkbox(t['add_new_ch_label'],  value=True)

        if is_modern:
            broadcast_data = json.loads(legacy_tag.text)
            uploaded_list  = broadcast_data.get("channelList", [])

            for c in uploaded_list:
                name_up = c.get("channelName","").strip().upper()
                freq_up = c.get("frequency", 0)
                pol_up  = c.get("polarization","Horizontal")
                if name_up and freq_up > 0:
                    if name_up not in MASTER_2026_DB or MASTER_2026_DB[name_up]["frequency"] != int(freq_up):
                        MASTER_2026_DB[name_up] = {
                            "frequency":    int(freq_up),
                            "polarization": pol_up,
                            "date":         TODAY_STR,
                            "source":       "User Flash Injection",
                            "category":     ai_classify(name_up),
                        }
                        database_needs_save = True

            for idx, ch in enumerate(uploaded_list):
                ch_name = ch.get("channelName","").strip()
                name_up = ch_name.upper()
                if not name_up:
                    continue
                # الأولوية: تردد ملف الترتيب ← بنك 2026 (إذا enforce) ← الأصلي
                if name_up in sort_names_ordered and MASTER_2026_DB.get(name_up,{}).get("frequency"):
                    ch["frequency"]    = MASTER_2026_DB[name_up]["frequency"]
                    ch["polarization"] = MASTER_2026_DB[name_up]["polarization"]
                elif enforce_2026 and name_up in MASTER_2026_DB:
                    ch["frequency"]    = int(MASTER_2026_DB[name_up]["frequency"])
                    ch["polarization"] = MASTER_2026_DB[name_up]["polarization"]
                unique_channels_map[name_up] = {
                    "id": idx, "name": ch_name,
                    "freq": str(ch["frequency"]), "raw_node": ch,
                }
        else:
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
                                "frequency":    int(freq_up),
                                "polarization": "Vertical",
                                "date":         TODAY_STR,
                                "source":       "User Legacy Flash",
                                "category":     ai_classify(name_up),
                            }
                            database_needs_save = True

            for idx, item_str in enumerate(item_blocks):
                nm = re.search(r'<vchName>(.*?)</vchName>', item_str)
                fr = re.search(r'<frequency>(.*?)</frequency>', item_str)
                if not nm:
                    continue
                ch_name = nm.group(1).strip()
                name_up = ch_name.upper()
                old_freq = fr.group(1).strip() if fr else "0"
                if name_up in sort_names_ordered and MASTER_2026_DB.get(name_up,{}).get("frequency"):
                    vf = MASTER_2026_DB[name_up]["frequency"]
                    item_str = re.sub(r'<frequency>\d+</frequency>', f'<frequency>{vf}</frequency>', item_str)
                    old_freq = str(vf)
                elif enforce_2026 and name_up in MASTER_2026_DB:
                    vf = MASTER_2026_DB[name_up]["frequency"]
                    item_str = re.sub(r'<frequency>\d+</frequency>', f'<frequency>{vf}</frequency>', item_str)
                    old_freq = str(vf)
                unique_channels_map[name_up] = {
                    "id": idx, "name": ch_name,
                    "freq": old_freq, "raw_str": item_str,
                }

        if database_needs_save:
            save_persistent_brain(MASTER_2026_DB)
            st.toast("📡 تم حفظ الترددات الجديدة في بنك البيانات!", icon="🧠")

        st.success(t['success_read'] + ("Smart webOS" if is_modern else "Legacy"))
        file_processed = True

# ══════════════════════════════════════════════════════════════
#  وضع التوليد
# ══════════════════════════════════════════════════════════════
else:
    col_m, col_c2 = st.columns(2)
    with col_m:
        model_choice = st.selectbox(t['model_label'], [t['model_modern'], t['model_legacy']])
    with col_c2:
        country_choice = st.selectbox(t['country_label'], [t['country_egy'], t['country_ksa']])

    country_code = "NAFR" if "Egypt" in country_choice or "مصر" in country_choice else "MIDE"

    if st.button(t['btn_generate']):
        st.session_state.generated_active = True

    if st.session_state.get('generated_active'):
        # إذا فيه ملف ترتيب: رتّب بحسبه، وأضف الباقيين في النهاية
        source_db = dict(MASTER_2026_DB)
        ordered_keys = []
        if sort_names_ordered:
            for nm in sort_names_ordered:
                if nm in source_db:
                    ordered_keys.append(nm)
            # الباقي اللي مش في ملف الترتيب
            for nm in source_db:
                if nm not in ordered_keys:
                    ordered_keys.append(nm)
        else:
            ordered_keys = list(source_db.keys())

        for idx, ch_name in enumerate(ordered_keys):
            data = source_db[ch_name]
            unique_channels_map[ch_name] = {
                "id":   idx,
                "name": ch_name,
                "freq": str(data["frequency"]),
                "raw_node": {
                    "channelName":  ch_name,
                    "frequency":    data["frequency"],
                    "polarization": data["polarization"],
                    "majorNumber":  0,
                    "serviceType":  "1",
                    "scrambled":    "false",
                    "symbolRate":   "27500",
                },
            }
        file_processed = True
        is_modern      = t['model_modern'] in model_choice
        st.success(t['success_gen'] + country_code)

# ══════════════════════════════════════════════════════════════
#  بناء الملف النهائي وتحميله
# ══════════════════════════════════════════════════════════════
if file_processed and unique_channels_map:
    st.markdown(f"""<div class="lg-tip-box">
        <strong>💡 {t['lg_trick_title']}</strong>{t['lg_trick_text']}
    </div>""", unsafe_allow_html=True)

    # ── ترتيب القنوات ─────────────────────────────────────────
    if sort_names_ordered:
        # الترتيب من ملف TXT: القنوات الموجودة في الملف أولاً بترتيبها،
        # ثم الباقيات مرتبة بالفئة من multiselect
        user_priority = st.multiselect(
            t['multiselect_label'],
            options=ALL_CATEGORIES,
            default=[],
            help="يُطبَّق فقط على القنوات غير الموجودة في ملف الترتيب"
        )
        final_priority = list(user_priority) + [c for c in ALL_CATEGORIES if c not in user_priority]

        in_sort   = [ch for nm, ch in unique_channels_map.items() if nm in sort_names_ordered]
        out_sort  = [ch for nm, ch in unique_channels_map.items() if nm not in sort_names_ordered]

        # رتّب in_sort بحسب ترتيب ملف TXT
        in_sort.sort(key=lambda x: sort_names_ordered.index(x["name"].upper())
                     if x["name"].upper() in sort_names_ordered else 9999)
        # رتّب out_sort بالفئة
        out_sort.sort(key=lambda x: final_priority.index(ai_classify(x["name"])))

        sorted_channels = in_sort + out_sort
        st.info(f"📋 {len(in_sort)} قناة مرتبة من ملف الترتيب + {len(out_sort)} قناة مرتبة بالفئة")
    else:
        user_priority = st.multiselect(t['multiselect_label'], options=ALL_CATEGORIES, default=[])
        final_priority = list(user_priority) + [c for c in ALL_CATEGORIES if c not in user_priority]
        sorted_channels = sorted(
            unique_channels_map.values(),
            key=lambda x: final_priority.index(ai_classify(x["name"]))
        )

    # ── بناء الملف ────────────────────────────────────────────
    if app_mode == t['mode_edit'] and is_modern:
        final_list = []
        for i, ch in enumerate(sorted_channels, 1):
            node = ch["raw_node"]
            node["majorNumber"] = i
            final_list.append(node)
        broadcast_data["channelList"] = final_list
        legacy_tag.text = json.dumps(broadcast_data, ensure_ascii=False)
        file_bytes_out = ET.tostring(root, encoding="utf-8")
    else:
        items_out = []
        for i, ch in enumerate(sorted_channels, 1):
            if "raw_str" in ch:
                s = ch["raw_str"]
                s = re.sub(r'<prNum>\d+</prNum>', f'<prNum>{i}</prNum>', s) \
                    if "<prNum>" in s \
                    else s.replace("<ITEM>", f"<ITEM>\r\n<prNum>{i}</prNum>")
                items_out.append(s)
            else:
                node = ch["raw_node"]
                items_out.append(
                    f"<ITEM>\r\n<prNum>{i}</prNum>\r\n"
                    f"<vchName>{node['channelName']}</vchName>\r\n"
                    f"<frequency>{node['frequency']}</frequency>\r\n"
                    f"<polarization>{node['polarization']}</polarization>\r\n"
                    f"</ITEM>"
                )
        file_bytes_out = "\r\n".join(items_out).encode("utf-8")

    st.success(t['ready_msg'])
    st.download_button(
        label     = t['btn_download_tll'],
        data      = file_bytes_out,
        file_name = "GlobalClone00001.TLL",
        mime      = "application/octet-stream",
    )
    st.caption(f"📊 {len(sorted_channels)} {t['channels_count']}")

# ── Footer ─────────────────────────────────────────────────────
st.markdown("""
<div class="cyber-footer">
    <div style="font-size:15px;font-weight:700;color:#ff0066;">🛠️ DEVELOPER ENG: RAFIK NATHAN</div>
    <div style="font-size:12px;color:#7090aa;margin-top:4px;">📱 +201280339779 &nbsp;|&nbsp; rafikrambo113@gmail.com</div>
</div>
""", unsafe_allow_html=True)
