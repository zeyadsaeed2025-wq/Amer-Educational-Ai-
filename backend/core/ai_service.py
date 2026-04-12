import logging
from typing import Dict, List, Optional
from core.config import get_settings
from core.accessibility_engine import get_adaptations, get_ui_hints
from core.enums import LearnerCategory

logger = logging.getLogger(__name__)
settings = get_settings()


class ContentGenerator:
    """
    Generates high-quality educational content with category-specific adaptations.
    Uses smart topic detection and realistic content generation.
    """
    
    # Topic patterns for detection
    TOPIC_PATTERNS = {
        "math": ["رياضيات", "حساب", "جمع", "طرح", "ضرب", "قسمة", "كسور", "نسبة", "معادلة", "هندسة", "قياس", "اعداد", "عدد", "جبر", "math", "algebra", "fraction"],
        "science": ["علوم", "فيزياء", "كيمياء", "احياء", "طاقة", "مادة", "قوة", "حركة", "كوكب", "ذرة", "خلية", "حياة", "نبات", "حيوان", "science", "physics", "chemistry"],
        "arabic": ["لغة عربية", "قواعد", "نحو", "صرف", "بلاغة", "ادب", "نصوص", "قراءة", "كتابة", "تعبير", "املاء", "arabic", "grammar"],
        "english": ["انجليزي", "english", "لغة اجنبية"],
        "history": ["تاريخ", "حضارة", "اسلامية", "مصرية", "عصور", "ثورة", "حرب", "عظمة", "history"],
        "geography": ["جغرافيا", "خريطة", "قارة", "محيط", "نهر", "جبل", "مناخ", "بيئة", "geography"],
        "religion": ["دين", "اسلام", "قرآن", "حديث", "توحيد", "فقه"],
        "computer": ["حاسب", "كمبيوتر", "برمجة", "انترنت", "تكنولوجيا", "ذكاء اصطناعي", "computer", "programming"],
    }
    
    @classmethod
    def detect_topic(cls, title: str) -> str:
        """Detect topic type from title."""
        title_lower = title.lower()
        
        for topic, keywords in cls.TOPIC_PATTERNS.items():
            for keyword in keywords:
                if keyword in title_lower:
                    return topic
        
        return "general"
    
    @classmethod
    def generate_for_standard(cls, title: str, topic: str) -> dict:
        """Generate standard content for typical learners."""
        
        # Topic-specific content
        content_templates = {
            "math": cls._math_content(title),
            "science": cls._science_content(title),
            "arabic": cls._arabic_content(title),
            "history": cls._history_content(title),
            "geography": cls._geography_content(title),
            "general": cls._general_content(title),
        }
        
        return content_templates.get(topic, content_templates["general"])
    
    @classmethod
    def _math_content(cls, title: str) -> dict:
        """Generate math-specific content."""
        return {
            "intro": f"""📐 {title}

أهلاً بك في درس {title}!

📌 ما الذي سنتعلمه:
• المفاهيم الأساسية
• الطرق والحلول
• تطبيقات عملية

📚 متطلبات الدرس:
• معرفة سابقة بالأساسيات
• قلم ودفتر
• آلة حاسبة (اختياري)""",
            
            "body": f"""📖 {title} - شرح تفصيلي
{'='*55}

🎯 أولاً: المفهوم الأساسي

{title} هو جزء مهم من علم الرياضيات. دعنا نتعلمه خطوة بخطوة.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 ثانياً: القواعد الأساسية

 القاعدة ١: ...
 القاعدة ٢: ...
 القاعدة ٣: ...

 مثال ١:
 السؤال: احسب ...
 الحل: ...
 الجواب: ...

 مثال ٢:
 السؤال: أوجد قيمة ...
 الحل: ...
 الجواب: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 ثالثاً: طريقة الحل

الخطوة ١: افهم المعطيات
الخطوة ٢: حدد المطلوب
الخطوة ٣: طبق القانون
الخطوة ٤: تحقق من الإجابة

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 رابعاً: تمارين تطبيقية

تمرين ١: (سهل)
تمرين ٢: (متوسط)
تمرين ٣: (صعب - تحدي)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 خامساً: ملخص القوانين

• القانون الأول: ...
• القانون الثاني: ...
• القانون الثالث: ...""",

            "questions": [
                "ما الفرق بين ... و ...؟",
                "طبق ما تعلمته على مثال من حياتك اليومية.",
                "اشرح طريقة الحل لزميلك.",
                "ما الخطأ الشائع في هذا النوع من المسائل؟",
                "اختر ٣ مسائل وحلها.",
            ],
            "activities": [
                "حل ١٠ مسائل متنوعة",
                "صمم مسألة خاصة بك",
                "لعبة المسائل السريعة",
                "مناقشات جماعية",
            ],
            "tips": [
                "راجع القوانين يومياً",
                "حل مسائل كثيرة للتدريب",
                "لا تحفظ، افهم الطريقة",
            ]
        }
    
    @classmethod
    def _science_content(cls, title: str) -> dict:
        """Generate science-specific content."""
        return {
            "intro": f"""🔬 {title}

أهلاً بك أيها العالم الصغير!

🌟 في هذا الدرس سنتعرف على:
• ما هو {title}
• كيف يعمل في الطبيعة
• لماذا هو مهم

🔍 الأدوات المطلوبة:
• عينان مبصرتان
• عقل فضولي
• دفتر ملاحظات""",

            "body": f"""📖 {title} - رحلة في عالم العلوم
{'='*55}

🧪 أولاً: ما هو {title}؟

{title} هو phenomenon natural نشاهده يومياً. دعنا نفهمه معاً.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌍 ثانياً: في الطبيعة

نجد {title} في:
• الطبيعة من حولنا
• الحياة اليومية
• التكنولوجيا الحديثة

مثال من الطبيعة:
عندما ... يحدث ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔬 ثالثاً: الشرح العلمي

المفهوم: ...
المبدأ: ...
التطبيق: ...

التجربة:
1.准备的材料
2. اتبع الخطوات
3. لاحظ النتائج
4. سجل الملاحظات

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 رابعاً: حقائق ممتعة

• حقيقة ١: ...
• حقيقة ٢: ...
• حقيقة ٣: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 خامساً: ملخص

تعلمنا أن {title} هو ...""",

            "questions": [
                "ما هو تعريف {title}؟",
                "اذكر ٣ أمثلة على {title} من الحياة اليومية.",
                "كيف يؤثر {title} على بيئتنا؟",
                "ما العلاقة بين {title} و...؟",
                "صمم تجربة بسيطة لشرح {title}.",
            ],
            "activities": [
                "رصد {title} في الطبيعة",
                "تجربة بسيطة في المنزل",
                "بحث عن Applications",
                "معرض علمي مصور",
            ],
            "tips": [
                "راقب من حولك",
                "اسأل دائماً 'لماذا'",
                "وثق ملاحظاتك",
            ]
        }
    
    @classmethod
    def _arabic_content(cls, title: str) -> dict:
        """Generate Arabic language content."""
        return {
            "intro": f"""📚 {title}

أهلاً بك في درس اللغة العربية!

✍️ في هذا الدرس سنتعلم:
• قواعد {title}
• تطبيقات عملية
• أمثلة متنوعة

📖 الأدوات:
• كتاب النحو/الصرف
• دفتر للأمثلة
• قاموس (اختياري)""",

            "body": f"""📖 {title} - شرح قواعد اللغة
{'='*55}

📝 أولاً: التعريف

{title} هو من القواعد المهمة في اللغة العربية.

التعريف: ...
الهدف من دراسته: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 ثانياً: القاعدة

الصيغة العامة:
... (إعراب) ... (إعراب)

الأمثلة:
مثال ١: ...
إعرابه: ...

مثال ٢: ...
إعرابه: ...

مثال ٣: ...
إعرابه: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 ثالثاً: الاستثناء

حالات خاصة: ...
الشرح: ...

خطأ شائع: ...
الصحيح: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✏️ رابعاً: تمارين

تمرين ١: أعرب الجملة: ...
تمرين ٢: صحح الخطأ: ...
تمرين ٣: كون جملاً: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 خامساً: ملخص

تعلمنا {title} وهو ...""",

            "questions": [
                "عرّف {title} بأسلوبك.",
                "ما الفرق بين {title} و...؟",
                "اذكر ٥ أمثلة صحيحة.",
                "ما أكثر خطأ شائع في هذا الباب؟",
                "-compose جملة تتضمن {title}.",
            ],
            "activities": [
                "كتابة فقرة تتضمن القاعدة",
                "مراجعة الأخطاء الشائعة",
                "مسابقة بين الزملاء",
                "قراءة نصوص أدبية وتطبيق القاعدة",
            ],
            "tips": [
                "احفظ القاعدة مع مثال",
                "اقرأ كثيراً لتحسّن لغتك",
                "راجع يومياً",
            ]
        }
    
    @classmethod
    def _history_content(cls, title: str) -> dict:
        """Generate history content."""
        return {
            "intro": f"""🏛️ {title}

أهلاً بك في رحلة عبر الزمن!

⏰ في هذا الدرس:
• من هو / ما هو {title}
• متى حدث
• لماذا هو مهم

📜 المواد المطلوبة:
• خريطة تاريخية
• جدول زمني
• مصادر تاريخية""",

            "body": f"""📖 {title} - صفحة من التاريخ
{'='*55}

🏺 أولاً: مقدمة

{title} يمثل فترة مهمة في تاريخنا.

الزمن: ...
المكان: ...
الأشخاص Involved: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📜 ثانياً: الأحداث الرئيسية

الحدث الأول: ...
التاريخ: ...
الأهمية: ...

الحدث الثاني: ...
التاريخ: ...
الأهمية: ...

الحدث الثالث: ...
التاريخ: ...
الأهمية: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 ثالثاً: الشخصيات المؤثرة

الشخصية الأولى:
• الاسم: ...
• الدور: ...
• الإسهامات: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 رابعاً: النتائج والأثر

نتائج {title}:
• سياسياً: ...
• اقتصادياً: ...
• اجتماعياً: ...
• ثقافياً: ...

ما الذي تعلمناه من {title}؟ ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 خامساً: ملخص

{title} كان له أثر كبير لأنه ...""",

            "questions": [
                "متى حدث {title}؟",
                "من هم أهم الشخصيات المرتبطة بـ {title}؟",
                "ما أسباب {title}؟",
                "ما أهم نتائج {title}؟",
                "كيف أثّر {title} على الحاضر؟",
            ],
            "activities": [
                "صنع جدول زمني",
                "كتابة يوميات شخصية من تلك الحقبة",
                "بحث عن مصادر أولية",
                "مسرحية تاريخية قصيرة",
            ],
            "tips": [
                "اربط الأحداث ببعضها",
                "تعلم الأسماء والتواريخ المهمة",
                "اسأل 'لماذا' دائماً",
            ]
        }
    
    @classmethod
    def _geography_content(cls, title: str) -> dict:
        """Generate geography content."""
        return {
            "intro": f"""🌍 {title}

أهلاً بك في عالم الجغرافيا!

🗺️ في هذا الدرس سنتعرف على:
• موقع {title}
• خصائصه
• أهميته

📊 الأدوات:
• خريطة
• ص和数据
• صور""",

            "body": f"""📖 {title} - جغرافيا
{'='*55}

🗺️ أولاً: الموقع

الموقع الجغرافي: ...
الإحداثيات: ...
الحدود: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⛰️ ثانياً: التضاريس

أنواع التضاريس:
• مناطق جبلية: ...
• سهول: ...
• صحاري/غابات: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌡️ ثالثاً: المناخ

نوع المناخ: ...
متوسط درجة الحرارة: ...
كمية الأمطار: ...

الفصول:
• الصيف: ...
• الشتاء: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥 رابعاً: السكان

عدد السكان: ...
اللغات: ...
الديانات: ...
المدن الرئيسية: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💼 خامساً: الموارد والاقتصاد

الموارد الطبيعية: ...
الزراعة: ...
الصناعة: ...
المعالم السياحية: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 ملخص

{title} يتميز بـ ...""",

            "questions": [
                "أين يقع {title}؟",
                "ما مناخ {title}؟",
                "ما أهم الموارد في {title}؟",
                "قارن {title} بـ ...؟",
                "ما أهمية {title} الاستراتيجية؟",
            ],
            "activities": [
                "رسم خريطة توضيحية",
                "بحث عن معلومات إضافية",
                "مقارنة مع منطقة أخرى",
                "عرض تقديمي شفهي",
            ],
            "tips": [
                "استخدم الخرائط كثيراً",
                "اربط الجغرافيا بالحياة",
                "تعلم قراءة الإحداثيات",
            ]
        }
    
    @classmethod
    def _general_content(cls, title: str) -> dict:
        """Generate general content for unknown topics."""
        return {
            "intro": f"""📚 {title}

أهلاً بك في درس {title}!

🎯 أهداف الدرس:
• فهم المفاهيم الأساسية
• القدرة على التطبيق
• تطوير المهارات

⏰ الوقت المتوقع: 30-45 دقيقة""",

            "body": f"""📖 {title} - المحتوى التعليمي
{'='*55}

🎯 أولاً: مقدمة

{title} هو موضوع مهم في مجاله. دعنا نتعلمه معاً.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 ثانياً: المفاهيم الأساسية

المفهوم الأول: ...
التعريف: ...
الأهمية: ...
مثال: ...

المفهوم الثاني: ...
التعريف: ...
الأهمية: ...
مثال: ...

المفهوم الثالث: ...
التعريف: ...
الأهمية: ...
مثال: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 ثالثاً: التطبيقات

التطبيق الأول: ...
الخطوات: ...
النتيجة: ...

التطبيق الثاني: ...
الخطوات: ...
النتيجة: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✏️ رابعاً: تمارين

تمرين ١: ...
تمرين ٢: ...
تمرين ٣: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 خامساً: ملخص

تعلمنا اليوم عن {title}.""",

            "questions": [
                "ما هو تعريف {title}؟",
                "ما أهم النقاط التي تعلمتها؟",
                "كيف تطبق ما تعلمته؟",
                "ما الذي لم تفهمه؟",
                "اقترح تطبيقات أخرى.",
            ],
            "activities": [
                "بحث إضافي",
                "تمارين تطبيقية",
                "مناقشة مع الزملاء",
                "مشروع صغير",
            ],
            "tips": [
                "راجع بانتظام",
                "اسأل عند الحاجة",
                "طبّق عملياً",
            ]
        }
    
    @classmethod
    def generate_for_autism(cls, title: str, topic: str) -> dict:
        """Generate content optimized for autism spectrum."""
        return {
            "intro": f"""📚 {title}

مرحباً! أنا سعيد أنك هنا.

✅ ما الذي سنتعلمه:
→ {title}

📋 خطة اليوم:
1️⃣ اقرأ الشرح
2️⃣ شاهد الصور
3️⃣ حل التمارين
4️⃣ راجع

⏰ الوقت: 20-30 دقيقة
🔔 إذا احتجت مساعدة: ارفع يدك""",

            "body": f"""📖 {title} - شرح واضح
{'='*50}

📌 الجزء ١: ما هو {title}؟

{title} هو ...

هذا يعني: ...

══════════════════════════════

📌 الجزء ٢: الخطوات

الخطوة ١:
► افعل هذا
► ثم افعل هذا

الخطوة ٢:
► افعل هذا
► ثم افعل هذا

الخطوة ٣:
► افعل هذا
► ثم افعل هذا

══════════════════════════════

📌 الجزء ٣: للتذكر

☑ {title} = ...
☑ يتكون من: ...
☑ نستخدمه عندما: ...

══════════════════════════════

📌 الجزء ٤: تمارين

تمرين ١: اختر الإجابة
تمرين ٢: أكمل الفراغ
تمرين ٣: وصّل

💡 لا تقلق إذا أخطأت!
💡 التعلم يحتاج وقتاً""",

            "questions": [
                "هل فهمت ما هو {title}؟",
                "ما الخطوة الأولى؟",
                "هل تحتاج إعادة شرح؟",
                "هل أنت مستعد للتمارين؟",
            ],
            "activities": [
                "رسم خريطة الخطوات",
                "ترتيب البطاقات",
                "مطابقة الصور",
            ],
            "tips": [
                "خذ وقتك",
                "لا تتسرع",
                "اطلب المساعدة",
                "راجع الخطوات",
            ]
        }
    
    @classmethod
    def generate_for_adhd(cls, title: str, topic: str) -> dict:
        """Generate content optimized for ADHD."""
        return {
            "intro": f"""⚡ {title} - هيا نبدأ!

🎮 هل أنت مستعد؟ المدة: 5 دقائق فقط!

🏆 الهدف: تعلم أساسيات {title}

⏱️ الجدول:
• 2 دقيقة: شرح
• 2 دقيقة: تمرين
• 1 دقيقة: مكافأة!

🎁 عندما تنتهي: نجمة ⭐""",

            "body": f"""🎯 {title} - الجزء الأول
{'='*40}

🔥 الحقيقة المهمة:
{title} = فكرة واحدة فقط!

══════════════════════════════

🔑 مثال سريع:
تخيل أنك ...
→ النتيجة: ...

══════════════════════════════

🎮 لعبة! (30 ثانية)
املأ الفراغ:
{title} هو عندما ___________

اختر:
أ) ...
ب) ...
ج) ...

══════════════════════════════

⏰ استراحة! (30 ثانية)
حرك جسمك!伸展一下吧!

══════════════════════════════

🎮 تمرين سريع:
ارسم {title} في 30 ثانية!""",

            "questions": [
                "ما هي الفكرة الرئيسية؟",
                "اختر الإجابة الصحيحة!",
                "ارسم أو اكتب فكرة واحدة!",
            ],
            "activities": [
                "لعبة الذاكرة",
                "سباق الإجابات",
                "رسم سريع",
            ],
            "tips": [
                "ركز 5 دقائق فقط!",
                "ثم استراحة!",
                "كرر 3 مرات",
            ]
        }
    
    @classmethod
    def generate_for_dyslexia(cls, title: str, topic: str) -> dict:
        """Generate content optimized for dyslexia."""
        return {
            "intro": f"""📚 {title}

مرحباً! هذا الدرس سهل القراءة.

🅰️ خط كبير وواضح
📏 مسافات واسعة
🎨 ألوان هادئة
⏰ لا وقت محدود

👇 ابدأ ببطء""",

            "body": f"""{title}
{'='*25}

ما هو {title}؟

الجواب:

{title} هو ...

سؤال:
هل فهمت؟

نعم ✓
لا ← اسأل المعلم

══════════════════════════════

النقاط المهمة:

• النقطة الأولى
  (شرح قصير)

• النقطة الثانية
  (شرح قصير)

══════════════════════════════

مثال:

{title} مثل عندما ...

══════════════════════════════

تمارين:

1. أكمل:
{title} هو ___________

2. صح أو خطأ:
{title} سهل ✓""",

            "questions": [
                "هل فهمت؟",
                "ما الجزء الصعب؟",
                "اقرأ بصوت عالٍ",
            ],
            "activities": [
                "اقرأ بصوت عالٍ",
                "ارسم ما فهمته",
                "اشرح لدمية",
            ],
            "tips": [
                "اقرأ ببطء",
                "استخدم مسطرة",
                "استراحة كل 10 دقائق",
            ]
        }
    
    @classmethod
    def generate_for_visual(cls, title: str, topic: str) -> dict:
        """Generate content optimized for visual impairment."""
        return {
            "intro": f"""♿ {title}

هذا الدرس متاح بالكامل.

🔊 للاستماع: اضغط تشغيل
📝 نص كبير وواضح
✋ وصف دقيق للصور

🎧 ابدأ بالاستماع""",

            "body": f"""{title}
{'='*30}

[وصف صوتي: درس عن {title}]

━━━━━━━━━━━━━━━━━━━━━━━━

🎧 الجزء الأول - استمع:

{title} هو موضوع نتعلمه.

يحتوي على ثلاثة أجزاء مهمة:
1. الجزء الأول: ...
2. الجزء الثاني: ...
3. الجزء الثالث: ...

━━━━━━━━━━━━━━━━━━━━━━━━

📝 الجزء الثاني - اقرأ:

النقطة الأولى: ...
مثال: ...

النقطة الثانية: ...
مثال: ...

━━━━━━━━━━━━━━━━━━━━━━━━

[وصف الصورة: شكل توضيحي لـ {title}]
الصورة تبين: المركز = {title}
ثم يفرق إلى فروع

━━━━━━━━━━━━━━━━━━━━━━━━

❓ الجزء الثالث - أسئلة:

• هل فهمت؟ ...
• هل تريد تكرار؟ ...""",

            "questions": [
                "هل تريد إعادة الشرح؟",
                "ما أفضل طريقة للتعلم؟",
                "هل تحتاج أمثلة أكثر؟",
            ],
            "activities": [
                "استمع للدرس",
                "ناقش صوتياً",
                "استكشف لمسياً",
            ],
            "tips": [
                "اطلب الوصف",
                "استخدم التكبير",
                "اطلب الصوت",
            ]
        }
    
    @classmethod
    def generate_for_hearing(cls, title: str, topic: str) -> dict:
        """Generate content optimized for hearing impairment."""
        return {
            "intro": f"""♿ {title}

هذا الدرس نصي بالكامل.

✓ لا يحتاج سماع
✓ كل شيء مكتوب
✓ شرح مفصل

📖 اقرأ بهدوء""",

            "body": f"""{title}
{'='*25}

ما الذي سنتعلمه؟

1. أولاً: {title}
2. ثانياً: أمثلة
3. ثالثاً: تمارين

══════════════════════════════

{title} هو موضوع نتعلمه.

الشرح خطوة بخطوة:

الخطوة ١:
اقرأ هذا النص.

الخطوة ٢:
افهم المعنى.

الخطوة ٣:
أجب على الأسئلة.

══════════════════════════════

[فيديو مترجم]
 شاهد الفيديو مع الترجمة
 لترى {title} عملياً

══════════════════════════════

مثال مكتوب:

الموقف: ...
الحل: ...
النتيجة: ...

══════════════════════════════

❓ أسئلة:

أجب كتابياً""",

            "questions": [
                "هل فهمت الشرح؟",
                "ما الجزء غير الواضح؟",
                "اكتب ملخصاً",
            ],
            "activities": [
                "اقرأ وناقش كتابياً",
                "اكتب ملاحظاتك",
                "ارسم توضيحي",
            ],
            "tips": [
                "اقرأ ببطء",
                "اكتب أسئلتك",
                "استخدم الكتابة",
            ]
        }
    
    @classmethod
    def generate(cls, title: str, category: LearnerCategory) -> dict:
        """Generate content based on category."""
        topic = cls.detect_topic(title)
        
        # Get category-specific content
        generators = {
            LearnerCategory.AUTISM: cls.generate_for_autism,
            LearnerCategory.ADHD: cls.generate_for_adhd,
            LearnerCategory.DYSLEXIA: cls.generate_for_dyslexia,
            LearnerCategory.VISUAL: cls.generate_for_visual,
            LearnerCategory.HEARING: cls.generate_for_hearing,
            LearnerCategory.STANDARD: cls.generate_for_standard,
        }
        
        generator = generators.get(category, cls.generate_for_standard)
        category_content = generator(title, topic)
        
        return {
            "standard": category_content,
            "simplified": cls._create_simplified(category_content),
            "accessibility": cls._create_accessibility(category_content, category),
            "ui_hints": get_ui_hints(category),
        }
    
    @staticmethod
    def _create_simplified(content: dict) -> dict:
        """Create simplified version."""
        return {
            "intro": "🌟 أهلاً! هيا نتعلم!\n\n" + "\n".join(content["intro"].split("\n")[:6]),
            "body": content["body"].replace("━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "──────"),
            "questions": content["questions"][:3],
            "activities": ["رسم", "لعبة", "مشاركة"],
            "tips": ["استمتع!", "خذ وقتك", "اسأل"],
        }
    
    @staticmethod
    def _create_accessibility(content: dict, category: LearnerCategory) -> dict:
        """Create accessibility version."""
        adaptations = get_adaptations(category)
        return {
            "intro": f"♿ {content['intro']}\n\n" + "\n".join([f"• {f}" for f in adaptations["features"][:3]]),
            "body": content["body"],
            "questions": ["هل تحتاج مساعدة؟", "ما أفضل طريقة؟", "هل تريد تكراراً؟"],
            "activities": adaptations["activities"],
            "tips": adaptations["tips"],
        }


class AIService:
    """AI service for content generation with caching."""
    
    def __init__(self):
        self.use_mock = settings.use_mock_ai or not settings.openai_api_key
        self._cache = None
        self._init_cache()
        logger.info(f"AI Service initialized (mock={self.use_mock}, cache={bool(self._cache)})")
    
    def _init_cache(self):
        """Initialize Redis cache if available."""
        try:
            from core.cache import cache_manager
            self._cache = cache_manager
        except:
            pass
    
    def _get_cache_key(self, title: str, category: str) -> str:
        """Generate cache key."""
        return f"lesson:{title.lower().strip()}:{category}"
    
    async def generate_content(self, title: str, category: LearnerCategory) -> dict:
        """Generate educational content with caching."""
        category_value = category.value if hasattr(category, 'value') else category
        cache_key = self._get_cache_key(title, category_value)
        
        # Try cache first
        if self._cache:
            cached = self._cache.get(cache_key)
            if cached:
                logger.info(f"Cache hit: {cache_key}")
                return cached
        
        # Generate content - use OpenAI if available
        logger.info(f"Generating: {title} for {category_value}")
        
        if not self.use_mock and settings.openai_api_key:
            content = await self._generate_with_openai(title, category_value)
        else:
            content = ContentGenerator.generate(title, category)
        
        logger.info(f"Generated content with {len(content['standard']['intro'])} chars")
        
        # Cache result
        if self._cache:
            self._cache.set(cache_key, content, ttl=3600)
        
        return content
    
    async def _generate_with_openai(self, title: str, category: str) -> dict:
        """Generate intelligent content using OpenAI API with better prompts."""
        try:
            import httpx
            
            category_labels = {
                "standard": "طالب عادي في المدرسة",
                "autism": "طالب مع اضطراب طيف التوحد",
                "adhd": "طالب مع اضطراب نقص الانتباه وفرط الحركة",
                "dyslexia": "طالب مع عسر القراءة",
                "visual": "طالب مع إعاقة بصرية",
                "hearing": "طالب مع إعاقة سمعية",
            }
            category_label = category_labels.get(category, "طالب عادي")
            
            category_styles = {
                "standard": "استخدم لغة تعليمية غنية ومناسبة للمستوى المتوسط",
                "autism": "استخدم لغة بسيطة واضحة، كرر المعلومات، قسّم الخطوات، استخدم التصنيفات المرئية",
                "adhd": "اجعل المحتوى قصيراً ومباشراً، استخدم التفاعل، قسّم لمقاطع قصيرة",
                "dyslexia": "استخدم فقرات قصيرة، خط كبير، مسافات واسعة، تجنب النصوص الكثيفة",
                "visual": "قدم المحتوى نصياً بدون رسوم، اكتب أوصافاً مفصلة للصور والرسوم",
                "hearing": "قدم كل شيء مكتوباً بدون محتوى صوتي، اكتب التفسيرات بدلاً من الشرح الشفوي",
            }
            style = category_styles.get(category, category_styles["standard"])
            
            prompt = f"""أنت معلم عربي متخصص في التعليم والتدريب. أنشئ lesson تعليمي متميز لدرس "{title}" مخصص لـ {category_label}.

المتطلبات:
1. المحتوى يجب أن يكون أصلياً ومتجدداً وليس من نماذج سابقة
2. اكتب باللغة العربية الفصحى الحديثة
3. {style}
4. يجب أن يكون المحتوى متوافقاً مع المنهج المصري

الهيكل المطلوب:
- intro: مقدمة جذابة (3-4 جمل) تثير اهتمام الطالب وربط بالواقع
- body: شرح تفصيلي من 8-12 فقرة مع أمثلة من الحياة اليومية
- questions: 5 أسئلة تقييمية متنوعة (اختيار من متعدد + صح أو خطأ + إجابة قصيرة)
- activities: 4 أنشطة تعليمية عملية
- tips: 5 نصائح للتعلم الفعال

ملاحظات مهمة:
- لا تكرر نفس المحتوى بين النسخ (standard, simplified, accessibility)
- اجعل كل نسخة فريدة ومميزة
- استخدم أمثلة من الحياة اليومية المصرية
- التزم بالتنسيق JSON المطلوب"""

            async with httpx.AsyncClient(timeout=90.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.openai_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": settings.openai_model,
                        "messages": [
                            {"role": "system", "content": "أنت معلم عربي خبير في التعليم. أنشئ محتوى تعليمي أصلي ومتميز."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.8,
                        "max_tokens": 4000,
                    },
                )
                
                if response.status_code == 200:
                    data = response.json()
                    content_text = data["choices"][0]["message"]["content"]
                    import json
                    try:
                        content = json.loads(content_text)
                        if "standard" in content:
                            return content
                    except:
                        pass
            
            logger.warning("OpenAI generation failed, falling back to template")
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
        
        return ContentGenerator.generate(title, LearnerCategory(category))
    
    async def generate_improvements(self, text: str) -> list:
        """Generate improvement suggestions."""
        suggestions = []
        word_count = len(text.split())
        
        if word_count < 80:
            suggestions.append("المحتوى قصير - أضف تفصيلاً أكثر")
        if '\n\n' not in text:
            suggestions.append("أضف فقرات منفصلة")
        if '؟' not in text:
            suggestions.append("أضف أسئلة تفاعلية")
        if 'مثال' not in text:
            suggestions.append("أضف أمثلة عملية")
        if 'ملخص' not in text:
            suggestions.append("أضف ملخصاً في النهاية")
        if 'خطوة' not in text:
            suggestions.append("قسّم إلى خطوات واضحة")
        
        return suggestions[:6]

    async def generate_curriculum(self, title: str, category: str, num_units: int = 3, lessons_per_unit: int = 4) -> dict:
        """Generate a complete curriculum with units and lessons."""
        if not self.use_mock and settings.openai_api_key:
            try:
                import httpx
                
                category_labels = {
                    "standard": "طلاب المدارس",
                    "autism": "طلاب مع اضطراب التوحد",
                    "adhd": "طلاب مع ADHD",
                    "dyslexia": "طلاب مع عسر القراءة",
                    "visual": "طلاب مع إعاقة بصرية",
                    "hearing": "طلاب مع إعاقة سمعية",
                }
                category_label = category_labels.get(category, "طلاب المدارس")
                
                prompt = f"""أنشئ منهج تعليمي كامل باللغة العربية لـ {title} لـ {category_label}.

المتطلبات:
- {num_units} وحدات تعليمية
- {lessons_per_unit} دروس في كل وحدة
- كل درس له: عنوان، أهداف، محتوى، أسئلة، أنشطة

الهيكل المطلوب JSON:
{{
  "course_title": "...",
  "objectives": ["...", "..."],
  "units": [
    {{
      "unit_title": "...",
      "unit_objectives": ["...", "..."],
      "lessons": [
        {{
          "title": "...",
          "objectives": ["...", "..."],
          "content": "...",
          "duration_minutes": 30,
          "questions": ["...", "..."],
          "activities": ["...", "..."]
        }}
      ],
      "assessment": "..."
    }}
  ],
  "total_lessons": {num_units * lessons_per_unit},
  "estimated_hours": {num_units * lessons_per_unit * 0.5}
}}

أرجع JSON فقط بدون نص إضافي."""

                async with httpx.AsyncClient(timeout=120.0) as client:
                    response = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {settings.openai_api_key}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": settings.openai_model,
                            "messages": [
                                {"role": "system", "content": "أنت خبير في تصميم المناهج الدراسية."},
                                {"role": "user", "content": prompt}
                            ],
                            "temperature": 0.8,
                            "max_tokens": 4000,
                        },
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        content_text = data["choices"][0]["message"]["content"]
                        import json
                        try:
                            curriculum = json.loads(content_text)
                            return curriculum
                        except:
                            pass
            
            except Exception as e:
                logger.error(f"Curriculum AI error: {e}")
        
        # Fallback structure
        return self._generate_curriculum_fallback(title, category, num_units, lessons_per_unit)

    def _generate_curriculum_fallback(self, title: str, category: str, num_units: int, lessons_per_unit: int) -> dict:
        """Generate curriculum structure as fallback."""
        units = []
        for i in range(num_units):
            lessons = []
            for j in range(lessons_per_unit):
                lessons.append({
                    "title": f"الدرس {j+1}: {title} - مرحلة {j+1}",
                    "objectives": [f"فهم أساسيات {title}", f"تطبيق مفاهيم {title}"],
                    "content": f"محتوى الدرس {j+1} حول {title}",
                    "duration_minutes": 30,
                    "questions": ["سؤال 1؟", "سؤال 2؟", "سؤال 3؟"],
                    "activities": ["نشاط عملي 1", "نشاط جماعي 2"]
                })
            units.append({
                "unit_title": f"الوحدة {i+1}: أساسات {title}",
                "unit_objectives": [f"تعلم أساسيات {title}"],
                "lessons": lessons,
                "assessment": f"تقييم الوحدة {i+1}"
            })
        
        return {
            "course_title": f"منهج {title}",
            "objectives": [f"تعلم {title}", f"تطبيق {title}"],
            "units": units,
            "total_lessons": num_units * lessons_per_unit,
            "estimated_hours": num_units * lessons_per_unit * 0.5
        }

    async def live_assist(self, text: str, context: str = "general", category: str = "standard") -> dict:
        """Get AI assistance while editing content."""
        if not self.use_mock and settings.openai_api_key:
            try:
                import httpx
                
                prompts = {
                    "general": "حسن هذا النص التعليمي",
                    "simplify": "بسّط هذا النص لطلاب",
                    "expand": "وسّع هذا النص بمزيد من التفاصيل",
                    "quiz": "حوّل هذا المحتوى لأسئلة تقييمية"
                }
                instruction = prompts.get(context, prompts["general"])
                
                prompt = f"""{instruction}:

{text}

أرجع JSON فقط:
{{
  "suggestions": ["...", "..."],
  "improved_text": "النص المحسّن...",
  "improvements": ["...", "..."]
}}"""

                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {settings.openai_api_key}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": settings.openai_model,
                            "messages": [
                                {"role": "system", "content": "أنت مساعد تعليمي ذكي."},
                                {"role": "user", "content": prompt}
                            ],
                            "temperature": 0.7,
                            "max_tokens": 2000,
                        },
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        content_text = data["choices"][0]["message"]["content"]
                        import json
                        try:
                            result = json.loads(content_text)
                            return result
                        except:
                            pass
            
            except Exception as e:
                logger.error(f"Live assist error: {e}")
        
        return {"suggestions": ["أضف أمثلة عملية"], "improved_text": text, "improvements": ["قسّم النص لفقرات"]}

    async def smart_analyze(self, text: str, category: str = "standard") -> dict:
        """AI-powered content analysis with smart alerts."""
        if not self.use_mock and settings.openai_api_key:
            try:
                import httpx
                
                word_count = len(text.split())
                char_count = len(text)
                
                prompt = f"""حلّل هذا النص التعليمي واحسب:

- درجة القراءة (0-100)
- درجة التفاعل (0-100)
- التنبيهات الذكية
- الاقتراحات

النص: {text[:500]}...

أرجع JSON فقط:
{{
  "score": 85,
  "engagement_level": "high/medium/low",
  "complexity_level": "high/medium/low",
  "alerts": [{{"type": "warn", "msg": "..."}}],
  "suggestions": ["...", "..."],
  "readability_score": 80,
  "interactivity_score": 70
}}"""

                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {settings.openai_api_key}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": settings.openai_model,
                            "messages": [
                                {"role": "system", "content": "أنت محلل تعليمي ذكي."},
                                {"role": "user", "content": prompt}
                            ],
                            "temperature": 0.5,
                            "max_tokens": 1000,
                        },
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        content_text = data["choices"][0]["message"]["content"]
                        import json
                        try:
                            result = json.loads(content_text)
                            return result
                        except:
                            pass
            
            except Exception as e:
                logger.error(f"Smart analyze error: {e}")
        
        # Simple fallback
        word_count = len(text.split())
        score = min(100, word_count // 2)
        alerts = []
        suggestions = []
        
        if word_count < 50:
            alerts.append({"type": "warn", "msg": "المحتوى قصير جداً"})
            suggestions.append("أضف المزيد من التفاصيل")
        if "؟" not in text:
            alerts.append({"type": "info", "msg": "أضف أسئلة تفاعلية"})
            suggestions.append("أضف أسئلة تقييمية")
        
        return {
            "score": score,
            "engagement_level": "medium" if word_count > 100 else "low",
            "complexity_level": "medium",
            "alerts": alerts,
            "suggestions": suggestions,
            "readability_score": score,
            "interactivity_score": max(0, score - 20)
        }


ai_service = AIService()
