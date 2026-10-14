# More Citations or More Sources? — Anonymous CHIIR 2027 Review Artifact

This repository is the anonymous review artifact for the manuscript:

**More Citations or More Sources? Source Breadth in Human Preferences for Generative Search**

It is designed for double-anonymous review. **Do not add author names, affiliations, personal email addresses, ORCID IDs, personal GitHub URLs, local user paths, or identifying commit metadata to the anonymous mirror.**

## What is included

- `paper/` — anonymous submission PDF and LaTeX source.
- `artifact/plan/analysis_plan.md` — frozen confirmatory analysis plan.
- `artifact/data/analysis_features.parquet` — exact derived feature table used by the frozen analysis (24,069 rows; SHA-256 locked below).
- `artifact/logs/` — outcome-blind feasibility audit and original reproducibility log.
- `artifact/outputs/` — result tables, figures, and the frozen results report.
- `scripts/verify_artifact.py` — verifies hashes and checks that key reported outputs match the frozen result files.
- `code/EXPECTED_CODE_HASHES.txt` — SHA-256 values of the five original execution scripts recorded at analysis time.
- `code/CODE_RECOVERY_INSTRUCTIONS.md` — safe instructions for adding the **original** scripts if they are available locally.

## Important code-status note

The exact five original execution scripts referenced in the frozen reproducibility log were **not available in the file handoff used to assemble this repository**. They have therefore **not been recreated or replaced with look-alike code**. This repository currently provides the exact frozen feature table, plan, audit, outputs, and execution hashes, but it should not be described as a complete executable source-code release until the original scripts are added and their hashes verify.

This choice is deliberate: preserving provenance is more important than supplying reconstructed code that might differ from the code that generated the reported results.

## Quick verification

From the repository root:

```bash
python scripts/verify_artifact.py
```

This uses only the Python standard library. It verifies the frozen plan and feature-table hashes and checks the headline results against the included CSV/JSON files.

To inspect the Parquet file itself, install a Parquet engine such as `pyarrow` and use pandas, or use the environment described in `environment.yml`.

## Frozen identifiers

- Frozen plan SHA-256: `4c818f8f6702331360e3e1b7b23585fb69fe719780e2efbbd46ccb54d502c843`
- Frozen feature table SHA-256: `30674ff535afc2249734ef3b87d1f9e10e631163d5f7104ed6316c50e86dec1d`
- Random seed: `20261006`
- Outcome-blind feasibility verdict: `GREEN`

## Data provenance

The study is a secondary analysis of the **public Search Arena 24K release**. The included `analysis_features.parquet` is a derived analysis table: it contains model/pair metadata and measured response/citation features used for the study, rather than the original full conversational text. The manuscript and frozen plan define the sample, variables, and deterministic citation/domain constructs.

No new participants were recruited, no new personal data were collected, no re-identification was attempted, and no LLM-generated preference labels were used.

## Anonymous-review workflow

1. Keep the source repository private under the author's normal account.
2. Add the original execution scripts only if their SHA-256 hashes match `code/EXPECTED_CODE_HASHES.txt`.
3. Mirror the repository through an anonymous-review service.
4. Inspect the anonymous mirror manually for names, usernames, emails, affiliations, personal paths, commit-author information, image/PDF metadata, and non-anonymized links.
5. Share **only the anonymous mirror URL** with reviewers/submission systems during double-anonymous review.

## After acceptance

After the review process, replace anonymous metadata with the real author information, choose explicit licenses for code/materials as appropriate, add a `CITATION.cff`, and archive a versioned release (for example via Zenodo) if desired.
