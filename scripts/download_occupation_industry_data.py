import requests
import os
import pandas as pd
import time

def download_occupation_industry_data():
    """
    Download occupation and industry data for Puerto Rican population.
    
    Uses detailed tables:
    - B24010: Sex by Occupation for the Civilian Employed Population 16 Years and Over
    - B24030: Sex by Industry for the Civilian Employed Population 16 Years and Over
    
    Note: These tables provide overall state data. For Puerto Rican-specific
    occupation/industry data, we'll need to use IPUMS microdata or detailed
    tables with Hispanic origin cross-tabs (which may not be available via API).
    
    This script downloads the overall state data which can be used for comparison.
    """
    # Define the base output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'census_acs5_occupation_industry')
    os.makedirs(output_dir, exist_ok=True)
    
    # Range of years
    years = range(2010, 2024)  # 2010 to 2023
    
    for year in years:
        print(f"Fetching occupation and industry data for {year}...")
        
        # For occupation, we'll get the main categories from B24010
        # B24010_001E: Total (civilian employed population 16+)
        # We'll get a few key occupation categories
        # Note: Full occupation breakdown requires many variables
        
        # For industry, we'll get the main categories from B24030
        # B24030_001E: Total (civilian employed population 16+)
        
        # Let's get summary data first - we can expand later
        occupation_vars = "B24010_001E"  # Total employed
        industry_vars = "B24030_001E"     # Total employed
        
        # Construct URLs
        occ_url = f"https://api.census.gov/data/{year}/acs/acs5?get=NAME,{occupation_vars}&for=state:*"
        ind_url = f"https://api.census.gov/data/{year}/acs/acs5?get=NAME,{industry_vars}&for=state:*"
        
        try:
            # Get occupation data
            occ_response = requests.get(occ_url)
            occ_response.raise_for_status()
            occ_data = occ_response.json()
            
            # Get industry data
            ind_response = requests.get(ind_url)
            ind_response.raise_for_status()
            ind_data = ind_response.json()
            
            # Process occupation data
            occ_headers = occ_data[0]
            occ_rows = occ_data[1:]
            occ_df = pd.DataFrame(occ_rows, columns=occ_headers)
            occ_df['year'] = year
            occ_df['B24010_001E'] = pd.to_numeric(occ_df['B24010_001E'], errors='coerce')
            occ_df = occ_df.rename(columns={'B24010_001E': 'total_employed'})
            
            # Process industry data
            ind_headers = ind_data[0]
            ind_rows = ind_data[1:]
            ind_df = pd.DataFrame(ind_rows, columns=ind_headers)
            ind_df['year'] = year
            ind_df['B24030_001E'] = pd.to_numeric(ind_df['B24030_001E'], errors='coerce')
            ind_df = ind_df.rename(columns={'B24030_001E': 'total_employed'})
            
            # Save to CSV
            occ_output = os.path.join(output_dir, f"acs5_occupation_{year}.csv")
            ind_output = os.path.join(output_dir, f"acs5_industry_{year}.csv")
            
            occ_df.to_csv(occ_output, index=False)
            ind_df.to_csv(ind_output, index=False)
            
            print(f"Saved {occ_output}")
            print(f"Saved {ind_output}")
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error for {year}: {e}")
        except Exception as e:
            print(f"Error for {year}: {e}")
        
        # Be nice to the API
        time.sleep(1)

if __name__ == "__main__":
    download_occupation_industry_data()
