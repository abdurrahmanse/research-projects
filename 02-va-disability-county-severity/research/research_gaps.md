# Research gaps, ranked by feasibility with THIS dataset

Dataset: `data/Disability.csv`, 3,144 counties, counts by rating band, age band, sex; no denominators, no year, no source confirmation; counts below 10 blank. Reference numbers [n] point to references.md. RQ1 = how much the high-rating share varies; RQ2 = relation to age/sex/size; RQ3 = prediction in unseen states and random vs grouped CV. "Limitation" names the README limitation each gap touches.

| Rank | Gap | Feasibility | Needs beyond the file | RQ | Limitation addressed |
|---|---|---|---|---|---|
| G1 | Shrink noisy county shares (empirical-Bayes beta-binomial or Fay-Herriot-style) instead of dropping 470 small counties | High | nothing | RQ1 | Hidden small cells; small-county exclusion |
| G2 | Multilevel model (county within state, binomial counts) with state random effect; report ICC and compare predictive skill with grouped CV | High | nothing | RQ1, RQ3 | No explanation of state differences; ecological fallacy |
| G3 | Sensitivity bounds for suppressed cells (<10 treated as 1-9, not missing at random) | High | nothing | RQ1, RQ3 | Hidden small cells |
| G4 | Separate leakage from extrapolation in the random-vs-grouped gap: area-of-applicability / dissimilarity index for held-out states; per-state error | High | nothing | RQ3 | One snapshot; no external validation |
| G5 | Test whether the gap persists with spatial (distance) blocks or neighbouring-state leave-out, and measure residual spatial autocorrelation (Moran's I) | Medium | county centroids or shapefile (public Census gazetteer) | RQ3 | Leakage across neighbouring counties |
| G6 | Group by the unit that actually adjudicates (VA regional office, which can span states) rather than state | Medium | state-to-regional-office crosswalk (VA public lists; must be verified) | RQ1, RQ3 | No explanation of state differences |
| G7 | Convert shares into claim rates and decompose "who is on the rolls" from "how severe": add veteran population denominators | Low-medium | external veteran-population counts by county (ACS/VA), compatible vintage | RQ1, RQ2 | No denominators |
| G8 | Confirm source and year of the file; repeat across years to test stability of state ranking (e.g. Minnesota 37.9%) | Low (blocked until provenance known) | original VA release, multiple years | RQ1 | Source/year not confirmed; one snapshot |
| G9 | Individual-level inference (do older/female veterans receive different ratings?) | Not feasible with aggregates | claimant-level data | RQ2 | Ecological fallacy [15][16]; can only be stated as a limit |

## Notes by gap

**G1.** Justified by the SAE literature [11]-[14] (the first three are bibliographic-only verification; re-read before quoting). The README already shows 92.4% of variance is not binomial noise, so shrinkage will be mild for large counties and strong for the small ones; report raw vs shrunken ranks of the extreme counties. Cheap: counts of 70%+ and totals are already in the file.

**G2.** The state mean alone gives R2 0.62 under random folds, and 63% of variance is between states. A random-intercept binomial model gives the ICC directly and a principled prediction for known states (random effect) vs new states (population mean only), which formalises why grouped R2 collapses for the state-mean baseline. Supported by [16] on multilevel analysis.

**G3.** Suppression below 10 means each of 5 band columns can hide up to 9 recipients. For the outcome, 70-90% and 100% blanks (121 and 161 counties) can be bounded between 0 and 9 per cell; report how much the high-rating share and the modelling set change. Do not impute silently (Constitution rule on missing data applies to the project, not verified here).

**G4.** Roberts [5] warns that blocking can force extrapolation; Meyer & Pebesma [7] give a tool to quantify it. Compute, per held-out state, a dissimilarity of its counties to the training counties in feature space and relate it to the per-state error. If error tracks dissimilarity, the 0.41 to 0.34 gap is partly extrapolation, not only leakage. Also report the spread of per-fold R2 across the 10 repeats.

**G5.** Ploton [6] shows the gap can be large when autocorrelation is long-range; Valavi [9] gives a way to pick block size from the autocorrelation range. The file has FIPS codes, so centroids can be attached from a public Census gazetteer (a new input that must be cited and verified). Wadoux [10] cautions that spatial CV has no formal basis for accuracy estimation, so frame this as a robustness check of a stated target (new state), not as the "right" estimator.

**G6.** GAO and CRS [1][2][4] identify regional offices, not states, as the adjudicating units. If a crosswalk is obtained, grouping by office could show more variance explained than state. Risk: crosswalk accuracy; verify against a VA source before use (none opened in this review).

**G7.** Without denominators the project can say nothing about rates; the 2004-2005 GAO dollar disparities [2][3] mix prevalence and severity, which the file separates only for severity. Feasibility is lower because of vintage matching and because the file's year is unknown (see G8).

**G8.** The probable origin (VA GDX reports) could not be confirmed in this review (see Unverified leads in references.md). This blocks any quote of state-level findings, and the README already flags it. First action for the author: obtain the original download page, year and licence.

**G9.** Not a research gap that this dataset can close; keep as an explicit limit.

## Suggested order
G3 and G1 (same notebook cells, no new data) then G2, then G4; add G5 only if centroid data are acceptable; G8 before submission.
