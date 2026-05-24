import streamlit as st
import xml.etree.ElementTree as ET
import json

# 1. إعدادات واجهة الموقع وهويته (ألوان قريبة من LG)
st.set_page_config(page_title="LGAISort - منسق قنوات LG الذكي", page_icon="📺", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f7f9fa; }
    h1 { color: #a50034; text-align: center; font-family: 'Cairo', sans-serif; }
    .stButton>button { background-color: #a50034; color: white; border-radius: 8px; width: 100%; }
    </style>
""", unsafe_style_code=True)

st.title("📺 LGAISort - المنسق الذكي لشاشات LG webOS")
st.subheader("ارفع ملف القنوات (.TLL)، سيتعرف الذكاء الاصطناعي على الفئات ويحدث الترددات فوراً!")

# محاكاة قاعدة البيانات الحية للترددات المحدثة
LIVE_SATELLITE_DB = {
    "QATAR TV HD": {"frequency": 10834, "polarization": "Horizontal", "symbolRate": 27500},
    "AL RAHMA": {"frequency": 10873, "polarization": "Vertical", "symbolRate": 27500},
    "ELKHOLASA MOSALSALAT": {"frequency": 10873, "polarization": "Vertical", "symbolRate": 27500},
    "MBC 2": {"frequency": 11938, "polarization": "Vertical", "symbolRate": 27500}, 
    "CTV": {"frequency": 12022, "polarization": "Vertical", "symbolRate": 27500}
}

# قائمة الفئات الافتراضية للذكاء الاصطناعي
def ai_classify(channel_name):
    name = channel_name.upper()
    if any(w in name for w in ["CTV", "AGHAPY", "MESAT", "KARMA", "NOURSAT"]): return "⛪ ديني مسيحي"
    if any(w in name for w in ["QURAN", "RAHMA", "MAJD", "MAKKA"]): return "🕌 ديني إسلامي"
    if any(w in name for w in ["MOSALSALAT", "DRAMA", "SERIES"]): return "🎬 مسلسلات ودراما"
    if any(w in name for w in ["CINEMA", "ROTANA", "AFLAM", "MIX", "FOX"]): return "🍿 أفلام عربية وأجنبية"
    if any(w in name for w in ["SPACE TOON", "CN", "MAJID", "KIDS", "TOM"]): return "👶 أطفال وكرتون"
    if any(w in name for w in ["SPORT", "ONTIME", "KASS", "AD_SPORTS"]): return "⚽ رياضة"
    if any(w in name for w in ["NEWS", "JAZEERA", "ARABIYA", "HADATH", "CAIRO"]): return "📰 أخبار وسياسة"
    return "📺 قنوات عامة ومنوعات"

# 2. منطقة رفع الملف من المستخدم
uploaded_file = st.file_uploader("اختر ملف GlobalClone00001.TLL من الفلاشة:", type=["TLL"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    
    # خيار تحديث الترددات الاختياري
    update_freq = st.checkbox("⚡ تفعيل ميزة تحديث الترددات القديمة تلقائياً مقارنة بالقمر الصناعي")
    
    # قراءة ومعالجة الملف
    root = ET.fromstring(file_bytes)
    country_setting = root.find(".//BroadcastCountrySetting").text
    legacy_broadcast_tag = root.find(".//legacybroadcast")
    broadcast_data = json.loads(legacy_broadcast_tag.text)
    channels = broadcast_data.get("channelList", [])
    
    st.info(f"✅ تم قراءة الملف بنجاح. بلد البث المهيأ في الشاشة: **{country_setting}** (يدعم الترتيب الحر).")
    
    # تصنيف وفلترة القنوات
    categorized = {}
    report_changes = []
    
    for ch in channels:
        name = ch.get("channelName", "")
        cat = ai_classify(name)
        if cat not in categorized: categorized[cat] = []
        categorized[cat].append(name)
        
        # إذا تم تفعيل تحديث الترددات
        if update_freq and name.upper() in LIVE_SATELLITE_DB:
            live = LIVE_SATELLITE_DB[name.upper()]
            if ch.get("frequency") != live["frequency"]:
                report_changes.append({"القناة": name, "التردد القديم": ch.get("frequency"), "التردد الجديد": live["frequency"]})
                ch["frequency"] = live["frequency"]
                ch["polarization"] = live["polarization"]
                ch["symbolRate"] = live["symbolRate"]

    # 3. الميزة اللي طلبتها: عرض الفئات، عدد قنواتها، وأسمائها
    st.write("### 📊 استعراض القنوات المكتشفة داخل كل فئة:")
    col1, col2 = st.columns(2)
    
    for i, (cat_name, ch_list) in enumerate(categorized.items()):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            with st.expander(f"{cat_name} — (يحتوي على {len(ch_list)} قناة)"):
                st.write(", ".join(ch_list))
                
    # عرض جدول التحديثات لو وُجدت
    if update_freq and report_changes:
        st.write("### 🔁 جدول الترددات التي تم صيانته وتحديثها:")
        st.table(report_changes)
        
    # 4. إعادة الترتيب وبناء الملف للتحميل
    # (الترتيب الافتراضي: مسيحي -> إسلامي -> مسلسلات -> أفلام -> أطفال -> رياضة -> أخبار -> عامة)
    priority_order = ["⛪ ديني مسيحي", "🕌 ديني إسلامي", "🎬 مسلسلات ودراما", "🍿 أفلام عربية وأجنبية", "👶 أطفال وكرتون", "⚽ رياضة", "📰 أخبار وسياسة", "📺 قنوات عامة ومنوعات"]
    
    channels_sorted = sorted(channels, key=lambda x: priority_order.index(ai_classify(x.get("channelName", ""))))
    
    # إعادة ترقيم القنوات من 1 تصاعدياً
    for index, ch in enumerate(channels_sorted, start=1):
        ch["majorNumber"] = index
        
    broadcast_data["channelList"] = channels_sorted
    legacy_broadcast_tag.text = json.dumps(broadcast_data, ensure_ascii=False)
    final_xml = ET.tostring(root, encoding="utf-8")
    
    st.write("---")
    st.success("🎉 الملف جاهز ومُنظم الآن تماماً حسب أولوياتك المتناسقة!")
    st.download_button(
        label="📥 اضغط هنا لتحميل ملف القنوات الجديد المعدل",
        data=final_xml,
        file_name="GlobalClone00001.TLL",
        mime="application/octet-stream"
    )
