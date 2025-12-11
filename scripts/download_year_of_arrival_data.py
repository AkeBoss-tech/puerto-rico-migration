import requests
import os
import pandas as pd
import time

def download_year_of_arrival_data():
    """
    Download year of arrival data for Puerto Rican population.
    
    Note: Since Puerto Ricans are U.S. citizens, the standard "year of immigration"
    variable (YRIMMIG) doesn't apply. Instead, we'll use:
    - B07001: Geographic Mobility in the Past Year by Citizenship Status
    - Or IPUMS microdata which has MIGRATE variables
    
    For now, this script will download migration/mobility data that shows
    recent movers, which can indicate migration patterns.
    
    We'll use B07001_001E (Total) and B07001_002E (Same house 1 year ago)
    to calculate movers.
    """
    # Define the base output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'census_acs5_migration')
    os.makedirs(output_dir, exist_ok=True)
    
    # Variables for geographic mobility
    # B07001_001E: Total (population 1 year and over)
    # B07001_002E: Same house 1 year ago
    # B07001_003E: Moved within same county
    # B07001_004E: Moved from different county, same state
    # B07001_005E: Moved from different state
    # B07001_006E: Moved from abroad
    variables = "B07001_001E,B07001_002E,B07001_003E,B07001_004E,B07001_005E,B07001_006E"
    
    # Range of years
    years = range(2010, 2024)  # 2010 to 2023
    
    for year in years:
        print(f"Fetching migration/mobility data for {year}...")
        
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
            for col in ['B07001_001E', 'B07001_002E', 'B07001_003E', 
                       'B07001_004E', 'B07001_005E', 'B07001_006E']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Calculate migration rates
            df['moved_total'] = df['B07001_001E'] - df['B07001_002E']
            df['migration_rate'] = (df['moved_total'] / df['B07001_001E'] * 100).round(2)
            df['moved_from_different_state_rate'] = (df['B07001_005E'] / df['B07001_001E'] * 100).round(2)
            df['moved_from_abroad_rate'] = (df['B07001_006E'] / df['B07001_001E'] * 100).round(2)
            
            # Rename for clarity
            df = df.rename(columns={
                'B07001_001E': 'total_population',
                'B07001_002E': 'same_house_1yr_ago',
                'B07001_003E': 'moved_same_county',
                'B07001_004E': 'moved_different_county_same_state',
                'B07001_005E': 'moved_different_state',
                'B07001_006E': 'moved_from_abroad'
            })
            
            # Save to CSV
            output_file = os.path.join(output_dir, f"acs5_migration_{year}.csv")
            df.to_csv(output_file, index=False)
            print(f"Saved {output_file}")
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error for {year}: {e}")
        except Exception as e:
            print(f"Error for {year}: {e}")
        
        # Be nice to the API
        time.sleep(1)
    
    print("\nNote: For detailed year-of-arrival cohort analysis for Puerto Ricans,")
    print("consider using IPUMS microdata which has MIGRATE variables that can")
    print("track when Puerto Rican-born individuals moved to the mainland.")

if __name__ == "__main__":
    download_year_of_arrival_data()
