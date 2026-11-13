# Literature review: county variation in VA disability severity mix and group-aware cross-validation

Scope. Question: how and why does the share of VA compensation recipients rated 70%+ vary across counties and states, and how should a model predicting that share be validated when counties are clustered in states? Inclusion: government or peer-reviewed sources that I opened and could read (numbers in brackets refer to references.md); years not restricted because the VA-specific literature that could be opened is 2004-2010. Excluded: any source in the "Unverified leads" list. Four of the references (Robinson, Efron-Morris, Fay-Herriot, Clayton-Kaldor) and Meyer et al. 2018 were verified at bibliographic level only; statements about them are limited to their well-established roles and are flagged below.

## Comparison table

| Ref | Question | Data / setting | Method | Key result (as read) | Limitation for this project |
|---|---|---|---|---|---|
| [1] GAO-05-99 (2004) | Does VA assess decision consistency across 57 regional offices? | VA claims data systems | Audit | VA did not systematically assess it; judgment adds variability; no measured office-level rating differences (data limits) | No quantitative variation; pre-dates the file |
| [2] GAO-06-120T (2005) | State differences in compensation | Average payment per veteran by state | Testimony summarising audits | Up to 63% difference between states (2002); Ohio $6,710 vs New Mexico $10,851 (Dec 2004) | Dollar averages, not rating mix; averages conflate claim rate and severity |
| [3] GAO-05-655T (2005) | Same, plus quality reviews | As above | Testimony | VBA review of 1,750 decisions (hearing loss, PTSD, knee) under way | Results of that review not in this text |
| [4] CRS RL33323 | Benefit structure | Statute/regulation | Legal summary | Rates are national; rating decisions vary by office (citing GAO) | No state-level data |
| [5] Roberts 2017 | Which CV for structured data? | Simulations + case studies | Compare random vs block CV | Block CV nearly always more appropriate when predicting to new data | Ecological/species data; blocks may restrict predictor range |
| [6] Ploton 2020 | Is random CV optimistic for maps? | Central African forest inventory | Random forest, random vs spatial CV | R2 0.53 random 10-fold vs 0.14 spatial; ~0 beyond ~100 km | Strong, long-range autocorrelation; different domain |
| [7] Meyer & Pebesma 2021 | Where can a model be trusted? | Simulations | Dissimilarity index, area of applicability | CV error holds inside the AOA only | Presented for raster mapping |
| [8] Meyer 2018 (metadata only) | Leave-location/time-out validation | Antarctic temperature, soil water | Forward feature selection + target-oriented CV | Random CV overly optimistic | Not read in full |
| [9] Valavi 2019 | Practical block construction | SDM software | blockCV package | Tools to choose block size from autocorrelation range | Software paper |
| [10] Wadoux 2021 | Is spatial CV valid for map accuracy? | Biomass mapping experiment | Compare standard vs spatial CV | Spatial CV has "no theoretical underpinning"; standard CV less biased except for strongly clustered, uneven samples | About accuracy over a mapped area, not new-group generalisation |
| [11]-[13] Efron-Morris, Fay-Herriot, Clayton-Kaldor (metadata only) | Estimating many small-unit rates | Batting averages, income, disease rates | Empirical Bayes / James-Stein / Poisson-gamma | Shrinkage beats raw unit estimates in MSE | Not read in full |
| [14] Pfeffermann 2013 | State of small-area estimation | Review | Design- vs model-based, frequentist and Bayesian | Framework for areas with small or no samples | Survey-oriented; here the counts are administrative totals |
| [15] Robinson 1950 (metadata only), [16] Subramanian 2009 | Can area correlations speak for individuals? | 1930 US Census | Ecological correlation; multilevel logistic re-analysis | Area and individual associations can differ; state context matters; individualistic fallacy also exists | Not directly about VA |

## Themes

### 1. Geographic variation in VA ratings is long documented, but as dollars and decision consistency, not as county severity mix
The opened government sources [1]-[4] establish three things. First, average compensation per disabled veteran differed substantially between states (up to 63% in 2002; $6,710 to $10,851 in December 2004) [2][3]. Second, GAO attributed part of the concern to inconsistent adjudication across the 57 regional offices and said VA lacked a routine way to tell [1][2]. Third, CRS confirms that payment rates are set nationally, so state differences must come from who applies, who is awarded what rating, and who is on the rolls, not from the rate schedule [4]. None of these sources reports the share of recipients at 70%+ by county, so the present project's descriptive findings (county SD 8.1 vs 2.2 points expected from chance; 63% of variance between states) are new relative to what I could verify. The OIG and IDA reports, which the GAO testimony says examined causes (OIG) and which are known to cover state and office variation (IDA), could not be opened and are left as leads.

