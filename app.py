import streamlit as st
import xml.etree.ElementTree as ET
import json
import re
import os

# 1. تهيئة الحالات الافتراضية للغة والثيم
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# قاموس اللغتين لترجمة واجهة المستخدم السيبرانية بالكامل
UI_TEXT = {
    'ar': {
        'title': "📺 RAMBO ULTRA - المنصة العالمية الذكية لشاشات LG",
        'subtitle': "⚡ الذاكرة الأبدية الحية: محرك AI يتعلم ويحفظ التحديثات في الخلفية مدى الحياة",
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
        'search_header': "🔍 محرك البحث والتدقيق الذكي داخل باقات الـ AI:",
        'search_placeholder': "اكتب اسم القناة هنا لفحص فئتها وترددها...",
        'search_col_num': "الرقم الحالي",
        'search_col_name': "اسم القناة",
        'search_col_cat': "الفئة الدقيقة (Category)",
        'search_col_freq': "التردد النشط 2026",
        'search_no_results': "⚠️ لم يتم العثور على أي قنوات مطابقة.",
        'config_title': "🎛️ مصفوفة ترتيب الفئات المخصصة حسب اختيارك اليدوي:",
        'config_tip': "💡 ملحوظة: اضغط على الفئات بالترتيب الفعلي المفضل لديك. الفئة التي تختارها أولاً ستتصدر شاشة التلفزيون.",
        'multiselect_label': "اضغط هنا لبناء تسلسل خطة العرض التفاعلي للفئات:",
        'preview_title': "📊 مجسم المعاينة الحية لتوزيع القنوات الحالي:",
        'channels_count': "قناة نقيّة",
        'ready_msg': "🌌 تم دمج مصفوفة RAMBO وتطهير البيانات بنجاح! الملفات جاهزة للتحميل:",
        'btn_download_tll': "📥 تحميل ملف الشاشة المحدث والمنظم (GlobalClone00001.TLL)",
        'btn_download_txt': "📄 تحميل تقرير الترتيب والترددات (Channels_List.txt)",
        'txt_header': "📄 تقرير الترتيب النهائي الفائق النقاء لشاشة LG",
        'txt_order': "🛠️ ترتيب الفئات المختار: ",
        'lg_trick_title': "💡 ملحوظة فنية هامة جداً بعد تنزيل الملف على شاشة LG:",
        'lg_trick_text': "في بعض الحالات، بعد تنزيل ملف القنوات على الشاشة، قد تشعر أن القنوات ليست منظمة كما رتبتها. لحل هذا الأمر فوراً واجبار الشاشة على تفعيل الترتيب الصحيح، قم بالآتي:\n1. من إعدادات التلفزيون اختار **القنوات (Channels)**.\n2. بعد ذلك اختار **مدير القنوات (Channel Manager)**.\n3. اختار **التعديل على كل القنوات (Edit All Channels)**.\n4. ستظهر لك القنوات المرتبة ويكون بعضها في وضع مخفي، قم **بتحديد كل القنوات** واختار **استعادة (Restore)**.\n*ملحوظة: تفعل هذه الخطوة فقط إذا شعرت أن الملف بعد التنزيل غير مرتب كما حددته على الموقع.*"
    },
    'en': {
        'title': "📺 RAMBO ULTRA - LG Universal Live-AI Platform",
        'subtitle': "⚡ Persistent Background Memory: AI Learning & Saving Real-Time Frequency Changes Forever",
        'mode_selector': "🛠️ Select Desired Operations Mode:",
        'mode_edit': "🛸 Edit/Optimize USB File (Cleanse & Feed AI)",
        'mode_gen': "⚛️ Generate Brand New Raw .TLL (Evolved from Persistent AI Memory)",
        'model_label': "📺 Select Target LG TV Model Type:",
        'model_modern': "Smart webOS (Modern Smart Models)",
        'model_legacy': "Legacy / 32 Inch (Classic & 32\" Screen Profile)",
        'country_label': "🌍 Select Broadcast Country Profile:",
        'country_egy': "Egypt — North Africa Grouping [NAFR]",
        'country_ksa': "Saudi Arabia (KSA) — Middle East Grouping [MIDE]",
        'btn_generate': "🚀 Fire Matrix Generation Engine",
        'upload_label': "🚀 Upload Channel File (GlobalClone00001.TLL) to Cleanse and Sort:",
        'update_freq_label': "⚛️ Enforce Official Live Frequencies (Wipe Dead Frequencies)",
        'add_new_ch_label': "✨ Absorb New Channels and Save to Site Persistent Memory",
        'success_read': "🛸 Matrix Structure Decoded Successfully! Model Profile: ",
        'success_gen': "🌌 Created brand new ultra-pure LG channel structure for: ",
        'search_header': "🔍 Dynamic Channel & AI Category Inspection Engine:",
        'search_placeholder': "Type channel name to inspect...",
        'search_col_num': "No.",
        'search_col_name': "Channel Name",
        'search_col_cat': "Precise Category",
        'search_col_freq': "Active Freq",
        'search_no_results': "⚠️ No verified channels found matching criteria.",
        'config_title': "🎛️ Custom Category Priority Control Matrix:",
        'config_tip': "💡 Hint: Click categories in exact order. The first selection populates the absolute top of your TV.",
        'multiselect_label': "Select categories one by one to configure your linear priority:",
        'preview_title': "📊 Channel Grid Live 3D Preview Dashboard:",
        'channels_count': "Pure Channels",
        'ready_msg': "🌌 Quantum Matrix Cleansing Successful! Assets ready for transfer:",
        'btn_download_tll': "📥 Download Verified TV Configuration (GlobalClone00001.TLL)",
        'btn_download_txt': "📄 Download Sorting Text Diagnostics (Channels_List.txt)",
        'txt_header': "📄 Final Clean LG TV Channel Sorting Report",
        'txt_order': "🛠️ Selected Category Priority: "
    }
}

