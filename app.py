import streamlit as st
import joblib

from utils.url_predict import predict_url
from utils.firebase_db import log_result, get_impact_stats


# -------------------------------
# Load TEXT model
# -------------------------------

text_model = joblib.load("models/text_scam_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")


def predict_message(message):
    vec = vectorizer.transform([message])
    prob = text_model.predict_proba(vec)[0][1]

    if prob > 0.5:
        label = "scam"
        risk = "high" if prob > 0.7 else "medium"
    else:
        label = "safe"
        risk = "low"

    return label, round(prob, 2), risk


# -------------------------------
# Language Dictionary
# -------------------------------

TEXT = {
    "English": {
        "title": "🌾 AgriSecure",
        "subtitle": "AI-based Scam Detection for Farmers",
        "about": "AgriSecure helps farmers identify scam messages and fake websites related to subsidies, loans, and government schemes in English & Hindi.",
        "dashboard": "Impact Dashboard",
        "total": "Total Checks",
        "scams": "Scams Detected",
        "prevented": "Frauds Prevented",
        "breakdown": "Text Checks: {text} | URL Checks: {url}",
        "mode": "Select Check Type",
        "msg": "WhatsApp / SMS Message",
        "url": "Website URL",
        "placeholder_msg": "Example: Your PM-Kisan subsidy is pending. Verify now...",
        "placeholder_url": "Example: http://verify-account-now.com/login",
        "btn": "Check",
        "scam": "🚨 Scam Detected",
        "safe": "✅ Safe",
        "risk": "Risk Level",
        "confidence": "Confidence",
        "warning": "Please enter input",
        "footer": "⚠️ Educational demo for awareness. AgriSecure does not guarantee 100% accuracy.",
        "dev": "Developed by ViperVision"
    },

    "Hindi": {
        "title": "🌾 एग्रीसिक्योर",
        "subtitle": "किसानों के लिए एआई आधारित धोखाधड़ी पहचान",
        "about": "एग्रीसिक्योर किसानों को सब्सिडी, ऋण और सरकारी योजनाओं से जुड़े फर्जी संदेशों और वेबसाइटों की पहचान करने में मदद करता है।",
        "dashboard": "प्रभाव डैशबोर्ड",
        "total": "कुल जांच",
        "scams": "पाई गई धोखाधड़ी",
        "prevented": "रोकी गई धोखाधड़ी",
        "breakdown": "संदेश जांच: {text} | लिंक जांच: {url}",
        "mode": "जांच का प्रकार चुनें",
        "msg": "व्हाट्सएप / एसएमएस संदेश",
        "url": "वेबसाइट लिंक",
        "placeholder_msg": "उदाहरण: आपकी पीएम-किसान सब्सिडी लंबित है, अभी सत्यापित करें...",
        "placeholder_url": "उदाहरण: http://verify-account-now.com/login",
        "btn": "जांच करें",
        "scam": "🚨 धोखाधड़ी पाई गई",
        "safe": "✅ सुरक्षित",
        "risk": "जोखिम स्तर",
        "confidence": "विश्वास स्तर",
        "warning": "कृपया जानकारी दर्ज करें",
        "footer": "⚠️ यह केवल जागरूकता के लिए एक डेमो है। एग्रीसिक्योर 100% सटीकता की गारंटी नहीं देता।",
        "dev": "वाइपरविजन द्वारा विकसित"
    }
}


# -------------------------------
# Streamlit UI
# -------------------------------

st.set_page_config(page_title="AgriSecure", page_icon="🌾")

language = st.selectbox("🌐 Language / भाषा", ["English", "Hindi"])
t = TEXT[language]

st.title(t["title"])
st.write(t["subtitle"])
st.info(f"🌾 {t['about']}")

st.markdown("---")

# -------------------------------
# Impact Dashboard
# -------------------------------

st.subheader(f"📊 {t['dashboard']}")

stats = get_impact_stats()

col1, col2, col3 = st.columns(3)
col1.metric(t["total"], stats["total_checks"])
col2.metric(t["scams"], stats["scams_detected"])
col3.metric(t["prevented"], stats["scams_detected"])

st.caption(
    t["breakdown"].format(
        text=stats["text_checks"],
        url=stats["url_checks"]
    )
)

st.markdown("---")

# -------------------------------
# Mode Selection
# -------------------------------

mode = st.radio(t["mode"], [t["msg"], t["url"]])


# -------------------------------
# MESSAGE CHECK
# -------------------------------

if mode == t["msg"]:
    message = st.text_area(
        t["msg"],
        placeholder=t["placeholder_msg"]
    )

    if st.button(t["btn"]):
        if message.strip() == "":
            st.warning(t["warning"])
        else:
            label, prob, risk = predict_message(message)

            log_result(
                check_type="text",
                input_value=message,
                result=label,
                confidence=prob
            )

            if label == "scam":
                st.error(t["scam"])
            else:
                st.success(t["safe"])

            st.write(f"**{t['risk']}:** {risk.upper()}")
            st.write(f"**{t['confidence']}:** {prob}")


# -------------------------------
# URL CHECK
# -------------------------------

if mode == t["url"]:
    url = st.text_input(
        t["url"],
        placeholder=t["placeholder_url"]
    )

    if st.button(t["btn"]):
        if url.strip() == "":
            st.warning(t["warning"])
        else:
            result, prob = predict_url(url)

            log_result(
                check_type="url",
                input_value=url,
                result=result,
                confidence=prob
            )

            if "phishing" in result.lower():
                st.error(t["scam"])
            else:
                st.success(t["safe"])

            st.write(f"**{t['confidence']}:** {prob}")


# -------------------------------
# Footer
# -------------------------------

st.markdown("---")
st.caption(t["footer"])
st.caption(t["dev"])
