# New Data Sources Documentation

This document describes the new data sources added to the Puerto Rican migration project.

## Overview

Five new data sources have been added to enhance the analysis:

1. **Year of Arrival / Migration Patterns** - Geographic mobility data
2. **Housing Costs** - Median rent and home values
3. **Occupation/Industry** - Employment sector data
4. **Poverty Rates** - Economic hardship indicators
5. **Puerto Rico Economic Data** - Push factors (unemployment, GDP)

## Data Download Scripts

### 1. Year of Arrival / Migration Data

**Script:** `download_year_of_arrival_data.py`

**What it downloads:**
- Geographic mobility data from ACS table B07001
- Includes: same house, moved within county, moved from different state, moved from abroad
- Calculates migration rates and interstate migration rates

**Usage:**
```bash
python scripts/download_year_of_arrival_data.py
```

**Output:**
- `data/census_acs5_migration/acs5_migration_YYYY.csv`
- Columns: NAME, total_population, same_house_1yr_ago, moved_same_county, moved_different_county_same_state, moved_different_state, moved_from_abroad, migration_rate, moved_from_different_state_rate, year

**Note:** For detailed year-of-arrival cohort analysis, consider using IPUMS microdata which has MIGRATE variables that can track when Puerto Rican-born individuals moved to the mainland.

---

### 2. Housing Costs Data

**Script:** `download_housing_data.py`

**What it downloads:**
- Median gross rent (B25064_001E) - for renter-occupied units
- Median home value (B25077_001E) - for owner-occupied units
- State-level data from ACS 5-year estimates

**Usage:**
```bash
python scripts/download_housing_data.py
```

**Output:**
- `data/census_acs5_housing/acs5_housing_YYYY.csv`
- Columns: NAME, median_gross_rent, median_home_value, state, year

**Note:** These are overall state medians. For Puerto Rican-specific housing data, you would need to use detailed tables with Hispanic origin filters (may require IPUMS microdata).

---

### 3. Poverty Rates Data

**Script:** `download_poverty_data.py`

**What it downloads:**
- Poverty status data from ACS table B17001
- Total population in poverty universe and below poverty level
- Calculates poverty rates

**Usage:**
```bash
python scripts/download_poverty_data.py
```

**Output:**
- `data/census_acs5_poverty/acs5_poverty_YYYY.csv`
- Columns: NAME, total_population, below_poverty_level, poverty_rate, state, year

**Note:** This is overall state data. For Puerto Rican-specific poverty rates, consider using IPUMS microdata or detailed tables with Hispanic origin cross-tabs.

---

### 4. Occupation/Industry Data

**Script:** `download_occupation_industry_data.py`

**What it downloads:**
- Total employed population from occupation table (B24010)
- Total employed population from industry table (B24030)
- State-level summary data

**Usage:**
```bash
python scripts/download_occupation_industry_data.py
```

**Output:**
- `data/census_acs5_occupation_industry/acs5_occupation_YYYY.csv`
- `data/census_acs5_occupation_industry/acs5_industry_YYYY.csv`

**Note:** This script downloads summary data. For detailed occupation/industry breakdowns by Puerto Rican origin, you would need to use IPUMS microdata which provides OCC and IND variables that can be filtered by birthplace.

---

### 5. Puerto Rico Economic Data

**Script:** `download_puerto_rico_economic_data.py`

**What it downloads:**
- Unemployment rate (LAURT)
- Real GDP (PRGDPALL)
- Labor force (PRLF)
- Total employment (PREMP)
- Population (POPPRM)

**Data Source:** FRED (Federal Reserve Economic Data) API

**Usage:**
```bash
# Set your FRED API key (get one free from https://fred.stlouisfed.org/docs/api/api_key.html)
export FRED_API_KEY="your_api_key_here"
python scripts/download_puerto_rico_economic_data.py
```

**Output:**
- `data/puerto_rico_economic/pr_unemployment_rate.csv`
- `data/puerto_rico_economic/pr_gdp.csv`
- `data/puerto_rico_economic/pr_labor_force.csv`
- `data/puerto_rico_economic/pr_employment.csv`
- `data/puerto_rico_economic/pr_population.csv`
- `data/puerto_rico_economic/pr_economic_combined.csv` (combined dataset)

