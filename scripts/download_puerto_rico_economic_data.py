import requests
import os
import pandas as pd
import time

def load_env_file():
    """Load environment variables from .env file if it exists."""
    env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes if present
                    value = value.strip('"').strip("'")
                    os.environ[key.strip()] = value

def download_puerto_rico_economic_data():
    """
    Download Puerto Rico economic data from FRED (Federal Reserve Economic Data) API.
    
    Key indicators:
    - Unemployment rate
    - GDP
    - Labor force participation
    - Other economic indicators
    
    FRED API documentation: https://fred.stlouisfed.org/docs/api/fred/
    Note: You may need a free API key from https://fred.stlouisfed.org/docs/api/api_key.html
    """
    # Load .env file if it exists
    load_env_file()
    
    # Define the base output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'puerto_rico_economic')
    os.makedirs(output_dir, exist_ok=True)
    
    # FRED API key (set as environment variable or get from .env file)
    # You can get a free API key from https://fred.stlouisfed.org/docs/api/api_key.html
    api_key = os.environ.get('FRED_API_KEY', '')
    
    if not api_key:
        print("Warning: FRED_API_KEY environment variable not set.")
        print("You can get a free API key from https://fred.stlouisfed.org/docs/api/api_key.html")
        print("Setting API key to 'demo' for limited access...")
        api_key = 'demo'
    
    # FRED series IDs for Puerto Rico
    # These are the standard series IDs used by FRED
    series_ids = {
        'unemployment_rate': 'PRURN',  # Puerto Rico Unemployment Rate (monthly, not seasonally adjusted)
        'gdp': 'NYGDPMKTPCDPRI',  # Puerto Rico GDP (annual, current US dollars)
        # Note: Some series may require different frequencies or may not be available
        # Check https://fred.stlouisfed.org/ for available series
    }
    
    # Base URL for FRED API
    base_url = "https://api.stlouisfed.org/fred/series/observations"
    
    all_data = {}
    
    for series_name, series_id in series_ids.items():
        print(f"Fetching {series_name} (series ID: {series_id})...")
        
        # Set frequency based on series (unemployment is monthly, GDP is annual)
        frequency = 'a'  # Annual by default
        if series_id == 'PRURN':
            frequency = 'a'  # Convert monthly to annual average
        
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': '2010-01-01',  # Start from 2010 to match other data
            'observation_end': '2024-12-31',
            'frequency': frequency,
            'units': 'lin',  # Levels (not transformed)
            'aggregation_method': 'avg' if frequency == 'a' else None  # Average for annual
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if 'observations' in data:
                # Convert to DataFrame
                observations = data['observations']
                df = pd.DataFrame(observations)
                
                # Convert date and value columns
                df['date'] = pd.to_datetime(df['date'])
                df['year'] = df['date'].dt.year
                df['value'] = pd.to_numeric(df['value'], errors='coerce')
                
                # Remove rows with missing values (marked as '.')
                df = df[df['value'].notna()]
                
                # Save to CSV
                output_file = os.path.join(output_dir, f"pr_{series_name}.csv")
                df.to_csv(output_file, index=False)
                print(f"Saved {output_file} ({len(df)} observations)")
                
                all_data[series_name] = df
            else:
                print(f"Warning: No observations found for {series_name}")
                
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error for {series_name}: {e}")
            if '401' in str(e):
                print("  -> This might be due to API key issues. Check your FRED_API_KEY.")
        except Exception as e:
            print(f"Error for {series_name}: {e}")
        
        # Be nice to the API
        time.sleep(0.5)
    
    # Create a combined dataset with all indicators
    if len(all_data) > 0:
        # Start with the first series
        combined = all_data[list(all_data.keys())[0]][['year']].copy()
        
        # Merge all other series
        for series_name, df in all_data.items():
            if series_name != list(all_data.keys())[0]:
                combined = combined.merge(
                    df[['year', 'value']].rename(columns={'value': series_name}),
                    on='year',
                    how='outer'
                )
            else:
                combined[series_name] = df['value'].values
        
        # Sort by year
        combined = combined.sort_values('year')
        
        # Save combined file
        combined_output = os.path.join(output_dir, "pr_economic_combined.csv")
        combined.to_csv(combined_output, index=False)
        print(f"\nSaved combined economic data: {combined_output}")
    
    print("\nNote: If you need more detailed data or different series,")
    print("visit https://fred.stlouisfed.org/ and search for 'Puerto Rico'")
    print("to find additional economic indicators.")

if __name__ == "__main__":
    download_puerto_rico_economic_data()
