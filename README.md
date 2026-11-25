# Smart Academic Management Platform (SAMP) — Firebase starter

This is **Phase 1 foundation**, not the completed 50-page project. It includes a Vite/React frontend, Firebase Authentication (email/password), Firestore profile creation, protected dashboard, Firebase Hosting configuration, security-rule starting points, and a FastAPI health/token-verification service.

## Architecture decision
- Firebase Hosting: React frontend.
- Firebase Authentication: registration, login, password reset.
- Cloud Firestore: application data.
- Firebase Storage: user files.
- FastAPI: protected AI/NLP and server-side operations, deployed separately (for example, Cloud Run).
- Firebase Admin SDK: verifies Firebase ID tokens in FastAPI.

The original prompt specifies PostgreSQL/SQLAlchemy. This Firebase-first version uses Firestore for application data. If PostgreSQL is a hard requirement for evaluation, keep it as a separate FastAPI data store rather than assuming Firebase Hosting provides a SQL database.

## Requirements
- Windows 10/11
- Node.js LTS and npm
- Python 3.11+
- VS Code
- Firebase project with a registered Web App
- Firebase CLI: `npm install -g firebase-tools`

## 1. Open project
Extract the ZIP, open the `SAMP-Firebase-Starter` folder in VS Code.

## 2. Configure Firebase frontend
In Firebase Console:
1. Open Project settings (gear icon) → General.
2. Under Your apps, create/register a Web app if you have not already.
3. Copy the web app configuration values.
4. In `frontend`, copy `.env.example` to `.env` and fill every `VITE_FIREBASE_*` value.
5. Authentication → Sign-in method → enable Email/Password.
6. Firestore Database → Create database.
7. Storage → Get started.

Firebase web config is not a server secret; security must be enforced by Firebase Rules. Never put service-account JSON or private keys in frontend `.env`.

## 3. Run frontend
Open VS Code terminal:
```powershell
cd frontend
copy .env.example .env
# Edit .env with your Firebase Web App values
npm install
npm run dev
```
Open http://localhost:5173

## 4. Run FastAPI backend (second terminal)
```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```
For local Firebase Admin verification, create a service account in Firebase Console → Project settings → Service accounts → Generate new private key. Save it as `backend/service-account.json` and keep it private. Set `GOOGLE_APPLICATION_CREDENTIALS=./service-account.json` in `backend/.env`.
```powershell
uvicorn app.main:app --reload --port 8000
```
API docs: http://localhost:8000/docs

## 5. Deploy frontend to Firebase Hosting
From the project root:
```powershell
npm install -g firebase-tools
firebase login
firebase projects:list
```
Copy `.firebaserc.example` to `.firebaserc`, replace the project ID with your real Firebase project ID. Then:
```powershell
cd frontend
npm install
npm run build
cd ..
firebase deploy --only hosting,firestore:rules,storage
```
The deployed website URL is shown by the Firebase CLI.

## Important security note
The rules in this starter deliberately deny access to all collections except a user's own basic profile document. Do not loosen rules to `allow read, write: if true`. Add and test collection-specific rules as each feature is implemented. The Storage rule only permits authenticated users to access their own user folder.

## Current implementation status
- [x] React/Vite starter and responsive sign-in/register screens
- [x] Firebase email/password authentication
- [x] Firestore student profile document
- [x] Protected dashboard route
- [x] Password reset email
- [x] Firebase Hosting SPA rewrite
- [x] Initial Firestore/Storage rules
- [x] FastAPI health endpoint and Firebase ID-token verification
- [ ] Dashboard live metrics and all six project modules
- [ ] Vault permissions, AI/NLP analyzer, scheduler, social feed, friendships, communities, chat, bulletin, tests and production backend deployment

Build in phases and test each module before adding the next one. Never describe unimplemented modules as complete.