**Getting a FRED API Key:**
1. Visit https://fred.stlouisfed.org/docs/api/api_key.html
2. Sign up for a free account
3. Generate an API key
4. Set it as an environment variable: `export FRED_API_KEY="your_key"`

**Note:** The script will work with the 'demo' key for limited access, but a real API key is recommended for full functionality.

---

## Visualization Script

**Script:** `generate_new_data_visualizations.py`

**What it generates:**
- Housing cost visualizations (rent and home values over time)
- Poverty rate visualizations
- Migration/mobility pattern visualizations
- Puerto Rico economic indicator visualizations
- Correlation between PR economic conditions and mainland migration

**Usage:**
```bash
python scripts/generate_new_data_visualizations.py
```

**Output:**
All visualizations are saved to the `docs/` folder:
- `graph_housing_rent.html`
- `graph_housing_value.html`
- `graph_poverty_rates.html`
- `graph_migration_rate.html`
- `graph_interstate_migration.html`
- `graph_pr_unemployment.html`
- `graph_pr_gdp.html`
- `graph_pr_economic_combined.html`
- `graph_migration_economic_correlation.html`

---

## Data Limitations & Notes

### ACS Data Limitations

1. **Puerto Rican-Specific Data:** Many ACS variables are available at the state level but not broken down by Hispanic origin. For Puerto Rican-specific analysis, you may need to:
   - Use IPUMS microdata (recommended)
   - Use detailed tables with Hispanic origin cross-tabs (limited availability via API)
   - Use the overall state data for comparison purposes

2. **Year of Arrival:** Since Puerto Ricans are U.S. citizens, the standard "year of immigration" variable doesn't apply. The migration/mobility data provides alternative insights into movement patterns.

3. **Occupation/Industry:** The current script downloads summary data. For detailed occupation/industry analysis by Puerto Rican origin, use IPUMS microdata.

### FRED Data Notes

- FRED series IDs may change over time. If you encounter errors, check the FRED website for current series IDs.
- Some economic indicators may have different frequencies (annual, quarterly, monthly). The script uses annual data to match other datasets.
- Historical data availability varies by series.

---

## Workflow

### Complete Data Collection Workflow

1. **Download all new data sources:**
   ```bash
   python scripts/download_year_of_arrival_data.py
   python scripts/download_housing_data.py
   python scripts/download_poverty_data.py
   python scripts/download_occupation_industry_data.py
   python scripts/download_puerto_rico_economic_data.py
   ```

2. **Generate visualizations:**
   ```bash
   python scripts/generate_new_data_visualizations.py
   ```

3. **View results:**
   - Visualizations are in `docs/` folder
   - Data files are in `data/` subdirectories
   - Visualizations are already integrated into `index.html`

---

## Integration with Existing Project

The new visualizations have been integrated into `index.html`:

- **Housing Costs:** Added to "Socio-Economic Reality" section (Figures 16-17)
- **Poverty Rates:** Added to "Socio-Economic Reality" section (Figure 18)
- **Migration Patterns:** Added to "Socio-Economic Reality" section (Figures 19-20)
- **Puerto Rico Economic Data:** New section "Puerto Rico Economic Push Factors" (Figures 21-23)

---

## Future Enhancements

Potential improvements for these data sources:

1. **IPUMS Integration:** Use IPUMS microdata to get Puerto Rican-specific breakdowns for all variables
2. **Detailed Occupation/Industry:** Expand occupation and industry categories
3. **Cohort Analysis:** Use IPUMS MIGRATE variables for detailed year-of-arrival cohort analysis
4. **Additional Economic Indicators:** Add more PR economic indicators (inflation, wages, etc.)
5. **County-Level Analysis:** Expand housing and poverty data to county level for more granular analysis

---

## Questions or Issues?

- Check the Census API documentation: https://api.census.gov/
- Check FRED API documentation: https://fred.stlouisfed.org/docs/api/
- For IPUMS data: https://usa.ipums.org/

