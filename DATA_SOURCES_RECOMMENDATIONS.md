# Data Sources Recommendations & Puerto Rican-Specific Data Guide

## Quick Answers to Your Questions

### Q1: Can I limit poverty and housing data to Puerto Rican people specifically?

**Answer: Yes, but it requires using IPUMS microdata instead of the Census API aggregate tables.**

**Current Situation:**
- Your current scripts (`download_poverty_data.py`, `download_housing_data.py`) download **overall state-level** data
- The Census API doesn't provide direct Puerto Rican-specific cross-tabs for most variables
- Tables like `B17001I` (poverty for Hispanic/Latino) exist, but they're for ALL Hispanics, not Puerto Rican-specific

**Solution: Use IPUMS Microdata**
- IPUMS provides individual-level microdata
- Filter by `BPLD` (Birthplace) = 11000 (Puerto Rico)
- Aggregate any variable (poverty, housing, income, education) for just Puerto Rican-born individuals
- **See:** `scripts/download_ipums_pr_specific_data.py` (created for you)

**Alternative: Hispanic/Latino Comparison Data**
- Download Hispanic/Latino aggregate data as a comparison baseline
- **See:** `scripts/download_hispanic_comparison_data.py` (created for you)
- This gives you context, but not Puerto Rican-specific

---

### Q2: What other data sources would be useful to include?

Here are recommended data sources, organized by priority:

## High Priority Additions

### 1. **Puerto Rican-Specific Socioeconomic Data (IPUMS)**
**Status:** Script created (`download_ipums_pr_specific_data.py`)

**What it provides:**
- Poverty rates (Puerto Rican-specific)
- Housing costs (Puerto Rican-specific)
- Income statistics (Puerto Rican-specific)
- Education attainment (Puerto Rican-specific)
- Employment statistics (Puerto Rican-specific)
- Demographics (age, sex, etc.)

**Why it's important:** This is the ONLY way to get truly Puerto Rican-specific data for most variables.

---

### 2. **Educational Attainment by Generation**
**Source:** IPUMS microdata

**What it provides:**
- High school completion rates (1st vs. 2nd generation)
- Bachelor's degree attainment (1st vs. 2nd generation)
- Educational mobility across generations

**Why it's important:** Shows long-term integration patterns and intergenerational mobility.

---

### 3. **Health Insurance Coverage**
**Source:** 
- Census API table `B27001I` (Hispanic/Latino - comparison)
- IPUMS microdata (Puerto Rican-specific)

**What it provides:**
- Uninsured rates
- Coverage types (public vs. private)
- Correlation with migration timing (e.g., post-Hurricane Maria)

**Why it's important:** Healthcare access is a key pull/push factor, especially for families.

---

### 4. **Hurricane/Disaster Timeline Data**
**Source:** External research compilation

**What it provides:**
- Major natural disasters in Puerto Rico (dates, impacts)
- Hurricane Maria (2017) - massive migration driver
- Hurricane Irma (2017)
- Hurricane Fiona (2022)
- Other historical events

**Why it's important:** Major push factors that drive migration spikes. Essential for understanding migration patterns.

---

### 5. **Income and Earnings Disparities**
**Source:** IPUMS microdata

**What it provides:**
- Median household income (Puerto Rican vs. overall)
- Per capita income
- Wage gaps compared to non-Hispanic whites
- Income distribution

**Why it's important:** Economic outcomes are central to understanding migration decisions and outcomes.

---

## Medium Priority Additions

### 6. **Language and English Proficiency**
**Source:** Census API table `B16001` or IPUMS

**What it provides:**
- Spanish-speaking households
- English proficiency rates
- Language spoken at home
- Correlation with generation and integration

---

### 7. **Family Structure and Household Composition**
**Source:** IPUMS microdata

**What it provides:**
- Married vs. single-parent households
- Average household size
- Multi-generational households
- Fertility rates

---

### 8. **Employment and Labor Force Characteristics**
**Source:** IPUMS microdata (you have some data, but can expand)

**What it provides:**
- Detailed occupation breakdowns
- Industry sector employment
- Full-time vs. part-time work
- Underemployment rates

---

### 9. **Commuting Patterns**
**Source:** Census API table `B08301I` (Hispanic/Latino)

