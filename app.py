"""
RAMBO – AI Channel Generator  (pages/2_🛰️_AI_Channel_Generator.py)
────────────────────────────────────────────────────────────────────
• يبحث Claude على الإنترنت حياً عن أحدث قنوات وترددات القمر المختار
• يولّد ملف GlobalClone00001.TLL جاهز للشاشة بدون رفع أي ملف
• يدعم: Nilesat 7°W – Arabsat 26°E – Hotbird 13°E – Astra 19.2°E
"""

import streamlit as st
import json
import re
import requests
from datetime import datetime
import xml.etree.ElementTree as ET

# ══════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="RAMBO – AI Channel Generator",
    page_icon="🛰️",
    layout="wide",
)

# ══════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════
for k, v in [('lang', 'ar'), ('theme', 'dark'), ('ai_result', None),
             ('ai_sat', ''), ('ai_model', '')]:
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════
#  TRANSLATIONS
# ══════════════════════════════════════════════════════════
UI = {
    'ar': {
        'title':         "🛰️ RAMBO – مولّد القنوات بالذكاء الاصطناعي",
        'subtitle':      "يبحث على الإنترنت حياً ويولّد ملف TLL جاهز لشاشة LG بدون رفع أي ملف",
        'sat_label':     "📡 اختر القمر الصناعي",
        'country_label': "🌍 البلد / المنطقة (اختياري – لتخصيص النتائج)",
        'model_label':   "📺 موديل الشاشة (مثال: OLED55C1PVA)",
        'run_btn':       "🚀 ابدأ البحث وتوليد الملف",
        'spinner':       "⏳ الذكاء الاصطناعي يبحث على الإنترنت عن أحدث البيانات...",
        'no_key':        "⚠️ أدخل Anthropic API Key في الشريط الجانبي أولاً.",
        'api_label':     "🔑 Anthropic API Key",
        'result_title':  "📊 نتائج البحث الحي",
        'new_title':     "🆕 القنوات الجديدة المكتشفة",
        'dl_tll':        "📥 تحميل GlobalClone00001.TLL",
        'dl_txt':        "📄 تحميل تقرير القنوات (.txt)",
        'ready':         "✅ الملفات جاهزة للتحميل!",
        'err':           "❌ خطأ: ",
        'channels':      "قناة",
        'new_lbl':       "جديدة",
        'fta_lbl':       "مجانية FTA",
        'enc_lbl':       "مشفرة",
    },
    'en': {
        'title':         "🛰️ RAMBO – AI Channel Generator",
        'subtitle':      "Live Internet Search → Instant TLL file for LG TV — no file upload needed",
        'sat_label':     "📡 Select Satellite",
        'country_label': "🌍 Country / Region (optional – to refine results)",
        'model_label':   "📺 TV Model (e.g. OLED55C1PVA)",
        'run_btn':       "🚀 Start AI Search & Generate",
        'spinner':       "⏳ AI is performing a live search for the latest channel data...",
        'no_key':        "⚠️ Please enter your Anthropic API Key in the sidebar first.",
        'api_label':     "🔑 Anthropic API Key",
        'result_title':  "📊 Live Search Results",
        'new_title':     "🆕 Newly Discovered Channels",
        'dl_tll':        "📥 Download GlobalClone00001.TLL",
        'dl_txt':        "📄 Download Channel Report (.txt)",
        'ready':         "✅ Files are ready for download!",
        'err':           "❌ Error: ",
        'channels':      "Channels",
        'new_lbl':       "New",
        'fta_lbl':       "FTA",
        'enc_lbl':       "Encrypted",
    },
}
t = UI[st.session_state.lang]

# ══════════════════════════════════════════════════════════
#  SATELLITES & COUNTRIES
# ══════════════════════════════════════════════════════════
SATS = {
    "🇪🇬  Nilesat 7°W  (عربي / Arab)":          "Nilesat 7°W",
    "🇸🇦  Arabsat / Badr 26°E":                  "Arabsat/Badr 26°E",
    "🇪🇺  Hotbird 13°E  (Europe)":               "Hotbird 13°E",
    "🌍  Astra 19.2°E  (Global)":                "Astra 19.2°E",
}

