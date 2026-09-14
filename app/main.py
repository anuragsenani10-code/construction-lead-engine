import argparse
from .config import Settings
from .models import Lead
from .scoring import detect_pain_signals, score_lead, priority
from .exporter import export_csv

def main():
    p = argparse.ArgumentParser(description="Construction Lead Engine MVP")
    p.add_argument("--state", default="New York")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--query", default="construction contractor BIM")
    args = p.parse_args()

    settings = Settings(location=f"{args.state}, USA", lead_limit=args.limit)
    print(f"Configured: {settings.location} | limit={settings.lead_limit} | query={args.query}")
    print("Discovery adapters are intentionally separated from scoring/export so providers can be swapped cheaply.")
    # Provider integrations will append real, evidence-backed Lead objects here.
    leads: list[Lead] = []
    print(export_csv(leads))

if __name__ == "__main__":
    main()
