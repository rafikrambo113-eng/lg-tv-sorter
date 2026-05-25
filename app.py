"""
RAMBO – Smart Channel Editor  (pages/2_🔧_Smart_Channel_Editor.py)
──────────────────────────────────────────────────────────────────
صفحة منفصلة تقوم بـ:
  1. رفع ملف TLL وقراءته
  2. ترتيب القنوات حسب فئات يختارها المستخدم
  3. تحديث الترددات المتغيرة من قاعدة بيانات داخلية
  4. إضافة قنوات جديدة متاحة على القمر المكتشف
  5. تحميل الملف النهائي + تقرير نصي
"""

import streamlit as st
import xml.etree.ElementTree as ET
import json
import re

# ══════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="RAMBO – Smart Channel Editor",
    page_icon="🔧",
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
        'title':           "🔧 RAMBO – المحرر الذكي للقنوات",
        'subtitle':        "ارفع ملف القنوات → رتّب + حدّث الترددات + أضف قنوات جديدة → حمّل الملف النهائي",
        'upload_label':    "🚀 ارفع ملف القنوات (GlobalClone00001.TLL)",
        'success_read':    "✅ تم قراءة الملف بنجاح! الموديل: ",
        'opt_sort':        "🗂️ ترتيب القنوات حسب الفئات",
        'opt_freq':        "⚛️ تحديث الترددات المتغيرة تلقائياً",
        'opt_new':         "✨ إضافة القنوات الجديدة المتاحة",
        'sort_title':      "🎛️ اختر ترتيب الفئات (اضغط بالترتيب المفضل)",
        'sort_tip':        "💡 الفئة الأولى ستظهر في أعلى قائمة التلفزيون",
        'sort_label':      "اختر الفئات بالترتيب:",
        'preview_title':   "📊 معاينة توزيع القنوات:",
        'freq_title':      "🔁 تقرير تحديث الترددات:",
        'new_title':       "🆕 القنوات الجديدة المضافة:",
        'ready':           "🌌 الملف جاهز للتحميل!",
        'dl_tll':          "📥 تحميل GlobalClone00001.TLL",
        'dl_txt':          "📄 تحميل تقرير القنوات (.txt)",
        'channels':        "قناة",
        'lg_tip_title':    "💡 نصيحة مهمة بعد رفع الملف على شاشة LG:",
        'lg_tip_text':     (
            "إذا لاحظت أن الترتيب غير صحيح بعد رفع الملف على الشاشة، قم بالتالي:\n"
            "1. الإعدادات ← القنوات ← مدير القنوات\n"
            "2. تعديل كل القنوات\n"
            "3. حدّد كل القنوات ← استعادة (Restore)\n"
            "هذه الخطوة تجبر الشاشة على تفعيل الترتيب الجديد."
        ),
        'no_file':         "⬆️ ارفع ملف TLL أولاً للبدء.",
        'col_num':         "الرقم",
        'col_name':        "اسم القناة",
        'col_cat':         "الفئة",
        'col_freq':        "التردد",
        'search_label':    "🔍 ابحث عن قناة:",
        'search_ph':       "اكتب اسم القناة...",
        'no_results':      "⚠️ لا توجد نتائج مطابقة.",
    },
    'en': {
        'title':           "🔧 RAMBO – Smart Channel Editor",
        'subtitle':        "Upload TLL → Sort + Update Freqs + Add New Channels → Download Final File",
        'upload_label':    "🚀 Upload Channel File (GlobalClone00001.TLL)",
        'success_read':    "✅ File read successfully! Model: ",
        'opt_sort':        "🗂️ Sort channels by category",
        'opt_freq':        "⚛️ Auto-update changed frequencies",
        'opt_new':         "✨ Inject new available channels",
        'sort_title':      "🎛️ Choose category order (click in preferred order)",
        'sort_tip':        "💡 First category appears at the top of your TV list",
        'sort_label':      "Select categories in order:",
        'preview_title':   "📊 Channel distribution preview:",
        'freq_title':      "🔁 Frequency update report:",
        'new_title':       "🆕 Newly injected channels:",
        'ready':           "🌌 File ready for download!",
        'dl_tll':          "📥 Download GlobalClone00001.TLL",
        'dl_txt':          "📄 Download Channel Report (.txt)",
        'channels':        "Channels",
        'lg_tip_title':    "💡 Important tip after uploading to LG TV:",
        'lg_tip_text':     (
            "If channels appear unsorted after uploading:\n"
            "1. Settings → Channels → Channel Manager\n"
            "2. Edit All Channels\n"
            "3. Select All → Restore\n"
            "This forces the TV to apply the new sort order."
        ),
        'no_file':         "⬆️ Upload a TLL file above to get started.",
        'col_num':         "No.",
        'col_name':        "Channel Name",
        'col_cat':         "Category",
        'col_freq':        "Frequency",
        'search_label':    "🔍 Search channel:",
        'search_ph':       "Type channel name...",
        'no_results':      "⚠️ No matching channels found.",
    },
}
t = UI[st.session_state.lang]

