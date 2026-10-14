# Frozen CHIIR confirmatory results

## Feasibility and sample

The outcome-blind audit was **GREEN**. The primary sample contains **4,265** decisive, English, first-turn battles. The feature file and frozen plan hashes are recorded in `feasibility_audit.json`.

## Primary association

The M4 standardized domain-redundancy coefficient is **0.028** (odds ratio **1.028**, judge-cluster bootstrap 95% CI for the coefficient **[-0.071, 0.127]**, p=0.576; 1,000 bootstrap replicates). The odds-ratio interval is [0.931, 1.136]. At fixed citation quantity, positive redundancy corresponds to less domain breadth. The estimate is compatible with modest associations in either direction.

A one-unit increase in redundancy corresponds to an estimated odds ratio of **1.017**. The model-implied probability shift for one standard deviation of redundancy, at zeroed covariate contrasts and baseline model terms, is **0.69 percentage points**. M3→M4 LR p=0.588; AIC rises from 5114.50 to 5116.21.

## Matched comparison and intent

Among **173** battles with equal citation counts and different breadth, the broader-sourced answer won **0.572** of votes (judge-cluster bootstrap 95% CI **[0.497, 0.648]**; descriptive binomial p=0.068). The interval includes 0.50.

The prespecified model-by-intent adjusted omnibus interaction was significant: LR(14)=27.05, p=0.019, N=4,108. **No intent-specific redundancy coefficient survives Holm correction**; the smallest adjusted p is 0.189. Intent labels are released automated annotations, so this is secondary evidence for heterogeneity, without an identified intent-specific effect.

## Positive controls and robustness

The response-length and citation-quantity controls replicated the previously reported positive directions (β=0.488 and β=0.410, respectively).

Most full-sample sensitivities remain near zero: all languages, all turns, grounded-only citations, conservative bare URLs, complete marker resolution, standardized citation format, ties, model-by-week, model-by-country, and equal judge weighting. Unique-domain ratio and entropy also have intervals crossing zero; their directions are not directly comparable to redundancy because larger values represent broader sourcing.

Exact model-pair estimates **disagree in sign**: 2 of 5 qualifying pairs have intervals excluding zero in opposite directions. 2 pair fits have unstable standard errors and are not interpretable as precise estimates. This heterogeneity limits a pooled model-independent interpretation.

## Predictive increment

In five judge-grouped folds, held-out log loss is M3=0.6025 and M4=0.6027; M4−M3=0.0002 (judge-bootstrap 95% CI [-0.0002, 0.0006]). Brier scores are M3=0.2070 and M4=0.2071; difference=0.0001 (95% CI [-0.0001, 0.0002]). The added breadth term does not show a reliable held-out predictive gain.

## Defensible conclusion and limits

In this observational Search Arena sample, domain redundancy has no clearly estimated **overall** association with preference after the frozen measured controls. Citation quantity and response length have positive associations. The pooled interval does not prove no breadth effect, and the discordant model-pair estimates caution against a uniform effect claim.

Domain breadth is not viewpoint diversity or independent evidence. Preference is not factual quality, and votes do not show that users inspected citations. Provider trace disclosure differs; direct visible URLs were measured even when absent from a trace. The exact matched sample is small. The public parquet has no released Support/Irrelevant/Contradict attribution labels, so the planned attribution-quality sensitivity could not be computed without additional released data. No new annotation or model judging was performed.

All numeric tables, figures, code, audit hashes, and environment versions are in this `outputs` directory and its sibling `src` directory.
