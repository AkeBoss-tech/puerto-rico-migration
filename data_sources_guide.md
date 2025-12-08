# Data Sources for Historical Puerto Rican Population by State

This guide outlines where to find historical Puerto Rican population data by state, similar to the table showing 1960, 1970, and 1980 data.

## 1. IPUMS USA (Recommended for Historical Data)

**Website:** https://usa.ipums.org/

**What it provides:**
- Microdata from U.S. decennial censuses (1850-2010)
- American Community Survey microdata (2000-present)
- Samples from Puerto Rico (1910-2017)

**How to use:**
1. Create a free account at usa.ipums.org
2. Create a custom data extract
3. Select variables:
   - `BPL` (Birthplace) - filter for Puerto Rico (value: 25000)
   - `STATEFIP` (State FIPS code) - to get state-level data
   - `YEAR` - to select specific census years
4. For 1960, 1970, 1980: Use decennial census samples
5. Download and aggregate the microdata to get state-level counts

**Advantages:**
- Most comprehensive historical data source
- Can create custom extracts
- Includes detailed demographic variables
- Free for research purposes

**API/Programmatic Access:**
- IPUMS provides REST API for programmatic access
- Documentation: https://developer.ipums.org/

---

## 2. U.S. Census Bureau API

**Website:** https://api.census.gov/

**What it provides:**
- Decennial Census API: 2000, 2010, 2020
- ACS API: 2005-present (you're already using this)

**For Historical Data (1960-1990):**
- The API doesn't directly support pre-2000 decennial data
- You'll need to use other sources for 1960-1990

**For Recent Data (2000+):**
- Decennial Census API endpoint: `https://api.census.gov/data/{year}/dec/pl`
- Variables for Hispanic origin by specific origin (Puerto Rican)
- Similar structure to your current ACS script

**Example for 2000/2010:**
```python
# Decennial Census API (2000, 2010, 2020)
url = f"https://api.census.gov/data/{year}/dec/pl?get=NAME,P004010&for=state:*"
# Note: Variable codes differ by year - check API documentation
```

---

## 3. data.census.gov (Census Bureau's Main Data Portal)

**Website:** https://data.census.gov/

**What it provides:**
- Interactive tables and data downloads
- Historical tables from various Census publications
- Searchable interface

**How to find historical Puerto Rican data:**
1. Search for: "Puerto Rican population by state" or "Hispanic origin Puerto Rican"
2. Filter by:
   - **Years:** 1960, 1970, 1980, etc.
   - **Geography:** State
   - **Dataset:** Decennial Census
3. Browse available tables
4. Download as CSV or Excel

**Note:** Some historical tables may require searching the Census Bureau's publication archives.

---

## 4. Census Bureau Publication Archives

**Website:** https://www.census.gov/library/publications.html

**Specific Reports Mentioned in Your Table:**

**1980 Data:**
- "1980 United States Census Supplementary Report S1-7"
- Available in Census Bureau library/archives

**1970 Data:**
- "Puerto Ricans in the United States," PC (2) IK, Table 15, pp. 103-104
- "Persons of Spanish Ancestry," PC (SI)-30, February 1973, Table I, p. 1
- Available at: https://www.census.gov/library/publications/1965/dec/population-pc-2-1d.html

**1960 Data:**
- Subject Report on Puerto Ricans in the United States
- Available at: https://www.census.gov/library/publications/1965/dec/population-pc-2-1d.html

**How to access:**
- Many reports are digitized and available online
- Search by publication number or title
- Some may require contacting Census Bureau customer service

---

## 5. NHGIS (National Historical Geographic Information System)

**Website:** https://www.nhgis.org/

**What it provides:**
- Historical census data with geographic boundaries
- Pre-formatted tables for common variables
- Time series data

**How to use:**
1. Create a free account
2. Browse data tables by year and topic
3. Look for "Hispanic Origin" or "Race/Ethnicity" tables
4. Filter for state-level geography
5. Download pre-aggregated tables

**Advantages:**
- Pre-processed historical data
- Geographic boundary files included
- Easier than working with microdata

---

## 6. Census Bureau Legacy Data Tools

**American FactFinder Archive:**
- https://www.census.gov/data/legacy.html
- Contains archived data from older Census Bureau tools
- May have historical tables in downloadable formats

---

## Recommended Approach for Your Project

### For 1960, 1970, 1980 Data:
1. **Primary Option:** Use IPUMS USA to create custom extracts
   - Most reliable and comprehensive
   - Can match your current data structure
   - Allows for custom aggregation

2. **Secondary Option:** Download from Census Bureau publications
   - Directly matches the sources in your table
   - May require manual data entry or PDF extraction
   - Check digitized archives first

### For 1990-2000 Gap:
- Use IPUMS USA (1990 and 2000 decennial samples)
- Or use Census Bureau API for 2000

### For 2000+ Data:
- Continue using ACS API (as you currently do)
- Or supplement with Decennial Census API for 2000, 2010, 2020

---

## Python Script Example for IPUMS Data

If you decide to use IPUMS, you'll need to:
1. Download microdata extract
2. Process it to aggregate by state and year

Example processing:
```python
import pandas as pd

# Load IPUMS microdata extract
df = pd.read_csv('ipums_extract.csv')

# Filter for Puerto Rican born
pr_born = df[df['BPL'] == 25000].copy()

# Aggregate by state and year
state_counts = pr_born.groupby(['STATEFIP', 'YEAR']).size().reset_index(name='Population')

# Map state FIPS codes to state names
# (You'll need a FIPS code mapping)
```

---

## Quick Links Summary

- **IPUMS USA:** https://usa.ipums.org/
- **Census API:** https://api.census.gov/
- **data.census.gov:** https://data.census.gov/
- **Census Publications:** https://www.census.gov/library/publications.html
- **NHGIS:** https://www.nhgis.org/
- **1960 Puerto Rican Report:** https://www.census.gov/library/publications/1965/dec/population-pc-2-1d.html

---

## Notes

- Historical data (pre-2000) is not available through the modern Census API
- IPUMS USA is the most comprehensive source for historical microdata
- Some data may require manual extraction from PDF reports
- Consider data quality notes: The original table mentions "actual figures may be much higher due to a Census Bureau undercount of minority groups"
