# 11 · Clinical Relevance, Fairness, Ethics and Limitations

## 1. Screening vs prediction vs diagnosis vs risk stratification
| Term | Meaning | Applies here? |
|---|---|---|
| Diagnosis | Confirms a disorder (structured interview, DSM-5/ICD) | **No** |
| Screening | Brief tool flags people for further assessment (e.g., EPDS ≥ cut-off) | **Closest**: but against a *symptom item*, not a reference standard |
| Prediction (prognostic) | Forecasts future onset | **No** (no timing) |
| Risk stratification | Groups by estimated probability | **Exploratory only**, calibrated tiers, no clinical validation |

Wording rules for the thesis: "classifies self-reported anxious feeling", "symptom-based screening model", "exploratory tiers". Avoid "diagnose", "detect postpartum anxiety disorder", "early prediction", "clinical decision support".

## 2. Positioning decision
| Option | Defensible? |
|---|---|
| Exploratory predictive modelling | Yes |
| Retrospective screening-model development | Yes, as *exploratory*, with limitations |
| **Comparative methodological benchmarking** | **Yes — primary positioning** |
| Clinical prediction-model development | No (no validated outcome, no external validation, unknown population) |
| Preliminary clinical decision support | No |

**Chosen:** comparative methodological benchmarking, with an exploratory retrospective screening-model component.

## 3. Consequences of errors
| Error | Consequence in a screening context | Design response |
|---|---|---|
| False negative | Distressed mother not offered assessment; for anxiety symptoms potentially delayed care; especially serious if a suicidality signal is missed | Emphasise sensitivity at a rule-out tier; report FN analysis; never use model to *rule out* risk alone |
| False positive | Unnecessary worry, clinical workload, stigma | Report PPV vs prevalence; second-stage assessment must follow |
| Miscalibrated probabilities | Wrong tier thresholds | Calibration analysis (file 08) |
| Prevalence shift | PPV overstated if deployed where prevalence is lower than 58–65% | Show PPV vs prevalence curve |

## 4. Bias, representativeness and fairness
- **Representativeness:** unknown (single undocumented hospital questionnaire, 2022, ages 25–50, no younger mothers, no parity, SES, ethnicity or country). Findings cannot be generalised.
- **Selection bias:** convenience Google-Form respondents; non-response unknown.
- **Measurement bias:** inconsistent answer vocabularies; self-report; possibly translated instrument (unknown).
- **Label bias:** single-item outcome; possible acquiescence (Yes-sets).
- **Sensitive variables:** Age band only; "Suicide attempt" is a highly sensitive item.
- **Subgroup analysis:** feasible only by age band (5 levels); with n=326 some strata have ~35–70 cases → report CIs, treat as exploratory, no formal fairness claims. Fairness metrics (equalised odds gaps, calibration by group) can be shown, but power is low.
- **Missing demographics** are themselves a limitation: you cannot assess fairness across ethnicity, SES, parity or mode of delivery.

## 5. The "Suicide attempt" item
- 30.5% "Yes" is implausibly high; the wording ("attempt") may be mistranslated or misunderstood (e.g., "thoughts of self-harm").
- Do not use it as a clinical outcome and do not publish prevalence estimates from it.
- Primary analysis: run **with and without** (ablation A10). If included as a feature, explain that it is a co-symptom and that high-risk disclosures in a real deployment require immediate human follow-up pathways, not model output.
- Handle "Not interested to say" as a separate category.
- Ethics wording: the thesis should include a short statement on how suicidality data are handled and a pointer that any real deployment needs a clinical safety protocol.

## 6. Ethics and data governance
| Topic | Action |
|---|---|
| Secondary data use | Check university policy; many institutions treat anonymised public data as exempt but require a declaration. **Ask your supervisor/ethics office.** |
| Consent / provenance | Unknown for this dataset; record "consent status unknown" and avoid any re-identification attempt |
| Privacy | Do not link to external data; release only aggregated results and code; check Kaggle licence before redistributing the CSV (currently unverified) |
| Transparency | Publish code, configs, fold predictions, and the data card |
| Dual use / misuse | State the model is not for individual clinical use |
| Reproducibility | See `07` §6 |
| Responsible AI | Include TRIPOD+AI items, limitations, and communication of uncertainty |

## 7. Reporting guidelines and risk-of-bias
- **TRIPOD+AI** [M: Collins et al. 2024] — complete the checklist; where an item cannot be met (e.g., external validation) say "not done" and why.
- **PROBAST** [M: Wolff et al. 2019]: self-assess honestly; predicted domains: Participants (high risk: undocumented source, convenience sample), Predictors (unclear: self-report, same time as outcome), Outcome (high risk: single item, predictor-outcome overlap), Analysis (aim for low: nested CV, calibration, events-per-parameter, no leakage).
- Optionally add **PROBAST+AI** if available in your region/version (verify).
- Consider **CHAMP-ML**, **MI-CLAIM** or **DOME** checklists for ML-in-medicine reporting (verify availability/versions before citing).

## 8. Limitations to state (consolidated)
1. Outcome is a single self-reported symptom item, not a validated measure.
2. Predictors and outcome are concurrent; not "early".
3. Unknown origin, population, ethics, and heavy duplication (78% repeated patterns).
4. No external or temporal validation; no second dataset.
5. n≈326 unique patterns; wide uncertainty; subgroup analysis low-powered.
6. All features categorical and coarse; finite input space limits what any model can learn; label noise unknown.
7. Calibration holds only for this prevalence.
8. SHAP/attribution are not causal.
9. Tiers are not clinically validated and rely on assumed cost ratios.
10. Findings concern methods, not epidemiology.

## 9. Future clinical validation path (to state in Future Work)
Prospective multicentre cohort with EPDS/GAD-7 or structured interview as reference standard at defined postpartum time points; temporal and geographic external validation; impact/usability study with clinicians; fairness audits across ethnicity/SES; regulatory considerations if used as software as a medical device.
