import requests
import os
import pandas as pd
import time

def download_housing_data():
    """
    Download housing cost data (median gross rent and median home value) 
    for Puerto Rican population by state from ACS 5-year estimates.
    
    Variables:
    - B25064_001E: Median Gross Rent (for renter-occupied units)
    - B25077_001E: Median Value (Dollars) (for owner-occupied units)
    
    Note: These are overall medians. For Puerto Rican-specific data,
    we'll need to use detailed tables with Hispanic origin filters.
    """
    # Define the base output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'census_acs5_housing')
    os.makedirs(output_dir, exist_ok=True)
    
    # Variables for housing costs
    # B25064_001E: Median Gross Rent
    # B25077_001E: Median Value (Dollars) for Owner-Occupied Housing Units
    variables = "B25064_001E,B25077_001E"
    
    # Range of years
    years = range(2010, 2024)  # 2010 to 2023
    
    for year in years:
        print(f"Fetching housing data for {year}...")
        
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
            df['B25064_001E'] = pd.to_numeric(df['B25064_001E'], errors='coerce')
            df['B25077_001E'] = pd.to_numeric(df['B25077_001E'], errors='coerce')
            
            # Rename for clarity
            df = df.rename(columns={
                'B25064_001E': 'median_gross_rent',
                'B25077_001E': 'median_home_value'
            })
            
            # Save to CSV
            output_file = os.path.join(output_dir, f"acs5_housing_{year}.csv")
            df.to_csv(output_file, index=False)
            print(f"Saved {output_file}")
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error for {year}: {e}")
        except Exception as e:
            print(f"Error for {year}: {e}")
        
        # Be nice to the API
        time.sleep(1)

if __name__ == "__main__":
    download_housing_data()