**What it provides:**
- Public transit usage
- Commute times
- Car ownership
- Geographic mobility patterns

---

### 10. **Intergenerational Mobility**
**Source:** IPUMS microdata (requires multiple years/generations)

**What it provides:**
- Educational mobility (parent-child)
- Income mobility (parent-child)
- Social mobility patterns

---

## Lower Priority (But Interesting)

### 11. **Voting and Civic Engagement**
**Source:** External sources (state voter data, surveys)

**What it provides:**
- Voter registration and turnout
- Political participation patterns

---

### 12. **State Policy Context**
**Source:** External research/compilation

**What it provides:**
- Minimum wage laws by state
- Welfare benefits by state
- State taxes
- Right-to-work laws

**Why it's interesting:** These policies may influence where Puerto Ricans choose to settle.

---

### 13. **Residential Segregation Indices**
**Source:** Your county data + calculations

**What it provides:**
- Geographic concentration measures
- Segregation indices
- Neighborhood composition over time

---

### 14. **Puerto Rico Economic Indicators (Expanded)**
**Source:** FRED API (you already have some)

**Additional indicators:**
- Cost of living indices (PR vs. mainland)
- Energy costs (PR has high electricity costs)
- Healthcare access/costs in PR
- Minimum wage differences

---

## Implementation Priority

### Phase 1: Immediate (High Impact) ✅ COMPLETE
1. ✅ Run `download_ipums_pr_specific_data.py` to get Puerto Rican-specific poverty, housing, income, education, language, family structure
2. ✅ Run `download_hispanic_comparison_data.py` for comparison baseline
3. ✅ Run `create_hurricane_timeline_data.py` and research/fill in disaster timeline
4. ✅ Run `download_health_insurance_data.py` for health insurance coverage data
5. ✅ Run `download_language_data.py` for language/English proficiency data
6. ✅ Run `download_commuting_data.py` for commuting patterns data

### Phase 2: Analysis & Visualization (Next Steps)
7. Analyze and visualize the new Puerto Rican-specific data
8. Compare Puerto Rican-specific vs. overall Hispanic/Latino data
9. Correlate disaster timeline with migration patterns
10. Create visualizations for language, family structure, generation analysis

### Phase 3: Advanced Analysis
11. Intergenerational mobility analysis (requires multi-year IPUMS data)
12. Residential segregation analysis
13. State policy context compilation

---

## Scripts Created

### 1. `download_ipums_pr_specific_data.py` ⭐ PRIMARY SCRIPT
**Purpose:** Extract Puerto Rican-specific data for poverty, housing, income, education, employment, language, family structure, and more from IPUMS microdata.

