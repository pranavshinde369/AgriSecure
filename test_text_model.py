import joblib

# Load model and vectorizer
model = joblib.load("models/text_scam_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

def predict_message(message):
    vec = vectorizer.transform([message])
    prob = model.predict_proba(vec)[0][1]

    if prob > 0.5:
        return "Scam", prob
    else:
        return "Safe", prob

# ===== TEST MESSAGES =====
messages = [
    "You get interest free loan click to claim immediate ",
    "You have free gift of fertilizer claim now ",
    "Urgent! Your bank account will be blocked. Verify immediately"
]

for msg in messages:
    label, prob = predict_message(msg)
    print(f"\nMessage: {msg}")
    print(f"Prediction: {label}, Confidence: {round(prob,2)}")
