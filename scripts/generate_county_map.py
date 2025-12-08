import pandas as pd
import plotly.express as px
import os
import glob
import json
from urllib.request import urlopen

def generate_county_map():
    # 1. Load All Data
    input_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'census_acs5_county')
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))
    
    df_list = []
    for f in csv_files:
        df_list.append(pd.read_csv(f))
    
    if not df_list:
        print("No data found.")
        return

    full_df = pd.concat(df_list, ignore_index=True)
    
    # 2. Preprocessing
    # Pad state/county codes
    full_df['state'] = full_df['state'].astype(str).str.zfill(2)
    full_df['county'] = full_df['county'].astype(str).str.zfill(3)
    
    # CONNECTICUT FIX:
    # In 2022, CT switched from 8 counties to 9 planning regions, breaking standard GeoJSON maps.
    # We will replace 2022 and 2023 CT data with 2021 CT data (using old counties) to ensure visualization works.
    
    # Extract 2021 CT data
    ct_2021 = full_df[(full_df['year'] == 2021) & (full_df['state'] == '09')].copy()
    
    # Remove original 2022+ CT data
    full_df = full_df[~((full_df['year'] >= 2022) & (full_df['state'] == '09'))]
    
    # Add back 2021 data labelled as 2022 and 2023 if those years exist in dataset
    years_present = full_df['year'].unique()
    
    if 2022 in years_present and not ct_2021.empty:
        ct_2022_proxy = ct_2021.copy()
        ct_2022_proxy['year'] = 2022
        full_df = pd.concat([full_df, ct_2022_proxy], ignore_index=True)
        
    if 2023 in years_present and not ct_2021.empty:
        ct_2023_proxy = ct_2021.copy()
        ct_2023_proxy['year'] = 2023
        full_df = pd.concat([full_df, ct_2023_proxy], ignore_index=True)

    # Continue processing
    full_df['FIPS'] = full_df['state'] + full_df['county']
    full_df['Population'] = pd.to_numeric(full_df['B03001_005E'], errors='coerce').fillna(0)
    
    # Filter out Puerto Rico (72) for mainland map
    mainland_df = full_df[full_df['state'] != '72'].copy()
    mainland_df = mainland_df.sort_values('year')
    
    # 3. Load GeoJSON
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    # 4. Create Animated Map
    # We use a log scale-like effect by capping the range, otherwise NYC dwarfs everything.
    # Or we can use a custom color scale.
    
    fig = px.choropleth(
        mainland_df,
        geojson=counties,
        locations='FIPS',
        color='Population',
        color_continuous_scale="Reds",
        scope="usa",
        range_color=(0, 10000), # Cap at 10k to see spread in smaller counties. Major cities will just be dark red.
        hover_name='NAME',
        animation_frame='year',
        title='Puerto Rican Population by County (2010-2023)',
        labels={'Population': 'Population'}
    )
    
    fig.update_layout(
        template='plotly_white',
        margin={"r":0,"t":50,"l":0,"b":0}
    )
    
    # 5. Save
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'graph9_county_map.html')
    
    fig.write_html(output_file, include_plotlyjs='cdn', full_html=False)
    print(f"Saved {output_file}")

if __name__ == "__main__":
    generate_county_map()



