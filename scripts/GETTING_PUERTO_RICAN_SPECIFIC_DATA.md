# Getting Puerto Rican-Specific Data for Poverty, Housing, and Other Variables

## Current Situation

Currently, your poverty and housing data scripts download **overall state-level** data, not data specific to Puerto Rican populations. This is because:

1. **Census API Limitations**: The ACS API doesn't provide direct cross-tabs for most variables by Puerto Rican origin
2. **Table Structure**: Tables like `B17001I` (poverty for Hispanic/Latino) and `B25064I` (rent for Hispanic/Latino) exist, but they don't break down by specific Hispanic origins like Puerto Rican

## Solutions: How to Get Puerto Rican-Specific Data

### Option 1: IPUMS Microdata (RECOMMENDED)

**Best approach**: Use IPUMS microdata to filter ANY variable by Puerto Rican birthplace.

**How it works:**
- IPUMS provides individual-level microdata
- Filter by `BPLD` (Birthplace Detailed) = 11000 (Puerto Rico)
- Then aggregate housing, poverty, income, occupation, etc. variables for just Puerto Rican-born individuals
- Use person/household weights (`PERWT`, `HHWT`) to get accurate population estimates

**Advantages:**
- Can get ANY variable broken down by Puerto Rican origin
- Can create custom cross-tabs and aggregations
- More flexible than pre-formatted tables
- Free for research use

**Variables you can extract for Puerto Rican population:**
- Poverty status (`POVERTY`)
- Housing costs (`RENT`, `VALUEH`)
- Income (`FTOTINC`, `INCTOT`)
- Occupation (`OCC`, `OCC1950`, `OCC1990`)
- Industry (`IND`, `IND1950`, `IND1990`)
- Education (`EDUC`, `EDUCD`)
- Age, sex, marital status, etc.
- Year of arrival/migration patterns (`MIGRATE`, `YRIMMIG`)

**See:** `scripts/download_ipums_pr_specific_data.py` (to be created)

---

### Option 2: Census API Detailed Tables with Hispanic Origin

Some tables have Hispanic/Latino versions, but they're for ALL Hispanics, not Puerto Rican-specific:

- `B17001I`: Poverty Status (Hispanic or Latino)
- `B25064I`: Median Gross Rent (Hispanic or Latino)
- `B25077I`: Median Home Value (Hispanic or Latino)

**Limitation**: These are for all Hispanic/Latino, not Puerto Rican-specific.

**Partial workaround**: You can:
1. Download data for all Hispanics (B17001I, etc.)
2. Download Puerto Rican population data (B03001_005E)
3. Compare ratios, but this doesn't give you direct Puerto Rican-specific medians

---

### Option 3: Census Detailed Tables API (Advanced)

The Census Bureau has some detailed tables that cross-tabulate variables by detailed Hispanic origin, but they're:
- Limited availability
- Often require multi-year samples
- May require using the Census Data API with complex queries

**Example**: Some detailed tables exist for larger Hispanic subgroups, but Puerto Rican-specific housing/poverty tables are rare in the public API.

---

## Recommended Approach

**Use IPUMS microdata** to create Puerto Rican-specific datasets. A script is provided below to download and process this data.

---

## Additional Useful Data Sources

Beyond poverty and housing, here are other valuable data sources to consider:

### 1. **Educational Attainment** (Puerto Rican-specific via IPUMS)
- High school completion rates
- Bachelor's degree attainment
- By generation (1st vs. 2nd generation)

### 2. **Income and Earnings** (Puerto Rican-specific via IPUMS)
- Median household income
- Per capita income
- Income inequality (Gini coefficient)
- Wage gaps compared to non-Hispanic whites

### 3. **Employment and Labor Force** (Puerto Rican-specific via IPUMS)
- Unemployment rates
- Labor force participation
- Underemployment
- Work hours (full-time vs. part-time)

### 4. **Health Insurance Coverage** (via Census API)
- Table `B27001I`: Health Insurance Coverage Status (Hispanic or Latino)
- Could correlate with migration patterns

### 5. **Language and English Proficiency** (via Census API)
- Table `B16001`: Language Spoken at Home
- English proficiency rates
- Spanish-speaking households

### 6. **Family Structure** (Puerto Rican-specific via IPUMS)
- Married vs. single-parent households
- Average household size
- Multi-generational households
- Fertility rates

### 7. **Migration and Year of Arrival** (via IPUMS)
- Detailed year-of-arrival cohorts
- Migration patterns (from PR vs. from other states)
- Geographic mobility

### 8. **Commuting Patterns** (via Census API)
- Table `B08301I`: Means of Transportation to Work (Hispanic or Latino)
- Commute times
- Public transit usage

### 9. **Disaster/Event Data** (External Sources)
- **Hurricane Maria (2017)**: Impact on migration
- **Hurricane Irma (2017)**: Impact on migration
- **Puerto Rico Economic Crisis (2006-2016)**: Debt crisis impact
- Historical natural disasters

### 10. **Puerto Rico-Specific Economic Indicators** (FRED - Already using some)
- Minimum wage differences (PR vs. mainland)
- Cost of living indices
- Energy costs
- Healthcare access/costs in PR

### 11. **Geographic Concentration Data** (Your county data + additional)
- Residential segregation indices
- Neighborhood composition
- Geographic clustering over time

### 12. **Voting and Civic Engagement** (External sources)
- Voter registration and turnout
- Political participation

### 13. **Intergenerational Mobility** (via IPUMS with multiple years)
- Compare 1st vs. 2nd generation outcomes
- Parent-child educational/income mobility

### 14. **Housing Characteristics** (Puerto Rican-specific via IPUMS)
- Crowding (persons per room)
- Owner vs. renter occupancy
- Housing age/condition
- Cost burden (housing costs as % of income)

### 15. **State Policy Context** (External sources)
- Minimum wage laws by state
- Welfare benefits by state
- State taxes
- Right-to-work laws
- Driver's license policies (PR uses U.S. licenses)

---

## Data Source Priority Recommendations

**High Priority:**
1. ✅ IPUMS data for Puerto Rican-specific poverty and housing (create script)
2. ✅ Educational attainment by generation (IPUMS)
3. ✅ Income/earnings disparities (IPUMS)
4. ✅ Health insurance coverage (Census API - B27001I, then IPUMS for PR-specific)
5. ✅ Hurricane/disaster timeline data (external research)

**Medium Priority:**
6. Language and English proficiency
7. Family structure and household composition
8. Employment and labor force characteristics
9. Commuting patterns
10. Intergenerational mobility

**Lower Priority (but interesting):**
11. Voting and civic engagement
12. State policy context data
13. Residential segregation indices

---

## Next Steps

1. **Create IPUMS script** to extract Puerto Rican-specific poverty, housing, income, education data
2. **Download Hispanic-origin tables** from Census API (B17001I, B25064I) as a comparison baseline
3. **Research and compile disaster/event timeline** data for Puerto Rico
4. **Add health insurance coverage** data
5. **Extract additional IPUMS variables** based on your research questions

See the script `download_ipums_pr_specific_data.py` for implementation.
