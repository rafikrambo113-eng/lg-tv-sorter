import streamlit as st
import csv
from io import StringIO

if 'lang' not in st.session_state:
    st.session_state.lang = 'ar'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# نصوص الواجهة
UI_TEXT = {
    'ar': {
        'title': "RAMBO ULTRA",
        'mode_edit': "تعديل ملف",
        'mode_gen': "توليد جديد",
        'btn_tll': "تحميل TLL",
        'btn_csv': "تحميل CSV",
        'lg_tip': "Settings - Channels - Select All - Restore",
    },
    'en': {
        'title': "RAMBO ULTRA",
        'mode_edit': "Edit File",
        'mode_gen': "Generate New",
        'btn_tll': "Download TLL",
        'btn_csv': "Download CSV",
        'lg_tip': "Settings - Channels - Select All - Restore",
    }
}

st.set_page_config(page_title="RAMBO ULTRA", page_icon="📡")
t = UI_TEXT[st.session_state.lang]

# CSS
st.markdown("""
<style>
h1 {text-align:center; background: linear-gradient(90deg, #00e5ff, #ff0066); -webkit-background-clip: text; -webkit-text-fill-color: transparent}
</style>
""", unsafe_allow_html=True)

st.title(t['title'])

# بنك القنوات
def get_channels():
    return {
        "MBC1 HD": {"freq": 11938, "pol": "V"},
        "MBC2 HD": {"freq": 11938, "pol": "V"},
        "MBC3 HD": {"freq": 11938, "pol": "V"},
        "MBC DRAMA": {"freq": 11938, "pol": "V"},
        "NILE NEWS": {"freq": 11179, "pol": "V"},
        "NILE TV": {"freq": 11179, "pol": "V"},
        "DREAM TV": {"freq": 11843, "pol": "H"},
        "ON TIME SPORTS 1": {"freq": 11861, "pol": "V"},
        "ON TIME SPORTS 2": {"freq": 11843, "pol": "V"},
        "ROTANA CINEMA": {"freq": 11843, "pol": "H"},
        "ROTANA DRAMA": {"freq": 11843, "pol": "H"},
        "BEIN SPORTS 1": {"freq": 12226, "pol": "H"},
        "EGYPT QURAN": {"freq": 11179, "pol": "V"},
        "AL MAJD": {"freq": 12054, "pol": "H"},
        "SPACE TOON": {"freq": 11977, "pol": "H"},
        "AL JAZEERA": {"freq": 11938, "pol": "H"},
    }

ch_map = {}
if st.button("🚀 توليد / Generate"):
    DB = get_channels()
    for i, (name, data) in enumerate(DB.items(), 1):
        ch_map[name] = {
            "id": i,
            "name": name,
            "freq": data["freq"],
            "pol": data["pol"]
        }
    st.success(f"✅ جاهز: {len(ch_map)} قناة")

if ch_map:
    # 1. ملف TLL
    items = []
    for ch in ch_map.values():
        items.append(
            f"<ITEM><prNum>{ch['id']}</prNum><vchName>{ch['name']}</vchName>"
            f"<frequency>{ch['freq']}</frequency><polarization>{ch['pol']}</polarization></ITEM>"
        )
    tll_content = "\n".join(items).encode("utf-8")
    
    # 2. ملف CSV - ترتيب القنوات
    csv_output = StringIO()
    csv_writer = csv.writer(csv_output)
    csv_writer.writerow(["#", "Channel Name", "Frequency", "Polarization", "Category"])
    for ch in ch_map.values():
        csv_writer.writerow([ch['id'], ch['name'], ch['freq'], ch['pol'], "General"])
    csv_content = csv_output.getvalue().encode("utf-8")
    
    st.download_button(t['btn_tll'], tll_content, "GlobalClone00001.TLL")
    st.download_button(t['btn_csv'], csv_content, "channel_sort_order.csv")
    st.info(t['lg_tip'])
