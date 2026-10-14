# Frozen Analysis Plan — ACM CHIIR 2027

**Project:** More Citations or More Sources? Source Breadth in Human Preferences for Generative Search  
**Frozen:** 2026-10-05  
**Version:** 1.7 — final pre-outcome measurement and identifiability hardening. The primary sample remains independent of automated intent labels; RQ3 retains model-by-intent nuisance terms. The feasibility gate now requires a connected model-comparison graph, a full-rank and reasonably conditioned M4 design, and meaningful within-pair redundancy variation. A conservative bare-URL robustness definition was added. Audit reports are cryptographically bound to both this plan and the exact feature file. No source-breadth preference-effect estimate had been inspected before this amendment.  
**Status:** Confirmatory plan. Do not change primary RQs, filters, or outcomes after examining source-breadth preference coefficients. Any later changes must be labeled exploratory.

## 1. Objective

Test whether user preference between two search-augmented LLM responses is associated with **source breadth across web domains beyond citation quantity**, and whether the quantity–breadth relationship differs by information-seeking intent.

The study uses the public Search Arena 24K release. No participant recruitment, paid APIs, new LLM judging, or subjective outcome annotation is required.

## 2. Construct boundaries

- **Citation quantity** means the number of distinct canonical source URLs visibly cited in the assistant answer. Numeric citation markers (for example `[1]`) must resolve through that turn's Search Arena web-search trace; direct Markdown/autolink/bare URLs are measurable user-visible sources whether or not the provider disclosed them in the trace. This format-invariant definition was adopted before any preference-effect estimation after confirming that providers use different visible citation syntaxes and trace completeness can differ by provider.
- **Source breadth** means the number of distinct **registrable domains** represented by those resolved cited URLs.
- **Domain redundancy** = citation quantity − source breadth.
- Domain breadth is **not** called viewpoint diversity, perspective diversity, source independence, factual quality, or political diversity.
- Preference is an observed human vote. The study is observational; language such as “causes preference” is prohibited.

## 3. Unit of analysis and outcome

The unit is one Search Arena battle for a single-turn conversation.

Primary outcome:

- `Y = 1` if `winner == model_a`
- `Y = 0` if `winner == model_b`
- ties and “both bad” are excluded from the primary analysis.

A tie-inclusive robustness analysis may later use the Search Arena Bradley–Terry convention of 0.5 for ties, but it cannot replace the decisive-vote primary analysis.

## 4. Primary sample — fixed before outcomes are modeled

A record enters the primary sample only if all are true:

1. A human vote is present and is decisive (`model_a` or `model_b`).
2. `turn == 1`.
3. Primary language is English (`languages[0] == "English"`).
4. Both sides are search-augmented models. The known non-search comparator `gemini-2.5-pro` and mapped aliases are excluded.
5. **No minimum citation-count threshold is imposed in the primary sample.** Zero- and one-citation responses remain in the primary sample because excluding them would condition on provider-specific citation behavior and create selection bias. `C=0, U=0, R=0` for responses with no measurable visible sources.
6. Both sides have nonempty model names and messages. A disclosed first-turn web-search trace is **not required** for inclusion: some providers disclose incomplete or empty traces. Trace availability is measured diagnostically rather than used as a primary inclusion criterion.
7. **Primary intent is not an inclusion criterion for the main analysis.** Rows with `Other`, missing, or otherwise unusable intent annotations remain eligible for the primary RQ as long as the other criteria hold. This keeps the central breadth result independent of Search Arena's automated intent annotation. The eight pre-specified intent categories (Factual Lookup, Info Synthesis, Analysis, Recommendation, Explanation, Creative Generation, Guidance, Text Processing) are used only for secondary RQ3 heterogeneity analyses.

No exclusions may depend on whether a higher-breadth answer won.

## 5. Citation resolution — deterministic

For each side independently:

