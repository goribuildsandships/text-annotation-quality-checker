import argparse
import csv
from collections import Counter
from pathlib import Path

ALLOWED_LABELS = {"Billing", "Technical Support", "Account"}

def main():
    parser = argparse.ArgumentParser(description="Check a text annotation CSV for common quality issues.")
    parser.add_argument("--input", default="data/sample_annotations.csv")
    parser.add_argument("--output", default="outputs/annotation_issues.csv")
    args = parser.parse_args()

    source = Path(args.input)
    target = Path(args.output)
    if not source.exists():
        raise SystemExit(f"Input file not found: {source}")

    with source.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    id_counts = Counter(row.get("record_id", "").strip() for row in rows)
    text_counts = Counter(row.get("text", "").strip().casefold() for row in rows if row.get("text", "").strip())
    issues = []

    for line_number, row in enumerate(rows, start=2):
        record_id = row.get("record_id", "").strip()
        text = row.get("text", "").strip()
        label = row.get("label", "").strip()

        def add_issue(issue_type, detail):
            issues.append({
                "csv_line": line_number,
                "record_id": record_id,
                "issue_type": issue_type,
                "detail": detail
            })

        if not record_id:
            add_issue("MISSING_RECORD_ID", "Record ID is blank.")
        elif id_counts[record_id] > 1:
            add_issue("DUPLICATE_RECORD_ID", f"Record ID '{record_id}' appears more than once.")

        if not text:
            add_issue("MISSING_TEXT", "Text field is blank.")
        elif text_counts[text.casefold()] > 1:
            add_issue("DUPLICATE_TEXT", "Text matches another record; review for possible duplicate.")

        if not label:
            add_issue("MISSING_LABEL", "Label field is blank.")
        elif label not in ALLOWED_LABELS:
            add_issue("INVALID_LABEL", f"'{label}' is not an approved label.")

    target.parent.mkdir(parents=True, exist_ok=True)
    fields = ["csv_line", "record_id", "issue_type", "detail"]
    with target.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(issues)

    print(f"Records checked: {len(rows)}")
    print(f"Issues found: {len(issues)}")
    print(f"Issue report saved to: {target}")

if __name__ == "__main__":
    main()