# ══════════════════════════════════════════════════════════
#  DATABASES
# ══════════════════════════════════════════════════════════

# ── تحديثات الترددات الرسمية (Nilesat 7°W) ──
FREQ_DB = {
    "AL HAYAT":     {"frequency": 12207, "polarization": "Vertical",   "update_date": "2026-05-10"},
    "SAT-7 KIDS":   {"frequency": 11353, "polarization": "Vertical",   "update_date": "2026-04-18"},
    "SAT-7 ARABIC": {"frequency": 11353, "polarization": "Vertical",   "update_date": "2026-04-18"},
    "ALKARMA ME 1": {"frequency": 11096, "polarization": "Horizontal", "update_date": "2026-02-05"},
    "AGHAPY TV":    {"frequency": 11179, "polarization": "Horizontal", "update_date": "2026-03-12"},
    "CTV":          {"frequency": 12022, "polarization": "Vertical",   "update_date": "2026-05-01"},
    "MBC 2":        {"frequency": 11938, "polarization": "Vertical",   "update_date": "2026-01-20"},
    "QATAR TV HD":  {"frequency": 10834, "polarization": "Horizontal", "update_date": "2026-05-14"},
    "ON TIME SPORTS 1 HD": {"frequency": 11861, "polarization": "Vertical", "update_date": "2026-04-01"},
    "ON TIME SPORTS 2 HD": {"frequency": 11861, "polarization": "Vertical", "update_date": "2026-04-01"},
    "CBC":          {"frequency": 10853, "polarization": "Vertical",   "update_date": "2026-03-20"},
    "CBC DRAMA":    {"frequency": 10853, "polarization": "Vertical",   "update_date": "2026-03-20"},
    "MBC MASR":     {"frequency": 11938, "polarization": "Vertical",   "update_date": "2026-01-20"},
    "MBC MASR 2":   {"frequency": 11938, "polarization": "Vertical",   "update_date": "2026-01-20"},
    "DMC":          {"frequency": 11727, "polarization": "Vertical",   "update_date": "2026-02-15"},
    "DMC DRAMA":    {"frequency": 11727, "polarization": "Vertical",   "update_date": "2026-02-15"},
}

# ── قنوات جديدة للحقن ──
NEW_CHANNELS = [
    {"name": "ON TIME SPORTS 4 HD", "frequency": 11861, "polarization": "Vertical",   "launch": "2026-05-01", "source": "FlySat"},
    {"name": "CBC SOFRA HD",         "frequency": 10853, "polarization": "Vertical",   "launch": "2026-04-15", "source": "Nilesat Official"},
    {"name": "WATCH IT HD",          "frequency": 11727, "polarization": "Vertical",   "launch": "2026-03-10", "source": "KingOfSat"},
    {"name": "أبوظبي الرياضية 3",   "frequency": 11747, "polarization": "Horizontal", "launch": "2026-02-20", "source": "Arabsat"},
    {"name": "ROTANA COMEDY",        "frequency": 12034, "polarization": "Horizontal", "launch": "2026-01-05", "source": "FlySat"},
]

# ══════════════════════════════════════════════════════════
#  CATEGORIES
# ══════════════════════════════════════════════════════════
def get_categories():
    if st.session_state.lang == 'ar':
        return [
            "⛪ قنوات مسيحية",
            "🕌 قنوات إسلامية",
            "🎬 مسلسلات ودراما",
            "🍿 أفلام",
            "👶 أطفال وكرتون",
            "⚽ رياضة",
            "📰 أخبار وسياسة",
            "🎵 موسيقى وترفيه",
            "📺 قنوات عامة ومنوعات",
        ]
    else:
        return [
            "⛪ Christian",
            "🕌 Islamic",
            "🎬 Drama & Series",
            "🍿 Movies",
            "👶 Kids & Cartoon",
            "⚽ Sports",
            "📰 News & Politics",
            "🎵 Music & Entertainment",
            "📺 General",
        ]