Implication: state differences in the high-rating share are plausibly partly administrative (regional-office practice) and partly compositional (age, service era, representation), which the file cannot separate. This is consistent with, but not proven by, the strong state effect (R2 0.62 for state mean alone).

### 2. Random CV is optimistic when units are clustered; the size of the gap is context-dependent
Roberts et al. [5] argue that random CV ignores dependence and that block CV is nearly universally more appropriate when the goal is to predict new data, even when residuals show no autocorrelation. Ploton et al. [6] give an extreme example (R2 0.53 to 0.14, near zero at distance). Meyer et al. [7][8] add that random CV can reward misleading predictors and that CV error applies only where the new data resemble the training data. In this project the gap is modest (R2 0.41 random vs 0.34 state-grouped; baseline 0.62 vs -0.05 for the state mean), which is expected here because the features (age mix, sex mix) are county-specific rather than strongly state-structured. The state-mean row is the clearest illustration of leakage: a random fold lets the model look up the state's other counties, giving 0.62, while grouped folds make this impossible (-0.05).

### 3. Is group-aware CV "correct"? A genuine disagreement, and what it means here
Wadoux et al. [10] argue spatial CV lacks theoretical grounding for estimating map accuracy and that standard CV is acceptable except under strongly clustered, unevenly dense samples. This is not a contradiction of [5][6] so much as a different target: [10] concerns accuracy of a map over a region where training locations can be thought of as representative; [5] concerns generalisation to new data/space. For RQ3 the target is explicit, prediction for a state not seen in training, so leave-state-out CV matches the target by design. The statement is a reading of these abstracts, not a result any paper states about VA data. Caveat from [5]: blocking by state removes whole regions of predictor space, so the grouped score mixes leakage removal and extrapolation (see gap G4).

### 4. Noisy proportions: shrinkage is the standard remedy, with the caveat of non-random suppression
Empirical-Bayes and James-Stein shrinkage of many small-unit proportions toward a group or model mean is the foundation of small-area estimation [11][12][13] (bibliographic verification only for the three classic papers) and is reviewed in [14]. County shares based on a few dozen recipients (the 470 excluded counties have median 67 recipients) are the textbook case. The project currently drops small counties rather than shrinking them. Note that the file suppresses counts below 10, so cells are missing not at random; the SAE literature I read does not address this specific disclosure-suppression mechanism, and I make no claim that it does.

### 5. Ecological inference
Robinson [15] (metadata verified only) and Subramanian et al. [16] (read) support the README's cautions: county associations (e.g. older share vs high-rating share) do not license individual-level statements, and state context should be modelled rather than ignored. [16] goes further: single-level analyses at either level are inadequate, supporting a multilevel formulation (county within state) as the natural next step.

## Contradictions and tensions
- Roberts [5] vs Wadoux [10] on whether spatial/blocked CV is the correct default (resolved here only by the target-definition argument above).
- GAO attributes variation partly to inconsistency [1][2]; the OIG, as relayed in secondary snippets (unverified), stresses legitimate factors such as representation rates. The opened sources do not adjudicate; the file cannot either.
- Random-vs-grouped gap: large in Ploton [6], modest in this project; the gap size depends on how state-structured the predictors are.

## Synthesis
1. The existence of state-level variation in VA outcomes is established by verified government sources, though as average dollars and decision consistency. County-level severity mix is not covered in anything I could open.
2. The project's central methodological claim (random CV overstates accuracy for state-clustered data) is supported in direction by [5][6][7], and the magnitude is plausible and smaller than in strongly autocorrelated ecological data.
3. The "state mean" benchmark and the 63% between-state variance point to a multilevel model, not more flexible ML, as the natural analysis, in line with [16] and the SAE tradition [11]-[14].
4. Limits of this review: the VA-specific literature I could verify is 2004-2010; no peer-reviewed journal study of rating geography was found in the searches; five references are bibliographic-only; search coverage was via a general web search tool, not Scopus/PubMed.
