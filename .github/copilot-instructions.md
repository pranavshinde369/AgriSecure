# Copilot / AI Agent Instructions

Purpose: Quick reference to make AI coding agents productive in this repository.

Big picture
- Single-page Streamlit app: `app.py` provides the UI and ties together text and URL checks.
- Models: pre-trained pickles live in `models/` and are loaded via `joblib` (`text_scam_model.pkl`, `tfidf_vectorizer.pkl`, `url_phishing_model.pkl`).
- Prediction helpers: `utils/url_predict.py` and the inline `predict_message` in `app.py` implement feature extraction, thresholds, and labeling.
- Logging/metrics: `utils/firebase_db.py` writes to Firestore collection `logs` and provides `get_impact_stats()` for the dashboard.
- Training artifacts: notebooks under `Notebook/` created the models and must be used to retrain if features change.

Key files to inspect
- `app.py` — UI, language dictionary (`TEXT`), and main orchestration (calls `predict_message`, `predict_url`, `log_result`).
- `utils/url_predict.py` — feature engineering for URLs (`extract_url_features`) and prediction threshold (0.55).
- `utils/firebase_db.py` — Firebase init (uses `streamlit.secrets.firebase` or `firebase/firebase_key.json`) and `logs` collection format.
- `Notebook/` — training notebooks; retrain here to regenerate `models/*.pkl`.

Data flow & conventions
- Input → model → log_result in Firestore → dashboard reads `logs` for impact stats.
- Text model: vectorizer + classifier pattern. `app.py` loads `tfidf_vectorizer.pkl` and `text_scam_model.pkl`; threshold = 0.5, risk high if prob > 0.7.
- URL model: `extract_url_features()` must preserve exact features used in training (order/names). Threshold used in code: 0.55.
- Models are loaded at import-time with `joblib.load(...)`. Be mindful of cold-start cost in tests/CI; lazy-load if needed.

Secrets / External integrations
- Firebase: `utils/firebase_db.py` tries `streamlit.secrets.get("firebase")` first, then `firebase/firebase_key.json` for local dev. Ensure the JSON key exists for local runs or set Streamlit secrets for deployment.
- No external model-serving service; models are local pickles.

Developer workflows (commands)
- Install dependencies: `pip install -r requirements.txt`.
- Run app locally: `streamlit run app.py`.
- Quick model smoke tests: `python test_url_model.py` and `python test_text_model.py` (these are scripts that print predictions).
- Run all tests (if using pytest): `pytest` — note some `test_*.py` files are scripts without assertions.

Editing guidance for AI agents
- If you change URL/text feature names or ordering, update `extract_url_features()` and retrain notebooks in `Notebook/` to re-generate `models/*.pkl`.
- When changing model filenames or loading behavior, update `app.py` and `utils/*` imports accordingly.
- Avoid modifying Firebase logging schema without updating `get_impact_stats()` in `utils/firebase_db.py` and the dashboard metrics in `app.py`.

Project-specific patterns to follow
- Keep the model artifact filenames and simple thresholds in code (explicit numbers present in `app.py` and `utils/url_predict.py`).
- Language strings are centralized in the `TEXT` dict inside `app.py` — update both English and Hindi entries together.
- Notebooks under `Notebook/` are the source of truth for training; prefer regenerating the pickle artifacts from those notebooks.

If anything is unclear or you need a deeper merge with an existing instruction file, tell me which sections to expand or any local constraints (CI, secret management, or deployment target) and I'll update this file.