1. Read the first assistant answer.
2. Read the first turn of `system_{side}_metadata["web_search_trace"]`.
3. Construct a map from trace marker ID to URL and a canonicalized set of trace URLs.
4. Parse numeric citation markers appearing in the answer, including `[1]`, `[1][2]`, and comma-separated forms such as `[1, 2]`; resolve these through the trace marker map.
5. Parse direct Markdown links, autolinks, and bare `http(s)` URLs shown in the answer. A syntactically valid direct URL is a user-visible source **even if it is absent from the disclosed search trace**, because provider traces can be incomplete. Record separately whether each direct URL is trace-grounded.
6. Combine resolved numeric-marker URLs with all parseable direct-link URLs and deduplicate by canonical URL.
7. Primary citation quantity `C` is the number of **distinct measurable user-visible source URLs**, not all retrieved URLs and not repeated mentions of the same source. Numeric markers that cannot be resolved to a URL are not assigned a domain.
8. Secondary quantities include citation mentions, numeric-marker counts, direct-link counts, trace-grounded citation count/share, and unresolved numeric-marker counts.
9. Record unresolved/invalid references; do not silently treat them as valid sources.

The primary analysis concerns **what sources the user can see**, not all retrieved URLs and not only sources that vendors disclose in their traces. A grounded-only citation definition is retained as a robustness analysis. Using canonical URLs rather than provider-specific marker syntax makes `C` comparable across model families.

Because a bare URL can occasionally be answer content rather than a citation, a conservative pre-specified sensitivity retains all resolved numeric citations, Markdown links, and autolinks, but retains a bare URL only when it is trace-grounded. This sensitivity does not replace the primary format-invariant user-visible definition.

## 6. Domain extraction — deterministic

Before URL deduplication, canonicalization lowercases the host, removes fragments and default ports, removes only standard tracking parameters (`utm_*`, `gclid`, `fbclid`, `msclkid`, `mc_cid`, `mc_eid`), sorts remaining query parameters, and normalizes a leading `www.`. Semantic query parameters (for example a YouTube video ID) are retained. A robustness analysis also checks a stricter query-stripped URL identity.

Registrable domains are computed using `tldextract` with its bundled Public Suffix List snapshot and network fetching disabled. Examples:

- `news.bbc.co.uk` → `bbc.co.uk`
- `en.wikipedia.org` → `wikipedia.org`
- `subdomain.example.com` → `example.com`

Primary breadth `U` = number of unique registrable domains across the `C` distinct cited URLs.

Primary redundancy:

`R = C - U`

Interpretation: at fixed citation quantity, larger `R` means more citation slots come from domains already represented.

Robustness breadth measures:

- unique-domain ratio `U/C`
- normalized Shannon entropy of cited-domain counts
- unique canonical URL count

## 7. Response-level covariates — fixed

For each side:

- citation quantity `C` (distinct resolved visible URLs)
- unique domain count `U`
- domain redundancy `R`
- normalized domain entropy
- response word count
- model identity
- primary intent (conversation-level)
- deterministic source-category counts using the published Search Arena taxonomy: YouTube, government/education, wiki, U.S. news, foreign news, social media, community/blog, technical/coding, academic journal, retail, and other. The `other` category is omitted from the regression controls as the reference category so citation quantity plus category composition are not perfectly collinear.

If a citation-format experimental condition is present in the released schema, it will be included as a covariate and used for a standardized-format robustness subset. If no such field is publicly released, this limitation will be stated rather than inferred.

## 8. Primary estimand and model

The primary parameter is the association of **domain redundancy with preference while citation quantity is controlled**.

For each battle, features are represented as A-minus-B differences. Continuous difference features are standardized over the primary analysis sample.

Primary contextual Bradley–Terry/logistic form:

`logit P(A wins) = alpha_side + (theta_modelA - theta_modelB) + beta_C*ΔC + beta_R*ΔR + beta_L*ΔLength + source-category controls`

