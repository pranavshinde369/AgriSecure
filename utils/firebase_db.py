import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firebase only once
if not firebase_admin._apps:

    firebase_secrets = None
    try:
        firebase_secrets = st.secrets.get("firebase", None)
    except Exception:
        firebase_secrets = None

    if firebase_secrets:
        # Streamlit Cloud (or local secrets.toml)
        cred = credentials.Certificate(dict(firebase_secrets))
    else:
        # Local development fallback
        cred = credentials.Certificate("firebase/firebase_key.json")

    firebase_admin.initialize_app(cred)

db = firestore.client()


def log_result(check_type, input_value, result, confidence):
    db.collection("logs").add({
        "type": check_type,
        "input": input_value,
        "result": result,
        "confidence": confidence,
        "timestamp": datetime.utcnow()
    })


def get_impact_stats():
    docs = db.collection("logs").stream()

    total = 0
    scams = 0
    text = 0
    url = 0

    for doc in docs:
        data = doc.to_dict()
        total += 1

        if data["type"] == "text":
            text += 1
        elif data["type"] == "url":
            url += 1

        if "scam" in data["result"].lower() or "phishing" in data["result"].lower():
            scams += 1

    return {
        "total_checks": total,
        "scams_detected": scams,
        "text_checks": text,
        "url_checks": url
    }
