# Data and materials

## Source data

The study uses the public **Search Arena 24K** release cited in the manuscript. The original full Search Arena records are not duplicated here.

## Derived analysis data

`artifact/data/analysis_features.parquet` is the exact frozen derived feature table used by the confirmatory analysis.

- Rows: 24,069
- Frozen SHA-256: `30674ff535afc2249734ef3b87d1f9e10e631163d5f7104ed6316c50e86dec1d`

The table contains anonymized/derived analysis fields such as model identities, anonymized judge cluster ID, language/intent metadata released with the source dataset, timestamp/week and country fields used for prespecified sensitivity analyses, response-length measures, citation/domain measures, source-category counts, and A-minus-B difference features. It does **not** contain the original full prompt/response text.

## Frozen analysis plan

`artifact/plan/analysis_plan.md`

SHA-256: `4c818f8f6702331360e3e1b7b23585fb69fe719780e2efbbd46ccb54d502c843`

## Third-party rights

This repository does not grant rights to the underlying Search Arena dataset beyond those provided by its original distributors. Users should follow the source dataset's terms and citation requirements.
