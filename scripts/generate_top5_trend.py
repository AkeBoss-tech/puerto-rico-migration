import pandas as pd
import plotly.express as px
import os
import glob

def generate_top5_trend():
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
    full_df = full_df.rename(columns={'B03001_005E': 'Population', 'NAME': 'State', 'year': 'Year'})
    
    # 3. Identify Top 5 States (including Puerto Rico) based on 2023 population
    df_2023 = full_df[full_df['Year'] == 2023]
    top_5_states = df_2023.sort_values('Population', ascending=False).head(5)['State'].tolist()
    
    print(f"Top 5 regions found: {top_5_states}")
    
    # 4. Filter data for these 5 states
    plot_df = full_df[full_df['State'].isin(top_5_states)].copy()
    plot_df = plot_df.sort_values('Year')
    
    # 5. Create Line Plot
    fig = px.line(
        plot_df, 
        x='Year', 
        y='Population', 
        color='State',
        markers=True,
        title='Population Trend: Top 5 Regions (Including Puerto Rico)',
        labels={'Population': 'Population Count', 'State': 'Region'}
    )
    
    fig.update_layout(template='plotly_white')
    
    # 6. Save to HTML
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'graph8_top5_trend.html')
    
    fig.write_html(output_file, include_plotlyjs='cdn', full_html=False)
    print(f"Graph saved to {output_file}")

if __name__ == "__main__":
    generate_top5_trend()