`alpha_side` is a nuisance intercept for any residual left/right (A/B) position preference. Model sides are randomized in Arena, but explicitly estimating this intercept prevents a small presentation-side bias from leaking into model or source-feature coefficients.

- `theta` terms capture model strength in Bradley–Terry form.
- `beta_C` estimates the association of citation quantity with preference.
- **`beta_R` is the primary coefficient.** At fixed citation quantity, a positive `beta_R` means greater same-domain redundancy is associated with higher preference; a negative value means greater source breadth is associated with higher preference.
- Tests are two-sided. No directional hypothesis is required for acceptance of the design.

Effect reporting must include coefficient/odds interpretation, predicted probability contrasts, and 95% confidence intervals; p-values alone are insufficient.

## 9. High-credibility matched analysis

Secondary confirmatory analysis selects battles satisfying:

- `C_A == C_B`, where `C` is distinct resolved visible URLs
- `R_A != R_B`

Define the broader-sourced response as the one with lower `R` / higher `U`.

Report:

- proportion of matched battles won by the broader-sourced response
- judge-cluster bootstrap 95% confidence interval (missing judge IDs become row-specific singleton clusters rather than being dropped)
- conventional two-sided binomial test against 0.50 as a descriptive companion, with the cluster-bootstrap interval treated as the primary uncertainty estimate
- result stratified by breadth advantage of +1, +2, and +3 or more unique domains where counts permit

This analysis is confirmatory but **not required to contain 800 observations**; the full contextual model is primary.

## 10. Intent heterogeneity

RQ3 is tested through omnibus interactions, not by fishing across separate intent regressions. The Search Arena intent labels are released automated annotations rather than newly collected human labels; therefore intent heterogeneity is secondary to the primary RQ and the main source-breadth result must stand without it.

The RQ3 sample is restricted to the eight pre-specified non-`Other` intent labels, but this restriction does not affect RQ1/RQ2. Both the reduced and full RQ3 models include **model × intent nuisance terms**, allowing each model's Bradley--Terry strength to vary by intent. This prevents task-specific model quality from being absorbed by citation-feature interactions.

Compare that nuisance-adjusted base model against a model additionally containing:

- `ΔC × primary_intent`
- `ΔR × primary_intent`

First perform one omnibus likelihood-ratio test for the added citation-feature interaction terms. Only if the omnibus result supports heterogeneity will intent-specific coefficients be treated as confirmatory. Multiple intent-specific tests use Holm correction.

## 11. Estimation and nested-model comparison

The confirmatory fixed-effect logistic/Bradley–Terry models are fit **without penalization** so log-likelihood, AIC, and likelihood-ratio comparisons have their standard interpretation. A ridge-regularized contextual Bradley–Terry fit matching the Search Arena authors’ implementation is retained only as a robustness check if convergence or quasi-separation is encountered.

## 12. Source-category robustness

To test whether breadth is merely proxying for particular source types, compare nested models:

- M0: model-strength terms only
- M1: + response length
- M2: + citation quantity
- M3: + pre-specified source-category composition
- M4: + domain redundancy/source breadth

Report likelihood-ratio comparisons where valid plus AIC and pseudo-R². The key check is whether the source-breadth coefficient is materially stable from M2/M3 to M4.

## 13. Model-identity robustness

A source-breadth signal could be a disguised provider/model effect. Therefore:

1. Main model includes Bradley–Terry model-strength terms.
2. Repeat the primary relationship within the largest exact model-pair strata.
3. Report heterogeneity rather than pooling silently if major model pairs disagree.
4. A result that disappears within model-pair strata will be interpreted as model-level confounding, not as an independent source-breadth preference effect.

## 14. Dependence and uncertainty

If a public anonymized user/judge identifier is present, uncertainty is estimated with a **cluster bootstrap at that identifier level**, retaining all of a sampled user's battles together.

