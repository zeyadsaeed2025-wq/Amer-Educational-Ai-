import re
from dataclasses import dataclass
from typing import List


@dataclass
class QualityAlert:
    type: str
    msg: str


@dataclass
class QualityMetrics:
    score: int
    readability: int
    interactivity: int
    engagement: int
    alerts: List[QualityAlert]
    suggestions: List[str]


class QualityEngine:
    """Analyzes educational content quality across multiple dimensions."""
    
    @staticmethod
    def analyze(text: str, tab: str = "standard") -> QualityMetrics:
        """Analyze content and return quality metrics."""
        
        word_count = len(text.split())
        sentence_count = max(1, len(re.findall(r'[.!?؟]', text)))
        arabic_word_count = len(re.findall(r'[\u0600-\u06FF]+', text))
        
        # Calculate individual metrics
        readability = QualityEngine._calculate_readability(text, word_count, sentence_count)
        interactivity = QualityEngine._calculate_interactivity(text)
        engagement = QualityEngine._calculate_engagement(text, word_count)
        
        # Base score from metrics
        base_score = (readability + interactivity + engagement) // 3
        
        # Generate alerts and suggestions
        alerts = QualityEngine._generate_alerts(text, word_count, sentence_count, base_score)
        suggestions = QualityEngine._generate_suggestions(text, word_count, readability)
        
        # Adjust score based on alerts
        for alert in alerts:
            if alert.type == "danger":
                base_score -= 10
            elif alert.type == "warn":
                base_score -= 3
        
        score = max(0, min(100, base_score))
        
        return QualityMetrics(
            score=score,
            readability=readability,
            interactivity=interactivity,
            engagement=engagement,
            alerts=alerts,
            suggestions=suggestions[:5],
        )
    
    @staticmethod
    def _calculate_readability(text: str, word_count: int, sentence_count: int) -> int:
        """Calculate readability score (0-100)."""
        if word_count < 10:
            return 30
        
        avg_words_per_sentence = word_count / max(1, sentence_count)
        
        # Ideal: 10-20 words per sentence for Arabic
        if 10 <= avg_words_per_sentence <= 20:
            readability = 80
        elif avg_words_per_sentence < 10:
            readability = 60 + (avg_words_per_sentence * 2)
        else:
            readability = max(30, 80 - (avg_words_per_sentence - 20) * 3)
        
        # Length factor
        if 100 <= word_count <= 500:
            readability = min(100, readability + 10)
        elif word_count < 50:
            readability = max(20, readability - 20)
        
        return int(readability)
    
    @staticmethod
    def _calculate_interactivity(text: str) -> int:
        """Calculate interactivity score based on engagement elements."""
        score = 50
        
        # Positive elements
        interactive_markers = ['•', '✓', '1.', '2.', '3.', '؟', '?', 'تمرين', 'سؤال', 'مثال']
        for marker in interactive_markers:
            score += text.count(marker) * 3
        
        # Questions increase interactivity
        question_count = text.count('؟') + text.count('?')
        score += question_count * 5
        
        # Lists and steps
        if '•' in text or '✓' in text:
            score += 15
        if re.search(r'\d+\.', text):
            score += 10
        
        return min(100, max(0, score))
    
    @staticmethod
    def _calculate_engagement(text: str, word_count: int) -> int:
        """Calculate engagement potential score."""
        score = 50
        
        # Encouraging elements
        encouraging_markers = ['!', 'رائع', 'ممتاز', 'جيد', 'تعلم', 'اكتشف', 'هيا']
        for marker in encouraging_markers:
            score += text.count(marker) * 2
        
        # Variety in content
        unique_words = len(set(re.findall(r'[\u0600-\u06FF]+', text)))
        if word_count > 0:
            vocab_richness = (unique_words / word_count) * 100
            if vocab_richness > 30:
                score += 10
        
        # Activity mentions
        if 'نشاط' in text or 'تمرين' in text or 'مشروع' in text:
            score += 10
        
        return min(100, max(0, score))
    
    @staticmethod
    def _generate_alerts(text: str, word_count: int, sentence_count: int, base_score: int) -> List[QualityAlert]:
        """Generate quality alerts based on content analysis."""
        alerts = []
        
        if word_count < 50:
            alerts.append(QualityAlert("danger", "المحتوى قصير جداً - يحتاج مزيداً من التفصيل"))
        elif word_count > 1000:
            alerts.append(QualityAlert("warn", "المحتوى طويل - فكر في تقسيمه"))
        
        if sentence_count < 3 and word_count > 50:
            alerts.append(QualityAlert("warn", "استخدم فقرات متعددة لتحسين القراءة"))
        
        if word_count > 200 and sentence_count < 5:
            alerts.append(QualityAlert("danger", "جمل طويلة جداً - قسّمها"))
        
        # Check for structure
        if '🎯' not in text and 'الهدف' not in text and 'أهداف' not in text:
            alerts.append(QualityAlert("info", "أضف قسم الأهداف التعليمية"))
        
        return alerts
    
    @staticmethod
    def _generate_suggestions(text: str, word_count: int, readability: int) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []
        
        if 'مثال' not in text and 'امثلة' not in text:
            suggestions.append("أضف أمثلة توضيحية لجعل المحتوى أكثر وضوحاً")
        
        if ' سؤال' not in text.lower() and 'تمرين' not in text:
            suggestions.append("أضف أسئلة أو تمارين للتفاعل مع المتعلم")
        
        if '?' not in text and '؟' not in text:
            suggestions.append("تأكد من تضمين أسئلة تحفيزية")
        
        if '•' not in text and '✓' not in text and '-' not in text:
            suggestions.append("استخدم قوائم نقطية لتسهيل القراءة")
        
        if readability < 60:
            suggestions.append("فكر في تبسيط بعض الجمل الطويلة")
        
        if word_count < 100:
            suggestions.append("قم بتوسيع المحتوى بتفاصيل إضافية")
        
        if text.count('\n\n') < 2:
            suggestions.append("أضف فقرات منفصلة لتحسين التنسيق")
        
        if 'ملخص' not in text and 'خلاصة' not in text:
            suggestions.append("أضف ملخصاً في نهاية الدرس")
        
        return suggestions