t = UI_TEXT[st.session_state.lang]

st.set_page_config(page_title="RAMBO ULTRA - Brain AI Sorter", page_icon="⚡", layout="wide")

# التحكم في اللغة والثيمات
col_lang, col_theme, _ = st.columns([1.2, 1.5, 8])
with col_lang:
    if st.button("🌐 English" if st.session_state.lang == 'ar' else "🌐 العربية"):
        st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
        st.rerun()
with col_theme:
    if st.button("☀️ Light Mode" if st.session_state.theme == 'dark' else "🌙 Dark Mode"):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

# الـ CSS السيبراني الفخم
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
    .stCheckbox, .stMultiSelect, div[data-testid="stExpander"], div[data-testid="stFileUploader"], .lg-trick-box, .cyber-sidebar-box {{ background: {box_bg} !important; border: 2px solid {box_border} !important; box-shadow: 0px 5px 15px {box_shadow} !important; border-radius: 14px !important; padding: 18px !important; margin-bottom: 20px !important; }}
    .lg-trick-box {{ border-color: #ff007f !important; box-shadow: 0px 5px 15px rgba(255, 0, 127, 0.25) !important; }}
    .stButton>button {{ background: linear-gradient(135deg, #ff007f 0%, #aa0055 100%) !important; color: #ffffff !important; border: 2px solid #ff007f !important; border-radius: 12px !important; font-weight: bold; width: 100%; }}
    .futuristic-cyber-footer {{ background: {footer_bg}; border: 2px solid #00f0ff; color: {footer_text} !important; padding: 35px; text-align: center; border-radius: 20px; margin-top: 65px; font-family: 'Orbitron', sans-serif; }}
    .footer-dev {{ color: #ff007f; font-size: 26px; font-weight: bold; }}
    .cyber-whatsapp-btn {{ color: #25d366 !important; padding: 14px 35px; border-radius: 35px; display: inline-block; font-weight: bold; border: 2px solid #25d366; text-decoration: none; margin-top: 20px; }}
    </style>
""", unsafe_allow_html=True)

st.title(t['title'])
st.markdown(f"<h3>{t['subtitle']}</h3>", unsafe_allow_html=True)

# 💾 المستودع المرجعي الأساسي الصلب والانطلاقة لعام 2026
def get_base_2026_db():
    return {
        "ALHAYAT TV": {"frequency": 11392, "polarization": "Vertical"},
        "THE LIFE TV": {"frequency": 11392, "polarization": "Vertical"},
        "AL SHIFA TV": {"frequency": 11392, "polarization": "Vertical"},
        "AL MALAKOOT": {"frequency": 11392, "polarization": "Vertical"},
        "AL MOFADY TV": {"frequency": 11392, "polarization": "Vertical"},
        "CTV HD": {"frequency": 12022, "polarization": "Vertical"},
        "AGHAPY TV": {"frequency": 11179, "polarization": "Vertical"},
        "ME SAT HD": {"frequency": 11179, "polarization": "Vertical"},
        "MARMARKOS": {"frequency": 11137, "polarization": "Vertical"},
        "KOOGI TV": {"frequency": 11096, "polarization": "Vertical"},
        "SAT-7 KIDS": {"frequency": 11353, "polarization": "Vertical"},
        "SAT-7 ARABIC": {"frequency": 11353, "polarization": "Vertical"},
        "ALKARMA ME 1": {"frequency": 11096, "polarization": "Vertical"},
        "ALKARMA FE": {"frequency": 11096, "polarization": "Vertical"},
        "NOURSAT HD": {"frequency": 11179, "polarization": "Vertical"},
        "CYC TV": {"frequency": 11137, "polarization": "Vertical"},
        "LOGO TV": {"frequency": 11096, "polarization": "Vertical"},
        "SAMA TV": {"frequency": 11179, "polarization": "Vertical"},
        "BETHEL TV": {"frequency": 11137, "polarization": "Vertical"},
        "HEAVEN TV": {"frequency": 11179, "polarization": "Vertical"},
        "HOPE TV ARABIC": {"frequency": 11353, "polarization": "Vertical"},
        "MIRACLE TV": {"frequency": 11096, "polarization": "Vertical"},
        "HOLY TV": {"frequency": 11137, "polarization": "Vertical"},
        "GOOD NEWS TV": {"frequency": 12022, "polarization": "Vertical"},
        "LIGHT TV": {"frequency": 11179, "polarization": "Vertical"},
        "TRUTH TV": {"frequency": 11353, "polarization": "Vertical"},
        "SAUDI QURAN HD": {"frequency": 12149, "polarization": "Horizontal"},
        "AL MAJD QURAN": {"frequency": 12054, "polarization": "Horizontal"},
        "AL MAJD HADITH": {"frequency": 12054, "polarization": "Horizontal"},
        "AL MAJD SPACE": {"frequency": 11900, "polarization": "Horizontal"},
        "EGYPT QURAN": {"frequency": 11179, "polarization": "Vertical"},
        "AL SUNNAH HD": {"frequency": 12149, "polarization": "Horizontal"},
        "AL RAHMA TV": {"frequency": 10873, "polarization": "Vertical"},
        "ALAFASY TV": {"frequency": 10727, "polarization": "Horizontal"},
        "MEKKA TV": {"frequency": 12399, "polarization": "Vertical"},
        "MEDINA TV": {"frequency": 12149, "polarization": "Horizontal"},
        "ZAD TV": {"frequency": 12226, "polarization": "Horizontal"},
        "AL INSAAN": {"frequency": 11658, "polarization": "Vertical"},
        "DAWAH TV": {"frequency": 10758, "polarization": "Horizontal"},
        "SHAREQAH QURAN": {"frequency": 11012, "polarization": "Horizontal"},
        "IQRAA HD": {"frequency": 12034, "polarization": "Horizontal"},
        "RISALAH TV": {"frequency": 11296, "polarization": "Horizontal"},
        "AL NAS TV": {"frequency": 12054, "polarization": "Horizontal"},
        "MBC DRAMA HD": {"frequency": 11938, "polarization": "Vertical"},
        "DMC DRAMA": {"frequency": 12092, "polarization": "Vertical"},
        "CBC DRAMA": {"frequency": 11785, "polarization": "Vertical"},
        "ON DRAMA": {"frequency": 11861, "polarization": "Vertical"},
        "AL HAYAT DRAMA": {"frequency": 12207, "polarization": "Vertical"},
        "AL NAHAR DRAMA": {"frequency": 11785, "polarization": "Vertical"},
        "SADA EL BALAD DRAMA": {"frequency": 11823, "polarization": "Vertical"},
        "PANORAMA DRAMA": {"frequency": 12341, "polarization": "Horizontal"},
        "ZEE ALWAN HD": {"frequency": 11277, "polarization": "Horizontal"},
        "MIX DRAMA": {"frequency": 11843, "polarization": "Horizontal"},
        "TIME DRAMA": {"frequency": 11179, "polarization": "Vertical"},
        "NILE DRAMA": {"frequency": 11843, "polarization": "Horizontal"},
        "MBC 2 HD": {"frequency": 11938, "polarization": "Vertical"},
        "MBC ACTION HD": {"frequency": 11938, "polarization": "Vertical"},
        "MBC MAX HD": {"frequency": 11938, "polarization": "Vertical"},
        "ROTANA CINEMA HD": {"frequency": 12226, "polarization": "Horizontal"},
        "ROTANA CLASSIC": {"frequency": 12226, "polarization": "Horizontal"},
        "ROTANA COMEDY": {"frequency": 12226, "polarization": "Horizontal"},
        "MIX ONE HD": {"frequency": 11843, "polarization": "Horizontal"},
        "MIX MOVIES HD": {"frequency": 11843, "polarization": "Horizontal"},
        "SCARE TV": {"frequency": 10873, "polarization": "Vertical"},
        "TOP MOVIES": {"frequency": 10873, "polarization": "Vertical"},
        "ART AFLAM 1": {"frequency": 12034, "polarization": "Horizontal"},
        "ART AFLAM 2": {"frequency": 12034, "polarization": "Horizontal"},
        "FOX MOVIES": {"frequency": 11296, "polarization": "Horizontal"},
        "SPACE TOON HD": {"frequency": 11785, "polarization": "Vertical"},
        "CN ARABIA HD": {"frequency": 12226, "polarization": "Horizontal"},
        "MAJID KIDS HD": {"frequency": 11411, "polarization": "Horizontal"},
        "TOM AND JERRY TV": {"frequency": 11353, "polarization": "Vertical"},
        "MBC 3 HD": {"frequency": 11938, "polarization": "Vertical"},
        "KARAMEESH": {"frequency": 11430, "polarization": "Vertical"},
        "TOYOR AL JANNAH": {"frequency": 11315, "polarization": "Vertical"},
        "BATUT TV": {"frequency": 11595, "polarization": "Vertical"},
        "SPONGEBOB TV": {"frequency": 11353, "polarization": "Vertical"},
        "ON TIME SPORTS 1 HD": {"frequency": 11861, "polarization": "Vertical"},
        "ON TIME SPORTS 2 HD": {"frequency": 11861, "polarization": "Vertical"},
        "ON TIME SPORTS 3 HD": {"frequency": 11861, "polarization": "Vertical"},
        "AD SPORTS 1 HD": {"frequency": 11411, "polarization": "Horizontal"},
        "BEIN SPORTS NEWS HD": {"frequency": 11054, "polarization": "Horizontal"},
        "SSC NEWS HD": {"frequency": 12418, "polarization": "Horizontal"},
        "AL AHLY TV HD": {"frequency": 11747, "polarization": "Vertical"},
        "ZAMALEK TV HD": {"frequency": 11449, "polarization": "Vertical"},
        "AL JAZEERA HD": {"frequency": 10971, "polarization": "Vertical"},
        "AL ARABIYA HD": {"frequency": 12169, "polarization": "Vertical"},
        "AL HADATH HD": {"frequency": 12169, "polarization": "Vertical"},
        "CAIRO NEWS HD": {"frequency": 11747, "polarization": "Vertical"},
        "SKY NEWS ARABIA HD": {"frequency": 11977, "polarization": "Vertical"},
        "EXTRA NEWS HD": {"frequency": 11747, "polarization": "Vertical"},
        "AL HAYAT HD": {"frequency": 12207, "polarization": "Vertical"},
        "MBC MASR HD": {"frequency": 12015, "polarization": "Vertical"},
        "MBC MASR 2 HD": {"frequency": 11823, "polarization": "Vertical"},
        "ON E HD": {"frequency": 11861, "polarization": "Vertical"},
        "DMC HD": {"frequency": 12092, "polarization": "Vertical"},
        "CBC HD": {"frequency": 11785, "polarization": "Vertical"},
        "AL NAHAR HD": {"frequency": 11785, "polarization": "Vertical"},
        "SADA EL BALAD HD": {"frequency": 11823, "polarization": "Vertical"},
        "WANNASAH HD": {"frequency": 11938, "polarization": "Vertical"}
    }

# 🧠 نظام الذاكرة الأبدية (Persistent JSON Engine) لحفظ الداتا على السيرفر في الخلفية
BRAIN_FILE = "ai_brain_db.json"

def load_persistent_brain():
    base_db = get_base_2026_db()
    if os.path.exists(BRAIN_FILE):
        try:
            with open(BRAIN_FILE, "r", encoding="utf-8") as f:
                saved_db = json.load(f)
                # دمج الملف المحفوظ مع القائمة الأساسية لمنع الضياع
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

# تحميل بنك البيانات المتراكم والمحفوظ مدى الحياة في الخلفية
MASTER_2026_DB = load_persistent_brain()

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
    if any(w in name for w in ["CTV", "AGHAPY", "ME SAT", "MESAT", "MARMARKOS", "KOOGI", "SAT-7", "SAT7", "KARMA", "NOURSAT", "CYC", "LOGO TV", "SAMA", "MALAKOOT", "SHIFA", "BETHEL", "HEAVEN", "HOPE", "MIRACLE", "HOLY", "GOOD NEWS", "LIGHT TV", "TRUTH", "HAYAT TV", "LIFE TV", "MOFADY"]): 
        return ALL_AVAILABLE_CATEGORIES[0]
    if any(w in name for w in ["QURAN", "RAHMA", "MAJD", "MAKKA", "SUNNA", "NAS TV", "ZAD", "ISLAM", "AFASY", "MEDINA", "IQRA", "IQRAA", "RISALAH", "NAS", "FATH", "DAWAH", "INSAAN", "SHAREQAH"]): 
        return ALL_AVAILABLE_CATEGORIES[1]
    if any(w in name for w in ["MOSALSALAT", "DRAMA", "SERIES", "KHOLASA", "HEKAYAT", "ALWAN", "DOCH", "TIME DR", "NILE DRAMA"]): 
        return ALL_AVAILABLE_CATEGORIES[2]
    if any(w in name for w in ["CINEMA", "ROTANA", "AFLAM", "MIX", "FOX", "MBC2", "MBC 2", "ACTION", "RAMBO", "MISHMISH", "MOVIE", "MAX", "SCARE", "CIMA", "TOP MOV", "B4U MO", "SCIFI", "BLUE", "MELODY", "TOKTOK"]): 
        return ALL_AVAILABLE_CATEGORIES[3]
    if any(w in name for w in ["SPACE TOON", "SPACETOON", "CN", "MAJID", "KIDS", "TOM", "JERRY", "MODY", "CARTOON", "BOOMERANG", "BABY", "KARAMEESH", "TOYOR", "COCO", "BATUT", "SPONGEBOB"]): 
        return ALL_AVAILABLE_CATEGORIES[4]
    if any(w in name for w in ["SPORT", "ONTIME", "KASS", "AD_SPORTS", "AD SPORTS", "SSC", "RIYADIYA", "YALLA", "SHOOT", "BEIN", "AHLY", "ZAMALEK"]): 
        return ALL_AVAILABLE_CATEGORIES[5]
    if any(w in name for w in ["NEWS", "JAZEERA", "ARABIYA", "HADATH", "CAIRO", "EXTRA", "SKY", "AKHBAR", "RT AR", "MAYADEEN", "ASHARQ", "CNBC"]): 
        return ALL_AVAILABLE_CATEGORIES[6]
    return ALL_AVAILABLE_CATEGORIES[7]

st.sidebar.markdown(f"### {t['mode_selector']}")
app_mode = st.sidebar.radio("", [t['mode_edit'], t['mode_gen']])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧠 الذاكرة الدائمة المحفوظة بالسيرفر:")
st.sidebar.info(f"📊 حجم بنك القنوات الأبدي المتراكم حالياً: **{len(MASTER_2026_DB)} قناة** نشطة ومحمية من الضياع في الخلفية.")

file_processed = False
file_bytes_out = b""
text_report_out = ""
unique_channels_map = {}
report_changes = []
injected_report = []
model_name_display = ""
database_needs_save = False # راية برمجية لمعرفة هل تم رصد قنوات جديدة لحفظها فوراً

# --- 🟢 الوضع الأول: تعديل ملف العميل + امتصاص وتحديث الذاكرة الأبدية في الخلفية ---
if app_mode == t['mode_edit']:
    uploaded_file = st.file_uploader(t['upload_label'], type=["TLL"])
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        try: file_text_original = file_bytes.decode('utf-8')
        except UnicodeDecodeError: file_text_original = file_bytes.decode('latin-1')

        root = ET.fromstring(file_bytes)
        model_setting = root.find(".//ModelName")
        model_name_display = model_setting.text if model_setting is not None else "LG-TV"
        legacy_broadcast_tag = root.find(".//legacybroadcast")
        is_modern = legacy_broadcast_tag is not None and legacy_broadcast_tag.text
        
        st.info(f"{t['success_read']} **{model_name_display}**")
        
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1: enforce_2026 = st.checkbox(t['update_freq_label'], value=True)
        with col_opt2: inject_exclusive = st.checkbox(t['add_new_ch_label'], value=True)

        if is_modern:
            broadcast_data = json.loads(legacy_broadcast_tag.text)
            uploaded_list = broadcast_data.get("channelList", [])
            
            # الـ AI يفحص الملف المرفوع ويمتص أحدث الترددات والقنوات الجديدة لحفظها أبدياً
            for c in uploaded_list:
                name_up = c.get("channelName", "").strip().upper()
                freq_up = c.get("frequency", 0)
                pol_up = c.get("polarization", "Horizontal")
                if name_up and freq_up > 0:
                    # لو لقى قناة جديدة تماماً مش في الماستر، أو قناة قديمة بس نازلة بتردد أحدث وأنقى، يحفظها في الخلفية فوراً
                    if name_up not in MASTER_2026_DB or MASTER_2026_DB[name_up]["frequency"] != int(freq_up):
                        MASTER_2026_DB[name_up] = {"frequency": int(freq_up), "polarization": pol_up}
                        database_needs_save = True

            # تصفية وفك تكرار القنوات المعروضة للمستخدم حالياً بناءً على الذاكرة المحدثة
            for idx, ch in enumerate(uploaded_list):
                ch_name = ch.get("channelName", "").strip()
                ch_name_upper = ch_name.upper()
                if not ch_name_upper: continue
                
                old_freq = str(ch.get("frequency", "0"))
                
                if enforce_2026 and ch_name_upper in MASTER_2026_DB:
                    verified_freq = MASTER_2026_DB[ch_name_upper]["frequency"]
                    if old_freq != str(verified_freq):
                        report_changes.append({"القناة": ch_name, "التصنيف": ai_classify(ch_name), "التردد الملغي (قديم)": f"{old_freq} MHz", "التردد الحقيقي النشط": f"{verified_freq} MHz", "القرار": "تحديث فوري وقسري"})
                        ch["frequency"] = int(verified_freq)
                        ch["polarization"] = MASTER_2026_DB[ch_name_upper]["polarization"]
                        old_freq = str(verified_freq)
                
                if ch_name_upper not in unique_channels_map:
                    unique_channels_map[ch_name_upper] = {"id": idx, "name": ch_name, "freq": old_freq, "raw_node": ch}
                else:
                    unique_channels_map[ch_name_upper]["freq"] = old_freq
                    unique_channels_map[ch_name_upper]["raw_node"] = ch

            if inject_exclusive:
                for ch_name_master, data_master in MASTER_2026_DB.items():
                    if ch_name_master not in unique_channels_map:
                        new_node = {"channelName": ch_name_master, "frequency": data_master["frequency"], "polarization": data_master["polarization"], "majorNumber": 0, "serviceType": "1", "scrambled": "false", "symbolRate": "27500"}
                        unique_channels_map[ch_name_master] = {"id": len(unique_channels_map), "name": ch_name_master, "freq": str(data_master["frequency"]), "raw_node": new_node}
                        injected_report.append({"اسم القناة": ch_name_master, "التردد المعتمد": f"{data_master['frequency']} MHz", "التصنيف الدكي": ai_classify(ch_name_master), "الوضعية": "زرع من الذاكرة الأبدية"})

        else:
            # معالجة ملفات الأجهزة الكلاسيكية بنفس القوة والذكاء وحفظ الجديد في الخلفية
            item_blocks = re.findall(r'(<ITEM>.*?</ITEM>)', file_text_original, re.DOTALL)
            for item_str in item_blocks:
                name_match = re.search(r'<vchName>(.*?)</vchName>', item_str)
                freq_match = re.search(r'<frequency>(.*?)</frequency>', item_str)
                if name_match and freq_match:
                    name_up = name_match.group(1).strip().upper()
                    freq_up = freq_match.group(1).strip()
                    if name_up and freq_up.isdigit():
                        if name_up not in MASTER_2026_DB or MASTER_2026_DB[name_up]["frequency"] != int(freq_up):
                            MASTER_2026_DB[name_up] = {"frequency": int(freq_up), "polarization": "Vertical" if int(freq_up) in [11392, 12207, 11785] else "Horizontal"}
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
                    if old_freq != str(verified_freq):
                        report_changes.append({"القناة": ch_name, "التصنيف": ai_classify(ch_name), "التردد الملغي (قديم)": f"{old_freq} MHz", "التردد الحقيقي النشط": f"{verified_freq} MHz", "القرار": "تحديث فوري وقسري"})
                        item_str = re.sub(r'<frequency>\d+</frequency>', f'<frequency>{verified_freq}</frequency>', item_str)
                        old_freq = str(verified_freq)
                
                if ch_name_upper not in unique_channels_map:
                    unique_channels_map[ch_name_upper] = {"id": idx, "name": ch_name, "freq": old_freq, "raw_str": item_str}
            
            if inject_exclusive:
                for ch_name_master, data_master in MASTER_2026_DB.items():
                    if ch_name_master not in unique_channels_map:
                        new_item_raw = f"<ITEM>\r\n<prNum>0</prNum>\r\n<vchName>{ch_name_master}</vchName>\r\n<frequency>{data_master['frequency']}</frequency>\r\n<serviceType>1</serviceType>\r\n</ITEM>"
                        unique_channels_map[ch_name_master] = {"id": len(unique_channels_map), "name": ch_name_master, "freq": str(data_master["frequency"]), "raw_str": new_item_raw}
                        injected_report.append({"اسم القناة": ch_name_master, "التردد المعتمد": f"{data_master['frequency']} MHz", "التصنيف الدكي": ai_classify(ch_name_master), "الوضعية": "زرع من الذاكرة الأبدية"})

        # 🔥 الأمر العبقري: الحفظ الفوري في الخلفية على السيرفر للمستقبل من غير ما الموقع يصفر
        if database_needs_save:
            save_persistent_brain(MASTER_2026_DB)
            st.toast("💾 تم دمج وحفظ الترددات الجديدة أبدياً في ملف السيرفر الخلفي بنجاح!", icon="🧠")

        file_processed = True

# --- 🔵 الوضع الثاني: توليد ملف فائق النقاء معتمد كلياً على التحديث المتراكم في الخلفية ---
else:
    st.markdown(f'<div class="cyber-sidebar-box">', unsafe_allow_html=True)
    gen_model = st.selectbox(t['model_label'], [t['model_modern'], t['model_legacy']])
    gen_country = st.selectbox(t['country_label'], [t['country_egy'], t['country_ksa']])
    fire_gen = st.button(t['btn_generate'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    if fire_gen or 'generated_active' in st.session_state:
        st.session_state.generated_active = True
        is_modern = (gen_model == t['model_modern'])
        model_name_display = "LG-webOS-2026-PERSIST-GEN" if is_modern else "LG-Legacy-32-PERSIST-GEN"
        country_code = "EG" if gen_country == t['country_egy'] else "SA"
        country_group = "NAFR" if gen_country == t['country_egy'] else "MIDE"
        
        st.success(f"{t['success_gen']} **{gen_country}** ({model_name_display})")
        
        idx = 0
        for ch_name, data in MASTER_2026_DB.items():
            if is_modern:
                node = {"channelName": ch_name, "frequency": data["frequency"], "polarization": data["polarization"], "majorNumber": 0, "serviceType": "1", "scrambled": "false", "symbolRate": "27500"}
                unique_channels_map[ch_name] = {"id": idx, "name": ch_name, "freq": str(data["frequency"]), "raw_node": node}
            else:
                item_str = f"<ITEM>\r\n<prNum>0</prNum>\r\n<vchName>{ch_name}</vchName>\r\n<frequency>{data['frequency']}</frequency>\r\n<serviceType>1</serviceType>\r\n</ITEM>"
                unique_channels_map[ch_name] = {"id": idx, "name": ch_name, "freq": str(data["frequency"]), "raw_str": item_str}
            idx += 1
        file_processed = True

# --- 🚀 خط المعالجة الذكي، التصفية الميكانيكية، والترتيب ---
if file_processed:
    st.markdown(f"""
        <div class="lg-trick-box">
            <h4 style="color: #ff007f; margin-top:0;">{t['lg_trick_title']}</h4>
            <p style="white-space: pre-line; margin-bottom:0; font-size:14px;">{t['lg_trick_text']}</p>
        </div>
    """, unsafe_allow_html=True)

    cleaned_channels_list = list(unique_channels_map.values())

    st.write("---")
    st.write(f"### {t['config_title']}")
    user_priority = st.multiselect(t['multiselect_label'], options=ALL_AVAILABLE_CATEGORIES, default=[])
    final_priority = list(user_priority)
    for cat in ALL_AVAILABLE_CATEGORIES:
        if cat not in final_priority: final_priority.append(cat)

    channels_sorted = sorted(cleaned_channels_list, key=lambda x: final_priority.index(ai_classify(x["name"])))
    
    st.write("---")
    st.write(f"### {t['search_header']}")
    search_query = st.text_input("", placeholder=t['search_placeholder']).strip().upper()
    if search_query:
        search_results = []
        for idx, ch in enumerate(channels_sorted, start=1):
            if search_query in ch["name"].upper(): 
                search_results.append({t['search_col_num']: idx, t['search_col_name']: ch["name"], t['search_col_cat']: ai_classify(ch["name"]), t['search_col_freq']: ch["freq"]})
        if search_results: st.table(search_results)
        else: st.warning(t['search_no_results'])

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

    if app_mode == t['mode_edit'] and report_changes:
        st.write("### 🔁 تقرير تطهير الترددات الميتة وإبادة البيانات القديمة:")
        st.table(report_changes)
    if app_mode == t['mode_edit'] and injected_report:
        st.write("### 🆕 تقرير القنوات الحصرية المستدعاة من الذاكرة الحية الدائمة للموقع:")
        st.table(injected_report)

    # بناء ملف الـ TLL النهائي للتحميل
    if is_modern:
        final_list_modern = []
        for index, ch in enumerate(channels_sorted, start=1):
            node = ch["raw_node"]
            node["majorNumber"] = index
            final_list_modern.append(node)
        
        if app_mode == t['mode_edit']:
            broadcast_data["channelList"] = final_list_modern
            legacy_broadcast_tag.text = json.dumps(broadcast_data, ensure_ascii=False)
            file_bytes_out = ET.tostring(root, encoding="utf-8")
        else:
            built_root = ET.Element("CHANNELS")
            built_model = ET.SubElement(built_root, "ModelName")
            built_model.text = model_name_display
            built_legacy = ET.SubElement(built_root, "legacybroadcast")
            mock_json = {"countryCode": country_code, "countryGroup": country_group, "bTunedCountry": country_code, "channelList": final_list_modern}
            built_legacy.text = json.dumps(mock_json, ensure_ascii=False)
            file_bytes_out = ET.tostring(built_root, encoding="utf-8")
    else:
        item_strings_sorted = []
        for index, ch in enumerate(channels_sorted, start=1):
            original_item_str = ch["raw_str"]
            if "<prNum>" in original_item_str: 
                new_item_str = re.sub(r'<prNum>\d+</prNum>', f'<prNum>{index}</prNum>', original_item_str)
            else: 
                new_item_str = original_item_str.replace("<ITEM>", f"<ITEM>\r\n<prNum>{index}</prNum>")
            item_strings_sorted.append(new_item_str)
        combined_items_str = "\r\n".join(item_strings_sorted)
        
        if app_mode == t['mode_edit']:
            start_idx = file_text_original.find("<ITEM>")
            end_idx = file_text_original.rfind("</ITEM>") + len("</ITEM>")
            if start_idx != -1 and end_idx != -1: 
                final_text_output = file_text_original[:start_idx] + combined_items_str + file_text_original[end_idx:]
            else: 
                final_text_output = combined_items_str
        else:
            final_text_output = f"<CHANNELS>\r\n<ModelName>{model_name_display}</ModelName>\r\n<CountryGroup>{country_group}</CountryGroup>\r\n" + combined_items_str + "\r\n</CHANNELS>"
            
        try: file_bytes_out = final_text_output.encode('utf-8')
        except UnicodeEncodeError: file_bytes_out = final_text_output.encode('latin-1')

    text_report_out = f"{t['txt_header']} ({model_name_display})\n🧠 نظام الذاكرة الأبدية المحفوظة بالسيرفر\n"
    text_report_out += "==================================================\n"
    for index, ch in enumerate(channels_sorted, start=1):
        text_report_out += f"No. {index:03d} : {ch['name']:<25} | Freq: {ch['freq']} | Category: {ai_classify(ch['name'])}\n"

    st.write("---")
    st.success(t['ready_msg'])
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1: st.download_button(label=t['btn_download_tll'], data=file_bytes_out, file_name="GlobalClone00001.TLL", mime="application/octet-stream")
    with col_btn2: st.download_button(label=t['btn_download_txt'], data=text_report_out, file_name="Channels_List.txt", mime="text/plain; charset=utf-8")

# الفوتر السيبراني المعتمد للمهندس رفيق ناتان
whatsapp_url = "https://api.whatsapp.com/send?phone=201280339779&text=Hello%20Developer%20Rafik%20Nathan%2C%20I%20have%20an%20inquiry%20regarding%20your%20LG%20TV%20Sorter%20script%3A"
st.markdown(f"""
    <div class="futuristic-cyber-footer">
        <div class="footer-dev">🛠️ DEVELOPER ENG: RAFIK NATHAN</div>
        <div class="footer-item">📱 <b>MOBILE / الموبايل:</b> +201280339779</div>
        <div class="footer-item">✉️ <b>E-MAIL / البريد الإلكتروني:</b> rafikrambo113@gmail.com</div>
        <a href="{whatsapp_url}" target="_blank" class="cyber-whatsapp-btn">WhatsApp Web</a>
    </div>
""", unsafe_allow_html=True)
