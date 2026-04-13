# 🎓 EduForge AI - منصة التعليم الذكي الشاملة

منصة تعليمية ذكية شاملة مدعومة بالذكاء الاصطناعي لجميع المتعلمين:
- الطلاب العاديون
- طيف التوحد
- ADHD
- عسر القراءة
-ضعف البصر
- ضعف السمع

## 🏗️ الهيكل

```
EduForge AI/
├── backend/                    # FastAPI Backend
│   ├── main.py                # API الكامل
│   ├── requirements.txt       # المتطلبات
│   ├── supabase_setup.sql     # إعداد Supabase
│   └── render.yaml            # إعداد Render
│
└── frontend/                   # React + Vite Frontend
    ├── src/
    │   ├── App.jsx            # التطبيق الرئيسي
    │   ├── main.jsx           # نقطة الدخول
    │   └── styles/
    │       └── global.css     # الأنماط + Accessibility
    ├── package.json
    └── vite.config.js
```

## 🚀 التشغيل السريع

### الـ Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 10000
```

### الـ Frontend

```bash
cd frontend
npm install
npm run dev
```

افتح: http://localhost:5173

## ⚡ الـ APIs

| Endpoint | Method | الوصف |
|----------|--------|-------|
| `/api/generate-content` | POST | توليد درس AI |
| `/api/save` | POST | حفظ الدرس |
| `/api/lessons` | GET | جلب كل الدروس |
| `/api/lessons/{id}` | GET | جلب درس واحد |
| `/api/lessons/{id}` | DELETE | حذف الدرس |
| `/api/upload` | POST | رفع ملف |
| `/api/analyze-content` | POST | تحليل المحتوى |
| `/health` | GET | فحص الحالة |

## ♿ التسهيلات

- ✅ حجم خط كبير
- ✅ وضع التباين العالي
- ✅ تباعد الأسطر
- ✅ دعم قارئ الشاشة
- ✅ دعم الصوت

## 📦 النشر

### Backend (Render/Railway)
```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```

المتغيرات:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `OPENAI_API_KEY` (اختياري)

### Frontend (Vercel)
اربط_repo بـ Vercel ->deploys تلقائي

## 🎯 الوظائف

1. **إنشاء الدروس بالـ AI** - 3 مستويات (Standard, Simplified, Accessibility)
2. **محرر Quill.js** - محرر نصي غني كـ Word
3. **حفظ واسترجاع الدروس** - تخزين محلي أو Supabase
4. **إعدادات التسهيلات** - تخصيص العرض
5. **رفع الملفات** - صور وفيديو

## 🔧解決済み المشاكل

- ✅ دعم العربية الكامل
- ✅ تخزين محلي بدون Supabase
- ✅ معالجة الأخطاء
- ✅ CORS محمل
- ✅ Fallback للنظام

---
🎓 **EduForge AI** - تعليم للجميع!