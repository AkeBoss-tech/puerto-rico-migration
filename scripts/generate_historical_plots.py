"""
Generate interactive plots for historical Puerto Rican population data (1960, 1970, 1980).
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import glob

# Ensure output directory exists
output_dir = 'docs'
os.makedirs(output_dir, exist_ok=True)

# Load historical IPUMS data
historical_files = glob.glob('data/ipums_historical/ipums_puerto_rican_pop_*.csv')
historical_data = []

for file in sorted(historical_files):
    df = pd.read_csv(file)
    historical_data.append(df)

if not historical_data:
    print("No historical data files found!")
    exit(1)

# Combine all historical data
historical_df = pd.concat(historical_data, ignore_index=True)

# Also load modern ACS data for comparison
acs_files = glob.glob('data/census_acs5/acs5_puerto_rican_pop_*.csv')
acs_data = []
for file in sorted(acs_files):
    df = pd.read_csv(file)
    acs_data.append(df)

if acs_data:
    acs_df = pd.concat(acs_data, ignore_index=True)
    # Combine historical and modern data
    all_data = pd.concat([historical_df, acs_df], ignore_index=True)
else:
    all_data = historical_df

# Convert year to numeric
all_data['year'] = pd.to_numeric(all_data['year'])
all_data['B03001_005E'] = pd.to_numeric(all_data['B03001_005E'])

# Filter out Puerto Rico itself for mainland analysis
all_data = all_data[all_data['state'] != '72'].copy()

# --- Graph 1: Historical Population Trend by Top States ---
top_states_historical = historical_df.groupby('NAME')['B03001_005E'].sum().nlargest(10).index.tolist()
historical_top = historical_df[historical_df['NAME'].isin(top_states_historical)].copy()

fig1 = px.line(historical_top, x='year', y='B03001_005E', color='NAME', 
               markers=True, line_shape='linear',
               title='Historical Puerto Rican Population by Top States (1960-1980)',
               labels={'B03001_005E': 'Population', 'year': 'Year', 'NAME': 'State'})
fig1.update_layout(template='plotly_white', hovermode='x unified')
fig1.write_html(f"{output_dir}/graph11_historical_top_states.html", include_plotlyjs='cdn', full_html=False)

# --- Graph 2: Full Timeline (1960-2023) for Top States ---
if acs_data:
    top_states_all = all_data.groupby('NAME')['B03001_005E'].sum().nlargest(8).index.tolist()
    all_top = all_data[all_data['NAME'].isin(top_states_all)].copy()
    
    fig2 = px.line(all_top, x='year', y='B03001_005E', color='NAME',
                   markers=True, line_shape='linear',
                   title='Puerto Rican Population Trend: Historical to Modern (1960-2023)',
                   labels={'B03001_005E': 'Population', 'year': 'Year', 'NAME': 'State'})
    fig2.update_layout(template='plotly_white', hovermode='x unified')
    fig2.write_html(f"{output_dir}/graph12_full_timeline.html", include_plotlyjs='cdn', full_html=False)

# --- Graph 3: Historical State Rankings (Stacked Bar Chart) ---
# Create a comparison of top states across the three historical years
years_to_show = [1960, 1970, 1980]
comparison_data = []

# Get top 10 states by total population across all years
top_states = historical_df.groupby('NAME')['B03001_005E'].sum().nlargest(10).index.tolist()

for year in years_to_show:
    year_data = historical_df[historical_df['year'] == year]
    for state in top_states:
        state_data = year_data[year_data['NAME'] == state]
        if not state_data.empty:
            comparison_data.append({
                'Year': year,
                'State': state,
                'Population': state_data['B03001_005E'].values[0]
            })

comparison_df = pd.DataFrame(comparison_data)

# Sort states by total population (descending) for better visualization
state_totals = comparison_df.groupby('State')['Population'].sum().sort_values(ascending=False)
comparison_df['State'] = pd.Categorical(comparison_df['State'], categories=state_totals.index, ordered=True)
comparison_df = comparison_df.sort_values('State')

fig3 = px.bar(comparison_df, x='State', y='Population', color='Year',
              barmode='stack',  # Changed to 'stack' for stacked bars
              title='Top 10 States: Historical Comparison (1960, 1970, 1980)',
              labels={'Population': 'Puerto Rican Population', 'State': 'State'},
              color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c'])  # Blue, Orange, Green
fig3.update_layout(template='plotly_white', xaxis_tickangle=-45)
fig3.write_html(f"{output_dir}/graph13_historical_comparison.html", include_plotlyjs='cdn', full_html=False)

# --- Graph 4: New York's Dominance Over Time ---
ny_data = all_data[all_data['NAME'] == 'New York'].copy()
total_by_year = all_data.groupby('year')['B03001_005E'].sum().reset_index()
total_by_year.columns = ['year', 'Total']
ny_data = ny_data.merge(total_by_year, on='year')
ny_data['Percentage'] = (ny_data['B03001_005E'] / ny_data['Total']) * 100

fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=ny_data['year'], y=ny_data['B03001_005E'], 
                         mode='lines+markers', name='New York Population',
                         line=dict(color='#e74c3c', width=3)))
fig4.add_trace(go.Scatter(x=ny_data['year'], y=ny_data['Percentage'], 
                         mode='lines+markers', name='% of Total US PR Population',
                         yaxis='y2', line=dict(color='#3498db', width=3, dash='dash')))

fig4.update_layout(
    title='New York State: Population & Share of Total (1960-2023)',
    xaxis_title='Year',
    yaxis_title='Population',
    yaxis2=dict(title='Percentage (%)', overlaying='y', side='right'),
    template='plotly_white',
    hovermode='x unified'
)
fig4.write_html(f"{output_dir}/graph14_ny_dominance.html", include_plotlyjs='cdn', full_html=False)

# --- Graph 5: Historical Map (1980) ---
# Create a choropleth map for 1980
map_data_1980 = historical_df[historical_df['year'] == 1980].copy()

fig5 = px.choropleth(
    map_data_1980,
    locations='state',
    locationmode='USA-states',
    color='B03001_005E',
    hover_name='NAME',
    hover_data={'B03001_005E': ':,.0f'},
    color_continuous_scale='Blues',
    scope='usa',
    title='Puerto Rican Population by State (1980)',
    labels={'B03001_005E': 'Population'}
)
fig5.update_layout(template='plotly_white')
fig5.write_html(f"{output_dir}/graph15_historical_map_1980.html", include_plotlyjs='cdn', full_html=False)

# --- Graph 6: State Share Evolution (Stacked Area) ---
# Show how the top states' share of total population changed
top_5_states = historical_df.groupby('NAME')['B03001_005E'].sum().nlargest(5).index.tolist()
share_data = []

for year in sorted(historical_df['year'].unique()):
    year_data = historical_df[historical_df['year'] == year]
    total = year_data['B03001_005E'].sum()
    
    for state in top_5_states:
        state_pop = year_data[year_data['NAME'] == state]['B03001_005E'].values
        if len(state_pop) > 0:
            share = (state_pop[0] / total) * 100
            share_data.append({
                'Year': year,
                'State': state,
                'Share': share
            })

share_df = pd.DataFrame(share_data)

fig6 = px.area(share_df, x='Year', y='Share', color='State',
               title='Top 5 States: Share of Total Puerto Rican Population (1960-1980)',
               labels={'Share': 'Percentage (%)', 'Year': 'Year'},
               color_discrete_sequence=px.colors.qualitative.Set3)
fig6.update_layout(template='plotly_white', hovermode='x unified')
fig6.write_html(f"{output_dir}/graph16_state_share_evolution.html", include_plotlyjs='cdn', full_html=False)

print("Historical plots generated:")
print("  - graph11_historical_top_states.html")
print("  - graph12_full_timeline.html")
print("  - graph13_historical_comparison.html")
print("  - graph14_ny_dominance.html")
print("  - graph15_historical_map_1980.html")
print("  - graph16_state_share_evolution.html")

