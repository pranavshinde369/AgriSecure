import streamlit as st
import joblib

from utils.url_predict import predict_url


# Load TEXT model

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



# Language Dictionary

TEXT = {
    "English": {
        "title": "🌾 AgriSecure",
        "subtitle": "AI-based Scam Detection for Farmers",
        "mode": "Select Check Type",
        "msg": "WhatsApp / SMS Message",
        "url": "Website URL",
        "btn": "Check",
        "scam": "🚨 Scam Detected",
        "safe": "✅ Safe",
        "risk": "Risk Level",
        "confidence": "Confidence"
    },
    "Hindi": {
        "title": "🌾 एग्रीसिक्योर",
        "subtitle": "किसानों के लिए एआई आधारित धोखाधड़ी पहचान",
        "mode": "जांच का प्रकार चुनें",
        "msg": "व्हाट्सएप / एसएमएस संदेश",
        "url": "वेबसाइट लिंक",
        "btn": "जांच करें",
        "scam": "🚨 धोखाधड़ी",
        "safe": "✅ सुरक्षित",
        "risk": "जोखिम स्तर",
        "confidence": "विश्वास स्तर"
    }
}


# Streamlit UI

st.set_page_config(page_title="AgriSecure", page_icon="🌾")

language = st.selectbox("🌐 Language / भाषा", ["English", "Hindi"])
t = TEXT[language]

st.title(t["title"])
st.write(t["subtitle"])

mode = st.radio(t["mode"], [t["msg"], t["url"]])

# MESSAGE CHECK

if mode == t["msg"]:
    message = st.text_area(t["msg"])

    if st.button(t["btn"]):
        if message.strip() == "":
            st.warning("Please enter a message")
        else:
            label, prob, risk = predict_message(message)

            if label == "scam":
                st.error(t["scam"])
            else:
                st.success(t["safe"])

            st.write(f"**{t['risk']}:** {risk.upper()}")
            st.write(f"**{t['confidence']}:** {prob}")


# URL CHECK

if mode == t["url"]:
    url = st.text_input(t["url"])

    if st.button(t["btn"]):
        if url.strip() == "":
            st.warning("Please enter a URL")
        else:
            result, prob = predict_url(url)

            if "Phishing" in result:
                st.error(t["scam"])
            else:
                st.success(t["safe"])

            st.write(f"**{t['confidence']}:** {prob}")
