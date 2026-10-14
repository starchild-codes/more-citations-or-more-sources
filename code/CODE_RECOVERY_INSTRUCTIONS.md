# Recovering the original execution code

The original reproducibility log records five Python files and their SHA-256 hashes. They were not present in the artifact handoff used to assemble this repository.

If the private project machine still has the original files, recover them rather than reconstructing replacements.

## Safe recovery procedure

1. Search the author's private project directories for these exact filenames:
   - `prepare_analysis_data.py`
   - `audit_feasibility.py`
   - `run_confirmatory.py`
   - `run_remaining_sensitivities.py`
   - `finalize_outputs.py`
2. Compute SHA-256 for each candidate.
3. Compare against `EXPECTED_CODE_HASHES.txt`.
4. Copy **only exact hash matches** into `code/original/`.
5. Run `python scripts/verify_artifact.py`; it will report which original scripts are present and whether their hashes match.
6. Inspect the scripts for identifying comments, hard-coded personal paths, usernames, emails, or repository URLs before creating the anonymous mirror. If redaction is necessary, keep an unmodified hash-matching archival copy private and make a clearly documented anonymous-review copy; do not pretend the modified copy has the original hash.

## Suggested instruction for a local coding agent

> Search my local project folders for the five filenames listed in `code/EXPECTED_CODE_HASHES.txt`. Compute SHA-256 for every candidate. Copy only files whose hashes match exactly into `code/original/`. Do not modify them. Then scan the copied files for personal names, usernames, emails, absolute user paths, or private repository URLs and report any anonymity risks before making changes.
