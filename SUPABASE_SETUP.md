# Supabase Setup Guide for EduForge AI

## 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Note your:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **API Key**: `eyJhbGc...` (from Settings > API)

## 2. Create Tables

Go to **SQL Editor** in Supabase dashboard and run:

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

-- Enable Row Level Security
ALTER TABLE lessons ENABLE ROW LEVEL SECURITY;

-- Allow all operations (for demo)
CREATE POLICY "Allow all" ON lessons FOR ALL USING (true) WITH CHECK (true);
```

## 3. Deploy Backend

### Option A: Railway (Recommended - Free Tier)

1. Go to [railway.app](https://railway.app)
2. Login with GitHub
3. Click **New Project** → **Deploy from GitHub**
4. Select repository
5. Set **Root Directory**: `backend`
6. Add Environment Variables:
   ```
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=your-anon-key
   CORS_ORIGINS=https://amer-educational-ai.vercel.app
   ```
7. Click **Deploy**

### Option B: Render

1. Go to [render.com](https://render.com)
2. **New** → **Web Service**
3. Connect GitHub repo
4. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 8000`
5. Add Environment Variables (same as above)
6. Click **Create Web Service**

## 4. Get Backend URL

After deployment, note your backend URL:
- Railway: `https://eduforge-ai-backend.up.railway.app`
- Render: `https://your-app.onrender.com`

## 5. Update Vercel Frontend

1. Go to [vercel.com](https://vercel.com)
2. Select your project
3. **Settings** → **Environment Variables**
4. Add:
   ```
   VITE_API_URL = https://your-backend-url.com
   ```
5. **Deployments** → **Redeploy**

## 6. Update Vercel Rewrites

In `frontend/vercel.json`:
```json
{
  "rewrites": [
    {"source": "/api/:path*", "destination": "https://YOUR-BACKEND-URL/api/:path*"}
  ]
}
```

---

## Quick Commands

### Local Development
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

### Test API
```bash
curl http://localhost:8000/health
```

### With Supabase
```bash
export SUPABASE_URL=https://xxxx.supabase.co
export SUPABASE_KEY=your-key
python -m uvicorn main:app --reload
```

---

## Troubleshooting

### CORS Error
Make sure `CORS_ORIGINS` includes your Vercel domain:
```
CORS_ORIGINS=https://amer-educational-ai.vercel.app
```

### Database Connection Error
1. Check SUPABASE_URL is correct
2. Check SUPABASE_KEY is the `anon` key, not `service` key
3. Verify RLS policies allow access

### 404 on API
Make sure vercel.json rewrites are correct and redeployed.
