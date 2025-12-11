import requests
import os
import pandas as pd
import time

def download_county_data():
    # Define the base output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'census_acs5_county')
    os.makedirs(output_dir, exist_ok=True)
    
    # Variable B03001_005E: Hispanic or Latino Origin by Specific Origin: Puerto Rican
    # User provided a link with B03001_004E (Mexican) but the project is about Puerto Rico.
    # We stick to B03001_005E.
    variable = "B03001_005E"
    
    # Range of years
    years = range(2010, 2024) # 2010 to 2023
    
    for year in years:
        # Skip if file already exists to save time? No, let's ensure we have fresh data or just overwrite.
        # Checking existence might be faster.
        output_file = os.path.join(output_dir, f"acs5_puerto_rican_pop_county_{year}.csv")
        if os.path.exists(output_file):
            print(f"Data for {year} already exists. Skipping download.")
            continue

        print(f"Fetching county level data for {year}...")
        
        # Construct URL
        url = f"https://api.census.gov/data/{year}/acs/acs5?get=NAME,{variable}&for=county:*"
        
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
            
            # Save to CSV
            df.to_csv(output_file, index=False)
            print(f"Saved {output_file}")
            
        except Exception as e:
            print(f"Error for {year}: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    download_county_data()





