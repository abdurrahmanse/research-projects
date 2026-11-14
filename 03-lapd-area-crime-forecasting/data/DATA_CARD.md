# Data card — LAPD crime incidents, 2020–2024

## Identity and provenance

- Local file: `data/raw/CrimeData.csv` (read-only; 301,512,541 bytes)
- SHA-256: `340f6424bc40553f0c0b9522238ccb55b766f2707e79947a03e89f881b34391f`
- Rows and columns observed locally: 1,004,894 × 28
- Likely source: [Los Angeles Open Data, Crime Data from 2020 to 2024](https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-2024/2nrs-mtv8), provided by the Los Angeles Police Department
- Retrieval date and route: not supplied with the local file
- Licence: no licence statement accompanies the local file; confirm the portal's current reuse terms before redistribution

The column names, row count and date range match the official portal dataset, but this card does not claim an independently documented chain of custody for the local copy.

## Unit and scope

Each row is one recorded crime incident. The local file has unique `DR_NO` identifiers, occurrence dates from 2020-01-01 through 2024-12-30, and report dates from 2020-01-01 through 2025-03-28. The study keeps report dates through 2024-12-31 and aggregates them into 21 LAPD-area monthly counts.

The target is the number of incidents **reported** in an area-month. It is not the number of crimes that truly occurred, an individual's risk, or a causal measure of public safety.

## Columns used

| Column | Role |
|---|---|
| `DR_NO` | Duplicate/identity audit only |
| `Date Rptd` | Operational time axis and monthly target aggregation |
| `DATE OCC` | Date-range audit only |
| `AREA` | Stable panel identifier for 21 LAPD areas |
| `AREA NAME` | Human-readable label |

All person-level victim attributes, exact/approximate location, crime code, weapon, status and modus-operandi fields are excluded from modelling. This reduces leakage and avoids individual profiling.

## Known quality issues

- LAPD says the records were transcribed from paper reports and may contain inaccuracies.
- The portal masks addresses to the nearest hundred block and uses `(0°, 0°)` for some missing coordinates.
- Reporting depends on victims, police practices and administrative systems; unreported crime is absent.
- `Weapon Desc` is blank in about 67% of local rows, and several victim fields are blank or contain special codes. They are not used here.
- Victim age contains zero and implausible values. It is not used here.
- Ninety-four local rows have report dates in 2025 even though occurrence dates end in 2024; they are excluded by the declared study window.
- LAPD changed its records-management system on 2024-03-07 while moving from legacy UCR reporting to NIBRS. The sharp fall in legacy-file counts after that date is treated as measurement shift, not evidence that crime fell.

## Ethical use

This project is descriptive forecasting research. It must not be used to allocate patrols, label neighbourhoods or people as dangerous, or infer individual criminality. Place-based prediction can reproduce reporting and enforcement bias. Any operational use would require community governance, a fairness audit, current NIBRS data, and evidence beyond this historical file.
