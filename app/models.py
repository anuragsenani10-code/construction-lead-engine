from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Lead:
    company: str
    website: str = ""
    location: str = ""
    industry: str = ""
    decision_maker: str = ""
    title: str = ""
    work_email: str = ""
    direct_business_phone: str = ""
    email_status: str = "unverified"
    phone_status: str = "unverified"
    pain_signals: str = ""
    evidence_urls: str = ""
    score: int = 0
    priority: str = "C"
    reason: str = ""

    def row(self):
        return asdict(self)
