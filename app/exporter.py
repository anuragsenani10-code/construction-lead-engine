import csv
from pathlib import Path
from .models import Lead

FIELDS = list(Lead.__dataclass_fields__.keys())

def export_csv(leads: list[Lead], path: str = "output/leads.csv") -> str:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows([lead.row() for lead in leads])
    return str(out)
