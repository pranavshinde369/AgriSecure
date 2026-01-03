import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase/firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref = db.collection("test").add({
    "status": "Firebase connected",
    "project": "AgriSecure"
})

print("Firebase connection successful!")
