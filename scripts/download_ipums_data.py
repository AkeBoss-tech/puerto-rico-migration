"""
Download historical Puerto Rican population data from IPUMS USA.

This script uses the IPUMS API to extract microdata for 1960, 1970, and 1980,
then aggregates by state to get Puerto Rican population counts.

Requirements:
- pip install ipumspy
- IPUMS API key (get from https://account.ipums.org/api_keys)
- Set IPUMS_API_KEY environment variable or update the script
"""

import os
import pandas as pd
import time
from ipumspy import IpumsApiClient, MicrodataExtract

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

# Puerto Rico birthplace code in IPUMS
# Note: BPL code 11000 = Puerto Rico (not 25000 which is Cuba)
PUERTO_RICO_BPL = 11000

def download_ipums_data():
    """Download and process IPUMS data for historical Puerto Rican population."""
    
    if API_KEY == 'YOUR_API_KEY_HERE':
        print("ERROR: Please set IPUMS_API_KEY environment variable or update the script")
        print("Get your API key from: https://account.ipums.org/api_keys")
        return
    
    # Initialize IPUMS API client
    ipums = IpumsApiClient(API_KEY)
    
    # Define output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'ipums_historical')
    os.makedirs(output_dir, exist_ok=True)
    
    # Define samples and years
    # Using larger samples for better accuracy
    samples_config = {
        1960: {
            'samples': ['us1960b'],  # 5% sample
            'year': 1960
        },
        1970: {
            'samples': ['us1970a'],  # Form 1 State sample
            'year': 1970
        },
        1980: {
            'samples': ['us1980a'],  # 5% sample
            'year': 1980
        }
    }
    
    for year, config in samples_config.items():
        print(f"\n{'='*60}")
        print(f"Processing {year} Census Data")
        print(f"{'='*60}")
        
        # Create extract definition
        # Variables needed:
        # - BPLD: Birthplace Detailed (to identify Puerto Rican born - code 11000)
        # - STATEFIP: State FIPS code (for state-level aggregation)
        # - PERWT: Person weight (to get accurate population counts)
        extract = MicrodataExtract(
            collection="usa",
            samples=config['samples'],
            variables=['BPLD', 'STATEFIP', 'PERWT'],
            description=f'Puerto Rican population by state for {year}'
        )
        
        try:
            # Submit extract
            print(f"Submitting extract request for {year}...")
            ipums.submit_extract(extract)
            print(f"Extract submitted. Extract ID: {extract.extract_id}")
            
            # Wait for extract to be ready
            print("Waiting for extract to be processed...")
            max_wait = 300  # 5 minutes max wait
            wait_time = 0
            while wait_time < max_wait:
                status = ipums.extract_status(extract)
                print(f"Status: {status}")
                
                if status == 'completed':
                    print("Extract ready!")
                    break
                elif status == 'failed':
                    print("Extract failed!")
                    return
                
                time.sleep(10)
                wait_time += 10
            
            if wait_time >= max_wait:
                print("Timeout waiting for extract. Please check status manually.")
                print(f"Extract ID: {extract.extract_id}")
                continue
            
            # Download extract
            print(f"Downloading extract for {year}...")
            download_path = os.path.join(output_dir, f'ipums_{year}')
            os.makedirs(download_path, exist_ok=True)
            ipums.download_extract(extract, download_dir=download_path)
            print(f"Downloaded to {download_path}")
            
            # Process the data
            print(f"Processing data for {year}...")
            process_ipums_data(download_path, year, output_dir)
            
        except Exception as e:
            print(f"Error processing {year}: {e}")
            import traceback
            traceback.print_exc()
            continue

def process_ipums_data(download_path, year, output_dir):
    """Process downloaded IPUMS microdata and aggregate by state."""
    
    # Find the data file (usually ends with .dat.gz)
    import glob
    data_files = glob.glob(os.path.join(download_path, '*.dat.gz'))
    if not data_files:
        data_files = glob.glob(os.path.join(download_path, '*.dat'))
    
    if not data_files:
        print(f"Warning: No data file found in {download_path}")
        return
    
    data_file = data_files[0]
    
    # Find the DDI file for metadata
    ddi_files = glob.glob(os.path.join(download_path, '*.xml'))
    if not ddi_files:
        print(f"Warning: No DDI file found in {download_path}")
        return
    
    ddi_file = ddi_files[0]
    
    # Read the data using ipumspy's reader
    try:
        from ipumspy import readers
        # First read the DDI file
        ddi = readers.read_ipums_ddi(ddi_file)
        # Then read the microdata
        microdata = readers.read_microdata(ddi, data_file)
        
        # Filter for Puerto Rican born (BPLD == 11000)
        # Note: BPLD (Birthplace Detailed) code 11000 = Puerto Rico
        pr_born = microdata[microdata['BPLD'] == PUERTO_RICO_BPL].copy()
        
        if len(pr_born) == 0:
            print(f"Warning: No Puerto Rican born individuals found in {year} data")
            return
        
        # Aggregate by state using person weights
        # PERWT is the person weight - multiply by weight to get population estimate
        pr_born['weighted_count'] = pr_born['PERWT']
        
        state_counts = pr_born.groupby('STATEFIP')['weighted_count'].sum().reset_index()
        state_counts.columns = ['state', 'B03001_005E']  # Match existing column name
        
        # Convert state FIPS to string with zero padding
        state_counts['state'] = state_counts['state'].astype(str).str.zfill(2)
        
        # Map state FIPS to state names
        state_counts['NAME'] = state_counts['state'].map(STATE_FIPS_TO_NAME)
        
        # Add year
        state_counts['year'] = year
        
        # Reorder columns to match existing format
        state_counts = state_counts[['NAME', 'B03001_005E', 'state', 'year']]
        
        # Round population counts (weights are decimals)
        state_counts['B03001_005E'] = state_counts['B03001_005E'].round().astype(int)
        
        # Sort by population descending
        state_counts = state_counts.sort_values('B03001_005E', ascending=False)
        
        # Save to CSV
        output_file = os.path.join(output_dir, f'ipums_puerto_rican_pop_{year}.csv')
        state_counts.to_csv(output_file, index=False)
        print(f"Saved aggregated data to {output_file}")
        print(f"Total states with Puerto Rican population: {len(state_counts)}")
        print(f"Total Puerto Rican population (weighted): {state_counts['B03001_005E'].sum():,.0f}")
        
    except Exception as e:
        print(f"Error processing microdata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    download_ipums_data()