If no reusable user/judge identifier is present in the public release, the pre-specified fallback is a battle-level nonparametric bootstrap, and the inability to cluster repeated judges will be disclosed.

Use 1,000 bootstrap replicates for final estimates; 200 may be used for pipeline debugging only.

## 15. Missingness and parser quality

Before preference modeling, report:

- fraction of numeric citation markers resolvable to URLs through the disclosed trace
- fraction of direct visible URLs that are also present in the disclosed trace (a grounding diagnostic, **not** a validity requirement for user-visible sourcing)
- fraction of responses with zero, one, or two-plus measurable visible source URLs
- missingness/trace-disclosure patterns by model family
- distribution of `C`, `U`, and `R` by model family **without conditioning on winner**

The primary sample does **not** exclude zero- or one-citation responses and does not require a nonempty disclosed trace. A grounded-only citation subset and a complete-numeric-resolution subset are robustness analyses.

If numeric marker resolution differs sharply by model, this is treated as a design warning and investigated before outcome analysis. Provider-specific trace incompleteness is treated as a telemetry limitation, not as evidence that a visible direct URL is not a citation.

## 16. Feasibility gates — run before preference coefficients

The audit script may inspect schema, counts, source distributions, model pairs, and intent distributions, but it must not estimate the association between source breadth and winner.

### GREEN

Proceed if all hold:

- ≥1,500 usable primary battles
- ≥300 primary battles with `ΔR != 0`
- ≥3 major exact model-pair strata each have ≥100 usable battles and meaningful redundancy variation
- each of those major model-pair strata has ≥20 battles with nonzero `ΔR`
- median parse/resolution rate for measurable visible references ≥95% overall; unresolved numeric markers are audited by model family rather than allowing trace incompleteness to delete direct visible URLs
- mean measurable-reference parse/resolution rate ≥90% within every major model family (defined operationally as a family contributing at least 100 response sides to the audited data)
- no single model family accounts for >80% of all nonzero `ΔR` variation
- the model-comparison graph is connected
- the full M4 design matrix is full rank
- `|corr(ΔC, ΔR)| ≤ .95` and the standardized M4 design condition number is ≤1,000; exceeding either threshold yields YELLOW rather than silently proceeding with weakly identified quantity/breadth coefficients

### YELLOW

Reassess but do not automatically abandon if:

- 800–1,499 usable primary battles, or
- 150–299 battles with `ΔR != 0`, or
- only two major model-pair strata contain meaningful variation, or
- measurable-reference parse/resolution is 85–94% overall.

### KILL/PIVOT

Do not use this as the CHIIR full-paper core if any hold:

- <800 usable primary battles
- <150 with `ΔR != 0`
- breadth/redundancy is almost deterministic from model identity
- user-visible source URLs cannot be measured consistently enough across citation formats to derive domains
- a literature check before submission identifies prior work testing the same quantity × domain-breadth × intent relationship on in-the-wild Search Arena preferences.

## 17. Robustness analyses — pre-specified

1. English-only primary → all languages
2. first-turn primary → all turns where turn-level citation resolution is valid
3. `R = C-U` → unique-domain ratio
4. `R = C-U` → normalized Shannon entropy
5. primary canonical-URL identity → query-stripped canonical-URL identity
6. primary visible-source definition → grounded-only citation subset
7. primary visible-source definition → conservative bare-URL handling (off-trace bare URLs excluded; Markdown/autolinks retained)
8. primary sample → complete-numeric-resolution subset
9. contextual BT → exact model-pair strata
10. full controlled model → exact citation-count matched analysis (naturally restricted to pairs with enough citations for breadth to differ)
11. source categories included vs omitted
12. decisive votes → tie-inclusive BT sensitivity, if implementation is stable
13. practical incremental value → 5-fold judge-grouped out-of-sample comparison of M3 vs M4 using held-out log loss and Brier score; training-fold standardization only; judge-cluster bootstrap for paired loss differences
14. citation-attribution quality subset → on Search Arena's released attribution subset only, repeat M4 with attribution-volume plus support/irrelevant-share controls derived from the authors' released Support/Irrelevant/Contradict labels; no new LLM judging
15. temporal drift → repeat M4 with model-by-calendar-week nuisance interactions (ISO week; levels with <20 primary battles pooled)
16. locale heterogeneity → repeat M4 with model-by-client-country nuisance interactions (countries with <100 primary battles pooled into `__OTHER__`)
17. judge-balanced estimand → inverse-within-judge row weighting so each judge contributes equal total weight; uncertainty is estimated by resampling judge clusters and refitting the weighted model

