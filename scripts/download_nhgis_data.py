"""
Download historical Puerto Rican population data from NHGIS.

This script uses the IPUMS API to access NHGIS pre-aggregated tables
for Puerto Rican Hispanic origin by state for 1970 and 1980.

Note: 1960 Census did not include Hispanic origin question, so data
for that year is not available through NHGIS.

Requirements:
- pip install ipumspy
- IPUMS API key (get from https://account.ipums.org/api_keys)
- Set IPUMS_API_KEY environment variable or update the script
"""

import os
import pandas as pd
import time
from ipumspy import IpumsApiClient, AggregateDataExtract, NhgisDataset

# IPUMS API key - set as environment variable or replace with your key
API_KEY = os.getenv('IPUMS_API_KEY', 'YOUR_API_KEY_HERE')

# State FIPS code mapping
STATE_FIPS_TO_NAME = {
    '01': 'Alabama', '02': 'Alaska', '04': 'Arizona', '05': 'Arkansas',
    '06': 'California', '08': 'Colorado', '09': 'Connecticut', '10': 'Delaware',
    '11': 'District of Columbia', '12': 'Florida', '13': 'Georgia', '15': 'Hawaii',
    '16': 'Idaho', '17': 'Illinois', '18': 'Indiana', '19': 'Iowa',
    '20': 'Kansas', '21': 'Kentucky', '22': 'Louisiana', '23': 'Maine',
    '24': 'Maryland', '25': 'Massachusetts', '26': 'Michigan', '27': 'Minnesota',
    '28': 'Mississippi', '29': 'Missouri', '30': 'Montana', '31': 'Nebraska',
    '32': 'Nevada', '33': 'New Hampshire', '34': 'New Jersey', '35': 'New Mexico',
    '36': 'New York', '37': 'North Carolina', '38': 'North Dakota', '39': 'Ohio',
    '40': 'Oklahoma', '41': 'Oregon', '42': 'Pennsylvania', '44': 'Rhode Island',
    '45': 'South Carolina', '46': 'South Dakota', '47': 'Tennessee', '48': 'Texas',
    '49': 'Utah', '50': 'Vermont', '51': 'Virginia', '53': 'Washington',
    '54': 'West Virginia', '55': 'Wisconsin', '56': 'Wyoming', '72': 'Puerto Rico'
}

