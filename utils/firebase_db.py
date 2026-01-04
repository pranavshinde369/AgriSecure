import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase/firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def log_result(check_type, input_value, result, confidence):
    """
    Log prediction result to Firestore
    """
    db.collection("logs").add({
        "type": check_type,          # "text" or "url"
        "input": input_value,
        "result": result,            # Scam / Safe
        "confidence": confidence,
        "timestamp": datetime.utcnow()
    })


def get_impact_stats():
    """
    Fetch impact metrics from Firestore
    """
    docs = db.collection("logs").stream()

    total_checks = 0
    scam_count = 0
    text_checks = 0
    url_checks = 0

    for doc in docs:
        data = doc.to_dict()
        total_checks += 1

        if data["type"] == "text":
            text_checks += 1
        elif data["type"] == "url":
            url_checks += 1

        if "scam" in data["result"].lower() or "phishing" in data["result"].lower():
            scam_count += 1

    return {
        "total_checks": total_checks,
        "scams_detected": scam_count,
        "text_checks": text_checks,
        "url_checks": url_checks
    }