def classify(name: str) -> str:
    n = name.upper()
    cats = get_categories()
    if any(w in n for w in ["CTV","AGHAPY","KARMA","NOURSAT","SAT-7","MESAT","MIRAYA","FAITH"]): return cats[0]
    if any(w in n for w in ["QURAN","RAHMA","MAJD","MAKKA","HAYAT","IQRAA","HUDA","RESALA"]): return cats[1]
    if any(w in n for w in ["DRAMA","SERIES","MOSALSALAT","KHOLASA","CBC DRAMA","DMC DRAMA","MASRAWY"]): return cats[2]
    if any(w in n for w in ["CINEMA","ROTANA","AFLAM","MIX","FOX","MBC2","ACTION","MOVIE","MISHMISH","COMEDY","AFLAM"]): return cats[3]
    if any(w in n for w in ["SPACETOON","SPACE TOON","CN ","MAJID","KIDS","TOM","CARTOON","JEEM","TOYOR"]): return cats[4]
    if any(w in n for w in ["SPORT","ONTIME","ON TIME","KASS","AD SPORT","BEIN","SSC","MATCH","GOAL"]): return cats[5]
    if any(w in n for w in ["NEWS","JAZEERA","ARABIYA","HADATH","CAIRO","EXTRA","SKY NEWS","BBC","CNN","MEKAMELEEN"]): return cats[6]
    if any(w in n for w in ["MUSIC","MAZZIKA","MELODY","MTV","WATAN","NILE CULTURE","NILE SONG"]): return cats[7]
    return cats[8]

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
FTR = "#080314"
FTTC = "#ffffff"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;900&family=Cairo:wght@400;700&display=swap');
.main{{background:{BG}!important;color:{TC}!important;font-family:{FF};}}
h1{{color:#ff007f!important;text-shadow:0 0 10px #ff007f,0 0 25px rgba(255,0,127,.4)!important;text-align:center;font-weight:900;margin-top:5px;}}
h3,p,label,.stMarkdown,div[data-testid="stMarkdownContainer"] p{{color:{TC}!important;text-shadow:{TSH};}}
.stTextInput>div>div>input{{background:{BBG}!important;color:{TC}!important;border:2px solid {BBR}!important;border-radius:10px!important;}}
.stCheckbox,.stMultiSelect,div[data-testid="stExpander"],div[data-testid="stFileUploader"]{{
  background:{BBG}!important;border:2px solid {BBR}!important;
  box-shadow:0 5px 15px {BSH}!important;border-radius:14px!important;padding:18px!important;margin-bottom:20px!important;}}
.stButton>button{{background:linear-gradient(135deg,#ff007f,#aa0055)!important;color:#fff!important;
  border:2px solid #ff007f!important;border-radius:12px!important;font-weight:bold;}}
.tip-box{{background:{BBG};border:2px solid #ff007f;box-shadow:0 5px 15px rgba(255,0,127,.25);
  border-radius:14px;padding:18px;margin-bottom:20px;}}
.chip{{display:inline-block;background:linear-gradient(135deg,#ff007f,#aa0055);color:#fff;
  padding:4px 14px;border-radius:20px;font-size:13px;margin:3px;font-weight:bold;}}
.chip-c{{background:linear-gradient(135deg,#00f0ff,#0080a0);}}
.ch-row{{background:rgba(0,240,255,.04);border-left:3px solid #ff007f;
  padding:7px 14px;margin:3px 0;border-radius:6px;font-size:13px;}}
.futuristic-cyber-footer{{background:{FTR};border:2px solid #00f0ff;color:{FTTC}!important;
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
#  FILE UPLOAD
# ══════════════════════════════════════════════════════════
uploaded = st.file_uploader(t['upload_label'], type=["TLL"])

if not uploaded:
    st.info(t['no_file'])
    st.stop()

# ── Read file ──
file_bytes = uploaded.read()
try:
    file_text = file_bytes.decode('utf-8')
except UnicodeDecodeError:
    file_text = file_bytes.decode('latin-1')

root = ET.fromstring(file_bytes)
model_el = root.find(".//ModelName")
model_name = model_el.text if model_el is not None else "Unknown LG TV"
lb_tag = root.find(".//legacybroadcast")
is_modern = lb_tag is not None and lb_tag.text

st.info(f"{t['success_read']} **{model_name}**")

# ── LG Tip box ──
st.markdown(f"""
<div class="tip-box">
  <h4 style="color:#ff007f;margin-top:0;">{t['lg_tip_title']}</h4>
  <p style="white-space:pre-line;margin-bottom:0;font-size:14px;">{t['lg_tip_text']}</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  OPTIONS
# ══════════════════════════════════════════════════════════
co1, co2, co3 = st.columns(3)
with co1:
    do_sort = st.checkbox(t['opt_sort'],  value=True)
with co2:
    do_freq = st.checkbox(t['opt_freq'],  value=True)
with co3:
    do_new  = st.checkbox(t['opt_new'],   value=True)

# ══════════════════════════════════════════════════════════
#  PARSE CHANNELS
# ══════════════════════════════════════════════════════════
channels_raw = []   # list of dicts: {name, freq, raw_node/raw_str}
freq_changes = []
injected     = []

if is_modern:
    bd = json.loads(lb_tag.text)
    ch_list = bd.get("channelList", [])

    # ── Inject new ──
    if do_new:
        for nc in NEW_CHANNELS:
            ch_list.append({
                "channelName": nc["name"],
                "frequency":   nc["frequency"],
                "polarization":nc["polarization"],
                "majorNumber": 0,
                "serviceType": "1",
                "scrambled":   "false",
                "symbolRate":  "27500",
            })
            injected.append(nc)

    for idx, ch in enumerate(ch_list):
        name    = ch.get("channelName", "Unknown")
        old_f   = str(ch.get("frequency", "N/A"))
        name_up = name.upper()

        if do_freq and name_up in FREQ_DB:
            new_f = str(FREQ_DB[name_up]["frequency"])
            if old_f != new_f:
                freq_changes.append({
                    (t['col_name']):       name,
                    (t['col_cat']):        classify(name),
                    "التردد القديم / Old": f"{old_f} MHz",
                    "التردد الجديد / New": f"{new_f} MHz",
                    "تاريخ التحديث":       FREQ_DB[name_up]["update_date"],
                })
                ch["frequency"]    = int(new_f)
                ch["polarization"] = FREQ_DB[name_up]["polarization"]
                old_f = new_f

        channels_raw.append({"name": name, "freq": old_f, "raw_node": ch})

else:
    # ── Legacy XML format ──
    items = re.findall(r'(<ITEM>.*?</ITEM>)', file_text, re.DOTALL)

    for idx, item_str in enumerate(items):
        nm = re.search(r'<vchName>(.*?)</vchName>', item_str)
        fr = re.search(r'<frequency>(.*?)</frequency>', item_str)
        name  = nm.group(1) if nm else "Unknown"
        old_f = fr.group(1) if fr else "N/A"
        name_up = name.upper()

        if do_freq and name_up in FREQ_DB:
            new_f = str(FREQ_DB[name_up]["frequency"])
            if old_f != new_f:
                freq_changes.append({
                    (t['col_name']):       name,
                    (t['col_cat']):        classify(name),
                    "التردد القديم / Old": f"{old_f} MHz",
                    "التردد الجديد / New": f"{new_f} MHz",
                    "تاريخ التحديث":       FREQ_DB[name_up]["update_date"],
                })
                item_str = re.sub(r'<frequency>\d+</frequency>',
                                  f'<frequency>{new_f}</frequency>', item_str)
                old_f = new_f

        channels_raw.append({"name": name, "freq": old_f, "raw_str": item_str})

    if do_new:
        for nc in NEW_CHANNELS:
            new_item = (
                f"<ITEM>\r\n<prNum>0</prNum>\r\n"
                f"<vchName>{nc['name']}</vchName>\r\n"
                f"<frequency>{nc['frequency']}</frequency>\r\n"
                f"<serviceType>1</serviceType>\r\n</ITEM>"
            )
            channels_raw.append({"name": nc["name"], "freq": str(nc["frequency"]), "raw_str": new_item})
            injected.append(nc)

# ══════════════════════════════════════════════════════════
#  SEARCH BAR
# ══════════════════════════════════════════════════════════
st.write("---")
st.write(f"### {t['search_label']}")
query = st.text_input("", placeholder=t['search_ph']).strip().upper()
if query:
    results = [
        {t['col_num']: i+1, t['col_name']: c["name"],
         t['col_cat']: classify(c["name"]), t['col_freq']: c["freq"]}
        for i, c in enumerate(channels_raw)
        if query in c["name"].upper()
    ]
    if results:
        st.table(results)
    else:
        st.warning(t['no_results'])

# ══════════════════════════════════════════════════════════
#  CATEGORY SORT
# ══════════════════════════════════════════════════════════
CATS = get_categories()
if do_sort:
    st.write("---")
    st.write(f"### {t['sort_title']}")
    st.caption(t['sort_tip'])
    user_order = st.multiselect(t['sort_label'], options=CATS, default=[])
else:
    user_order = []

# Build final priority (user picks first, rest appended)
priority = list(user_order)
for c in CATS:
    if c not in priority:
        priority.append(c)

# Sort channels
if do_sort:
    channels_sorted = sorted(channels_raw, key=lambda x: priority.index(classify(x["name"])))
else:
    channels_sorted = channels_raw

# ══════════════════════════════════════════════════════════
#  LIVE PREVIEW
# ══════════════════════════════════════════════════════════
st.write("---")
st.write(f"### {t['preview_title']}")

# Stats chips
total_n = len(channels_sorted)
new_n   = len(injected)
freq_n  = len(freq_changes)
st.markdown(
    f'<span class="chip">📺 {total_n} {t["channels"]}</span>'
    f'<span class="chip chip-c">🆕 {new_n} جديدة/New</span>'
    f'<span class="chip chip-c">🔄 {freq_n} تحديث تردد</span>',
    unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)

cat_map: dict[str, list] = {}
for ch in channels_sorted:
    cat = classify(ch["name"])
    cat_map.setdefault(cat, []).append(ch["name"])

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
#  REPORT TABLES
# ══════════════════════════════════════════════════════════
if freq_changes:
    st.write("---")
    st.write(f"### {t['freq_title']}")
    st.table(freq_changes)

if injected:
    st.write("---")
    st.write(f"### {t['new_title']}")
    inj_table = [
        {"اسم القناة / Name": nc["name"],
         "التردد / Freq":     f"{nc['frequency']} MHz",
         "الاستقطاب / Pol":   nc["polarization"],
         "تاريخ الإضافة":     nc.get("launch", "—"),
         "المصدر / Source":   nc.get("source", "—")}
        for nc in injected
    ]
    st.table(inj_table)

# ══════════════════════════════════════════════════════════
#  BUILD FINAL FILES
# ══════════════════════════════════════════════════════════
txt_report = f"RAMBO – Smart Channel Editor Report\n"
txt_report += f"Model: {model_name}\n"
txt_report += "=" * 60 + "\n"
if freq_changes:
    txt_report += "\n[Frequency Updates]\n"
    for fc in freq_changes:
        txt_report += (
            f"  {fc[t['col_name']]:<25} "
            f"{fc['التردد القديم / Old']:>10} -> {fc['التردد الجديد / New']:<10} "
            f"| {fc['تاريخ التحديث']}\n"
        )
if injected:
    txt_report += "\n[New Channels Injected]\n"
    for nc in injected:
        txt_report += f"  {nc['name']:<25} {nc['frequency']} MHz  {nc['polarization']}\n"
txt_report += "\n" + "=" * 60 + "\n\n"
for idx, ch in enumerate(channels_sorted, 1):
    txt_report += f"No. {idx:04d} : {ch['name']:<30} | Freq: {ch['freq']}\n"

# Build TLL bytes
if is_modern:
    final_list = []
    for idx, ch in enumerate(channels_sorted, 1):
        node = ch["raw_node"]
        node["majorNumber"] = idx
        final_list.append(node)
    bd["channelList"] = final_list
    lb_tag.text = json.dumps(bd, ensure_ascii=False)
    final_bytes = ET.tostring(root, encoding="utf-8")
else:
    sorted_items = []
    for idx, ch in enumerate(channels_sorted, 1):
        s = ch["raw_str"]
        if "<prNum>" in s:
            s = re.sub(r'<prNum>\d+</prNum>', f'<prNum>{idx}</prNum>', s)
        else:
            s = s.replace("<ITEM>", f"<ITEM>\r\n<prNum>{idx}</prNum>")
        sorted_items.append(s)

    combined = "\r\n".join(sorted_items)
    si = file_text.find("<ITEM>")
    ei = file_text.rfind("</ITEM>") + len("</ITEM>")
    if si != -1 and ei != -1:
        final_text = file_text[:si] + combined + file_text[ei:]
    else:
        final_text = combined

    try:
        final_bytes = final_text.encode('utf-8')
    except UnicodeEncodeError:
        final_bytes = final_text.encode('latin-1')

# ══════════════════════════════════════════════════════════
#  DOWNLOAD BUTTONS
# ══════════════════════════════════════════════════════════
st.write("---")
st.success(t['ready'])

db1, db2 = st.columns(2)
with db1:
    st.download_button(
        label=t['dl_tll'],
        data=final_bytes,
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
  <div class="footer-item">📱 <b>MOBILE:</b> +201280339779</div>
  <div class="footer-item">✉️ <b>E-MAIL:</b> rafikrambo113@gmail.com</div>
  <a href="{wa}" target="_blank" class="cyber-whatsapp-btn">💬 WhatsApp</a>
</div>
""", unsafe_allow_html=True)
