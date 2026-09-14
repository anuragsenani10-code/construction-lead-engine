import argparse
from .config import Settings
from .pipeline import run
from .exporter import export_csv


def main():
    p = argparse.ArgumentParser(description="Construction Lead Engine")
    p.add_argument("--state", default="New York")
    p.add_argument("--limit", type=int, default=50)
    args = p.parse_args()
    settings = Settings(location=f"{args.state}, USA", lead_limit=args.limit)
    print(f"Configured: {settings.location} | limit={settings.lead_limit}")
    leads = run(settings)
    print(f"Collected {len(leads)} evidence-backed leads")
    print(export_csv(leads))


if __name__ == "__main__":
    main()
