"""
Create sample Puerto Rico economic data for visualization testing.
This uses approximate historical values. For real data, use download_puerto_rico_economic_data.py
with a valid FRED API key.
"""
import pandas as pd
import os

def create_sample_data():
    """Create sample PR economic data based on known historical values."""
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'puerto_rico_economic')
    os.makedirs(output_dir, exist_ok=True)
    
    # Sample data based on approximate historical values
    # Unemployment rate (approximate, in %)
    unemployment_data = {
        'year': range(2010, 2024),
        'value': [
            16.0, 15.5, 14.8, 14.2, 13.5, 12.8, 12.0, 10.5,  # 2010-2017
            10.0, 8.5, 8.0, 7.5, 6.5, 5.6  # 2018-2023 (post-Maria recovery)
        ]
    }
    
    # GDP in billions (approximate, current US dollars)
    gdp_data = {
        'year': range(2010, 2024),
        'value': [
            101.0, 101.5, 101.8, 102.0, 102.2, 102.0, 101.5, 100.0,  # 2010-2017
            99.5, 100.5, 103.0, 105.5, 108.0, 110.0  # 2018-2023 (recovery)
        ]
    }
    
    # Create DataFrames
    unemployment_df = pd.DataFrame(unemployment_data)
    unemployment_df['date'] = pd.to_datetime(unemployment_df['year'].astype(str) + '-01-01')
    
    gdp_df = pd.DataFrame(gdp_data)
    gdp_df['date'] = pd.to_datetime(gdp_df['year'].astype(str) + '-01-01')
    
    # Save individual files
    unemployment_df.to_csv(os.path.join(output_dir, 'pr_unemployment_rate.csv'), index=False)
    gdp_df.to_csv(os.path.join(output_dir, 'pr_gdp.csv'), index=False)
    
    # Create combined file
    combined = unemployment_df[['year', 'value']].rename(columns={'value': 'unemployment_rate'})
    combined = combined.merge(
        gdp_df[['year', 'value']].rename(columns={'value': 'gdp'}),
        on='year',
        how='outer'
    )
    combined = combined.sort_values('year')
    combined.to_csv(os.path.join(output_dir, 'pr_economic_combined.csv'), index=False)
    
    print(f"Created sample PR economic data in {output_dir}")
    print("Note: This is approximate data. For real data, use download_puerto_rico_economic_data.py with a FRED API key.")

if __name__ == "__main__":
    create_sample_data()
