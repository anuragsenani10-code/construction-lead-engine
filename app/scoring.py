SIGNAL_KEYWORDS = {
    "hiring": ("hiring", "we are hiring", "careers", "job opening"),
    "active_project": ("project", "groundbreaking", "construction underway", "award"),
    "expansion": ("expanding", "expansion", "new office", "growth"),
    "bim": ("bim", "building information modeling", "revit", "coordination"),
    "preconstruction": ("preconstruction", "estimating", "takeoff", "bid"),
    "schedule": ("schedule", "deadline", "fast-track", "accelerated"),
    "staffing": ("staff", "team", "talent", "shortage"),
    "outsourcing": ("outsourcing", "offshore", "external support", "subcontract")
}

def detect_pain_signals(text: str) -> list[str]:
    t = text.lower()
    return [name for name, words in SIGNAL_KEYWORDS.items() if any(w in t for w in words)]

def score_lead(signals: list[str], email_verified=False, phone_verified=False) -> int:
    weights = {"hiring":15,"active_project":15,"expansion":10,"bim":15,"preconstruction":10,"schedule":10,"staffing":10,"outsourcing":10}
    score = min(100, sum(weights.get(s, 0) for s in signals))
    if email_verified: score += 5
    if phone_verified: score += 5
    return min(100, score)

def priority(score: int) -> str:
    return "A" if score >= 60 else "B" if score >= 35 else "C"
