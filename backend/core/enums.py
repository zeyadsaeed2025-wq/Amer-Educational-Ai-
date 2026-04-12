from enum import Enum


class LearnerCategory(str, Enum):
    STANDARD = "standard"
    AUTISM = "autism"
    VISUAL = "visual"
    HEARING = "hearing"
    DYSLEXIA = "dyslexia"
    ADHD = "adhd"


class ContentTab(str, Enum):
    STANDARD = "standard"
    SIMPLIFIED = "simplified"
    ACCESSIBILITY = "accessibility"
