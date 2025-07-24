import firebase_admin
from firebase_admin import credentials, firestore

import config

cred = credentials.Certificate(config.FIREBASE_PATH)
firebase_admin.initialize_app(cred)

DB = firestore.client()

def get_user(user_id: str) -> dict | None:
    user_ref = DB.collection("users").document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        return user_doc.to_dict()
    else:
        return None
    
def create_user(user_id: str, user_data: dict) -> bool:
    user_ref = DB.collection("users").document(user_id)
    try:
        user_ref.set(user_data)
        return True
    except Exception as e:
        return False
    
def update_user(user_id: str, user_data: dict) -> bool:
    user_ref = DB.collection("users").document(user_id)
    user_doc = user_ref.get()
    if not user_doc.exists:
        created = create_user(user_id, user_data)
        return created
    else:
        try:
            user_ref.update(user_data)
            return True
        except Exception as e:
            return False