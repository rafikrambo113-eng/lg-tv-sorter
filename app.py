import streamlit as st
import xml.etree.ElementTree as ET
import json
import urllib.parse

# 1. إعدادات واجهة الموقع وتغيير الاسم إلى RAMBO
st.set_page_config(page_title="RAMBO - منسق قنوات LG الذكي", page_icon="📺", layout="wide")

# تصميم الألوان ليتماشى مع اسم RAMBO وشاشات LG (أحمر داكن مميز وأنيق)
st.markdown("""
    <style>
    .main { background-color: #f7f9fa; }
    h1 { color: #a50034; text-align: center; font-family: 'Cairo', sans-serif; font-weight: bold; }
    h3 { text-align: center; font-family: 'Cairo', sans-serif; }
    .stButton>button { background-color: #a50034; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    .footer { background-color: #a50034; color: white; padding: 20px; text-align: center; border-radius: 10px; margin-top: 50px; font-family: 'Cairo', sans-serif; }
    .footer a { color: #ffeb3b; text-decoration: none; font-weight: bold; }
    .whatsapp-btn { background-color: #25d366; color: white; padding: 10px 20px; text-align: center; border-radius: 8px; display: inline-block; font-weight: bold; text-decoration: none; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("📺 RAMBO - المنسق الذكي لشاشات LG webOS")
st.subheader("رتب فئات قنواتك باختيارك اليدوي (الفئة التي تختارها أولاً ستكون في صدارة التلفزيون!)")

# قاعدة البيانات الحية للترددات المحدثة
LIVE_SATELLITE_DB = {
    "QATAR TV HD": {"frequency": 10834, "polarization": "Horizontal", "symbolRate": 27500},
    "AL RAHMA": {"frequency": 10873, "polarization": "Vertical", "symbolRate": 27500},
    "ELKHOLASA MOSALSALAT": {"frequency": 10873, "polarization": "Vertical", "symbolRate": 27500},
    "MBC 2": {"frequency": 11938, "polarization": "Vertical", "symbolRate": 27500}, 
    "CTV": {"frequency": 12022, "polarization": "Vertical", "symbolRate": 27500}
}

# دالة التصنيف بالذكاء الاصطناعي والكلمات المفتاحية
def ai_classify(channel_name):
    name = channel_name.upper()
    if any(w in name for w in ["CTV", "AGHAPY", "MESAT", "KARMA", "NOURSAT"]): return "⛪ قنوات مسيحية"
    if any(w in name for w in ["QURAN", "RAHMA", "MAJD", "MAKKA"]): return "🕌 قنوات إسلامية"
    if any(w in name for w in ["MOSALSALAT", "DRAMA", "SERIES", "KHOLASA"]): return "🎬 مسلسلات ودراما"
    if any(w in name for w in ["CINEMA", "ROTANA", "AFLAM", "MIX", "FOX", "MBC2", "ACTION"]): return "🍿 أفلام عربية وأجنبية"
    if any(w in name for w in ["SPACE TOON", "CN", "MAID", "KIDS", "TOM"]): return "👶 أطفال وكرتون"
    if any(w in name for w in ["SPORT", "ONTIME", "KASS", "AD_SPORTS"]): return "⚽ رياضة"
    if any(w in name for w in ["NEWS", "JAZEERA", "ARABIYA", "HADATH", "CAIRO"]): return "📰 أخبار وسياسة"
    return "📺 قنوات عامة ومنوعات"

# قائمة الفئات المتاحة
ALL_AVAILABLE_CATEGORIES = [
    "⛪ قنوات مسيحية", "🕌 قنوات إسلامية", "🎬 مسلسلات ودراما", 
    "🍿 أفلام عربية وأجنبية", "👶 أطفال وكرتون", "⚽ رياضة", 
    "📰 أخبار وسياسة", "📺 قنوات عامة ومنوعات"
]

# رفع الملف
uploaded_file = st.file_uploader("اختر ملف GlobalClone00001.TLL من الفلاشة:", type=["TLL"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    
    # خيار تحديث الترددات الاختياري
    update_freq = st.checkbox("⚡ تفعيل ميزة تحديث الترددات القديمة تلقائياً مقارنة بالقمر الصناعي")
    
    # قراءة الملف
    root = ET.fromstring(file_bytes)
    country_setting = root.find(".//BroadcastCountrySetting").text
    legacy_broadcast_tag = root.find(".//legacybroadcast")
    broadcast_data = json.loads(legacy_broadcast_tag.text)
    channels = broadcast_data.get("channelList", [])
    
    st.info(f"✅ تم قراءة الملف بنجاح. بلد البث المهيأ في الشاشة: **{country_setting}**.")

    st.write("---")
    st.write("### 🎛️ حدد ترتيب الفئات المخصصة لك:")
    st.write("💡 *ملحوظة: اضغط على الفئات بالترتيب الذي تفضله. الفئة التي تضغط عليها أولاً ستأخذ الترتيب الأول في الشاشة.*")
    
    # اختيار تفاعلي يعتمد على ترتيب الضغط للمستخدم
    user_priority = st.multiselect(
        "اضغط هنا واختر الفئات واحدة تلو الأخرى حسب ترتيبك المفضل:",
        options=ALL_AVAILABLE_CATEGORIES,
        default=[]
    )
    
    # بناء القائمة النهائية
    final_priority = list(user_priority)
    for cat in ALL_AVAILABLE_CATEGORIES:
        if cat not in final_priority:
            final_priority.append(cat)

    # معالجة القنوات
    categorized = {}
    report_changes = []
    
    for ch in channels:
        name = ch.get("channelName", "")
        cat = ai_classify(name)
        if cat not in categorized: categorized[cat] = []
        categorized[cat].append(name)
        
        if update_freq and name.upper() in LIVE_SATELLITE_DB:
            live = LIVE_SATELLITE_DB[name.upper()]
            if ch.get("frequency") != live["frequency"]:
                report_changes.append({"القناة": name, "التردد القديم": ch.get("frequency"), "التردد الجديد": live["frequency"]})
                ch["frequency"] = live["frequency"]
                ch["polarization"] = live["polarization"]
                ch["symbolRate"] = live["symbolRate"]

    # عرض الفئات
    st.write("---")
    st.write("### 📊 استعراض القنوات بناءً على ترتيبك الحالي لفئات البث:")
    col1, col2 = st.columns(2)
    for i, cat_name in enumerate(final_priority):
        if cat_name in categorized:
            ch_list = categorized[cat_name]
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                is_user_chosen = "⭐ " if cat_name in user_priority else ""
                with st.expander(f"{is_user_chosen}{cat_name} — (يحتوي على {len(ch_list)} قناة)"):
                    st.write(", ".join(ch_list))
                    
    if update_freq and report_changes:
        st.write("### 🔁 جدول الترددات المحدثة:")
        st.table(report_changes)

    # الترتيب الفعلي للقنوات
    channels_sorted = sorted(channels, key=lambda x: final_priority.index(ai_classify(x.get("channelName", ""))))
    
    # بناء ملف التقرير النصي الترتيبي (.TXT)
    text_report = f"📄 تقرير الترتيب النهائي لقنوات شاشة LG ({country_setting})\n"
    text_report += f"🛠️ ترتيب الفئات المختار: " + " -> ".join([c.split()[-1] for c in final_priority]) + "\n"
    text_report += "==================================================\n\n"
    
    for index, ch in enumerate(channels_sorted, start=1):
        ch["majorNumber"] = index
        ch_name = ch.get("channelName", "Unknown")
        ch_cat = ai_classify(ch_name)
        text_report += f"رقم {index:03d} : القناة: {ch_name:<25} | الفئة: {ch_cat}\n"
        
    broadcast_data["channelList"] = channels_sorted
    legacy_broadcast_tag.text = json.dumps(broadcast_data, ensure_ascii=False)
    final_xml = ET.tostring(root, encoding="utf-8")
    
    # أزرار التحميل
    st.write("---")
    st.success("🎉 الترتيب تم بنجاح! حمل الملفات الآن وضعتها على الفلاشة:")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.download_button(
            label="📥 تحميل ملف القنوات للشاشة (GlobalClone00001.TLL)",
            data=final_xml,
            file_name="GlobalClone00001.TLL",
            mime="application/octet-stream"
        )
    with col_btn2:
        st.download_button(
            label="📄 تحميل تقرير الترتيب كملف نصي (Channels_List.txt)",
            data=text_report,
            file_name="Channels_List.txt",
            mime="text/plain; charset=utf-8"
        )

# 2. إضافة التوقيع، بيانات التواصل وزر الواتساب ويب في أسفل الصفحة (Footer)
st.markdown("---")

whatsapp_msg = urllib.parse.quote("مرحباً رفيق رامبو، قمت باستخدام موقع منسق قنوات LG ولدّي استفسار:")
whatsapp_url = f"https://web.whatsapp.com/send?phone=201280339779&text={whatsapp_msg}"

st.markdown(f"""
    <div class="footer">
        <h3>🛠️ تم العمل بواسطة RAFIK RAMBO</h3>
        <p>📱 <b>الموبايل:</b> +201280339779 | ✉️ <b>البريد الإلكتروني:</b> rafikrambo113@gmail.com</p>
        <p>للتواصل الفوري والاستفسارات اضغط على الزر أدناه:</p>
        <a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">💬 تواصل معنا عبر WhatsApp Web</a>
    </div>
""", unsafe_allow_html=True)
