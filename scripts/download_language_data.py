"""
Download language and English proficiency data from Census API.

Downloads language spoken at home and English proficiency statistics by state.
Uses table B16001I for Hispanic/Latino populations (comparison baseline).
For Puerto Rican-specific data, use IPUMS microdata.

Requirements:
- None (public Census API)
"""

import requests
import os
import pandas as pd
import time

def download_language_data():
    """
    Download language and English proficiency data by state from ACS 5-year estimates.
    
    Uses table B16001I: Language Spoken at Home by Ability to Speak English (Hispanic or Latino)
    This provides comparison baseline for all Hispanic/Latino populations.
    For Puerto Rican-specific data, use IPUMS microdata.
    """
    # Define output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'census_acs5_language')
    os.makedirs(output_dir, exist_ok=True)
    
    # Variables for language and English proficiency
    # B16001I_001E: Total population 5 years and over
    # B16001I_002E: Speaks only English
    # B16001I_003E: Speaks Spanish: Speaks English "very well"
    # B16001I_004E: Speaks Spanish: Speaks English "well"
    # B16001I_005E: Speaks Spanish: Speaks English "not well"
    # B16001I_006E: Speaks Spanish: Speaks English "not at all"
    # We'll calculate summary statistics from these
    variables = "B16001I_001E,B16001I_002E,B16001I_003E,B16001I_004E,B16001I_005E,B16001I_006E"
    
    # Range of years
    years = range(2010, 2024)  # 2010 to 2023
    
    for year in years:
        output_file = os.path.join(output_dir, f"acs5_language_{year}.csv")
        
        if os.path.exists(output_file):
            print(f"Data for {year} already exists. Skipping.")
            continue
        
        print(f"Fetching language data for {year}...")
        
        # Construct URL for state-level data
        url = f"https://api.census.gov/data/{year}/acs/acs5?get=NAME,{variables}&for=state:*"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            # data[0] is headers, data[1:] is rows
            headers = data[0]
            rows = data[1:]
            
            # Create DataFrame
            df = pd.DataFrame(rows, columns=headers)
            
            # Add year column
            df['year'] = year
            
            # Convert numeric columns
            for col in headers:
                if col not in ['NAME', 'state']:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Calculate summary statistics
            # Total speaking Spanish (all proficiency levels)
            df['speaks_spanish'] = (df['B16001I_003E'] + df['B16001I_004E'] + 
                                   df['B16001I_005E'] + df['B16001I_006E'])
            
            # Limited English proficiency (speaks English "not well" or "not at all")
            df['limited_english_proficiency'] = df['B16001I_005E'] + df['B16001I_006E']
            
            # Calculate rates
            df['english_only_rate'] = (df['B16001I_002E'] / df['B16001I_001E'] * 100).round(2)
            df['spanish_speaking_rate'] = (df['speaks_spanish'] / df['B16001I_001E'] * 100).round(2)
            df['limited_english_rate'] = (df['limited_english_proficiency'] / df['B16001I_001E'] * 100).round(2)
            
            # Rename for clarity
            df = df.rename(columns={
                'B16001I_001E': 'total_population_5plus',
                'B16001I_002E': 'speaks_english_only',
                'B16001I_003E': 'spanish_english_very_well',
                'B16001I_004E': 'spanish_english_well',
                'B16001I_005E': 'spanish_english_not_well',
                'B16001I_006E': 'spanish_english_not_at_all'
            })
            
            # Save to CSV
            df.to_csv(output_file, index=False)
            print(f"Saved {output_file}")
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error for {year}: {e}")
            if e.response.status_code == 404:
                print(f"  Note: This table may not be available for {year}")
        except Exception as e:
            print(f"Error for {year}: {e}")
        
        # Be nice to the API
        time.sleep(1)
    
    print(f"\nDownload complete! Data saved to: {output_dir}")
    print("Note: This is for ALL Hispanic/Latino populations, not Puerto Rican-specific.")
    print("For Puerto Rican-specific data, use IPUMS microdata (download_ipums_pr_specific_data.py)")

if __name__ == "__main__":
    download_language_data()

