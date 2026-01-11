# 🌾 AgriSecure – AI-based Scam Detection for Farmers

AgriSecure is an AI-powered web application designed to protect farmers from **fraudulent SMS/WhatsApp messages, phishing websites, and scam screenshots** related to government subsidies, loans, and schemes.  
The solution combines **Machine Learning, Computer Vision (OCR), and Google Firebase** to provide real-time scam detection with impact tracking.

---

## 🚀 Problem Statement

Farmers are frequently targeted by scammers through:
- Fake subsidy messages
- Phishing websites impersonating government portals
- Fraudulent WhatsApp screenshots

Due to language barriers, low digital literacy, and lack of verification tools, farmers often fall victim to financial fraud.

---

## 💡 Solution Overview

AgriSecure provides:
- **Text Scam Detection** for SMS/WhatsApp messages  
- **URL Phishing Detection** for suspicious websites  
- **Screenshot Scam Detection** using OCR (local deployment)  
- **Hindi & English language support**  
- **Verified Government Subsidy section** with official links  
- **Impact Dashboard** to measure scams detected and frauds prevented  

The application focuses on **simplicity, accessibility, and real-world usability**.

---

## 🧠 Key Features

### 🔴 Fraud Detection
- Detects scam messages using ML-based text classification
- Identifies phishing URLs using structural URL analysis
- Analyzes screenshots by extracting text via OCR and running scam detection

### 🟢 Trusted Government Subsidies
- Displays verified government schemes
- Clickable official `.gov.in` links
- Helps farmers cross-check suspicious messages

### 📊 Impact Dashboard
- Total checks performed
- Scams detected
- Fraud prevention insights
- Powered by Google Firebase Firestore

### 🌐 Language Support
- English 🇬🇧
- Hindi 🇮🇳

---


---

## 🧪 Machine Learning Details

### Text Scam Detection
- Type: Supervised Learning (Binary Classification)
- Features: TF-IDF Vectorization
- Output: Scam / Safe + Confidence Score
- Priority: High recall to minimize missed scams

### URL Phishing Detection
- Type: Supervised Learning
- Features: URL length, structure, special characters
- Output: Phishing / Legitimate

### Screenshot Scam Detection
- OCR extracts text from images
- Extracted text passed to Text Scam Detection model
- Implemented for **local deployment**

---

## 🔧 Technologies Used

### AI / ML
- Python
- Scikit-learn
- TF-IDF Vectorization
- OCR (Tesseract – Local)

### Google Technologies
- **Google Firebase (Firestore)** – Logging & impact tracking
- Google Cloud compatible architecture

### Frontend
- Streamlit

### Other Libraries
- Joblib
- Pillow
- Pytesseract
- Pandas / NumPy

---



