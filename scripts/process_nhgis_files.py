"""
Process manually downloaded NHGIS CSV files.

If you downloaded NHGIS data manually from the website, place the CSV files
in data/nhgis_historical/ and run this script to process them.
"""

import os
import pandas as pd
import glob

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

NAME_TO_FIPS = {v: k for k, v in STATE_FIPS_TO_NAME.items()}

def process_nhgis_files():
    """Process all NHGIS CSV files in the data directory."""
    
    # Import the processing function from download script
    import sys
    sys.path.append(os.path.dirname(__file__))
    from download_nhgis_data import process_nhgis_csv
    
    # Define directories
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_dir = os.path.join(base_dir, 'data', 'nhgis_historical')
    output_dir = os.path.join(base_dir, 'data', 'nhgis_historical')
    
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all CSV files
    csv_files = glob.glob(os.path.join(input_dir, '*.csv'))
    
    # Filter out already processed files
    csv_files = [f for f in csv_files if 'puerto_rican_pop_' not in os.path.basename(f)]
    
    if not csv_files:
        print(f"No unprocessed CSV files found in {input_dir}")
        print("\nTo use this script:")
        print("1. Download NHGIS data from https://www.nhgis.org/")
        print(f"2. Place CSV files in: {input_dir}")
        print("3. Run this script again")
        return
    
    print(f"Found {len(csv_files)} CSV file(s) to process")
    
    for csv_file in csv_files:
        print(f"\n{'='*60}")
        print(f"Processing: {os.path.basename(csv_file)}")
        print(f"{'='*60}")
        
        # Try to determine year from filename
        year = None
        filename = os.path.basename(csv_file).lower()
        if '1970' in filename:
            year = 1970
        elif '1980' in filename:
            year = 1980
        
        if year:
            print(f"Detected year: {year}")
        else:
            print("Could not detect year from filename")
            response = input("Enter year (1970 or 1980) or press Enter to skip: ").strip()
            if response:
                try:
                    year = int(response)
                except:
                    print("Invalid year, skipping...")
                    continue
        
        process_nhgis_csv(csv_file, year, output_dir)

if __name__ == "__main__":
    process_nhgis_files()



