"""
Download health insurance coverage data from Census API.

Downloads health insurance coverage statistics by state.
Uses table B27001I for Hispanic/Latino populations (comparison baseline).
For Puerto Rican-specific data, use IPUMS microdata.

Requirements:
- None (public Census API)
"""

import requests
import os
import pandas as pd
import time

def download_health_insurance_data():
    """
    Download health insurance coverage data by state from ACS 5-year estimates.
    
    Uses table B27001I: Health Insurance Coverage Status by Age (Hispanic or Latino)
    This provides comparison baseline for all Hispanic/Latino populations.
    For Puerto Rican-specific data, use IPUMS microdata.
    """
    # Define output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'census_acs5_health_insurance')
    os.makedirs(output_dir, exist_ok=True)
    
    # Variables for health insurance coverage
    # B27001I_001E: Total population
    # B27001I_003E: With health insurance coverage
    # B27001I_009E: Without health insurance coverage
    # Additional age breakdowns available if needed
    variables = "B27001I_001E,B27001I_003E,B27001I_009E"
    
    # Range of years
    years = range(2010, 2024)  # 2010 to 2023
    
    for year in years:
        output_file = os.path.join(output_dir, f"acs5_health_insurance_{year}.csv")
        
        if os.path.exists(output_file):
            print(f"Data for {year} already exists. Skipping.")
            continue
        
        print(f"Fetching health insurance data for {year}...")
        
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
            df['B27001I_001E'] = pd.to_numeric(df['B27001I_001E'], errors='coerce')
            df['B27001I_003E'] = pd.to_numeric(df['B27001I_003E'], errors='coerce')
            df['B27001I_009E'] = pd.to_numeric(df['B27001I_009E'], errors='coerce')
            
            # Calculate rates
            df['insurance_coverage_rate'] = (df['B27001I_003E'] / df['B27001I_001E'] * 100).round(2)
            df['uninsured_rate'] = (df['B27001I_009E'] / df['B27001I_001E'] * 100).round(2)
            
            # Rename for clarity
            df = df.rename(columns={
                'B27001I_001E': 'total_population',
                'B27001I_003E': 'with_insurance',
                'B27001I_009E': 'without_insurance'
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
    download_health_insurance_data()
