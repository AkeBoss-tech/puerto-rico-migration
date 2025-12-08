import pandas as pd
import plotly.express as px
import os
import glob

def generate_map():
    # 1. Load all CSV files
    input_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'census_acs5')
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))
    
    df_list = []
    for f in csv_files:
        df_list.append(pd.read_csv(f))
    
    if not df_list:
        print("No data found in data/census_acs5/")
        return

    full_df = pd.concat(df_list, ignore_index=True)
    
    # 2. Data Preprocessing
    # Rename columns for clarity
    full_df = full_df.rename(columns={'B03001_005E': 'Population', 'NAME': 'State', 'year': 'Year'})
    
    # Filter out Puerto Rico for the mainland map (to see the spread in US)
    # or keep it? If we keep it, the color scale will be dominated by PR (~3M) vs states.
    # Given the context is "Migration" (moving TO the US), let's focus on the mainland states.
    # Also Plotly 'USA-states' location mode expects 2-letter codes usually.
    
    # Map State Names to 2-letter codes
    us_state_to_abbrev = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
        "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
        "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
        "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
        "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
        "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
        "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
        "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
        "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
        "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
        "District of Columbia": "DC", "Puerto Rico": "PR"
    }
    
    full_df['StateCode'] = full_df['State'].map(us_state_to_abbrev)
    
    # Filter out rows where StateCode is NaN (if any) and Puerto Rico to focus on mainland distribution
    # creating a separate DF for the map to avoid skewing color scale
    map_df = full_df[full_df['State'] != 'Puerto Rico'].copy()
    map_df = map_df.dropna(subset=['StateCode'])
    
    # Sort by Year to ensure slider works correctly
    map_df = map_df.sort_values('Year')
    
    # 3. Create Choropleth Map
    fig = px.choropleth(
        map_df,
        locations='StateCode',
        locationmode="USA-states",
        color='Population',
        hover_name='State',
        animation_frame='Year',
        scope="usa",
        color_continuous_scale="Reds",
        range_color=(0, map_df['Population'].max()), # Fix the color scale to the max across all years
        title='Puerto Rican Population by State (2010-2023)',
        labels={'Population': 'Population Count'}
    )
    
    fig.update_layout(
        template='plotly_white',
        geo=dict(
            lakecolor='rgb(255, 255, 255)',
        ),
        margin={"r":0,"t":50,"l":0,"b":0}
    )
    
    # 4. Save to HTML
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'graph7_map.html')
    
    fig.write_html(output_file, include_plotlyjs='cdn', full_html=False)
    print(f"Map saved to {output_file}")

if __name__ == "__main__":
    generate_map()