## 17A. Positive-control replication diagnostic

Before interpreting the novel redundancy coefficient, report whether the reconstructed feature pipeline reproduces the previously published Search Arena directions for two established response characteristics: response-length difference and citation-count difference should each have positive coefficients in a Bradley--Terry/logistic model with model strengths and citation-format control. This diagnostic is **not** an exclusion gate and does not determine whether the breadth hypothesis is accepted; disagreement triggers parser/model investigation and is reported transparently.

## 18. Multiple testing and researcher degrees of freedom

- Primary coefficient: `beta_R` in the pre-specified primary model.
- Primary alpha: 0.05, two-sided.
- RQ3 intent-specific tests are secondary to an omnibus test and use Holm correction.
- Exploratory analyses must be explicitly labeled exploratory.
- No model/specification is selected because it produces a preferred sign or p-value.

## 19. Permitted interpretations

Permitted:

- “Domain redundancy/source breadth is associated with preference after measured controls.”
- “The association differs by information-seeking intent.”
- “Citation quantity explains more/less preference variation than domain breadth in this setting.”

Prohibited without new evidence:

- “Source breadth causes preference.”
- “Users consciously inspect source diversity.”
- “More domains mean more viewpoints.”
- “Broader sourcing is more factual/accurate.”
- “These results generalize to all search users.”

## 20. Outcome-independent interpretation matrix

- Quantity + breadth both informative → preference reflects both citation abundance and source breadth.
- Quantity informative, breadth near zero with tight CI → citation abundance is the stronger preference cue in this setting.
- Breadth informative, quantity attenuates → prior citation-count effects may partly proxy source breadth.
- Redundancy positively associated → concentrated sourcing is associated with preference after controls.
- Strong intent interactions → sourcing preferences are task-dependent.
- Both near zero with tight intervals → neither characteristic independently explains much preference after measured controls.

## 21. Freeze rule

The SHA-256 hash stored in `FROZEN_PLAN.sha256` identifies this exact plan. The analysis scripts verify it before running. A GREEN audit additionally stores the SHA-256 of the exact feature parquet; confirmatory scripts refuse to run if either the plan hash or feature-file hash differs from the audited version. Any modified plan must be given a new version and changes must be documented before examining corresponding outcome associations.

### v1.2 change log (made outcome-blind)

Two changes were made before any source-breadth→preference coefficient was inspected: (1) the ≥2-citations-per-side primary inclusion rule was removed because published provider-level marginal citation rates show it would create severe provider-dependent selection; and (2) direct user-visible URLs are counted whether or not they appear in a provider's disclosed trace, because prior auditing shows trace disclosure can be incomplete, especially for OpenAI. Both changes align measurement with the paper's user-facing construct and reduce avoidable selection/telemetry bias.

### v1.3 change log (made outcome-blind)

URL identity was hardened before outcome modeling: common tracking parameters are removed while semantic query parameters are retained, bare visible URLs are parsed in addition to Markdown/autolinks, and source-category controls are aligned to Search Arena's published source taxonomy (with `other` omitted as the regression reference category). These changes prevent duplicate-source inflation and improve control for known source-type preference effects.


### v1.4 change log (made outcome-blind)

