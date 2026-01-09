import streamlit as st
import joblib

from utils.url_predict import predict_url
from utils.firebase_db import log_result, get_impact_stats
from utils.ocr import extract_text_from_image


# -------------------------------------------------
# AI-Curated Government Subsidies (Verified Sources)
# -------------------------------------------------

SUBSIDIES = [
    {
        "name": "PM-Kisan Samman Nidhi",
        "desc": "₹6000 yearly income support for eligible farmers.",
        "link": "https://pmkisan.gov.in"
    },
    {
        "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "desc": "Crop insurance against natural calamities and crop loss.",
        "link": "https://pmfby.gov.in"
    },
    {
        "name": "Kisan Credit Card (KCC)",
        "desc": "Low-interest credit facility for farmers.",
        "link": "https://www.myscheme.gov.in/schemes/kcc"
    },
    {
        "name": "Soil Health Card Scheme",
        "desc": "Soil testing and fertilizer recommendations.",
        "link": "https://soilhealth.dac.gov.in"
    },
    {
        "name": "PM Krishi Sinchai Yojana",
        "desc": "Improves irrigation and water efficiency.",
        "link": "https://pmksy.gov.in"
    },
    {
        "name": "PM-KUSUM Yojana",
        "desc": "Support for solar pumps and renewable energy.",
        "link": "https://pmkusum.mnre.gov.in"
    },
    {
        "name": "e-NAM (National Agriculture Market)",
        "desc": "Online trading platform for better crop prices.",
        "link": "https://www.enam.gov.in"
    }
]


# -------------------------------------------------
# Load Text Scam Detection Model
# -------------------------------------------------

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


# -------------------------------------------------
# Language Dictionary
# -------------------------------------------------

TEXT = {
    "English": {
        "title": "🌾 AgriSecure",
        "subtitle": "AI-based Scam Detection for Farmers",
        "about": "AgriSecure helps farmers identify scam messages, phishing websites, "
                 "and suspicious screenshots related to subsidies, loans, and government schemes.",
        "dashboard": "Impact Dashboard",
        "total": "Total Checks",
        "scams": "Scams Detected",
        "prevented": "Frauds Prevented",
        "breakdown": "Text: {text} | URL: {url}",
        "mode": "Select Check Type",
        "msg": "WhatsApp / SMS Message",
        "url": "Website URL",
        "img": "Screenshot (Image)",
        "placeholder_msg": "Example: Your PM-Kisan subsidy is pending. Verify now...",
        "placeholder_url": "Example: http://verify-account-now.com/login",
        "btn": "Check",
        "analyze": "Analyze Screenshot",
        "scam": "🚨 Scam Detected",
        "safe": "✅ Safe",
        "risk": "Risk Level",
        "confidence": "Confidence",
        "warning": "Please enter input",
        "ocr_warning": "No readable text detected in image",
        "footer": "⚠️ Educational demo for awareness. Accuracy is not guaranteed.",
        "dev": "Developed by ViperVision"
    },

    "Hindi": {
        "title": "🌾 एग्रीसिक्योर",
        "subtitle": "किसानों के लिए एआई आधारित धोखाधड़ी पहचान",
        "about": "एग्रीसिक्योर किसानों को सब्सिडी, ऋण और सरकारी योजनाओं से जुड़े "
                 "फर्जी संदेशों, वेबसाइटों और स्क्रीनशॉट की पहचान करने में मदद करता है।",
        "dashboard": "प्रभाव डैशबोर्ड",
        "total": "कुल जांच",
        "scams": "पाई गई धोखाधड़ी",
        "prevented": "रोकी गई धोखाधड़ी",
        "breakdown": "संदेश: {text} | लिंक: {url}",
        "mode": "जांच का प्रकार चुनें",
        "msg": "व्हाट्सएप / एसएमएस संदेश",
        "url": "वेबसाइट लिंक",
        "img": "स्क्रीनशॉट (चित्र)",
        "placeholder_msg": "उदाहरण: आपकी पीएम-किसान सब्सिडी लंबित है, अभी सत्यापित करें...",
        "placeholder_url": "उदाहरण: http://verify-account-now.com/login",
        "btn": "जांच करें",
        "analyze": "स्क्रीनशॉट जांचें",
        "scam": "🚨 धोखाधड़ी पाई गई",
        "safe": "✅ सुरक्षित",
        "risk": "जोखिम स्तर",
        "confidence": "विश्वास स्तर",
        "warning": "कृपया जानकारी दर्ज करें",
        "ocr_warning": "चित्र से पाठ नहीं पढ़ा जा सका",
        "footer": "⚠️ यह केवल जागरूकता के लिए एक डेमो है।",
        "dev": "वाइपरविजन द्वारा विकसित"
    }
}