def download_nhgis_data():
    """Download and process NHGIS data for historical Puerto Rican population."""
    
    if API_KEY == 'YOUR_API_KEY_HERE':
        print("ERROR: Please set IPUMS_API_KEY environment variable or update the script")
        print("Get your API key from: https://account.ipums.org/api_keys")
        return
    
    # Initialize IPUMS API client
    ipums = IpumsApiClient(API_KEY)
    
    # Define output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'nhgis_historical')
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*60)
    print("NHGIS Data Download")
    print("="*60)
    print("\nNote: 1960 Census did not include Hispanic origin question.")
    print("This script will attempt to download 1970 and 1980 data.")
    print("\nFor 1960, use the IPUMS microdata script instead.")
    
    # Try to explore metadata first to find the right tables
    try:
        print("\nExploring NHGIS metadata to find Puerto Rican population tables...")
        print("(This may take a moment)")
        
        # Use the metadata API to find datasets
        # Note: The exact API structure may vary - this is a template
        # You may need to manually find table IDs from https://www.nhgis.org/
        
        # For now, we'll provide a structure that you can update with actual table IDs
        # Common NHGIS table patterns for Hispanic origin:
        # - 1980: Look for STF1 tables with "Spanish Origin" or "Hispanic"
        # - 1970: Look for sample-based tables with "Spanish Origin"
        
        print("\n" + "="*60)
        print("OPTION 1: Manual Table ID Lookup")
        print("="*60)
        print("\nTo find the correct table IDs:")
        print("1. Visit https://data2.nhgis.org/main/all_tst_details")
        print("2. Search for 'Puerto Rican' or 'Spanish Origin'")
        print("3. Filter by year (1970, 1980) and geography (State)")
        print("4. Note the dataset name and table ID")
        print("5. Update the extract definition below")
        
        print("\n" + "="*60)
        print("OPTION 2: Try Common Table Patterns")
        print("="*60)
        
        # Try to create extracts for known patterns
        # These may need to be adjusted based on actual NHGIS structure
        
        datasets_to_try = []
        
        # 1980 Census - Summary Tape File 1 (100% data)
        # Look for Spanish Origin tables
        try:
            # Example structure - update with actual table IDs from NHGIS
            datasets_to_try.append({
                'name': '1980_STF1',
                'data_tables': ['NP8'],  # Example - update with actual table ID
                'geog_levels': ['state']
            })
        except:
            pass
        
        # 1970 Census - Sample data
        try:
            datasets_to_try.append({
                'name': '1970_Cnt4Pb',  # Count 4Pb - Sample-Based Population
                'data_tables': ['NP8'],  # Example - update with actual table ID
                'geog_levels': ['state']
            })
        except:
            pass
        
        if datasets_to_try:
            print(f"\nAttempting to create extract with {len(datasets_to_try)} datasets...")
            print("Note: You may need to update table IDs if this fails.")
            
            # Convert to NhgisDataset objects
            nhgis_datasets = []
            for ds in datasets_to_try:
                nhgis_datasets.append(
                    NhgisDataset(
                        name=ds['name'],
                        data_tables=ds['data_tables'],
                        geog_levels=ds['geog_levels']
                    )
                )
            
            extract = AggregateDataExtract(
                collection="nhgis",
                description='Puerto Rican population by state 1970-1980',
                datasets=nhgis_datasets
            )
            
            print(f"Submitting extract request...")
            ipums.submit_extract(extract)
            print(f"Extract submitted. Extract ID: {extract.extract_id}")
            
            # Wait for extract
            print("Waiting for extract to be processed...")
            max_wait = 300
            wait_time = 0
            while wait_time < max_wait:
                status = ipums.extract_status(extract)
                print(f"Status: {status}")
                
                if status == 'completed':
                    print("Extract ready!")
                    break
                elif status == 'failed':
                    print("Extract failed. Please check table IDs.")
                    return
                
                time.sleep(10)
                wait_time += 10
            
            if wait_time >= max_wait:
                print("Timeout waiting for extract.")
                print(f"Extract ID: {extract.extract_id}")
                print("Please check status manually at https://account.ipums.org/extracts")
                return
            
            # Download extract
            print(f"Downloading extract...")
            download_path = os.path.join(output_dir, 'nhgis_extract')
            os.makedirs(download_path, exist_ok=True)
            ipums.download_extract(extract, path=download_path)
            print(f"Downloaded to {download_path}")
            
            # Process downloaded files
            process_nhgis_download(download_path, output_dir)
        else:
            print("\n" + "="*60)
            print("MANUAL DOWNLOAD INSTRUCTIONS")
            print("="*60)
            print("\nSince automatic table ID lookup is not available, please:")
            print("1. Visit https://www.nhgis.org/")
            print("2. Create an account and log in")
            print("3. Go to 'Data' -> 'Extract Data'")
            print("4. Select:")
            print("   - Geographic Level: State")
            print("   - Years: 1970, 1980")
            print("   - Dataset: Decennial Census")
            print("   - Tables: Look for 'Hispanic Origin' or 'Spanish Origin'")
            print("   - Specifically look for 'Puerto Rican' as a category")
            print("5. Submit extract and download")
            print("6. Place CSV files in:", output_dir)
            print("7. Run: python scripts/process_nhgis_files.py")
        
    except Exception as e:
        print(f"Error during extraction: {e}")
        print("\nFalling back to manual download instructions...")
        print("\nPlease download data manually from https://www.nhgis.org/")
        print(f"and place files in: {output_dir}")
        import traceback
        traceback.print_exc()

def process_nhgis_download(download_path, output_dir):
    """Process downloaded NHGIS files."""
    import glob
    
    csv_files = glob.glob(os.path.join(download_path, '*.csv'))
    
    if not csv_files:
        print(f"No CSV files found in {download_path}")
        return
    
    for csv_file in csv_files:
        # Try to determine year from filename or content
        year = None
        if '1970' in csv_file:
            year = 1970
        elif '1980' in csv_file:
            year = 1980
        
        if year:
            process_nhgis_csv(csv_file, year, output_dir)
        else:
            print(f"Could not determine year for {csv_file}, processing anyway...")
            process_nhgis_csv(csv_file, None, output_dir)

