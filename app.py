import streamlit as st
import xml.etree.ElementTree as ET
import json
import re

st.set_page_config(page_title="Web ChanSort Lite", layout="wide")

# ======================
# STATE
# ======================
if "channels" not in st.session_state:
    st.session_state.channels = []

if "order" not in st.session_state:
    st.session_state.order = []

# ======================
# CATEGORY ENGINE
# ======================
def ai_classify(name):
    name = name.upper()

    if any(x in name for x in ["SPORT", "SSC", "ONTIME"]):
        return "Sports"
    if any(x in name for x in ["MOVIE", "CINEMA", "MBC2", "ROTANA"]):
        return "Movies"
    if any(x in name for x in ["CARTOON", "KIDS"]):
        return "Kids"
    if any(x in name for x in ["NEWS", "JAZEERA"]):
        return "News"
    if any(x in name for x in ["QURAN", "HAYAT"]):
        return "Religion"

    return "General"


CATEGORIES = ["Sports", "Movies", "Kids", "News", "Religion", "General"]

# ======================
# UPLOAD FILE
# ======================
uploaded_file = st.file_uploader("Upload TLL File")

def parse_file(file_bytes):
    try:
        root = ET.fromstring(file_bytes)

        data_node = root.find(".//legacybroadcast")
        if data_node is not None:
            data = json.loads(data_node.text)
            channels = data.get("channelList", [])

            return [
                {
                    "name": c.get("channelName", ""),
                    "freq": c.get("frequency", ""),
                }
                for c in channels
            ]

    except:
        pass

    # fallback text
    text = file_bytes.decode("utf-8", errors="ignore")
    items = re.findall(r'vchName>(.*?)</vchName>', text)

    return [{"name": i, "freq": ""} for i in items]


# ======================
# LOAD
# ======================
if uploaded_file:
    data = parse_file(uploaded_file.read())

    st.session_state.channels = data
    st.session_state.order = list(range(len(data)))

# ======================
# CHANNELS
# ======================
channels = st.session_state.channels

# ======================
# SORT MODE
# ======================
mode = st.radio("Sort Mode", ["Manual", "By Category"])

# ======================
# CATEGORY PRIORITY
# ======================
priority = st.multiselect("Category Order", CATEGORIES)

for c in CATEGORIES:
    if c not in priority:
        priority.append(c)

# ======================
# APPLY SORT
# ======================
def get_cat(ch):
    return ai_classify(ch["name"])

if channels:

    if mode == "By Category":
        channels = sorted(
            channels,
            key=lambda x: (priority.index(get_cat(x)), x["name"])
        )

    # ======================
    # MANUAL SORT (Simple reorder)
    # ======================
    st.write("## Channels")

    new_list = []

    for i, ch in enumerate(channels):
        col1, col2, col3 = st.columns([6,2,2])

        with col1:
            st.write(f"{ch['name']}")

        with col2:
            st.write(get_cat(ch))

        with col3:
            if st.button("⬆", key=f"up{i}"):
                if i > 0:
                    channels[i], channels[i-1] = channels[i-1], channels[i]
                    st.rerun()

        new_list.append(ch)

    st.session_state.channels = channels

# ======================
# EXPORT
# ======================
st.write("---")

if st.button("Generate TXT"):
    txt = "CHANNEL LIST\n\n"

    for i, ch in enumerate(st.session_state.channels, 1):
        txt += f"{i:03d} | {ch['name']} | {ai_classify(ch['name'])}\n"

    st.download_button(
        "Download TXT",
        txt,
        file_name="channels.txt"
    )

if st.button("Generate TLL"):
    xml = "<CHANNELS>\n"

    for i, ch in enumerate(st.session_state.channels, 1):
        xml += f"""
        <ITEM>
            <prNum>{i}</prNum>
            <vchName>{ch['name']}</vchName>
            <frequency>{ch['freq']}</frequency>
        </ITEM>
        """

    xml += "\n</CHANNELS>"

    st.download_button(
        "Download TLL",
        xml,
        file_name="GlobalClone00001.TLL"
    )
