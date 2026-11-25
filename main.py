import os
import firebase_admin
from firebase_admin import auth as firebase_auth
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
if not firebase_admin._apps:
    # For local development, set GOOGLE_APPLICATION_CREDENTIALS to your
    # Firebase service-account JSON file. Never commit that file.
    firebase_admin.initialize_app()

app = FastAPI(title="SAMP API", version="1.0.0")
origins = [os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def root():
    return {"name": "SAMP API", "status": "running"}

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "samp-backend"}

@app.get("/api/auth/verify")
def verify_firebase_token(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Firebase ID token")
    token = authorization.removeprefix("Bearer ").strip()
    try:
        decoded = firebase_auth.verify_id_token(token)
        return {"uid": decoded["uid"], "email": decoded.get("email"), "verified": True}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired Firebase ID token")