The plan wording was made internally consistent with the already-adopted v1.2 user-visible-source rule: direct visible URLs need not appear in provider traces, whereas numeric markers must resolve through the trace. The obsolete robustness item comparing marker count to canonical-URL count was replaced with the pre-specified query-stripped URL-identity sensitivity. The confirmatory analysis executable is additionally locked to require a GREEN outcome-blind audit report. No source-breadth→preference coefficient had been inspected.


## Pre-outcome amendment log

- **v1.1:** format-invariant citation parsing after provider citation-syntax differences were identified.
- **v1.2:** removed the >=2-citations-per-side primary inclusion filter after published provider-level citation rates showed that it would induce provider-dependent selection.
- **v1.3–v1.4:** hardened URL canonicalization, source taxonomy, and the GREEN audit lock.
- **v1.5 (2026-10-06):** added A/B position intercept; removed model-strength ridge penalty from the confirmatory fit so LR/AIC comparisons are valid; made missing judge IDs singleton bootstrap clusters rather than dropping them; made the matched-analysis CI judge-cluster-aware; clarified intent labels as secondary released annotations. **No source-breadth preference coefficient had been estimated before these changes.**


### v1.6 change log (made outcome-blind)

Before any source-breadth→preference coefficient was inspected, the primary sample was made independent of the released automated intent labels. `Other` and missing-intent rows are now retained for the central RQ. Intent labels are used only for RQ3, whose models now include model-by-intent nuisance terms so task-specific model performance cannot create a spurious citation-feature interaction.

### v1.7 change log (made outcome-blind)

Before any source-breadth→preference coefficient was inspected, the feasibility gate was strengthened to require a connected model-comparison graph, a full-rank and reasonably conditioned M4 design, bounded `ΔC`–`ΔR` collinearity, and at least 20 nonzero redundancy contrasts within each of three major model-pair strata. Audit reports are now SHA-256-bound to the exact feature file as well as the analysis plan. A conservative bare-URL sensitivity was added to exclude off-trace bare URLs while retaining numeric, Markdown, and autolink citations. These additions reduce identifiability and source-misclassification risks without changing the primary estimand.

### v1.8 change log (made outcome-blind)

Before any source-breadth→preference coefficient was inspected, two secondary validation analyses were added without changing the primary estimand or model: (1) judge-grouped out-of-sample validation comparing M3 and M4 on held-out log loss and Brier score, with all observations from a judge kept in the same fold and all standardization learned from training folds only; and (2) a citation-quality-controlled sensitivity using only Search Arena's released citation-attribution subset and its authors' Support/Irrelevant/Contradict labels. The latter adds attribution volume plus support and irrelevant shares as nuisance controls and makes no new LLM calls. These analyses test practical incremental value and a citation-quality alternative explanation; neither can replace or rescue the pre-specified primary result.
### v1.9 change log (made outcome-blind)

Before any source-breadth→preference coefficient was inspected, two nuisance sensitivities were added to address residual model-quality confounding: (1) model-by-calendar-week interactions allow model strength to drift over the collection period, and (2) model-by-client-country interactions allow model strength to vary across adequately represented locales, with sparse countries deterministically pooled. The feature table now retains the public timestamp as an ISO week and extracts client country only when the two response-side metadata records agree. These are robustness analyses only; they do not alter the primary estimand, sample, or model. A non-gating positive-control diagnostic was also added: before interpreting the novel breadth effect, the pipeline reports whether it recovers the previously published positive directions for response length and citation count in Search Arena. The manuscript also commits to reporting practical magnitude (standardized odds ratio, raw-unit odds ratio, model-implied probability shift, and held-out predictive increment) and to interpreting non-significance through interval precision rather than treating `p>0.05` as evidence of no effect. A judge-balanced sensitivity was added so repeated-vote clustering is complemented by an alternative point estimand in which each judge contributes equal total weight; this guards against a small number of prolific judges dominating the coefficient.