**Requirements:**
- IPUMS API key (free at https://account.ipums.org/api_keys)
- `pip install ipumspy`

**Usage:**
```bash
export IPUMS_API_KEY="your_api_key_here"
python scripts/download_ipums_pr_specific_data.py
```

**Output:**
- `data/ipums_pr_specific/ipums_pr_poverty_YYYY.csv` - Poverty rates
- `data/ipums_pr_specific/ipums_pr_housing_YYYY.csv` - Median rent and home values
- `data/ipums_pr_specific/ipums_pr_income_YYYY.csv` - Income statistics
- `data/ipums_pr_specific/ipums_pr_education_YYYY.csv` - Education attainment
- `data/ipums_pr_specific/ipums_pr_employment_YYYY.csv` - Employment statistics
- `data/ipums_pr_specific/ipums_pr_demographics_YYYY.csv` - Demographics
- `data/ipums_pr_specific/ipums_pr_language_YYYY.csv` - Language and English proficiency
- `data/ipums_pr_specific/ipums_pr_family_YYYY.csv` - Family structure
- `data/ipums_pr_specific/ipums_pr_generation_YYYY.csv` - Generation analysis
- `data/ipums_pr_specific/ipums_pr_occupation_industry_YYYY.csv` - Occupation and industry

**Note:** This is the ONLY way to get truly Puerto Rican-specific data for most variables.

---

### 2. `download_hispanic_comparison_data.py`
**Purpose:** Download Hispanic/Latino aggregate data for comparison baseline.

**Requirements:**
- Just the Census API (no key needed for public data)

**Usage:**
```bash
python scripts/download_hispanic_comparison_data.py
```

**Output:**
- `data/census_acs5_hispanic_comparison/acs5_hispanic_poverty_YYYY.csv`
- `data/census_acs5_hispanic_comparison/acs5_hispanic_housing_rent_YYYY.csv`
- `data/census_acs5_hispanic_comparison/acs5_hispanic_housing_value_YYYY.csv`
- `data/census_acs5_hispanic_comparison/acs5_hispanic_health_insurance_YYYY.csv`

---

### 3. `download_health_insurance_data.py` ✨ NEW
**Purpose:** Download health insurance coverage data (Hispanic/Latino comparison).

**Requirements:**
- Census API (public, no key needed)

**Usage:**
```bash
python scripts/download_health_insurance_data.py
```

**Output:**
- `data/census_acs5_health_insurance/acs5_health_insurance_YYYY.csv`
  - Columns: insurance_coverage_rate, uninsured_rate, with_insurance, without_insurance

**Note:** For Puerto Rican-specific data, use IPUMS script above.

---

### 4. `download_language_data.py` ✨ NEW
**Purpose:** Download language and English proficiency data (Hispanic/Latino comparison).

**Requirements:**
- Census API (public, no key needed)

**Usage:**
```bash
python scripts/download_language_data.py
```

**Output:**
- `data/census_acs5_language/acs5_language_YYYY.csv`
  - Columns: english_only_rate, spanish_speaking_rate, limited_english_rate, detailed breakdowns

**Note:** For Puerto Rican-specific data, use IPUMS script above.

---

### 5. `download_commuting_data.py` ✨ NEW
**Purpose:** Download commuting patterns data (Hispanic/Latino comparison).

**Requirements:**
- Census API (public, no key needed)

**Usage:**
```bash
python scripts/download_commuting_data.py
```

**Output:**
- `data/census_acs5_commuting/acs5_commuting_YYYY.csv`
  - Columns: drove_alone_rate, carpooled_rate, public_transit_rate, walked_rate, worked_from_home_rate

**Note:** For Puerto Rican-specific data, use IPUMS script above.

---

### 6. `create_hurricane_timeline_data.py` ✨ NEW
**Purpose:** Create a template CSV file for hurricane/disaster timeline data.

**Requirements:**
- None (creates template file)

**Usage:**
```bash
python scripts/create_hurricane_timeline_data.py
```

**Output:**
- `data/puerto_rico_disasters/pr_disaster_timeline.csv`
  - Template with major events (Maria, Irma, Fiona, Georges, Hugo, economic crises)
  - **Action Required:** Research and fill in missing details manually

**Note:** This creates a template that you should research and complete with:
- Precise dates and durations
- Detailed migration data by destination state
- Economic indicators (unemployment, GDP impact)
- Recovery timeline
- Additional events

---

## Documentation

- **`scripts/GETTING_PUERTO_RICAN_SPECIFIC_DATA.md`**: Detailed guide on how to get Puerto Rican-specific data
- **This file**: Overview and recommendations

---

## Next Steps

1. **Get IPUMS API key** from https://account.ipums.org/api_keys
2. **Run all data download scripts:**
   ```bash
   # Puerto Rican-specific data (requires IPUMS API key)
   export IPUMS_API_KEY="your_api_key_here"
   python scripts/download_ipums_pr_specific_data.py
   
   # Comparison baseline data (Census API - no key needed)
   python scripts/download_hispanic_comparison_data.py
   python scripts/download_health_insurance_data.py
   python scripts/download_language_data.py
   python scripts/download_commuting_data.py
   
   # Create disaster timeline template
   python scripts/create_hurricane_timeline_data.py
   ```

3. **Research and complete** the hurricane/disaster timeline CSV file manually

4. **Integrate new data** into your visualizations and analysis

5. **Compare** Puerto Rican-specific data vs. overall Hispanic/Latino comparison data

---

## Questions?

- Check the detailed guide: `scripts/GETTING_PUERTO_RICAN_SPECIFIC_DATA.md`
- IPUMS documentation: https://usa.ipums.org/
- Census API documentation: https://api.census.gov/