COUNTRIES = [
    "─── اختر ───",
    "مصر / Egypt", "السعودية / Saudi Arabia", "الإمارات / UAE",
    "المغرب / Morocco", "تونس / Tunisia", "الجزائر / Algeria",
    "لبنان / Lebanon", "العراق / Iraq", "سوريا / Syria",
    "ليبيا / Libya", "السودان / Sudan", "قطر / Qatar",
    "United Kingdom", "Germany", "France", "Italy",
    "Spain", "Netherlands", "Turkey", "Poland",
]

# ══════════════════════════════════════════════════════════
#  CSS  – same cyber palette as main app
# ══════════════════════════════════════════════════════════
dark = st.session_state.theme == 'dark'
BG   = "radial-gradient(circle at 50% 50%,#110926 0%,#05020d 100%)" if dark else "radial-gradient(circle at 50%,#f4f5f7,#e4e7eb)"
TC   = "#00f0ff" if dark else "#0d0722"
BBG  = "rgba(13,7,33,0.85)"              if dark else "#fff"
BBR  = "#00f0ff"                          if dark else "#ff007f"
BSH  = "rgba(0,240,255,.35)"             if dark else "rgba(255,0,127,.15)"
TSH  = "0 0 5px rgba(0,240,255,.4)"      if dark else "none"
FF   = "'Cairo',sans-serif" if st.session_state.lang == 'ar' else "'Orbitron',sans-serif"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;900&family=Cairo:wght@400;700&display=swap');
.main{{background:{BG}!important;color:{TC}!important;font-family:{FF};}}
h1{{color:#ff007f!important;text-shadow:0 0 10px #ff007f,0 0 25px rgba(255,0,127,.4)!important;text-align:center;font-weight:900;margin-top:5px;}}
h3,p,label,.stMarkdown,.stInfo,div[data-testid="stMarkdownContainer"] p{{color:{TC}!important;text-shadow:{TSH};}}
.stTextInput>div>div>input,.stSelectbox>div>div{{background:{BBG}!important;color:{TC}!important;border:2px solid {BBR}!important;border-radius:10px!important;}}
.stButton>button{{background:linear-gradient(135deg,#ff007f,#aa0055)!important;color:#fff!important;border:2px solid #ff007f!important;border-radius:12px!important;font-weight:bold;font-size:16px;padding:10px;}}
.box{{background:{BBG};border:2px solid {BBR};box-shadow:0 5px 15px {BSH};border-radius:14px;padding:18px;margin-bottom:18px;}}
.chip{{display:inline-block;background:linear-gradient(135deg,#ff007f,#aa0055);color:#fff;padding:4px 14px;border-radius:20px;font-size:13px;margin:3px;font-weight:bold;}}
.chip-cyan{{background:linear-gradient(135deg,#00f0ff,#0080a0);}}
.ch-row{{background:rgba(0,240,255,.04);border-left:3px solid #ff007f;padding:7px 14px;margin:3px 0;border-radius:6px;font-size:13px;}}
.new-badge{{background:#ff007f;color:#fff;font-size:11px;padding:2px 8px;border-radius:10px;margin-left:6px;}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  TOP BAR – Language / Theme toggles
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

# ══════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ⚙️ إعدادات / Settings")
    api_key = st.text_input(t['api_label'], type="password", placeholder="sk-ant-api03-...")
    st.markdown("---")
    st.markdown("🔗 [احصل على مفتاح مجاني](https://console.anthropic.com/)")
    st.markdown("""
**كيف يعمل الذكاء الاصطناعي؟**

1. يبحث على `lyngsat.com`
2. يبحث على `kingofsat.net`  
3. يبحث على `flysat.com`
4. يدمج النتائج ويولّد ملف TLL
""")

# ══════════════════════════════════════════════════════════
#  MAIN CONTROLS
# ══════════════════════════════════════════════════════════
st.write("---")
col1, col2, col3 = st.columns(3)
with col1:
    sat_key  = st.selectbox(t['sat_label'], list(SATS.keys()))
    sat_name = SATS[sat_key]
with col2:
    country_raw = st.selectbox(t['country_label'], COUNTRIES)
    country = "" if country_raw.startswith("─") else country_raw
with col3:
    tv_model = st.text_input(t['model_label'], value="LG-OLED55C1", placeholder="OLED55C1PVA")

# ══════════════════════════════════════════════════════════
#  CLAUDE AI – LIVE WEB SEARCH
# ══════════════════════════════════════════════════════════
SYSTEM_PROMPT = """You are a satellite TV database expert. You have web search access.

Search lyngsat.com, kingofsat.net, and flysat.com for the MOST CURRENT channel list for the requested satellite.

Return ONLY a valid JSON object — no markdown, no explanations, no text outside the JSON.

Schema:
{
  "satellite": "string",
  "scan_date": "YYYY-MM-DD",
  "summary": "one sentence in Arabic describing the scan result",
  "channels": [
    {
      "name": "CHANNEL NAME IN CAPS",
      "frequency": 12345,
      "symbol_rate": 27500,
      "polarization": "H",
      "encryption": "FTA",
      "category": "category string",
      "is_new": false,
      "language": "Arabic"
    }
  ],
  "stats": {
    "total": 0,
    "new_channels": 0,
    "fta": 0,
    "encrypted": 0
  }
}

Rules:
- polarization: ONLY "H" or "V"
- encryption: ONLY "FTA" or "Encrypted"  
- is_new: true if channel launched in last 6 months
- category must be one of:
  قنوات مسيحية | قنوات إسلامية | مسلسلات ودراما | أفلام | أطفال وكرتون |
  رياضة | أخبار وسياسة | موسيقى وترفيه | قنوات عامة ومنوعات |
  Entertainment | News | Sports | Movies | Kids | Religious | Music | General
- Include AT LEAST 30 channels, ideally 50-100+ for major satellites
- Return ONLY the JSON object, nothing else
"""

def search_channels_ai(api_key: str, sat: str, country: str) -> dict:
    country_line = f"Focus especially on channels popular in: {country}.\n" if country else ""
    user_msg = (
        f"Satellite: {sat}\n"
        f"{country_line}"
        "Search lyngsat.com, kingofsat.net, flysat.com RIGHT NOW for the latest complete "
        f"channel list on {sat}. Return the full JSON."
    )

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 8000,
        "system": SYSTEM_PROMPT,
        "tools": [{"type": "web_search_20250305", "name": "web_search"}],
        "messages": [{"role": "user", "content": user_msg}],
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }

    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        json=payload,
        headers=headers,
        timeout=180,
    )
    resp.raise_for_status()
    data = resp.json()

    # Collect all text blocks
    full_text = "".join(
        b.get("text", "") for b in data.get("content", [])
        if isinstance(b, dict) and b.get("type") == "text"
    )

    # Strip markdown fences
    clean = re.sub(r"```(?:json)?", "", full_text).strip()
    # Extract first JSON object
    start = clean.find("{")
    end   = clean.rfind("}") + 1
    if start == -1:
        raise ValueError(f"No JSON in response. Raw: {full_text[:500]}")

    return json.loads(clean[start:end])


# ══════════════════════════════════════════════════════════
#  BUILD TLL  (modern legacybroadcast format)
# ══════════════════════════════════════════════════════════
def build_tll(channels: list, tv_model: str, sat: str) -> bytes:
    ch_list = []
    for idx, ch in enumerate(channels, 1):
        ch_list.append({
            "majorNumber":  idx,
            "channelName":  ch.get("name", ""),
            "frequency":    int(ch.get("frequency", 0)),
            "symbolRate":   str(ch.get("symbol_rate", 27500)),
            "polarization": ch.get("polarization", "H"),
            "serviceType":  "1",
            "scrambled":    "false" if ch.get("encryption", "FTA") == "FTA" else "true",
            "satellite":    sat,
        })

    broadcast_json = json.dumps({"channelList": ch_list}, ensure_ascii=False)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    xml_str = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<LGSmartTVDatabase>\n'
        '  <TVSetup>\n'
        f'    <ModelName>{tv_model}</ModelName>\n'
        f'    <GeneratedBy>RAMBO AI Channel Generator</GeneratedBy>\n'
        f'    <GenerationDate>{now}</GenerationDate>\n'
        f'    <Satellite>{sat}</Satellite>\n'
        '  </TVSetup>\n'
        f'  <legacybroadcast>{broadcast_json}</legacybroadcast>\n'
        '</LGSmartTVDatabase>'
    )
    return xml_str.encode("utf-8")


# ══════════════════════════════════════════════════════════
#  BUILD TXT REPORT
# ══════════════════════════════════════════════════════════
def build_txt(result: dict, sat: str, tv_model: str) -> str:
    st2 = result.get("stats", {})
    chs = result.get("channels", [])
    lines = [
        "=" * 65,
        "  RAMBO – AI Satellite Channel Report  (Live Web Search)",
        f"  Satellite : {sat}",
        f"  TV Model  : {tv_model}",
        f"  Scan Date : {result.get('scan_date', datetime.now().strftime('%Y-%m-%d'))}",
        f"  Summary   : {result.get('summary', '')}",
        "=" * 65,
        f"  Total     : {st2.get('total', len(chs))}  |  "
        f"New: {st2.get('new_channels', 0)}  |  "
        f"FTA: {st2.get('fta', 0)}  |  "
        f"Encrypted: {st2.get('encrypted', 0)}",
        "",
        f"{'#':<5} {'Channel Name':<32} {'Freq':>7}  Pol  {'Category':<25}  Enc   New?",
        "-" * 85,
    ]
    for i, ch in enumerate(chs, 1):
        lines.append(
            f"{i:<5} {ch.get('name',''):<32} {ch.get('frequency',0):>7}  "
            f"{ch.get('polarization',''):>3}  {ch.get('category',''):25}  "
            f"{'FTA' if ch.get('encryption')=='FTA' else 'ENC':5} "
            f"{'YES' if ch.get('is_new') else ''}"
        )
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════
#  RUN BUTTON
# ══════════════════════════════════════════════════════════
st.write("---")
if st.button(t['run_btn'], use_container_width=True):
    if not api_key:
        st.warning(t['no_key'])
    else:
        with st.spinner(t['spinner']):
            try:
                result = search_channels_ai(api_key, sat_name, country)
                st.session_state.ai_result = result
                st.session_state.ai_sat    = sat_name
                st.session_state.ai_model  = tv_model
            except requests.HTTPError as e:
                st.error(f"{t['err']}{e.response.status_code} – {e.response.text[:300]}")
            except Exception as e:
                st.error(f"{t['err']}{e}")

# ══════════════════════════════════════════════════════════
#  DISPLAY RESULTS
# ══════════════════════════════════════════════════════════
if st.session_state.ai_result:
    result   = st.session_state.ai_result
    sat_used = st.session_state.ai_sat   or sat_name
    mod_used = st.session_state.ai_model or tv_model
    channels = result.get("channels", [])
    stats    = result.get("stats", {})
    total    = stats.get("total", len(channels))
    new_n    = stats.get("new_channels", sum(1 for c in channels if c.get("is_new")))
    fta_n    = stats.get("fta", sum(1 for c in channels if c.get("encryption") == "FTA"))
    enc_n    = stats.get("encrypted", sum(1 for c in channels if c.get("encryption") != "FTA"))

    st.write("---")
    st.markdown(f"### {t['result_title']}")
    st.markdown(f"<p>{result.get('summary', '')}</p>", unsafe_allow_html=True)

    # ── Stats bar ────────────────────────────────────────
    st.markdown(
        f'<div class="box">'
        f'<span class="chip">📺 {total} {t["channels"]}</span>'
        f'<span class="chip chip-cyan">🆕 {new_n} {t["new_lbl"]}</span>'
        f'<span class="chip">🔓 {fta_n} {t["fta_lbl"]}</span>'
        f'<span class="chip">🔒 {enc_n} {t["enc_lbl"]}</span>'
        f'<span class="chip chip-cyan">📡 {sat_used}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Channels by category ─────────────────────────────
    cat_map: dict[str, list] = {}
    for ch in channels:
        cat_map.setdefault(ch.get("category", "General"), []).append(ch)

    cola, colb = st.columns(2)
    for i, (cat, chs) in enumerate(cat_map.items()):
        new_in = sum(1 for c in chs if c.get("is_new"))
        badge  = f" 🆕×{new_in}" if new_in else ""
        with (cola if i % 2 == 0 else colb):
            with st.expander(f"{cat}  ({len(chs)} {t['channels']}){badge}"):
                for ch in chs:
                    enc_ic  = "🔒" if ch.get("encryption","FTA") != "FTA" else "🔓"
                    new_tag = '<span class="new-badge">NEW</span>' if ch.get("is_new") else ""
                    st.markdown(
                        f'<div class="ch-row">'
                        f'{enc_ic} <b>{ch.get("name","")}</b>{new_tag}'
                        f'&nbsp;|&nbsp; {ch.get("frequency","")} MHz'
                        f'&nbsp; {ch.get("polarization","")}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

    # ── New channels spotlight ────────────────────────────
    new_chs = [c for c in channels if c.get("is_new")]
    if new_chs:
        st.write("---")
        st.markdown(f"### {t['new_title']}")
        cols3 = st.columns(3)
        for i, ch in enumerate(new_chs):
            with cols3[i % 3]:
                st.markdown(
                    f'<div class="box" style="border-color:#ff007f;">'
                    f'<b>🆕 {ch.get("name","")}</b><br>'
                    f'📡 {ch.get("frequency","")} MHz &nbsp; {ch.get("polarization","")}<br>'
                    f'📂 {ch.get("category","")}&nbsp;&nbsp;'
                    f'{"🔓 FTA" if ch.get("encryption","FTA")=="FTA" else "🔒 Encrypted"}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    # ── Download ──────────────────────────────────────────
    st.write("---")
    st.success(t['ready'])

    tll_bytes  = build_tll(channels, mod_used, sat_used)
    txt_report = build_txt(result, sat_used, mod_used)

    d1, d2 = st.columns(2)
    with d1:
        st.download_button(
            label=t['dl_tll'],
            data=tll_bytes,
            file_name="GlobalClone00001.TLL",
            mime="application/octet-stream",
            use_container_width=True,
        )
    with d2:
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
wa = "https://api.whatsapp.com/send?phone=201280339779&text=Hello%20RAMBO%20Dev"
st.markdown(f"""
<div style="background:#080314;border:2px solid #00f0ff;color:#fff;padding:28px;
            text-align:center;border-radius:20px;margin-top:60px;font-family:'Orbitron',sans-serif;">
  <div style="color:#ff007f;font-size:22px;font-weight:bold;">🛠️ DEVELOPER ENG: RAFIK NATHAN</div>
  <div style="margin-top:8px;">📱 +201280339779 &nbsp;|&nbsp; ✉️ rafikrambo113@gmail.com</div>
  <a href="{wa}" target="_blank"
     style="color:#25d366;padding:10px 28px;border-radius:30px;display:inline-block;
            font-weight:bold;border:2px solid #25d366;text-decoration:none;margin-top:16px;">
    💬 WhatsApp
  </a>
</div>
""", unsafe_allow_html=True)
