"""
Download Hispanic/Latino-origin comparison data from Census API.

This script downloads data for ALL Hispanic/Latino populations (not Puerto Rican-specific)
to serve as a comparison baseline. Tables with "I" suffix are for Hispanic/Latino populations.

Variables:
- B17001I: Poverty Status (Hispanic or Latino)
- B25064I: Median Gross Rent (Hispanic or Latino)  
- B25077I: Median Home Value (Hispanic or Latino)
- B27001I: Health Insurance Coverage (Hispanic or Latino)

This provides context for comparing Puerto Rican-specific data when available.
"""

import requests
import os
import pandas as pd
import time

def download_hispanic_comparison_data():
    """Download Hispanic/Latino comparison data from Census API."""
    
    # Define output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'census_acs5_hispanic_comparison')
    os.makedirs(output_dir, exist_ok=True)
    
    # Tables with Hispanic origin breakdowns
    tables = {
        'poverty': {
            'name': 'Poverty Status',
            'variables': 'B17001I_001E,B17001I_002E',  # Total, Below poverty
            'description': 'Poverty Status in the Past 12 Months by Sex by Age (Hispanic or Latino)'
        },
        'housing_rent': {
            'name': 'Median Gross Rent',
            'variables': 'B25064I_001E',  # Median gross rent
            'description': 'Median Gross Rent (Dollars) (Hispanic or Latino)'
        },
        'housing_value': {
            'name': 'Median Home Value',
            'variables': 'B25077I_001E',  # Median home value
            'description': 'Median Value (Dollars) for Owner-Occupied Housing Units (Hispanic or Latino)'
        },
        'health_insurance': {
            'name': 'Health Insurance Coverage',
            'variables': 'B27001I_001E,B27001I_003E,B27001I_009E',  # Total, With coverage, Without coverage
            'description': 'Health Insurance Coverage Status by Age (Hispanic or Latino)'
        }
    }
    
    # Range of years
    years = range(2010, 2024)  # 2010 to 2023
    
    for table_key, table_info in tables.items():
        print(f"\n{'='*60}")
        print(f"Downloading {table_info['name']} data")
        print(f"Table: {table_info['description']}")
        print(f"{'='*60}")
        
        for year in years:
            output_file = os.path.join(output_dir, f"acs5_hispanic_{table_key}_{year}.csv")
            
            if os.path.exists(output_file):
                print(f"Data for {table_key} {year} already exists. Skipping.")
                continue
            
            print(f"Fetching {table_key} data for {year}...")
            
            # Construct URL for state-level data
            url = f"https://api.census.gov/data/{year}/acs/acs5?get=NAME,{table_info['variables']}&for=state:*"
            
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
                
                # Calculate rates/percentages for specific tables
                if table_key == 'poverty':
                    df['poverty_rate'] = (df['B17001I_002E'] / df['B17001I_001E'] * 100).round(2)
                    df = df.rename(columns={
                        'B17001I_001E': 'total_population',
                        'B17001I_002E': 'below_poverty_level'
                    })
                elif table_key == 'health_insurance':
                    df['insurance_coverage_rate'] = (df['B27001I_003E'] / df['B27001I_001E'] * 100).round(2)
                    df['uninsured_rate'] = (df['B27001I_009E'] / df['B27001I_001E'] * 100).round(2)
                    df = df.rename(columns={
                        'B27001I_001E': 'total_population',
                        'B27001I_003E': 'with_insurance',
                        'B27001I_009E': 'without_insurance'
                    })
                elif table_key == 'housing_rent':
                    df = df.rename(columns={'B25064I_001E': 'median_gross_rent'})
                elif table_key == 'housing_value':
                    df = df.rename(columns={'B25077I_001E': 'median_home_value'})
                
                # Save to CSV
                df.to_csv(output_file, index=False)
                print(f"Saved {output_file}")
                
            except requests.exceptions.HTTPError as e:
                print(f"HTTP Error for {year}: {e}")
                # Some tables may not exist for all years
                if e.response.status_code == 404:
                    print(f"  Note: This table may not be available for {year}")
            except Exception as e:
                print(f"Error for {year}: {e}")
            
            # Be nice to the API
            time.sleep(1)
    
    print(f"\n{'='*60}")
    print("Download complete!")
    print(f"Data saved to: {output_dir}")
    print(f"{'='*60}")
    print("\nNote: This data is for ALL Hispanic/Latino populations, not Puerto Rican-specific.")
    print("Use IPUMS microdata (download_ipums_pr_specific_data.py) for Puerto Rican-specific data.")

if __name__ == "__main__":
    download_hispanic_comparison_data()

