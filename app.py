"""
RAMBO – Channel File Generator  (pages/3_📡_Channel_Generator.py)
──────────────────────────────────────────────────────────────────
صفحة توليد ملف قنوات من الصفر:
  • اختر البلد  →  اختر الموديل  →  اختر ترتيب الفئات
  • يولّد ملف GlobalClone00001.TLL + تقرير نصي فوراً
  • بدون رفع أي ملف - بدون AI Key
  • قاعدة بيانات كاملة لـ: مصر، السعودية، الإمارات، المغرب، تونس،
    الجزائر، لبنان، العراق، سوريا، ليبيا، السودان، قطر، الكويت
"""

import streamlit as st
import json
import re
from datetime import datetime

# ══════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="RAMBO – Channel Generator",
    page_icon="📡",
    layout="wide",
)

# ══════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════
for k, v in [('lang', 'ar'), ('theme', 'dark')]:
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════
#  TRANSLATIONS
# ══════════════════════════════════════════════════════════
UI = {
    'ar': {
        'title':        "📡 RAMBO – مولّد ملف القنوات",
        'subtitle':     "اختر بلدك وموديل شاشتك → يولّد ملف TLL جاهز فوراً بدون رفع أي ملف",
        'country_lbl':  "🌍 اختر بلد البث",
        'model_lbl':    "📺 أدخل موديل الشاشة",
        'model_ph':     "مثال: OLED55C1PVA",
        'sort_title':   "🎛️ رتّب الفئات حسب تفضيلك (اضغط بالترتيب)",
        'sort_tip':     "💡 الفئة الأولى ستظهر في أعلى قائمة التلفزيون",
        'sort_lbl':     "اختر الفئات بالترتيب:",
        'gen_btn':      "🚀 توليد ملف القنوات",
        'preview':      "📊 معاينة القنوات:",
        'ready':        "✅ الملف جاهز للتحميل!",
        'dl_tll':       "📥 تحميل GlobalClone00001.TLL",
        'dl_txt':       "📄 تحميل تقرير القنوات (.txt)",
        'channels':     "قناة",
        'lg_tip_title': "💡 نصيحة مهمة بعد رفع الملف على شاشة LG:",
        'lg_tip_text':  (
            "إذا لاحظت أن الترتيب غير صحيح بعد رفع الملف:\n"
            "1. الإعدادات ← القنوات ← مدير القنوات\n"
            "2. تعديل كل القنوات\n"
            "3. حدّد كل القنوات ← استعادة (Restore)"
        ),
        'sat_detected': "القمر الصناعي المكتشف تلقائياً:",
        'total_ch':     "إجمالي القنوات:",
        'categories':   [
            "⛪ قنوات مسيحية",
            "🕌 قنوات إسلامية",
            "🎬 مسلسلات ودراما",
            "🍿 أفلام",
            "👶 أطفال وكرتون",
            "⚽ رياضة",
            "📰 أخبار وسياسة",
            "🎵 موسيقى وترفيه",
            "📺 قنوات عامة ومنوعات",
        ],
    },
    'en': {
        'title':        "📡 RAMBO – Channel File Generator",
        'subtitle':     "Select country & TV model → Instant TLL file — no upload, no API key",
        'country_lbl':  "🌍 Select Broadcast Country",
        'model_lbl':    "📺 Enter TV Model",
        'model_ph':     "e.g. OLED55C1PVA",
        'sort_title':   "🎛️ Sort categories in preferred order (click in order)",
        'sort_tip':     "💡 First category appears at the top of your TV list",
        'sort_lbl':     "Select categories in order:",
        'gen_btn':      "🚀 Generate Channel File",
        'preview':      "📊 Channel Preview:",
        'ready':        "✅ File ready for download!",
        'dl_tll':       "📥 Download GlobalClone00001.TLL",
        'dl_txt':       "📄 Download Channel Report (.txt)",
        'channels':     "Channels",
        'lg_tip_title': "💡 Important tip after uploading to LG TV:",
        'lg_tip_text':  (
            "If channels appear unsorted after uploading:\n"
            "1. Settings → Channels → Channel Manager\n"
            "2. Edit All Channels\n"
            "3. Select All → Restore"
        ),
        'sat_detected': "Auto-detected Satellite:",
        'total_ch':     "Total Channels:",
        'categories':   [
            "⛪ Christian",
            "🕌 Islamic",
            "🎬 Drama & Series",
            "🍿 Movies",
            "👶 Kids & Cartoon",
            "⚽ Sports",
            "📰 News & Politics",
            "🎵 Music & Entertainment",
            "📺 General",
        ],
    },
}
t = UI[st.session_state.lang]
CATS = t['categories']

