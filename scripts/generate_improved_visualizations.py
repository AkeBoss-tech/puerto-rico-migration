import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy import stats
import os
import glob

# Ensure output directory exists
output_dir = 'docs'
os.makedirs(output_dir, exist_ok=True)

# American/Puerto Rican color theme (Red, White, Blue)
PR_COLORS = {
    'red': '#DC143C',      # Crimson red
    'red_dark': '#B22234', # Dark red
    'red_light': '#E4002B', # Light red
    'blue': '#0051BA',     # American blue
    'blue_dark': '#003087', # Navy blue
    'blue_light': '#0066FF', # Light blue
    'white': '#FFFFFF',
    'gray': '#F5F5F5'
}

# Color sequences for multi-category charts
PR_COLOR_SEQUENCE = ['#DC143C', '#0051BA', '#B22234', '#0066FF', '#E4002B', '#003087', '#FF6B6B', '#4A90E2']

# ============================================================================
# 1. MERGED POPULATION CHART: Total vs Island-Born (Figures 1 & 13)
# ============================================================================
def generate_merged_population_chart():
    """Merge Figure 1 & 13: Total Puerto Rican Population vs Island-Born Population"""
    file_path = 'data/usa_00001.csv'
    df = pd.read_csv(file_path)
    
    # Identify Puerto Rican population (by BPL or other identifier)
    # Assuming BPL == 110 is Puerto Rico born, and we need to identify all Puerto Ricans
    # For this, we'll use the same logic: BPL == 110 for island-born
    df['IS_PR_BORN'] = df['BPL'] == 110
    
    # Calculate total Puerto Rican population (island-born + US-born of PR descent)
    # For now, we'll use island-born as a proxy, but ideally we'd have ancestry data
    # Total PR population = Island-born PR population (from our data)
    pr_data = df[df['IS_PR_BORN']]
    
    # Total PR population (island-born)
    pr_yearly = pr_data.groupby('YEAR')['PERWT'].sum().reset_index()
    pr_yearly.columns = ['YEAR', 'Island_Born_Population']
    
    # For total PR population, we need to estimate US-born Puerto Ricans
    # Since we don't have ancestry data, we'll use a different approach:
    # Use the total sample population as a proxy, or calculate from available data
    # Actually, let's use the census ACS5 data which has total PR population
    census_dir = 'data/census_acs5'
    census_files = glob.glob(os.path.join(census_dir, 'acs5_puerto_rican_pop_*.csv'))
    
    if census_files:
        all_census = []
        for f in sorted(census_files):
            df_census = pd.read_csv(f)
            # Extract year from filename
            year = int(f.split('_')[-1].replace('.csv', ''))
            df_census['YEAR'] = year
            all_census.append(df_census)
        
        census_df = pd.concat(all_census, ignore_index=True)
        # Sum all states for total PR population
        total_pr = census_df.groupby('YEAR')['B03001_005E'].sum().reset_index()
        total_pr.columns = ['YEAR', 'Total_PR_Population']
        
        # Merge with island-born data
        merged = pr_yearly.merge(total_pr, on='YEAR', how='outer')
        merged = merged.sort_values('YEAR')
        
        # Create the merged chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=merged['YEAR'],
            y=merged['Total_PR_Population'],
            mode='lines+markers',
            name='Total Puerto Rican Population',
            line=dict(color=PR_COLORS['blue'], width=3),
            marker=dict(size=8, color=PR_COLORS['blue'])
        ))
        
        fig.add_trace(go.Scatter(
            x=merged['YEAR'],
            y=merged['Island_Born_Population'],
            mode='lines+markers',
            name='Island-Born Population',
            line=dict(color=PR_COLORS['red'], width=3, dash='dash'),
            marker=dict(size=8, color=PR_COLORS['red'])
        ))
        
        # Calculate and add US-born population (difference)
        merged['US_Born_Population'] = merged['Total_PR_Population'] - merged['Island_Born_Population']
        merged['US_Born_Population'] = merged['US_Born_Population'].clip(lower=0)  # Ensure non-negative
        
        fig.add_trace(go.Scatter(
            x=merged['YEAR'],
            y=merged['US_Born_Population'],
            mode='lines+markers',
            name='US-Born Population (Estimated)',
            line=dict(color=PR_COLORS['blue_light'], width=2, dash='dot'),
            marker=dict(size=6, color=PR_COLORS['blue_light']),
            fill='tonexty',
            fillcolor='rgba(0, 81, 186, 0.1)'
        ))
        
        fig.update_layout(
            title={
                'text': 'The "Nuyorican" Shift: Total vs Island-Born Puerto Rican Population',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            xaxis=dict(title='Year'),
            yaxis=dict(title='Population'),
            template='plotly_white',
            plot_bgcolor=PR_COLORS['gray'],
            paper_bgcolor='white',
            hovermode='x unified',
            legend=dict(
                x=0.02,
                y=0.98,
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='rgba(0, 0, 0, 0.2)',
                borderwidth=1
            )
        )
        
        fig.write_html(f"{output_dir}/graph_merged_population.html", include_plotlyjs='cdn', full_html=False)
        print("Generated merged population chart (Total vs Island-Born)")
    else:
        print("Census ACS5 data not found. Skipping merged population chart.")

# ============================================================================
# 2. STATE PERCENT SHARE CHART (Consolidating Figures 3, 5, 14, 17)
# ============================================================================
def generate_state_percent_share_chart():
    """Create a percent share chart showing how each state's share of PR population changed over time"""
    census_dir = 'data/census_acs5'
    census_files = glob.glob(os.path.join(census_dir, 'acs5_puerto_rican_pop_*.csv'))
    
    if not census_files:
        print("Census ACS5 data not found. Skipping state percent share chart.")
        return
    
    all_census = []
    for f in sorted(census_files):
        df = pd.read_csv(f)
        year = int(f.split('_')[-1].replace('.csv', ''))
        df['YEAR'] = year
        all_census.append(df)
    
    census_df = pd.concat(all_census, ignore_index=True)
    census_df = census_df.rename(columns={'B03001_005E': 'Population', 'NAME': 'State'})
    census_df['Population'] = pd.to_numeric(census_df['Population'], errors='coerce')
    
    # Calculate total PR population by year
    total_by_year = census_df.groupby('YEAR')['Population'].sum().reset_index()
    total_by_year.columns = ['YEAR', 'Total_Population']
    
    # Merge to calculate percentages
    census_df = census_df.merge(total_by_year, on='YEAR')
    census_df['Percent_Share'] = (census_df['Population'] / census_df['Total_Population']) * 100
    
    # Get top states (by 2023 population)
    top_states_2023 = census_df[census_df['YEAR'] == 2023].nlargest(8, 'Population')['State'].tolist()
    
    # Filter to top states
    plot_df = census_df[census_df['State'].isin(top_states_2023)].copy()
    plot_df = plot_df.sort_values(['YEAR', 'State'])
    
    # Create line chart
    fig = px.line(
        plot_df,
        x='YEAR',
        y='Percent_Share',
        color='State',
        markers=True,
        title='State Share of Puerto Rican Population Over Time (The Great Dispersion)',
        labels={'Percent_Share': 'Percent Share (%)', 'YEAR': 'Year', 'State': 'State'},
        color_discrete_sequence=PR_COLOR_SEQUENCE
    )
    
    fig.update_layout(
        template='plotly_white',
        plot_bgcolor=PR_COLORS['gray'],
        paper_bgcolor='white',
        hovermode='x unified',
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='rgba(0, 0, 0, 0.2)',
            borderwidth=1
        )
    )
    
    fig.write_html(f"{output_dir}/graph_state_percent_share.html", include_plotlyjs='cdn', full_html=False)
    print("Generated state percent share chart")

