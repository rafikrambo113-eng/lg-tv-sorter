# app.py - Simplified Complete Version
import streamlit as st
import xml.etree.ElementTree as ET
import json
import re
import os

if 'lang' not in st.session_state: st.session_state.lang = 'ar'
if 'theme' not in st.session_state: st.session_state.theme = 'dark'

UI_TEXT = {
    'ar': {'title': "📺 RAMBO ULTRA", 'mode_edit': "🛸 تعديل ملف", 'mode_gen': "⚛️ توليد جديد', 'btn_tll': '📥 تحميل TLL', 'btn_csv': '📥 تحميل CSV', 'lg_tip': 'Settings ← Channels ← Select All ← Restore'},
    'en': {'title': "📺 RAMBO ULTRA", 'mode_edit': "🛸 Edit File", 'mode_gen': "⚛️ Generate New", 'btn_tll': '📥 Download TLL', 'btn_csv': '📥 Download CSV', 'lg_tip': 'Settings ← Channels ← Select All ← Restore'}
}

st.set_page_config(page_title="RAMBO ULTRA", page_icon="📡")
t = UI_TEXT[st.session_state.lang]

BG, BG2, CYAN, PINK = "#06020f", "#0d0520", "#00e5ff", "#ff0066"
st.markdown(f"<h1 style='text-align:center;background:linear-gradient(90deg,{CYAN},{PINK});-webkit-background-clip:text;-webkit-text-fill-color:transparent'>RAMBO ULTRA</h1>", unsafe_allow_html=True)

def get_db(): return {
    "MBC1 HD": {"freq": 11938, "pol": "V"}, "MBC2 HD": {"freq": 11938, "pol": "V"},
    "MBC3 HD": {"freq": 11938, "pol": "V"}, "MBC DRAMA": {"freq": 11938, "pol": "V"},
    "NILE NEWS": {"freq": 11179, "pol": "V"}, "NILE TV": {"freq": 11179, "pol": "V"},
    "DREAM TV": {"freq": 11843, "pol": "H"}, "ON TIME SPORTS 1": {"freq": 11861, "pol": "V"},
    "ON TIME SPORTS 2": {"freq": 11843, "pol": "V"}, "ROTANA CINEMA": {"freq": 11843, "pol": "H"},
    "ROTANA DRAMA": {"freq": 11843, "pol": "H"}, "BEIN SPORTS 1": {"freq": 12226, "pol": "H"},
    "EGYPT QURAN": {"freq": 11179, "pol": "V"}, "AL MAJD": {"freq": 12054, "pol": "H"},
    "SPACE TOON": {"freq": 11977, "pol": "H"}, "AL JAZEERA": {"freq": 11938, "pol": "H"},
}

DB = get_db()
st.sidebar.title("🛠️ Mode")
mode = st.sidebar.radio("Choisir:", [t['mode_edit'], t['mode_gen']])

ch_map = {}
if mode == t['mode_gen']:
    if st.button("🚀 Generate"):
        for i, (n, d) in enumerate(DB.items(), 1):
            ch_map[n] = {"id": i, "name": n, "freq": d["freq"], "pol": d["pol"]}
        st.success(f"✅ {len(ch_map)} channels ready!")

if ch_map:
    # Generate TLL
    items = []
    for ch in ch_map.values():
        items.append(f"<ITEM><prNum>{ch['id']}</prNum><vchName>{ch['name']}</vchName><frequency>{ch['freq']}</frequency><polarization>{ch['pol']}</polarization></ITEM>")
    tll_content = "\n".join(items).encode('utf-8')
    
    # Generate CSV - SORT FILE
    import csv
    from io import StringIO
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["#", "Channel", "Frequency", "Polarization", "Category"])
    for ch in ch_map.values():
        writer.writerow([ch['id'], ch['name'], ch['freq'], ch['pol'], "General"])
    csv_content = output.getvalue().encode('utf-8')
    
    st.download_button(t['btn_tll'], tll_content, "GlobalClone00001.TLL")
    st.download_button(t['btn_csv'], csv_content, "channel_sort_order.csv")
    st.info(t['lg_tip'])
