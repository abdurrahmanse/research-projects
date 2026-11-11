# Data card: Disability.csv

| | |
|---|---|
| Source | **Not confirmed.** The file was supplied without documentation. Its columns match the US Department of Veterans Affairs (VA) county-level report of disability compensation recipients. **Add the download link, fiscal year and access date here before submission** |
| Content | Number of veterans receiving VA disability compensation per county, split by service-connected disability (SCD) rating band, age band and sex |
| Size | 3,148 rows, 14 columns: FIPS code, state, county name, total, 5 rating bands, 3 age bands, male, female |
| Rows | 3,144 counties (50 states + DC) and 4 non-county rows: Puerto Rico as one total (`72000`), other US territories (`88888`), foreign countries (`00000`), unknown (`Unknown`) |
| Total recipients | 6,248,803 in the county rows; 6,331,627 including the 4 other rows |
| Outcome used | High-rating share = (`SCD rating: 70% to 90%` + `SCD rating: 100%`) ÷ total |
| Licence | **Not confirmed.** US federal government data are normally public domain; verify on the source page |
| Number format | Counts are text with thousands separators (`"2,949"`); converted in the notebook |
| Blank cells | Counts below 10 are blank (the smallest value in every column is 10). Per column: total 13, 0–20% 164, 30–40% 327, 50–60% 314, 70–90% 121, 100% 161, age 17–44 182, age 45–64 179, age 65+ 73, male and female 464 each (always blank together) |
| Consistency | In the 2,649 counties with no blank cell, the rating bands, the age bands and male + female each add up exactly to the total |
| Duplicates | No duplicate FIPS codes |
| Not in the file | Population, veteran population, year, type of disability, payment amounts |
| Sensitivity | Aggregate counts with small cells suppressed; no individual-level data |
| Handling | The raw file is never modified; all cleaning happens in the notebook |