# ============================================================================
# 3. POPULATION PYRAMID (Improving Figure 15)
# ============================================================================
def generate_population_pyramid():
    """Convert age distribution to a population pyramid"""
    file_path = 'data/usa_00001.csv'
    df = pd.read_csv(file_path)
    
    df['IS_PR_BORN'] = df['BPL'] == 110
    df['SEX_LABEL'] = df['SEX'].map({1: 'Male', 2: 'Female'})
    
    # Create age groups
    def age_group(age):
        if age < 5: return '0-4'
        if age < 10: return '5-9'
        if age < 15: return '10-14'
        if age < 20: return '15-19'
        if age < 25: return '20-24'
        if age < 30: return '25-29'
        if age < 35: return '30-34'
        if age < 40: return '35-39'
        if age < 45: return '40-44'
        if age < 50: return '45-49'
        if age < 55: return '50-54'
        if age < 60: return '55-59'
        if age < 65: return '60-64'
        if age < 70: return '65-69'
        if age < 75: return '70-74'
        if age < 80: return '75-79'
        return '80+'
    
    df['AGE_GROUP'] = df['AGE'].apply(age_group)
    
    # Use most recent year for the pyramid
    latest_year = df['YEAR'].max()
    df_latest = df[df['YEAR'] == latest_year].copy()
    
    # Calculate population by age group, sex, and PR status
    pyramid_data = df_latest.groupby(['AGE_GROUP', 'SEX_LABEL', 'IS_PR_BORN'])['PERWT'].sum().reset_index()
    
    # Separate PR Born and Total Population
    pr_born = pyramid_data[pyramid_data['IS_PR_BORN'] == True].copy()
    total_pop = pyramid_data.groupby(['AGE_GROUP', 'SEX_LABEL'])['PERWT'].sum().reset_index()
    
    # Create age group order
    age_order = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', 
                 '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']
    
    # Prepare data for pyramid
    pr_male = pr_born[pr_born['SEX_LABEL'] == 'Male'].set_index('AGE_GROUP')['PERWT'].reindex(age_order, fill_value=0)
    pr_female = pr_born[pr_born['SEX_LABEL'] == 'Female'].set_index('AGE_GROUP')['PERWT'].reindex(age_order, fill_value=0)
    total_male = total_pop[total_pop['SEX_LABEL'] == 'Male'].set_index('AGE_GROUP')['PERWT'].reindex(age_order, fill_value=0)
    total_female = total_pop[total_pop['SEX_LABEL'] == 'Female'].set_index('AGE_GROUP')['PERWT'].reindex(age_order, fill_value=0)
    
    # Create figure with subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('PR Born Population', 'Total Population'),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    # PR Born Pyramid
    fig.add_trace(
        go.Bar(y=age_order, x=-pr_male.values, name='Male (PR Born)', 
               orientation='h', marker_color=PR_COLORS['blue'], showlegend=True),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(y=age_order, x=pr_female.values, name='Female (PR Born)', 
               orientation='h', marker_color=PR_COLORS['red'], showlegend=True),
        row=1, col=1
    )
    
    # Total Population Pyramid
    fig.add_trace(
        go.Bar(y=age_order, x=-total_male.values, name='Male (Total)', 
               orientation='h', marker_color=PR_COLORS['blue_light'], showlegend=True),
        row=1, col=2
    )
    fig.add_trace(
        go.Bar(y=age_order, x=total_female.values, name='Female (Total)', 
               orientation='h', marker_color=PR_COLORS['red_light'], showlegend=True),
        row=1, col=2
    )
    
    # Update layout
    max_pr = max(pr_male.max(), pr_female.max()) * 1.1
    max_total = max(total_male.max(), total_female.max()) * 1.1
    
    fig.update_xaxes(title_text="Population", row=1, col=1, range=[-max_pr, max_pr])
    fig.update_xaxes(title_text="Population", row=1, col=2, range=[-max_total, max_total])
    fig.update_yaxes(title_text="Age Group", row=1, col=1)
    fig.update_yaxes(title_text="Age Group", row=1, col=2)
    
    fig.update_layout(
        title={
            'text': f'Population Pyramid: PR Born vs Total Population ({latest_year})',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        template='plotly_white',
        plot_bgcolor=PR_COLORS['gray'],
        paper_bgcolor='white',
        barmode='overlay',
        height=800
    )
    
    fig.write_html(f"{output_dir}/graph_population_pyramid.html", include_plotlyjs='cdn', full_html=False)
    print("Generated population pyramid")

# ============================================================================
# 4. SCATTER PLOT: Economic Conditions vs Migration (Improving Figure 30)
# ============================================================================
def generate_economic_scatter_plot():
    """Convert economic correlation to a scatter plot with regression line"""
    # Load Puerto Rico economic data
    pr_econ_dir = 'data/puerto_rico_economic'
    combined_file = os.path.join(pr_econ_dir, 'pr_economic_combined.csv')
    
    if not os.path.exists(combined_file):
        print("Puerto Rico economic data not found. Skipping scatter plot.")
        return
    
    pr_econ_df = pd.read_csv(combined_file)
    
    # Load Puerto Rican population data
    pop_dir = 'data/census_acs5'
    pop_files = glob.glob(os.path.join(pop_dir, 'acs5_puerto_rican_pop_*.csv'))
    
    if not pop_files:
        print("Puerto Rican population data not found. Skipping scatter plot.")
        return
    
    all_pop = []
    for file in sorted(pop_files):
        df = pd.read_csv(file)
        all_pop.append(df)
    
    pop_df = pd.concat(all_pop, ignore_index=True)
    pop_df['B03001_005E'] = pd.to_numeric(pop_df['B03001_005E'], errors='coerce')
    mainland_pop = pop_df.groupby('year')['B03001_005E'].sum().reset_index()
    mainland_pop.columns = ['year', 'mainland_population']
    
    # Merge with economic data
    merged = pr_econ_df.merge(mainland_pop, on='year', how='inner')
    merged = merged.sort_values('year')
    
    # Calculate net migration (change in population)
    # Note: diff() returns NaN for the first row (no previous year to compare)
    # We exclude the first year since we can't calculate net migration without baseline
    merged['population_change'] = merged['mainland_population'].diff()
    merged['net_migration'] = merged['population_change']  # Don't fillna(0) - keep NaN for first year
    
    # Filter to years with both unemployment and migration data
    # dropna() will exclude 2010 since it has no previous year for comparison
    if 'unemployment_rate' in merged.columns:
        scatter_df = merged[['unemployment_rate', 'net_migration', 'year']].dropna()
        
        if len(scatter_df) > 2:
            # Calculate regression
            x = scatter_df['unemployment_rate'].values
            y = scatter_df['net_migration'].values
            
            # Perform linear regression
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            line_x = np.linspace(x.min(), x.max(), 100)
            line_y = slope * line_x + intercept
            
            # Create scatter plot
            fig = go.Figure()
            
            # Add scatter points
            fig.add_trace(go.Scatter(
                x=scatter_df['unemployment_rate'],
                y=scatter_df['net_migration'],
                mode='markers+text',
                name='Data Points',
                marker=dict(
                    size=10,
                    color=scatter_df['year'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Year"),
                    line=dict(width=1, color='black')
                ),
                text=[f"{int(y)}" for y in scatter_df['year']],
                textposition="top center",
                hovertemplate='<b>Year:</b> %{text}<br>' +
                            '<b>Unemployment:</b> %{x:.1f}%<br>' +
                            '<b>Net Migration:</b> %{y:,.0f}<extra></extra>'
            ))
            
            # Add regression line
            fig.add_trace(go.Scatter(
                x=line_x,
                y=line_y,
                mode='lines',
                name=f'Regression Line (R²={r_value**2:.3f})',
                line=dict(color=PR_COLORS['red'], width=3, dash='dash')
            ))
            
            # Add annotation with correlation info
            fig.add_annotation(
                x=0.05,
                y=0.95,
                xref='paper',
                yref='paper',
                text=f'R² = {r_value**2:.3f}<br>p-value = {p_value:.4f}',
                showarrow=False,
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='black',
                borderwidth=1
            )
            
            fig.update_layout(
                title={
                    'text': 'Economic Push Factor: Puerto Rico Unemployment vs Net Migration',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20}
                },
                xaxis=dict(title='Puerto Rico Unemployment Rate (%)'),
                yaxis=dict(title='Net Migration to Mainland'),
                template='plotly_white',
                plot_bgcolor=PR_COLORS['gray'],
                paper_bgcolor='white',
                hovermode='closest',
                legend=dict(
                    x=0.02,
                    y=0.02,
                    bgcolor='rgba(255, 255, 255, 0.8)',
                    bordercolor='rgba(0, 0, 0, 0.2)',
                    borderwidth=1
                )
            )
            
            fig.write_html(f"{output_dir}/graph_economic_scatter.html", include_plotlyjs='cdn', full_html=False)
            print("Generated economic scatter plot with regression line")
        else:
            print("Insufficient data for scatter plot")
    else:
        print("Unemployment rate data not found in economic data")

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    print("Generating improved visualizations...")
    generate_merged_population_chart()
    generate_state_percent_share_chart()
    generate_population_pyramid()
    generate_economic_scatter_plot()
    print("All improved visualizations generated!")

