import requests
import os
import pandas as pd
import time

def download_poverty_data():
    """
    Download poverty status data for Puerto Rican population by state.
    
    Uses table B17001: Poverty Status in the Past 12 Months by Sex by Age
    We'll get the total below poverty (B17001_002E) and total population (B17001_001E)
    to calculate poverty rates.
    
    Note: For Puerto Rican-specific data, we'll need to use detailed tables
    with Hispanic origin filters. This script gets overall state data which
    can be compared with Puerto Rican population data.
    """
    # Define the base output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'census_acs5_poverty')
    os.makedirs(output_dir, exist_ok=True)
    
    # Variables for poverty status
    # B17001_001E: Total (for population in poverty status universe)
    # B17001_002E: Income in the past 12 months below poverty level
    # We can calculate poverty rate = B17001_002E / B17001_001E
    variables = "B17001_001E,B17001_002E"
    
    # Range of years
    years = range(2010, 2024)  # 2010 to 2023
    
    for year in years:
        print(f"Fetching poverty data for {year}...")
        
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
            df['B17001_001E'] = pd.to_numeric(df['B17001_001E'], errors='coerce')
            df['B17001_002E'] = pd.to_numeric(df['B17001_002E'], errors='coerce')
            
            # Calculate poverty rate
            df['poverty_rate'] = (df['B17001_002E'] / df['B17001_001E'] * 100).round(2)
            
            # Rename for clarity
            df = df.rename(columns={
                'B17001_001E': 'total_population',
                'B17001_002E': 'below_poverty_level'
            })
            
            # Save to CSV
            output_file = os.path.join(output_dir, f"acs5_poverty_{year}.csv")
            df.to_csv(output_file, index=False)
            print(f"Saved {output_file}")
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error for {year}: {e}")
        except Exception as e:
            print(f"Error for {year}: {e}")
        
        # Be nice to the API
        time.sleep(1)

if __name__ == "__main__":
    download_poverty_data()
