from dataclasses import dataclass, field

@dataclass
class Settings:
    location: str = "New York, USA"
    industries: list[str] = field(default_factory=lambda: [
        "General Contractor", "Construction Management", "Architecture",
        "Engineering", "BIM", "MEP"
    ])
    min_employees: int = 5
    max_employees: int = 500
    lead_limit: int = 50
    decision_titles: list[str] = field(default_factory=lambda: [
        "Owner", "President", "CEO", "VP", "Director", "Project Manager",
        "Preconstruction Manager", "Estimator", "BIM Manager"
    ])
    pain_signals: dict[str, int] = field(default_factory=lambda: {
        "hiring": 15, "active_project": 15, "expansion": 10,
        "bim": 15, "preconstruction": 10, "schedule": 10,
        "staffing": 10, "outsourcing": 10
    })

DEFAULTS = Settings()
