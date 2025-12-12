# Quick Start: Historical Data Extraction

## Setup (One-time)

1. **Install package:**
   ```bash
   pip install ipumspy pandas
   ```

2. **Get API key:**
   - Go to https://account.ipums.org/api_keys
   - Create account if needed
   - Generate API key
   - Set environment variable:
     ```bash
     export IPUMS_API_KEY='59cba10d8a5da536fc06b59d4ae2e0bca7f44727b3840e7168531562'
     ```

## Extract Data

### Step 1: IPUMS (1960, 1970, 1980)

```bash
python scripts/download_ipums_data.py
```

This will:
- Create extracts for all three years
- Wait for processing (may take 5-15 minutes)
- Download and process microdata
- Save to `data/ipums_historical/`

**Output files:**
- `ipums_puerto_rican_pop_1960.csv`
- `ipums_puerto_rican_pop_1970.csv`
- `ipums_puerto_rican_pop_1980.csv`

### Step 2: NHGIS (1970, 1980 only)

**Option A: Manual Download (Recommended)**
1. Visit https://www.nhgis.org/
2. Extract data: State level, 1970 & 1980, Hispanic Origin tables
3. Download CSV files
4. Place in `data/nhgis_historical/`
5. Run: `python scripts/process_nhgis_files.py`

**Option B: Programmatic (Requires table IDs)**
```bash
python scripts/download_nhgis_data.py
```
*(Note: You'll need to find and update table IDs first)*

## Data Format

All files match your existing ACS format:
```csv
NAME,B03001_005E,state,year
New York,986389,36,1980
...
```

## Next Steps

Combine with existing data or use in your analysis scripts!

For detailed instructions, see `scripts/README_HISTORICAL_DATA.md`




