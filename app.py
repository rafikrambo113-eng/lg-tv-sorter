import streamlit as st
import xml.etree.ElementTree as ET
import json
import re
import streamlit.components.v1 as components

# Session state
if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

UI_TEXT = {
    'ar': {
        'title': "📺 RAMBO - LG Channel Sorter",
        'subtitle': "AI Channel Manager"
    },
    'en': {
        'title': "📺 RAMBO - LG Channel Sorter",
        'subtitle': "AI Channel Manager"
    }
}

t = UI_TEXT[st.session_state.lang]

st.set_page_config(page_title="RAMBO", layout="wide")

st.title(t['title'])
st.write(t['subtitle'])

# Toggles
col1, col2, col3 = st.columns(3)

with col1:
    update_freq = st.checkbox("Update Frequencies", value=True)
with col2:
    add_new_channels = st.checkbox("Add New Channels", value=True)
with col3:
    smart_mode = st.checkbox("Smart Mode", value=True)

# Fake DB
NILESAT_LIVE_DB = {
    "MBC 2": {"frequency": 11938, "update_date": "2026-01-20"},
    "QATAR TV HD": {"frequency": 10834, "update_date": "2026-05-14"}
}

NILESAT_NEW_CHANNELS = [
    {"name": "RAMBO ACTION HD", "frequency": 10834},
    {"name": "MISHMISH CINEMA", "frequency": 11938}
]

ALL_CATEGORIES = ["Sports", "Movies", "Kids", "News", "Religion", "General"]

def ai_classify(name):
    name = name.upper()
    if "SPORT" in name:
        return "Sports"
    if "MBC" in name or "MOVIE" in name or "CINEMA" in name:
        return "Movies"
    if "CARTOON" in name or "KIDS" in name:
        return "Kids"
    if "NEWS" in name:
        return "News"
    if "QURAN" in name or "HAYAT" in name:
        return "Religion"
    return "General"

uploaded_file = st.file_uploader("Upload TLL", type=["TLL"])

if uploaded_file:

    file_bytes = uploaded_file.read()

    try:
        root = ET.fromstring(file_bytes)
        is_modern = True
    except:
        is_modern = False
        file_text = file_bytes.decode("utf-8", errors="ignore")

    channels = []

    # MODERN XML
    if is_modern:
        broadcast = root.find(".//legacybroadcast")
        data = json.loads(broadcast.text)
        lst = data.get("channelList", [])

        for i, ch in enumerate(lst):
            name = ch.get("channelName", "")
            freq = ch.get("frequency", "")

            if update_freq and name.upper() in NILESAT_LIVE_DB:
                freq = NILESAT_LIVE_DB[name.upper()]["frequency"]

            channels.append({
                "name": name,
                "freq": freq,
                "raw": ch
            })

        if add_new_channels:
            for n in NILESAT_NEW_CHANNELS:
                channels.append({
                    "name": n["name"],
                    "freq": n["frequency"],
                    "raw": {}
                })

    # OLD XML
    else:
        items = re.findall(r'(<ITEM>.*?</ITEM>)', file_text, re.DOTALL)

        for item in items:
            name = re.search(r'<vchName>(.*?)</vchName>', item)
            freq = re.search(r'<frequency>(.*?)</frequency>', item)

            name = name.group(1) if name else "Unknown"
            freq = freq.group(1) if freq else ""

            channels.append({
                "name": name,
                "freq": freq,
                "raw": item
            })

    # CATEGORY PRIORITY
    priority = st.multiselect("Category Order", ALL_CATEGORIES)

    for c in ALL_CATEGORIES:
        if c not in priority:
            priority.append(c)

    # SORT (IMPROVED)
    channels_sorted = sorted(
        channels,
        key=lambda x: (priority.index(ai_classify(x["name"])), x["name"])
    )

    # SEARCH
    q = st.text_input("Search")
    if q:
        channels_sorted = [c for c in channels_sorted if q.lower() in c["name"].lower()]

    st.write("## Channels")

    for c in channels_sorted:
        st.write(f"{c['name']}  |  {c['freq']}  |  {ai_classify(c['name'])}")

    # DRAG & DROP UI (optional visual)
    st.write("## Drag Sort (Visual)")

    html = """
    <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js"></script>
    <ul id="list">
    """ + "".join([f"<li style='padding:8px;margin:5px;background:#222;color:#fff'>{c['name']}</li>" for c in channels_sorted]) + """
    </ul>

    <script>
    new Sortable(list,{animation:150});
    </script>
    """

    components.html(html, height=400)

    # EXPORT TXT
    if st.button("Export TXT"):
        txt = "CHANNEL LIST\n\n"
        for i, c in enumerate(channels_sorted, 1):
            txt += f"{i:03d} | {c['name']} | {ai_classify(c['name'])}\n"

        st.download_button(
            "Download TXT",
            txt,
            file_name="channels.txt"
        )
