"""
Download commuting patterns data from Census API.

Downloads means of transportation to work and commute time statistics by state.
Uses table B08301I for Hispanic/Latino populations (comparison baseline).
For Puerto Rican-specific data, use IPUMS microdata.

Requirements:
- None (public Census API)
"""

import requests
import os
import pandas as pd
import time

def download_commuting_data():
    """
    Download commuting patterns data by state from ACS 5-year estimates.
    
    Uses table B08301I: Means of Transportation to Work (Hispanic or Latino)
    This provides comparison baseline for all Hispanic/Latino populations.
    For Puerto Rican-specific data, use IPUMS microdata.
    """
    # Define output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'census_acs5_commuting')
    os.makedirs(output_dir, exist_ok=True)
    
    # Variables for means of transportation
    # B08301I_001E: Total workers 16 years and over
    # B08301I_003E: Car, truck, or van (drove alone)
    # B08301I_004E: Car, truck, or van (carpooled)
    # B08301I_010E: Public transportation (excluding taxicab)
    # B08301I_016E: Walked
    # B08301I_017E: Other means
    # B08301I_018E: Worked from home
    variables = "B08301I_001E,B08301I_003E,B08301I_004E,B08301I_010E,B08301I_016E,B08301I_017E,B08301I_018E"
    
    # Range of years
    years = range(2010, 2024)  # 2010 to 2023
    
    for year in years:
        output_file = os.path.join(output_dir, f"acs5_commuting_{year}.csv")
        
        if os.path.exists(output_file):
            print(f"Data for {year} already exists. Skipping.")
            continue
        
        print(f"Fetching commuting data for {year}...")
        
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
            df['drove_alone'] = df['B08301I_003E']
            df['carpooled'] = df['B08301I_004E']
            df['public_transit'] = df['B08301I_010E']
            df['walked'] = df['B08301I_016E']
            df['other_means'] = df['B08301I_017E']
            df['worked_from_home'] = df['B08301I_018E']
            
            # Calculate rates
            df['drove_alone_rate'] = (df['drove_alone'] / df['B08301I_001E'] * 100).round(2)
            df['carpooled_rate'] = (df['carpooled'] / df['B08301I_001E'] * 100).round(2)
            df['public_transit_rate'] = (df['public_transit'] / df['B08301I_001E'] * 100).round(2)
            df['walked_rate'] = (df['walked'] / df['B08301I_001E'] * 100).round(2)
            df['worked_from_home_rate'] = (df['worked_from_home'] / df['B08301I_001E'] * 100).round(2)
            
            # Rename for clarity
            df = df.rename(columns={
                'B08301I_001E': 'total_workers_16plus'
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
    download_commuting_data()

