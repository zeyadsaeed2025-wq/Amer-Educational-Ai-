# EduForge AI - Deployment Guide

## Project Structure

```
eduforge-ai/
├── frontend/              # Vercel Deployment
│   ├── index.html
│   └── vercel.json
├── backend/              # FastAPI Backend
│   ├── main.py
│   ├── core/
│   ├── api/
│   └── db/
├── .gitignore
└── DEPLOYMENT.md
```

---

## 1. Backend Deployment (Railway / Render / Fly.io)

### Option A: Railway (Recommended)
1. Create account at railway.app
2. Connect GitHub repository
3. Add environment variables:
   ```
   SUPABASE_URL=your-supabase-url
   SUPABASE_KEY=your-supabase-key
   OPENAI_API_KEY=your-openai-key (optional)
   USE_MOCK_AI=false (if using OpenAI)
   ```
4. Deploy

### Option B: Render
1. Create account at render.com
2. Create Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port 8000`
5. Add environment variables

### Option C: Fly.io
1. Create `fly.toml`:
```toml
app = "eduforge-ai"
primary_region = "fra"

[build]
  builder = "heroku/buildpacks:20"

[env]
  PORT = "8080"

[[services]]
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

---

## 2. Supabase Setup

### Create Tables in Supabase Dashboard

```sql
-- Lessons table
CREATE TABLE lessons (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  category TEXT NOT NULL,
  content_standard TEXT,
  content_simplified TEXT,
  content_accessibility TEXT,
  ui_hints TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE lessons ENABLE ROW LEVEL SECURITY;

-- Allow all operations (for demo)
CREATE POLICY "Allow all" ON lessons FOR ALL USING (true) WITH CHECK (true);
```

---

## 3. Frontend Deployment (Vercel)

### Deploy Steps
1. Go to vercel.com
2. Import GitHub repository
3. Select `frontend` folder
4. Configure:
   - Framework Preset: Other
   - Build Command: Leave empty
   - Output Directory: ./
5. Add Environment Variable:
   ```
   API_BASE_URL = https://your-backend-url.railway.app
   ```
6. Deploy

### Update vercel.json
Replace `YOUR-BACKEND-URL` with your actual backend URL.

---

## 4. Environment Variables

### Backend (.env)
```env
APP_NAME=EduForge AI
DEBUG=false
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=https://your-frontend.vercel.app
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxx
OPENAI_API_KEY=xxx (optional)
USE_MOCK_AI=true
```

### Frontend (Vercel)
```env
API_BASE_URL=https://your-backend-url.railway.app
```

---

## 5. Testing Checklist

- [ ] Backend starts successfully
- [ ] Health endpoint works: `/health`
- [ ] Generate content works: `/api/generate-content`
- [ ] Analyze content works: `/api/analyze-content`
- [ ] Database connection works
- [ ] CORS configured correctly
- [ ] Frontend builds successfully
- [ ] Frontend connects to backend API
- [ ] WebSocket connection works

---

## 6. Production URLs

After deployment, update:

1. **Backend CORS**: Set `CORS_ORIGINS` to your Vercel frontend URL
2. **Frontend vercel.json**: Update backend URL
3. **Frontend ENV**: Set production API URL

---

## Quick Commands

```bash
# Local Development
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload

# Test API
curl http://localhost:8000/health

# Generate Content
curl -X POST http://localhost:8000/api/generate-content \
  -H "Content-Type: application/json" \
  -d '{"title": "Math Test", "category": "standard"}'
```
