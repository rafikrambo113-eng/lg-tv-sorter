import streamlit as st
import xml.etree.ElementTree as ET
import json
import re
import os
import csv
from io import StringIO
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
        'update_freq_label': "⚛️ تطبيق الترددات الرسمية 2026",
        'add_new_ch_label': "✨ امتصاص القنوات الجديدة وحفظها",
        'success_read': "🛸 تم قراءة الملف بنجاح! الموديل: ",
        'success_gen': "🌌 تم توليد ملف قنوات LG لنطاق: ",
        'search_header': "🔍 محرك الفرز والبحث الاستخباراتي:",
        'search_placeholder': "ابحث باسم القناة، التردد، المصدر، أو التاريخ...",
        'multiselect_label': "ترتيب خطة العرض حسب الفئات:",
        'ready_msg': "🌌 تم دمج المصفوفة وتطهير البيانات! الملف جاهز:",
        'btn_download_tll': "📥 تحميل ملف الشاشة المحدث (GlobalClone00001.TLL)",
        'btn_download_sort': "📥 تحميل ترتيب القنوات (CSV)",
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
        'update_freq_label': "⚛️ Enforce Official Live 2026 Frequencies",
        'add_new_ch_label': "✨ Absorb New Channels to Persistent Memory",
        'success_read': "🛸 File Decoded. Profile: ",
        'success_gen': "🌌 Pure LG layout created for: ",
        'search_header': "🔍 Quantum Search & Temporal Timeline Filter:",
        'search_placeholder': "Search by channel, frequency, source, or date...",
        'multiselect_label': "Build your interactive category sequence:",
        'ready_msg': "🌌 Matrix Cleansing Successful! Asset ready:",
        'btn_download_tll': "📥 Download Verified TV Config (GlobalClone00001.TLL)",
        'btn_download_sort': "📥 Download Sort File (CSV)",
        'channels_count': "Pure Channels",
        'lg_trick_title': "💡 LG Post-Installation Step:",
        'lg_trick_text': "Settings → Channels → Channel Manager → Edit All Channels → Select All → Restore to enforce correct sort order.",
    }
}

st.set_page_config(page_title="RAMBO ULTRA", page_icon="📡", layout="wide")

t = UI_TEXT[st.session_state.lang]

# ── زر اللغة والثيم ──────────────────────────────────────────
col_lang, col_theme, _ = st.columns([1.2, 1.5, 8])
with col_lang:
    if st.button("🌐 English" if st.session_state.lang == 'ar' else "🌐 العربية"):
        st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
        st.rerun()
with col_theme:
    if st.button("☀️ Light Mode" if st.session_state.theme == 'dark' else "🌙 Dark Mode"):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

# ── CSS احترافي ───────────────────────────────────────────────
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

# ── العنوان ────────────────────────────────────────────────────
st.title(t['title'])
st.markdown(f"<h3 style='text-align:center;color:{MUTED};font-size:13px;'>{t['subtitle']}</h3>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  بنك الترددات 2026
# ══════════════════════════════════════════════════════════════
def get_base_2026_db():
    return {
        "CTV HD":            {"frequency": 12022, "polarization": "Vertical",   "date": "2026-05-25", "source": "FlySat Official",    "category": "⛪ قنوات مسيحية"},
        "ME SAT HD":         {"frequency": 11179, "polarization": "Vertical",   "date": "2026-05-24", "source": "Nilesat Spectrum",    "category": "⛪ قنوات مسيحية"},
        "AGHAPY TV":         {"frequency": 11179, "polarization": "Vertical",   "date": "2026-05-20", "source": "FlySat",              "category": "⛪ قنوات مسيحية"},
        "KOOGI TV":          {"frequency": 11096, "polarization": "Vertical",   "date": "2026-05-15", "source": "LyngSat",             "category": "⛪ قنوات مسيحية"},
        "ALHAYAT TV":        {"frequency": 11392, "polarization": "Vertical",   "date": "2026-05-01", "source": "Nilesat Official",    "category": "⛪ قنوات مسيحية"},
        "MARMARKOS":         {"frequency": 11137, "polarization": "Vertical",   "date": "2026-04-18", "source": "FlySat",              "category": "⛪ قنوات مسيحية"},
        "SAT-7 ARABIC":      {"frequency": 11977, "polarization": "Vertical",   "date": "2026-05-10", "source": "FlySat",              "category": "⛪ قنوات مسيحية"},
        "EGYPT QURAN":       {"frequency": 11179, "polarization": "Vertical",   "date": "2026-05-25", "source": "Nilesat Official",    "category": "🕌 قنوات إسلامية"},
        "SAUDI QURAN HD":    {"frequency": 12149, "polarization": "Horizontal", "date": "2026-05-22", "source": "Arabsat Feed",        "category": "🕌 قنوات إسلامية"},
        "AL MAJD QURAN":     {"frequency": 12054, "polarization": "Horizontal", "date": "2026-05-10", "source": "Almajd Network",      "category": "🕌 قنوات إسلامية"},
        "RAHMA TV":          {"frequency": 11283, "polarization": "Vertical",   "date": "2026-05-08", "source": "Nilesat",             "category": "🕌 قنوات إسلامية"},
        "MBC DRAMA HD":      {"frequency": 11938, "polarization": "Vertical",   "date": "2026-05-12", "source": "MBC Group",           "category": "🎬 مسلسلات ودراما"},
        "ROTANA DRAMA":      {"frequency": 11843, "polarization": "Horizontal", "date": "2026-05-05", "source": "Rotana Group",        "category": "🎬 مسلسلات ودراما"},
        "ALWAN HD":          {"frequency": 11958, "polarization": "Horizontal", "date": "2026-04-30", "source": "LyngSat",             "category": "🎬 مسلسلات ودراما"},
        "MIX ONE HD":        {"frequency": 11843, "polarization": "Horizontal", "date": "2026-05-25", "source": "Nilesat Monitor",     "category": "🍿 أفلام عربية وأجنبية"},
        "MBC2 HD":           {"frequency": 11938, "polarization": "Vertical",   "date": "2026-05-14", "source": "MBC Group",           "category": "🍿 أفلام عربية وأجنبية"},
        "ROTANA CINEMA":     {"frequency": 11843, "polarization": "Horizontal", "date": "2026-05-03", "source": "Rotana Group",        "category": "🍿 أفلام عربية وأجنبية"},
        "ON TIME SPORTS 1 HD":{"frequency":11861, "polarization": "Vertical",   "date": "2026-05-18", "source": "URC Egypt",           "category": "⚽ رياضة"},
        "ON TIME SPORTS 2 HD":{"frequency":11843, "polarization": "Vertical",   "date": "2026-05-18", "source": "URC Egypt",           "category": "⚽ رياضة"},
        "BEIN SPORTS HD1":   {"frequency": 12226, "polarization": "Horizontal", "date": "2026-05-15", "source": "beIN Sports",         "category": "⚽ رياضة"},
        "WANNASAH HD":       {"frequency": 11938, "polarization": "Vertical",   "date": "2026-05-24", "source": "Nilesat Transponder", "category": "👶 أطفال وكرتون"},
        "SPACE TOON":        {"frequency": 11977, "polarization": "Horizontal", "date": "2026-04-20", "source": "FlySat",              "category":
