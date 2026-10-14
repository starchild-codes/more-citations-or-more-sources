#!/usr/bin/env python3
"""Verify frozen hashes and headline CHIIR artifact outputs.

Standard library only. This does not rerun the statistical models; it verifies
that the frozen plan, derived feature table, and reported result files have not
been altered and that key values remain internally consistent.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    ROOT / "artifact/plan/analysis_plan.md": "4c818f8f6702331360e3e1b7b23585fb69fe719780e2efbbd46ccb54d502c843",
    ROOT / "artifact/data/analysis_features.parquet": "30674ff535afc2249734ef3b87d1f9e10e631163d5f7104ed6316c50e86dec1d",
}
CODE_EXPECTED = {
    "prepare_analysis_data.py": "bd6d5c5f515def0522818f44fd9f3fd5f1070964d333b01f368e4ca4d71a2569",
    "audit_feasibility.py": "e16557a05f044bae7438f19682544e5783f7b41abeecc1d82574daedbf13d4e8",
    "run_confirmatory.py": "43d90432887ce0fd7362d0f65c83f0a3718148013fadf63e14626c57d1a4af94",
    "run_remaining_sensitivities.py": "274fc23e7e7f6c9f86e8985e52fc0b0af65111642ab410067ad60bf381a68e08",
    "finalize_outputs.py": "4d17d154b56b03f75acd3e1675028d8b0a4c20a2b753bd1b4275b59b5f4544d1",
}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def close(a: float, b: float, tol: float = 5e-12) -> bool:
    return abs(a - b) <= tol

def require(ok: bool, message: str, errors: list[str]) -> None:
    if ok:
        print(f"[OK] {message}")
    else:
        print(f"[FAIL] {message}")
        errors.append(message)

def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def main() -> int:
    errors: list[str] = []
    print("== Frozen file hashes ==")
    for path, expected in EXPECTED.items():
        require(path.exists(), f"exists: {path.relative_to(ROOT)}", errors)
        if path.exists():
            got = sha256(path)
            require(got == expected, f"SHA-256 matches: {path.relative_to(ROOT)}", errors)

    print("\n== Feasibility audit ==")
    audit_path = ROOT / "artifact/logs/feasibility_audit.json"
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    require(audit.get("status") == "GREEN", "feasibility verdict is GREEN", errors)
    require(audit.get("n_feature_rows") == 24069, "feature rows = 24,069", errors)
    require(audit.get("n_primary") == 4265, "primary battles = 4,265", errors)
    require(audit.get("n_primary_nonzero_delta_redundancy") == 2057, "nonzero redundancy contrasts = 2,057", errors)
    require(audit.get("n_exact_count_match_with_breadth_difference") == 173, "exact-count breadth-different battles = 173", errors)
    require(audit.get("analysis_plan_sha256") == EXPECTED[ROOT / "artifact/plan/analysis_plan.md"], "audit records frozen plan hash", errors)
    require(audit.get("features_sha256") == EXPECTED[ROOT / "artifact/data/analysis_features.parquet"], "audit records frozen feature hash", errors)

    print("\n== Headline outputs ==")
    tables = ROOT / "artifact/outputs/tables"
    practical = read_csv(tables / "practical_effects.csv")[0]
    require(int(float(practical["n"])) == 4265, "primary M4 N = 4,265", errors)
    require(close(float(practical["beta"]), 0.0277325653190094), "primary redundancy beta matches frozen output", errors)
    require(close(float(practical["ci_low"]), -0.071458335522035), "bootstrap CI lower bound matches", errors)
    require(close(float(practical["ci_high"]), 0.1274496457133414), "bootstrap CI upper bound matches", errors)
    require(close(float(practical["p"]), 0.576), "bootstrap p = 0.576", errors)
    require(int(float(practical["bootstrap_success"])) == 1000, "primary bootstrap success = 1000", errors)
    require(close(float(practical["probability_shift"]), 0.0069308238800552), "1-SD model-implied probability shift matches", errors)
    require(close(float(practical["logloss_M4_minus_M3"]), 0.00019859230775371776), "held-out log-loss delta matches", errors)
    require(close(float(practical["brier_M4_minus_M3"]), 7.44379941034383e-05), "held-out Brier delta matches", errors)

    matched = read_csv(tables / "matched_analysis.csv")
    all_row = next(r for r in matched if r["stratum"] == "all")
    require(int(all_row["n"]) == 173, "exact-count comparison N = 173", errors)
    require(close(float(all_row["broader_win_probability"]), 0.5722543352601156), "broader-source win probability matches", errors)
    require(close(float(all_row["ci_low"]), 0.4970414201183432), "matched CI lower bound matches", errors)
    require(close(float(all_row["ci_high"]), 0.6480523666277856), "matched CI upper bound matches", errors)

    intent = read_csv(tables / "intent_analysis.csv")
    omnibus = next(r for r in intent if r["intent"] == "omnibus")
    require(int(omnibus["n"]) == 4108, "intent omnibus N = 4,108", errors)
    require(close(float(omnibus["lr"]), 27.04772251369741), "intent omnibus LR matches", errors)
    require(close(float(omnibus["p"]), 0.01898040089168544), "intent omnibus p matches", errors)
    adjusted = [float(r["holm_p"]) for r in intent if r["intent"] != "omnibus" and r["holm_p"]]
    require(min(adjusted) > 0.05, "no intent-specific Holm-adjusted p < .05", errors)

    comparisons = read_csv(tables / "model_comparisons.csv")
    m4 = next(r for r in comparisons if r["model"] == "M4")
    require(close(float(m4["aic"]), 5116.20963925003), "M4 AIC matches", errors)
    require(close(float(m4["p_vs_previous"]), 0.5882136683068302), "M3→M4 LR p matches", errors)

    print("\n== Original execution scripts ==")
    code_dir = ROOT / "code/original"
    present = 0
    for name, expected in CODE_EXPECTED.items():
        path = code_dir / name
        if not path.exists():
            print(f"[INFO] not present: code/original/{name}")
            continue
        present += 1
        require(sha256(path) == expected, f"original script hash matches: {name}", errors)
    if present == 0:
        print("[INFO] No original execution scripts are included; see code/CODE_RECOVERY_INSTRUCTIONS.md")

    print("\n== Result ==")
    if errors:
        print(f"Artifact verification FAILED with {len(errors)} issue(s).")
        return 1
    print("Artifact verification PASSED for all included frozen files and reported outputs.")
    if present < len(CODE_EXPECTED):
        print("Code-release status: PARTIAL — original execution scripts are not all present.")
    else:
        print("Code-release status: original execution scripts present and hash-verified.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
