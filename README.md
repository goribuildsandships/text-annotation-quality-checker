# Text Data Annotation Quality Checker

A beginner-friendly Python script that checks a small labeled-text dataset for common data quality problems.

## What it checks

- Missing text or labels
- Labels outside the approved category list
- Duplicate record IDs
- Duplicate text entries (reported as a warning, not automatically removed)

## Dataset

`data/sample_annotations.csv` is fictional and intended only to demonstrate validation. Categories are `Billing`, `Technical Support`, and `Account`.

## Requirements

Python 3.9 or newer. No third-party packages required.

## Run it

```bash
python src/check_annotations.py
```

To choose files:

```bash
python src/check_annotations.py --input data/sample_annotations.csv --output outputs/annotation_issues.csv
```

## Output

The script creates `outputs/annotation_issues.csv` with one row per issue. If no issues are found, it creates a CSV with the appropriate headers and reports that the data passed these basic checks.

## Limitations

These checks only identify straightforward formatting and labeling problems. They do not decide whether an annotation is semantically correct; that still requires guidelines and human review.