# -------------------------------------------------
# Streamlit UI
# -------------------------------------------------

st.set_page_config(page_title="AgriSecure", page_icon="🌾")

language = st.selectbox("🌐 Language / भाषा", ["English", "Hindi"])
t = TEXT[language]

st.title(t["title"])
st.write(t["subtitle"])
st.info(f"🌾 {t['about']}")

st.markdown("---")


# -------------------------------------------------
# Impact Dashboard
# -------------------------------------------------

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


# -------------------------------------------------
# TWO MAIN SECTIONS (TABS)
# -------------------------------------------------

tab1, tab2 = st.tabs(["🚨 Fraud Detection", "🌾 Real Government Subsidies"])


# =========================
# TAB 1 — FRAUD DETECTION
# =========================

with tab1:

    mode = st.radio(
        t["mode"],
        [t["msg"], t["url"], t["img"]]
    )

    # TEXT MESSAGE CHECK
    if mode == t["msg"]:
        message = st.text_area(t["msg"], placeholder=t["placeholder_msg"])

        if st.button(t["btn"]):
            if message.strip() == "":
                st.warning(t["warning"])
            else:
                label, prob, risk = predict_message(message)
                log_result("text", message, label, prob)

                st.error(t["scam"]) if label == "scam" else st.success(t["safe"])
                st.write(f"**{t['risk']}:** {risk.upper()}")
                st.write(f"**{t['confidence']}:** {prob}")

    # URL CHECK
    if mode == t["url"]:
        url = st.text_input(t["url"], placeholder=t["placeholder_url"])

        if st.button(t["btn"]):
            if url.strip() == "":
                st.warning(t["warning"])
            else:
                result, prob = predict_url(url)
                log_result("url", url, result, prob)

                st.error(t["scam"]) if "phishing" in result.lower() else st.success(t["safe"])
                st.write(f"**{t['confidence']}:** {prob}")

    # SCREENSHOT CHECK
    if mode == t["img"]:
        uploaded_file = st.file_uploader(
            "Upload WhatsApp / SMS Screenshot",
            type=["png", "jpg", "jpeg"]
        )

        if uploaded_file:
            extracted_text = extract_text_from_image(uploaded_file)

            if extracted_text == "":
                st.warning(
                    "📸 Screenshot analysis is available in local deployment. "
                    "Cloud demo shows feature preview only."
                )


            st.text_area("📄 Extracted Text (OCR)", extracted_text, height=150)

            if st.button(t["analyze"]):
                if extracted_text.strip() == "":
                    st.warning(t["ocr_warning"])
                else:
                    label, prob, risk = predict_message(extracted_text)
                    log_result("screenshot", extracted_text, label, prob)

                    st.error("🚨 Scam Detected from Screenshot") if label == "scam" else st.success("✅ Screenshot looks Safe")
                    st.write(f"**{t['risk']}:** {risk.upper()}")
                    st.write(f"**{t['confidence']}:** {prob}")
                    st.caption("Future Scope: Real-time on-device screen monitoring, even offline.")


# =========================
# TAB 2 — REAL SUBSIDIES
# =========================

with tab2:
    st.subheader("🌾 Verified Government Subsidies")

    st.info(
        "These are real government schemes from official sources. "
        "Use them to verify any message you receive."
    )

    for s in SUBSIDIES:
        st.markdown(
            f"### {s['name']}\n"
            f"{s['desc']}\n"
            f"🔗 [Official Website]({s['link']})"
        )

    st.caption("Always trust official government portals (.gov.in).")


# -------------------------------------------------
# Footer
# -------------------------------------------------

st.markdown("---")
st.caption(t["footer"])
st.caption(t["dev"])
