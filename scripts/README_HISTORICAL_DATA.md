# Historical Data Extraction Guide

This guide explains how to extract historical Puerto Rican population data (1960, 1970, 1980) from IPUMS and NHGIS.

## Prerequisites

1. **Install required packages:**
   ```bash
   pip install ipumspy pandas
   ```

2. **Get an IPUMS API key:**
   - Visit https://account.ipums.org/api_keys
   - Create an account if you don't have one
   - Generate an API key
   - Set it as an environment variable:
     ```bash
     export IPUMS_API_KEY='your_api_key_here'
     ```
   - Or update the scripts directly (not recommended for security)

## Method 1: IPUMS USA (Recommended for 1960, 1970, 1980)

IPUMS provides microdata from decennial censuses. This method works for all three years.

### Steps:

1. **Set your API key:**
   ```bash
   export IPUMS_API_KEY='your_api_key_here'
   ```

2. **Run the extraction script:**
   ```bash
   python scripts/download_ipums_data.py
   ```

3. **What it does:**
   - Creates data extracts for 1960, 1970, and 1980
   - Uses birthplace (BPL) variable to identify Puerto Rican born individuals
   - Aggregates by state using person weights
   - Saves results to `data/ipums_historical/`

4. **Output format:**
   - Files: `ipums_puerto_rican_pop_1960.csv`, `ipums_puerto_rican_pop_1970.csv`, `ipums_puerto_rican_pop_1980.csv`
   - Format matches existing ACS data: `NAME, B03001_005E, state, year`

5. **Note:**
   - Extracts may take several minutes to process
   - The script will wait for extracts to complete
   - If timeout occurs, check status at https://account.ipums.org/extracts

## Method 2: NHGIS (For 1970 and 1980 only)

NHGIS provides pre-aggregated tables. Note: 1960 data is not available through NHGIS as the Hispanic origin question wasn't asked.

### Option A: Programmatic Download (Requires Table IDs)

1. **Find table IDs:**
   - Visit https://data2.nhgis.org/main/all_tst_details
   - Search for "Puerto Rican" or "Spanish Origin"
   - Filter by year (1970, 1980) and geography (State)
   - Note the dataset name and table ID

2. **Update the script:**
   - Edit `scripts/download_nhgis_data.py`
   - Update the `datasets_to_try` list with correct table IDs

3. **Run the script:**
   ```bash
   python scripts/download_nhgis_data.py
   ```

### Option B: Manual Download (Easier)

1. **Download from NHGIS website:**
   - Visit https://www.nhgis.org/
   - Create an account and log in
   - Go to "Data" → "Extract Data"
   - Select:
     - Geographic Level: **State**
     - Years: **1970, 1980**
     - Dataset: **Decennial Census**
     - Tables: Look for **"Hispanic Origin"** or **"Spanish Origin"** tables
     - Specifically look for **"Puerto Rican"** as a category
   - Submit extract and download

2. **Process downloaded files:**
   - Place CSV files in `data/nhgis_historical/`
   - Run the processing script:
     ```bash
     python scripts/process_nhgis_files.py
     ```

3. **Output:**
   - Processed files saved to `data/nhgis_historical/`
   - Format: `nhgis_puerto_rican_pop_1970.csv`, `nhgis_puerto_rican_pop_1980.csv`

## Data Format

Both methods produce CSV files with the same format as your existing ACS data:

```csv
NAME,B03001_005E,state,year
New York,986389,36,1980
New Jersey,243540,34,1980
...
```

Where:
- `NAME`: State name
- `B03001_005E`: Puerto Rican population count
- `state`: State FIPS code (2-digit)
- `year`: Census year

## Troubleshooting

### IPUMS Issues:

1. **"Extract failed" error:**
   - Check that you're using valid sample codes
   - Verify your API key is correct
   - Check extract status at https://account.ipums.org/extracts

2. **Timeout waiting for extract:**
   - Large extracts can take 10+ minutes
   - Check status manually and download when ready
   - Re-run script with longer timeout if needed

3. **No Puerto Rican data found:**
   - Verify BPL code (25000) is correct for your sample
   - Check that you're using the right sample for the year

### NHGIS Issues:

1. **Can't find table IDs:**
   - Use the manual download method instead
   - Or explore metadata at https://data2.nhgis.org/

2. **Column not found errors:**
   - NHGIS column names may vary
   - Check the CSV file manually
   - Update `process_nhgis_csv()` function with correct column names

3. **State mapping errors:**
   - Verify state names in CSV match expected format
   - May need to adjust state name mapping in processing function

## Combining with Existing Data

After extraction, you can combine historical data with your existing ACS data:

```python
import pandas as pd
import glob

# Load historical data
ipums_files = glob.glob('data/ipums_historical/*.csv')
nhgis_files = glob.glob('data/nhgis_historical/*.csv')
acs_files = glob.glob('data/census_acs5/*.csv')

# Combine all
all_data = []
for files in [ipums_files, nhgis_files, acs_files]:
    for f in files:
        all_data.append(pd.read_csv(f))

combined = pd.concat(all_data, ignore_index=True)
combined = combined.sort_values(['year', 'B03001_005E'], ascending=[True, False])
combined.to_csv('data/combined_puerto_rican_pop_all_years.csv', index=False)
```

## Resources

- **IPUMS USA:** https://usa.ipums.org/
- **IPUMS API Docs:** https://developer.ipums.org/
- **NHGIS:** https://www.nhgis.org/
- **NHGIS Data Finder:** https://data2.nhgis.org/main/all_tst_details
- **IPUMS Account:** https://account.ipums.org/

## Notes

- Historical data (1960-1980) uses different methodologies than modern ACS data
- 1960 Census did not ask about Hispanic origin directly - IPUMS uses birthplace instead
- Population counts from microdata are estimates based on sample weights
- Some states may have very small populations that round to zero in samples




