import requests
import os
import pandas as pd
import time

def download_census_data():
    # Define the base output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'census_acs5')
    os.makedirs(output_dir, exist_ok=True)
    
    # Variable B03001_005E: Hispanic or Latino Origin by Specific Origin: Puerto Rican
    # We also get B03001_001E (Total) to potentially calculate percentages if needed later, 
    # but user specifically requested B03001_005E.
    # Let's stick to the user's request but also add Total Population (B01003_001E) or Total Hispanic (B03001_001E) might be useful context?
    # The user strictly asked for "this" pointing to the URL with just B03001_005E. 
    # I will stick to the requested variable B03001_005E plus NAME.
    
    variable = "B03001_005E"
    
    # Range of years
    years = range(2010, 2024) # 2010 to 2023
    
    for year in years:
        print(f"Fetching data for {year}...")
        
        # Construct URL
        # Note: In some earlier years, the API endpoint might be slightly different or variable names might change.
        # ACS 5-year data API endpoint pattern.
        url = f"https://api.census.gov/data/{year}/acs/acs5?get=NAME,{variable}&for=state:*"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            # data[0] is headers, data[1:] is rows
            headers = data[0]
            rows = data[1:]
            
            # Create DataFrame
            df = pd.DataFrame(rows, columns=headers)
            
            # Add year column for easier merging later
            df['year'] = year
            
            # Save to CSV
            output_file = os.path.join(output_dir, f"acs5_puerto_rican_pop_{year}.csv")
            df.to_csv(output_file, index=False)
            print(f"Saved {output_file}")
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error for {year}: {e}")
            # Sometimes APIs fail for specific years or have different structures
            if year == 2020:
                print("Note: 2020 data might have different handling or availability issues due to COVID-19, though ACS5 should be fine.")
        except Exception as e:
            print(f"Error for {year}: {e}")
        
        # Be nice to the API
        time.sleep(1)

if __name__ == "__main__":
    download_census_data()






