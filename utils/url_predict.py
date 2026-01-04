import joblib
import pandas as pd

# Load trained URL phishing model
url_model = joblib.load("models/url_phishing_model.pkl")

def extract_url_features(url: str):
    """
    Extract EXACT features used during training
    """
    url = url.lower()

    suspicious_words = [
        "login", "verify", "update", "secure", "account",
        "free", "bonus", "reward", "claim",
        "kyc", "blocked", "suspend"
    ]

    return {
        "url_length": len(url),
        "dot_count": url.count("."),
        "digit_count": sum(c.isdigit() for c in url),
        "hyphen_count": url.count("-"),
        "slash_count": url.count("/"),
        "https_present": int(url.startswith("https")),
        "at_symbol": int("@" in url),
        "ip_present": int(url.replace(".", "").isdigit()),
        "suspicious_word_present": int(any(word in url for word in suspicious_words))
    }


def predict_url(url: str):
    """
    Predict whether a URL is Phishing or Legitimate
    Uses calibrated threshold (0.55)
    """
    features = extract_url_features(url)
    X = pd.DataFrame([features])

    prob = url_model.predict_proba(X)[0][1]

    if prob >= 0.55:
        return "🚨 Phishing URL", round(prob, 2)
    else:
        return "✅ Legitimate URL", round(prob, 2)
