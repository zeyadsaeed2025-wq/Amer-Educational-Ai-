from core.enums import LearnerCategory, ContentTab

CATEGORY_ADAPTATIONS = {
    LearnerCategory.STANDARD: {
        "name": "طالب عادي",
        "font_size": "normal",
        "high_contrast": False,
        "simplified_ui": False,
        "features": [
            "محتوى تعليمي متوازن ومنظم",
            "أمثلة متنوعة من الواقع",
            "أنشطة تطبيقية متعددة",
            "تدرج من البسيط إلى المعقد",
            "تشجيع على التفكير النقدي",
        ],
        "activities": ["قراءة وكتابة", "مناقشات", "تطبيق عملي"],
        "tips": ["راجع بانتظام", "طبّق ما تعلمته", "اسأل عند الحاجة"],
    },
    LearnerCategory.AUTISM: {
        "name": "طالب مصاب بالتوحد",
        "font_size": "large",
        "high_contrast": True,
        "simplified_ui": True,
        "features": [
            "هيكل واضح وثابت مع أقسام محددة بوضوح",
            "تجنب العبارات المجازية والاستعارات المعقدة",
            "استخدم لغة مباشرة ودقيقة",
            "وفر وقتاً كافياً لكل نشاط",
            "قلل المحفزات الحسية",
            "قدم التعليمات خطوة بخطوة",
        ],
        "activities": ["روتين منتظم", "أنشطة بصرية متكررة", "مساحات هادئة"],
        "tips": ["اتبع نفس الترتيب في كل درس", "أعطِ وقتاً إضافياً", "قلل الضوضاء"],
    },
    LearnerCategory.ADHD: {
        "name": "طالب ADHD",
        "font_size": "normal",
        "high_contrast": False,
        "simplified_ui": True,
        "features": [
            "تقسيم المحتوى إلى أجزاء صغيرة",
            "استخدم مؤقتات لجلسات قصيرة مركزة",
            "أضف عناصر تفاعلية ومتعددة",
            "وفر مكافآت تحفيزية صغيرة",
            "اسمح بالحركة بين الأنشطة",
            "استخدم ألواناً جذابة وعناصر بصرية",
        ],
        "activities": ["دقائق تركيز", "تبديل بين الأنشطة", "مكافآت فورية"],
        "tips": ["جلسات قصيرة (10-15 دقيقة)", "ألعاب تعليمية", "فواصل منتظمة"],
    },
    LearnerCategory.DYSLEXIA: {
        "name": "طالب عسر قراءة",
        "font_size": "xlarge",
        "high_contrast": True,
        "simplified_ui": True,
        "features": [
            "استخدم خطاً sans-serif كبير وواضح",
            "تجنب الخطوط الزخرفية",
            "وفر خلفية داكنة مع نص فاتح",
            "استخدم مسافات واسعة بين الأسطر",
            "أضف صوراً توضيحية لكل فكرة",
            "وفر نسخة صوتية",
        ],
        "activities": ["استماع مع قراءة", "ألعاب صوتية", "خرائط ذهنية"],
        "tips": ["اقرأ بصوت عالٍ", "استخدم مسطرة للقراءة", "خذ استراحات قصيرة"],
    },
    LearnerCategory.VISUAL: {
        "name": "طالب إعاقة بصرية",
        "font_size": "xlarge",
        "high_contrast": True,
        "simplified_ui": True,
        "features": [
            "وصف دقيق وشامل للصور",
            "استخدم نصوصاً كبيرة وعالية التباين",
            "وفر معلومات صوتية مكافئة",
            "استخدم نظام برايل عند الحاجة",
            "تجنب الاعتماد على الألوان فقط",
            "وفر خرائط ملموسة",
        ],
        "activities": ["تعليم صوتي", "مواد لمسية", "وصف سمعي مفصل"],
        "tips": ["اسمع المحتوى صوتياً", "استخدم التكبير", "اطلب وصف الصور"],
    },
    LearnerCategory.HEARING: {
        "name": "طالب إعاقة سمعية",
        "font_size": "normal",
        "high_contrast": False,
        "simplified_ui": False,
        "features": [
            "وفر ترجمة نصية لكل محتوى صوتي",
            "استخدم مقاطع فيديو مع ترجمة",
            "أضف نصوصاً بدلاً من الأوامر الصوتية",
            "استخدم لغة الإشارة عند الإمكان",
            "وفر أدوات اتصال كتابية",
            "تجنب الاعتماد على الاستماع فقط",
        ],
        "activities": ["قراءة وتفسير", "لغة إشارة", "تواصل كتابي"],
        "tips": ["اقرأ الترجمات", "استخدم الكتابة", "انتبه للغة الجسد"],
    },
}


def get_adaptations(category: LearnerCategory) -> dict:
    """Get content adaptations for a learner category."""
    return CATEGORY_ADAPTATIONS.get(category, CATEGORY_ADAPTATIONS[LearnerCategory.STANDARD])


def get_ui_hints(category: LearnerCategory) -> dict:
    """Get UI hints for a learner category."""
    adaptations = get_adaptations(category)
    return {
        "font_size": adaptations["font_size"],
        "high_contrast": adaptations["high_contrast"],
        "simplified_ui": adaptations["simplified_ui"],
    }