# ══════════════════════════════════════════════════════════
#  CHANNEL DATABASE  (per-country, Nilesat 7°W)
# ══════════════════════════════════════════════════════════
# كل قناة: name, frequency, symbol_rate, polarization, category_index
# category_index → index في قائمة CATS أعلاه (0-8)

CHANNELS_DB = {

    # ── مصر ──────────────────────────────────────────────
    "مصر / Egypt": {
        "satellite": "Nilesat 7°W",
        "channels": [
            # أخبار
            {"name": "CBC",                  "f": 10853, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "CBC EXTRA",            "f": 10853, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "EXTRA NEWS",           "f": 10853, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "ON E",                 "f": 11727, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "ON TIME NEWS",         "f": 11727, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "DMC",                  "f": 11727, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "AL NAHAR",             "f": 11938, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "AL NAHAR DRAMA",       "f": 11938, "sr": 27500, "pol": "V", "cat": 2},
            {"name": "AL NAHAR SPORT",       "f": 11938, "sr": 27500, "pol": "V", "cat": 5},
            # رياضة
            {"name": "ON TIME SPORTS 1 HD",  "f": 11861, "sr": 27500, "pol": "V", "cat": 5},
            {"name": "ON TIME SPORTS 2 HD",  "f": 11861, "sr": 27500, "pol": "V", "cat": 5},
            {"name": "ON TIME SPORTS 3 HD",  "f": 11861, "sr": 27500, "pol": "V", "cat": 5},
            {"name": "ON TIME SPORTS 4 HD",  "f": 11861, "sr": 27500, "pol": "V", "cat": 5},
            # دراما وترفيه
            {"name": "CBC DRAMA",            "f": 10853, "sr": 27500, "pol": "V", "cat": 2},
            {"name": "DMC DRAMA",            "f": 11727, "sr": 27500, "pol": "V", "cat": 2},
            {"name": "WATCH IT HD",          "f": 11727, "sr": 27500, "pol": "V", "cat": 2},
            {"name": "MBC MASR",             "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "MBC MASR 2",           "f": 11938, "sr": 27500, "pol": "V", "cat": 2},
            # أفلام
            {"name": "ROTANA CINEMA",        "f": 12034, "sr": 27500, "pol": "H", "cat": 3},
            {"name": "ROTANA CLASSIC",       "f": 12034, "sr": 27500, "pol": "H", "cat": 3},
            {"name": "ROTANA COMEDY",        "f": 12034, "sr": 27500, "pol": "H", "cat": 3},
            {"name": "CBC SOFRA HD",         "f": 10853, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "MBC 2",                "f": 11938, "sr": 27500, "pol": "V", "cat": 3},
            {"name": "MBC ACTION",           "f": 11938, "sr": 27500, "pol": "V", "cat": 3},
            # أطفال
            {"name": "SPACETOON",            "f": 11220, "sr": 27500, "pol": "H", "cat": 4},
            {"name": "TOYOR AL JANNAH",      "f": 11220, "sr": 27500, "pol": "H", "cat": 4},
            {"name": "JEEM TV",              "f": 11220, "sr": 27500, "pol": "H", "cat": 4},
            # إسلامية
            {"name": "AL HAYAT",             "f": 12207, "sr": 27500, "pol": "V", "cat": 1},
            {"name": "IQRAA",                "f": 11747, "sr": 27500, "pol": "H", "cat": 1},
            {"name": "AL RESALA",            "f": 11747, "sr": 27500, "pol": "H", "cat": 1},
            # مسيحية
            {"name": "AGHAPY TV",            "f": 11179, "sr": 27500, "pol": "H", "cat": 0},
            {"name": "CTV",                  "f": 12022, "sr": 27500, "pol": "V", "cat": 0},
            {"name": "SAT-7 ARABIC",         "f": 11353, "sr": 27500, "pol": "V", "cat": 0},
            {"name": "SAT-7 KIDS",           "f": 11353, "sr": 27500, "pol": "V", "cat": 0},
            {"name": "ALKARMA ME 1",         "f": 11096, "sr": 27500, "pol": "H", "cat": 0},
            # موسيقى
            {"name": "MAZZIKA",              "f": 11727, "sr": 27500, "pol": "V", "cat": 7},
            {"name": "MELODY AFLAM",         "f": 11727, "sr": 27500, "pol": "V", "cat": 7},
            {"name": "NILE SONG",            "f": 11881, "sr": 27500, "pol": "V", "cat": 7},
            # عامة
            {"name": "NILE LIFE",            "f": 11881, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "NILE DRAMA",           "f": 11881, "sr": 27500, "pol": "V", "cat": 2},
            {"name": "NILE NEWS",            "f": 11881, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "AL HAYAH",             "f": 10992, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "TEN TV",               "f": 11220, "sr": 27500, "pol": "H", "cat": 8},
        ],
    },

    # ── السعودية ──────────────────────────────────────────
    "السعودية / Saudi Arabia": {
        "satellite": "Arabsat/Badr 26°E",
        "channels": [
            {"name": "MBC 1",                "f": 11862, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "MBC 2",                "f": 11862, "sr": 27500, "pol": "H", "cat": 3},
            {"name": "MBC 3",                "f": 11862, "sr": 27500, "pol": "H", "cat": 4},
            {"name": "MBC 4",                "f": 11862, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "MBC ACTION",           "f": 11862, "sr": 27500, "pol": "H", "cat": 3},
            {"name": "MBC DRAMA",            "f": 11862, "sr": 27500, "pol": "H", "cat": 2},
            {"name": "MBC MAX",              "f": 11862, "sr": 27500, "pol": "H", "cat": 3},
            {"name": "MBC MASR",             "f": 11862, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "MBC BOLLYWOOD",        "f": 11862, "sr": 27500, "pol": "H", "cat": 3},
            {"name": "ROTANA CINEMA",        "f": 11785, "sr": 27500, "pol": "V", "cat": 3},
            {"name": "ROTANA KHALIJIA",      "f": 11785, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "ROTANA CLASSIC",       "f": 11785, "sr": 27500, "pol": "V", "cat": 3},
            {"name": "ROTANA COMEDY",        "f": 11785, "sr": 27500, "pol": "V", "cat": 3},
            {"name": "SSC SPORT 1",          "f": 11785, "sr": 27500, "pol": "V", "cat": 5},
            {"name": "SSC SPORT 2",          "f": 11785, "sr": 27500, "pol": "V", "cat": 5},
            {"name": "SSC SPORT 3",          "f": 11785, "sr": 27500, "pol": "V", "cat": 5},
            {"name": "SAUDI TV 1",           "f": 11727, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "SAUDI TV 2",           "f": 11727, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "AL EKHBARIYA",         "f": 11727, "sr": 27500, "pol": "H", "cat": 6},
            {"name": "AL ARABIYA",           "f": 11919, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "AL HADATH",            "f": 11919, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "IQRAA",                "f": 11747, "sr": 27500, "pol": "H", "cat": 1},
            {"name": "AL RESALA",            "f": 11747, "sr": 27500, "pol": "H", "cat": 1},
            {"name": "SPACETOON",            "f": 11220, "sr": 27500, "pol": "H", "cat": 4},
            {"name": "TOYOR AL JANNAH",      "f": 11220, "sr": 27500, "pol": "H", "cat": 4},
        ],
    },

    # ── الإمارات ──────────────────────────────────────────
    "الإمارات / UAE": {
        "satellite": "Arabsat/Badr 26°E",
        "channels": [
            {"name": "ABU DHABI TV",         "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "ABU DHABI DRAMA",      "f": 11938, "sr": 27500, "pol": "V", "cat": 2},
            {"name": "AD SPORT 1",           "f": 11938, "sr": 27500, "pol": "V", "cat": 5},
            {"name": "AD SPORT 2",           "f": 11938, "sr": 27500, "pol": "V", "cat": 5},
            {"name": "AD SPORT 3",           "f": 11938, "sr": 27500, "pol": "V", "cat": 5},
            {"name": "DUBAI TV",             "f": 11727, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "DUBAI RACING",         "f": 11727, "sr": 27500, "pol": "V", "cat": 5},
            {"name": "DUBAI ONE",            "f": 11727, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "MBC 1",                "f": 11862, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "MBC 2",                "f": 11862, "sr": 27500, "pol": "H", "cat": 3},
            {"name": "AL ARABIYA",           "f": 11919, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "AL JAZEERA",           "f": 11938, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "SKY NEWS ARABIA",      "f": 11919, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "ROTANA CINEMA",        "f": 11785, "sr": 27500, "pol": "V", "cat": 3},
            {"name": "SPACETOON",            "f": 11220, "sr": 27500, "pol": "H", "cat": 4},
            {"name": "CARTOON NETWORK AR",   "f": 11220, "sr": 27500, "pol": "H", "cat": 4},
        ],
    },

    # ── قطر ──────────────────────────────────────────────
    "قطر / Qatar": {
        "satellite": "Arabsat/Badr 26°E",
        "channels": [
            {"name": "AL JAZEERA HD",        "f": 11938, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "AL JAZEERA MUBASHER",  "f": 11938, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "AL JAZEERA ENGLISH",   "f": 11938, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "QATAR TV HD",          "f": 10834, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "QATAR TV 2",           "f": 10834, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "AL KASS SPORT 1",      "f": 11938, "sr": 27500, "pol": "V", "cat": 5},
            {"name": "AL KASS SPORT 2",      "f": 11938, "sr": 27500, "pol": "V", "cat": 5},
            {"name": "AL KASS SPORT 3",      "f": 11938, "sr": 27500, "pol": "V", "cat": 5},
            {"name": "MBC 1",                "f": 11862, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "ROTANA CINEMA",        "f": 11785, "sr": 27500, "pol": "V", "cat": 3},
            {"name": "SPACETOON",            "f": 11220, "sr": 27500, "pol": "H", "cat": 4},
        ],
    },

    # ── الكويت ──────────────────────────────────────────
    "الكويت / Kuwait": {
        "satellite": "Arabsat/Badr 26°E",
        "channels": [
            {"name": "KUWAIT TV 1",          "f": 11747, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "KUWAIT TV 2",          "f": 11747, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "KUWAIT SPORT",         "f": 11747, "sr": 27500, "pol": "H", "cat": 5},
            {"name": "SCOPE TV",             "f": 11747, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "MBC 1",                "f": 11862, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "MBC 2",                "f": 11862, "sr": 27500, "pol": "H", "cat": 3},
            {"name": "AL ARABIYA",           "f": 11919, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "ROTANA CINEMA",        "f": 11785, "sr": 27500, "pol": "V", "cat": 3},
            {"name": "SSC SPORT 1",          "f": 11785, "sr": 27500, "pol": "V", "cat": 5},
            {"name": "SPACETOON",            "f": 11220, "sr": 27500, "pol": "H", "cat": 4},
            {"name": "TOYOR AL JANNAH",      "f": 11220, "sr": 27500, "pol": "H", "cat": 4},
        ],
    },

    # ── المغرب ──────────────────────────────────────────
    "المغرب / Morocco": {
        "satellite": "Hotbird 13°E",
        "channels": [
            {"name": "2M MAROC",             "f": 11785, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "AL AOULA",             "f": 11785, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "MEDI 1 TV",            "f": 11785, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "ARRABIA",              "f": 11785, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "TAMAZIGHT TV",         "f": 11785, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "LAAYOUNE TV",          "f": 11785, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "MBC 1",                "f": 11862, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "AL ARABIYA",           "f": 11919, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "AL JAZEERA HD",        "f": 11938, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "ROTANA CINEMA",        "f": 11785, "sr": 27500, "pol": "V", "cat": 3},
            {"name": "SPACETOON",            "f": 11220, "sr": 27500, "pol": "H", "cat": 4},
            {"name": "AL RESALA",            "f": 11747, "sr": 27500, "pol": "H", "cat": 1},
            {"name": "FRANCE 24 AR",         "f": 11785, "sr": 27500, "pol": "V", "cat": 6},
        ],
    },

    # ── تونس ──────────────────────────────────────────────
    "تونس / Tunisia": {
        "satellite": "Hotbird 13°E",
        "channels": [
            {"name": "WATANIA 1",            "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "WATANIA 2",            "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "HANNIBAL TV",          "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "NESSMA TV",            "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "AL HIWAR ATTOUNSI",    "f": 11938, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "ZITOUNA TV",           "f": 11938, "sr": 27500, "pol": "V", "cat": 1},
            {"name": "MBC 1",                "f": 11862, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "AL ARABIYA",           "f": 11919, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "ROTANA CINEMA",        "f": 11785, "sr": 27500, "pol": "V", "cat": 3},
            {"name": "SPACETOON",            "f": 11220, "sr": 27500, "pol": "H", "cat": 4},
        ],
    },

    # ── الجزائر ──────────────────────────────────────────
    "الجزائر / Algeria": {
        "satellite": "Hotbird 13°E",
        "channels": [
            {"name": "ALGERIE 1",            "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "ALGERIE 3",            "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "AL SHURUK TV",         "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "ENNAHAR TV",           "f": 11938, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "SAMIRA TV",            "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "BEUR TV",              "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "AL ARABIYA",           "f": 11919, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "MBC 1",                "f": 11862, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "ROTANA CINEMA",        "f": 11785, "sr": 27500, "pol": "V", "cat": 3},
            {"name": "SPACETOON",            "f": 11220, "sr": 27500, "pol": "H", "cat": 4},
            {"name": "AL RESALA",            "f": 11747, "sr": 27500, "pol": "H", "cat": 1},
        ],
    },

    # ── لبنان ──────────────────────────────────────────────
    "لبنان / Lebanon": {
        "satellite": "Nilesat 7°W",
        "channels": [
            {"name": "LBC",                  "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "LBC LAHKI",            "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "AL MANAR",             "f": 11938, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "NBN",                  "f": 11938, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "MTV LEBANON",          "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "OTV",                  "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "FUTURE TV",            "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "AL JADEED",            "f": 11938, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "SAT-7 ARABIC",         "f": 11353, "sr": 27500, "pol": "V", "cat": 0},
            {"name": "AL ARABIYA",           "f": 11919, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "MBC 1",                "f": 11862, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "ROTANA CINEMA",        "f": 11785, "sr": 27500, "pol": "V", "cat": 3},
            {"name": "SPACETOON",            "f": 11220, "sr": 27500, "pol": "H", "cat": 4},
        ],
    },

    # ── العراق ──────────────────────────────────────────
    "العراق / Iraq": {
        "satellite": "Nilesat 7°W",
        "channels": [
            {"name": "ALSUMARIA TV",         "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "AL RASHEED TV",        "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "DIJLAH TV",            "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "SHARQIYA",             "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "IRAQIA TV",            "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "KURDISTAN TV",         "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "AL ARABIYA",           "f": 11919, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "AL JAZEERA HD",        "f": 11938, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "MBC 1",                "f": 11862, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "MBC 2",                "f": 11862, "sr": 27500, "pol": "H", "cat": 3},
            {"name": "ROTANA CINEMA",        "f": 11785, "sr": 27500, "pol": "V", "cat": 3},
            {"name": "SPACETOON",            "f": 11220, "sr": 27500, "pol": "H", "cat": 4},
            {"name": "AL RESALA",            "f": 11747, "sr": 27500, "pol": "H", "cat": 1},
        ],
    },

    # ── سوريا ──────────────────────────────────────────────
    "سوريا / Syria": {
        "satellite": "Nilesat 7°W",
        "channels": [
            {"name": "SYRIA TV",             "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "ORIENT TV",            "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "SHAM FM",              "f": 11938, "sr": 27500, "pol": "V", "cat": 7},
            {"name": "SAMA TV",              "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "AL ARABIYA",           "f": 11919, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "MBC 1",                "f": 11862, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "MBC DRAMA",            "f": 11862, "sr": 27500, "pol": "H", "cat": 2},
            {"name": "ROTANA CINEMA",        "f": 11785, "sr": 27500, "pol": "V", "cat": 3},
            {"name": "SPACETOON",            "f": 11220, "sr": 27500, "pol": "H", "cat": 4},
            {"name": "SAT-7 ARABIC",         "f": 11353, "sr": 27500, "pol": "V", "cat": 0},
        ],
    },

    # ── ليبيا ──────────────────────────────────────────────
    "ليبيا / Libya": {
        "satellite": "Nilesat 7°W",
        "channels": [
            {"name": "AL LIBIYA TV",         "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "AL NABAA TV",          "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "LIBYA AL AHRAR",       "f": 11938, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "AL ARABIYA",           "f": 11919, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "MBC 1",                "f": 11862, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "ROTANA CINEMA",        "f": 11785, "sr": 27500, "pol": "V", "cat": 3},
            {"name": "SPACETOON",            "f": 11220, "sr": 27500, "pol": "H", "cat": 4},
            {"name": "AL RESALA",            "f": 11747, "sr": 27500, "pol": "H", "cat": 1},
        ],
    },

    # ── السودان ──────────────────────────────────────────
    "السودان / Sudan": {
        "satellite": "Nilesat 7°W",
        "channels": [
            {"name": "SUDAN TV",             "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "BLUE NILE TV",         "f": 11938, "sr": 27500, "pol": "V", "cat": 8},
            {"name": "AL ARABIYA",           "f": 11919, "sr": 27500, "pol": "V", "cat": 6},
            {"name": "MBC 1",                "f": 11862, "sr": 27500, "pol": "H", "cat": 8},
            {"name": "ROTANA CINEMA",        "f": 11785, "sr": 27500, "pol": "V", "cat": 3},
            {"name": "SPACETOON",            "f": 11220, "sr": 27500, "pol": "H", "cat": 4},
            {"name": "AL RESALA",            "f": 11747, "sr": 27500, "pol": "H", "cat": 1},
            {"name": "AGHAPY TV",            "f": 11179, "sr": 27500, "pol": "H", "cat": 0},
        ],
    },
}

# ══════════════════════════════════════════════════════════
#  LG TV MODELS
# ══════════════════════════════════════════════════════════
LG_MODELS = [
    "─── اختر موديل ───",
    # OLED
    "OLED55C1PVA", "OLED65C1PVA", "OLED77C1PVA",
    "OLED55C2PSA", "OLED65C2PSA", "OLED77C2PSA",
    "OLED55C3PSA", "OLED65C3PSA", "OLED55G3PSA",
    # NanoCell
    "65NANO86VPA", "55NANO86VPA", "75NANO86VPA",
    "65NANO91VPA", "55NANO91VPA",
    # UHD / 4K
    "65UP8050PSB", "55UP8050PSB", "75UP8050PSB",
    "65UQ80006LB", "55UQ80006LB", "75UQ80006LB",
    "65UR8050PSB", "55UR8050PSB",
    # Full HD
    "43LM6370PVA", "50LM6370PVA", "43LQ63006LA",
    "32LM6370PVA", "32LQ630BPSA",
    # Smart
    "55SM8600PVA", "65SM8600PVA",
    # Custom (يكتب المستخدم)
    "✏️ موديل مخصص / Custom Model",
]

# ══════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════
dark = st.session_state.theme == 'dark'
BG  = "radial-gradient(circle at 50% 50%,#110926 0%,#05020d 100%)" if dark else "radial-gradient(circle at 50%,#f4f5f7,#e4e7eb)"
TC  = "#00f0ff" if dark else "#0d0722"
BBG = "rgba(13,7,33,0.85)"              if dark else "#fff"
BBR = "#00f0ff"                          if dark else "#ff007f"
BSH = "rgba(0,240,255,.35)"             if dark else "rgba(255,0,127,.15)"
TSH = "0 0 5px rgba(0,240,255,.4)"      if dark else "none"
FF  = "'Cairo',sans-serif" if st.session_state.lang == 'ar' else "'Orbitron',sans-serif"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;900&family=Cairo:wght@400;700&display=swap');
.main{{background:{BG}!important;color:{TC}!important;font-family:{FF};}}
h1{{color:#ff007f!important;text-shadow:0 0 10px #ff007f,0 0 25px rgba(255,0,127,.4)!important;text-align:center;font-weight:900;margin-top:5px;}}
h3,p,label,.stMarkdown,div[data-testid="stMarkdownContainer"] p{{color:{TC}!important;text-shadow:{TSH};}}
.stTextInput>div>div>input,.stSelectbox>div>div{{background:{BBG}!important;color:{TC}!important;border:2px solid {BBR}!important;border-radius:10px!important;}}
.stCheckbox,.stMultiSelect,div[data-testid="stExpander"],div[data-testid="stFileUploader"]{{
  background:{BBG}!important;border:2px solid {BBR}!important;
  box-shadow:0 5px 15px {BSH}!important;border-radius:14px!important;padding:18px!important;margin-bottom:20px!important;}}
.stButton>button{{background:linear-gradient(135deg,#ff007f,#aa0055)!important;color:#fff!important;
  border:2px solid #ff007f!important;border-radius:12px!important;font-weight:bold;font-size:15px;}}
.info-box{{background:{BBG};border:2px solid {BBR};box-shadow:0 5px 15px {BSH};border-radius:14px;padding:18px;margin-bottom:18px;}}
.tip-box{{background:{BBG};border:2px solid #ff007f;box-shadow:0 5px 15px rgba(255,0,127,.25);border-radius:14px;padding:18px;margin-bottom:18px;}}
.chip{{display:inline-block;background:linear-gradient(135deg,#ff007f,#aa0055);color:#fff;padding:4px 14px;border-radius:20px;font-size:13px;margin:3px;font-weight:bold;}}
.chip-c{{background:linear-gradient(135deg,#00f0ff,#0080a0);}}
.ch-row{{background:rgba(0,240,255,.04);border-left:3px solid #ff007f;padding:7px 14px;margin:3px 0;border-radius:6px;font-size:13px;}}
.futuristic-cyber-footer{{background:#080314;border:2px solid #00f0ff;color:#fff!important;
  padding:35px;text-align:center;border-radius:20px;margin-top:65px;font-family:'Orbitron',sans-serif;}}
.footer-dev{{color:#ff007f;font-size:26px;font-weight:bold;}}
.cyber-whatsapp-btn{{color:#25d366!important;padding:14px 35px;border-radius:35px;
  display:inline-block;font-weight:bold;border:2px solid #25d366;text-decoration:none;margin-top:20px;}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  TOP BAR
# ══════════════════════════════════════════════════════════
c1, c2, _ = st.columns([1.2, 1.5, 8])
with c1:
    if st.button("🌐 English" if st.session_state.lang == 'ar' else "🌐 العربية"):
        st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
        st.rerun()
with c2:
    if st.button("☀️ Light" if dark else "🌙 Dark"):
        st.session_state.theme = 'light' if dark else 'dark'
        st.rerun()

st.title(t['title'])
st.markdown(f"<h3 style='text-align:center'>{t['subtitle']}</h3>", unsafe_allow_html=True)
st.write("---")

# ══════════════════════════════════════════════════════════
#  CONTROLS
# ══════════════════════════════════════════════════════════
col_country, col_model = st.columns(2)

with col_country:
    country_key = st.selectbox(t['country_lbl'], list(CHANNELS_DB.keys()))

with col_model:
    model_choice = st.selectbox(t['model_lbl'], LG_MODELS)
    if model_choice.startswith("✏️") or model_choice.startswith("─"):
        custom_model = st.text_input("", placeholder=t['model_ph'])
        tv_model = custom_model.strip() if custom_model.strip() else "LG-TV"
    else:
        tv_model = model_choice

# ── Auto-detected satellite ──
sat_name   = CHANNELS_DB[country_key]["satellite"]
ch_data    = CHANNELS_DB[country_key]["channels"]

st.markdown(
    f'<div class="info-box">'
    f'<span class="chip chip-c">📡 {t["sat_detected"]} <b>{sat_name}</b></span>'
    f'&nbsp;&nbsp;'
    f'<span class="chip">📺 {t["total_ch"]} <b>{len(ch_data)}</b> {t["channels"]}</span>'
    f'&nbsp;&nbsp;'
    f'<span class="chip chip-c">🖥️ {tv_model}</span>'
    f'</div>',
    unsafe_allow_html=True,
)

# ── LG Tip ──
st.markdown(f"""
<div class="tip-box">
  <h4 style="color:#ff007f;margin-top:0;">{t['lg_tip_title']}</h4>
  <p style="white-space:pre-line;margin-bottom:0;font-size:14px;">{t['lg_tip_text']}</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  CATEGORY SORT
# ══════════════════════════════════════════════════════════
st.write("---")
st.write(f"### {t['sort_title']}")
st.caption(t['sort_tip'])
user_order = st.multiselect(t['sort_lbl'], options=CATS, default=[])

priority = list(user_order)
for c in CATS:
    if c not in priority:
        priority.append(c)

# ══════════════════════════════════════════════════════════
#  SORT CHANNELS
# ══════════════════════════════════════════════════════════
channels_sorted = sorted(ch_data, key=lambda x: priority.index(CATS[x["cat"]]))

# ══════════════════════════════════════════════════════════
#  LIVE PREVIEW
# ══════════════════════════════════════════════════════════
st.write("---")
st.write(f"### {t['preview']}")

cat_map: dict[str, list] = {}
for ch in channels_sorted:
    cat_label = CATS[ch["cat"]]
    cat_map.setdefault(cat_label, []).append(ch["name"])

col_a, col_b = st.columns(2)
for i, cat in enumerate(priority):
    if cat not in cat_map:
        continue
    names = cat_map[cat]
    star  = "⭐ " if cat in user_order else ""
    with (col_a if i % 2 == 0 else col_b):
        with st.expander(f"{star}{cat}  —  ({len(names)} {t['channels']})"):
            for name in names:
                st.markdown(f'<div class="ch-row">📺 {name}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  BUILD TLL
# ══════════════════════════════════════════════════════════
def build_tll(channels: list, model: str, sat: str, country: str) -> bytes:
    ch_list = []
    for idx, ch in enumerate(channels, 1):
        ch_list.append({
            "majorNumber":  idx,
            "channelName":  ch["name"],
            "frequency":    ch["f"],
            "symbolRate":   str(ch["sr"]),
            "polarization": "Horizontal" if ch["pol"] == "H" else "Vertical",
            "serviceType":  "1",
            "scrambled":    "false",
            "satellite":    sat,
        })
    bd_json  = json.dumps({"channelList": ch_list}, ensure_ascii=False)
    now      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    xml_str  = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<LGSmartTVDatabase>\n'
        '  <TVSetup>\n'
        f'    <ModelName>{model}</ModelName>\n'
        f'    <Country>{country}</Country>\n'
        f'    <Satellite>{sat}</Satellite>\n'
        f'    <GeneratedBy>RAMBO AI Channel Generator</GeneratedBy>\n'
        f'    <GenerationDate>{now}</GenerationDate>\n'
        '  </TVSetup>\n'
        f'  <legacybroadcast>{bd_json}</legacybroadcast>\n'
        '</LGSmartTVDatabase>'
    )
    return xml_str.encode("utf-8")

def build_txt(channels: list, model: str, sat: str, country: str) -> str:
    lines = [
        "=" * 65,
        "  RAMBO – Channel File Generator",
        f"  Country   : {country}",
        f"  Satellite : {sat}",
        f"  TV Model  : {model}",
        f"  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"  Total     : {len(channels)} channels",
        "=" * 65,
        "",
        f"{'No.':<5} {'Channel Name':<30} {'Freq':>7}  Pol  Category",
        "-" * 65,
    ]
    for idx, ch in enumerate(channels, 1):
        lines.append(
            f"{idx:<5} {ch['name']:<30} {ch['f']:>7}  "
            f"{'H' if ch['pol']=='H' else 'V'}    {CATS[ch['cat']]}"
        )
    return "\n".join(lines)

# ══════════════════════════════════════════════════════════
#  GENERATE BUTTON
# ══════════════════════════════════════════════════════════
st.write("---")
if st.button(t['gen_btn'], use_container_width=True):
    tll_bytes  = build_tll(channels_sorted, tv_model, sat_name, country_key)
    txt_report = build_txt(channels_sorted, tv_model, sat_name, country_key)

    st.success(t['ready'])

    db1, db2 = st.columns(2)
    with db1:
        st.download_button(
            label=t['dl_tll'],
            data=tll_bytes,
            file_name="GlobalClone00001.TLL",
            mime="application/octet-stream",
            use_container_width=True,
        )
    with db2:
        st.download_button(
            label=t['dl_txt'],
            data=txt_report,
            file_name="Channels_List.txt",
            mime="text/plain; charset=utf-8",
            use_container_width=True,
        )

# ══════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════
wa = "https://api.whatsapp.com/send?phone=201280339779&text=Hello%20Developer%20Rafik%20Rambo"
st.markdown(f"""
<div class="futuristic-cyber-footer">
  <div class="footer-dev">🛠️ DEVELOPER ENG: RAFIK NATHAN</div>
  <div style="margin-top:8px;">📱 <b>MOBILE:</b> +201280339779 &nbsp;|&nbsp; ✉️ <b>E-MAIL:</b> rafikrambo113@gmail.com</div>
  <a href="{wa}" target="_blank" class="cyber-whatsapp-btn">💬 WhatsApp</a>
</div>
""", unsafe_allow_html=True)
