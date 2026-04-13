# EduForge AI - Backend

Run locally:
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Fill in your Supabase credentials
uvicorn main:app --host 0.0.0.0 --port 10000
```

Deploy to Render/Railway:
- Set environment variables: SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY (optional)
- Build command: pip install -r requirements.txt
- Start command: uvicorn main:app --host 0.0.0.0 --port 10000