def process_nhgis_csv(csv_file, year, output_dir):
    """Process a downloaded NHGIS CSV file and format it."""
    
    try:
        # Read the CSV
        df = pd.read_csv(csv_file)
        
        print(f"\nProcessing {csv_file}")
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()[:10]}...")  # Show first 10 columns
        
        # Find Puerto Rican column
        pr_column = None
        for col in df.columns:
            col_lower = col.lower()
            if 'puerto' in col_lower and 'rican' in col_lower:
                pr_column = col
                break
            elif 'puerto' in col_lower:
                pr_column = col
                break
        
        if pr_column is None:
            # Try looking for Spanish origin columns that might contain PR
            for col in df.columns:
                if 'spanish' in col.lower() or 'hispanic' in col.lower():
                    # Check if this might be a PR-specific column
                    if 'pr' in col.lower() or 'puerto' in col.lower():
                        pr_column = col
                        break
        
        if pr_column is None:
            print("\nWarning: Could not find Puerto Rican column automatically.")
            print("Available columns:", df.columns.tolist())
            print("\nPlease manually identify the Puerto Rican column and update the script.")
            return
        
        print(f"Found Puerto Rican column: {pr_column}")
        
        # Find state name/code column
        state_col = None
        state_name_col = None
        
        # Try common NHGIS column names
        for col in df.columns:
            col_lower = col.lower()
            if col_lower == 'state' or col_lower == 'statename' or 'state_name' in col_lower:
                state_name_col = col
            elif 'gisjoin' in col_lower or 'geoid' in col_lower:
                state_col = col
            elif 'name' in col_lower and 'state' in col_lower:
                state_name_col = col
        
        # If we found state name, use it; otherwise try to extract from GISJOIN
        if state_name_col:
            result = df[[state_name_col, pr_column]].copy()
            result.columns = ['NAME', 'B03001_005E']
        elif state_col:
            # Extract state name from GISJOIN or use FIPS code
            result = df[[state_col, pr_column]].copy()
            result.columns = ['state_code', 'B03001_005E']
            # Try to map state codes to names
            result['NAME'] = result['state_code'].astype(str)
        else:
            # Use first column as identifier
            first_col = df.columns[0]
            result = df[[first_col, pr_column]].copy()
            result.columns = ['identifier', 'B03001_005E']
            result['NAME'] = result['identifier'].astype(str)
        
        # Map state names to FIPS codes
        # Create reverse mapping
        NAME_TO_FIPS = {v: k for k, v in STATE_FIPS_TO_NAME.items()}
        result['state'] = result['NAME'].map(NAME_TO_FIPS)
        
        # If mapping failed, try to extract from state name variations
        if result['state'].isna().any():
            # Try fuzzy matching or manual mapping
            for idx, row in result.iterrows():
                if pd.isna(row['state']):
                    name = str(row['NAME']).strip()
                    # Try direct match
                    for state_name, fips in NAME_TO_FIPS.items():
                        if name.lower() == state_name.lower():
                            result.at[idx, 'state'] = fips
                            result.at[idx, 'NAME'] = state_name
                            break
        
        # Add year if provided
        if year:
            result['year'] = year
        else:
            # Try to infer from filename or data
            result['year'] = None
        
        # Ensure numeric population
        result['B03001_005E'] = pd.to_numeric(result['B03001_005E'], errors='coerce').fillna(0).astype(int)
        
        # Reorder columns to match existing format
        if 'year' in result.columns:
            result = result[['NAME', 'B03001_005E', 'state', 'year']]
        else:
            result = result[['NAME', 'B03001_005E', 'state']]
        
        # Remove rows with missing state codes (likely headers or invalid data)
        result = result[result['state'].notna()].copy()
        
        # Sort by population descending
        result = result.sort_values('B03001_005E', ascending=False)
        
        # Determine output filename
        if year:
            output_file = os.path.join(output_dir, f'nhgis_puerto_rican_pop_{year}.csv')
        else:
            output_file = os.path.join(output_dir, f'nhgis_puerto_rican_pop_processed.csv')
        
        result.to_csv(output_file, index=False)
        print(f"Saved to {output_file}")
        print(f"Total states: {len(result)}")
        print(f"Total population: {result['B03001_005E'].sum():,}")
        
    except Exception as e:
        print(f"Error processing CSV: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    download_nhgis_data()



