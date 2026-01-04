from utils.url_predict import predict_url

urls = [
    "http://subsidy-farm-login.com",
    "http://verify-bank-account-now.net/login",
    "http://free-reward-claim-now.net",
    "http://pm-kisan-benefit-verify.in/login",
    "http://farmer-subsidy-update.gov.in.verify-account.com",
    "http://agri-scheme-apply-now.net",
    "http://pmfby-claim-check.in/verify",
    "http://sbi-secure-login-alert.com",
    "https://www.google.com",
    "https://www.mahagov.in"
]

for u in urls:
    label, confidence = predict_url(u)
    print(f"\nURL: {u}")
    print(f"Prediction: {label} | Confidence: {confidence}")
