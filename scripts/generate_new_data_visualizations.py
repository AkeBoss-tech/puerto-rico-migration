import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import glob

# Ensure output directory exists
output_dir = 'docs'
os.makedirs(output_dir, exist_ok=True)

# Puerto Rican color theme
PR_COLORS = {
    'red': '#DC143C',
    'red_dark': '#B22234',
    'blue': '#0051BA',
    'blue_dark': '#003087',
    'blue_light': '#0066FF',
    'white': '#FFFFFF',
    'gray': '#F5F5F5'
}

PR_COLOR_SEQUENCE = ['#DC143C', '#0051BA', '#B22234', '#0066FF', '#E4002B', '#003087', '#FF6B6B', '#4A90E2']

# Base data directory
base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

# ============================================================================
# 1. HOUSING COSTS VISUALIZATION
# ============================================================================
def generate_housing_visualizations():
    """Generate visualizations for housing costs (rent and home values)."""
    housing_dir = os.path.join(base_dir, 'census_acs5_housing')
    
    if not os.path.exists(housing_dir):
        print("Housing data directory not found. Run download_housing_data.py first.")
        return
    
    # Load all housing data files
    housing_files = glob.glob(os.path.join(housing_dir, 'acs5_housing_*.csv'))
    
    if not housing_files:
        print("No housing data files found.")
        return
    
    all_housing = []
    for file in sorted(housing_files):
        df = pd.read_csv(file)
        all_housing.append(df)
    
    housing_df = pd.concat(all_housing, ignore_index=True)
    
    # Filter for top states with Puerto Rican population (for comparison)
    # We'll focus on states with significant Puerto Rican populations
    top_states = ['New York', 'Florida', 'Pennsylvania', 'New Jersey', 'Massachusetts', 
                  'Connecticut', 'Texas', 'California']
    
    housing_df_filtered = housing_df[housing_df['NAME'].isin(top_states)].copy()
    
    # Convert to numeric
    housing_df_filtered['median_gross_rent'] = pd.to_numeric(
        housing_df_filtered['median_gross_rent'], errors='coerce')
    housing_df_filtered['median_home_value'] = pd.to_numeric(
        housing_df_filtered['median_home_value'], errors='coerce')
    
    # Graph 1: Median Gross Rent Over Time by State
    fig1 = px.line(housing_df_filtered, x='year', y='median_gross_rent', 
                   color='NAME', markers=True,
                   title='Median Gross Rent Over Time: Top Puerto Rican States',
                   labels={'median_gross_rent': 'Median Gross Rent ($)', 
                          'year': 'Year', 'NAME': 'State'},
                   color_discrete_sequence=PR_COLOR_SEQUENCE)
    fig1.update_layout(template='plotly_white', plot_bgcolor=PR_COLORS['gray'], 
                      paper_bgcolor='white', hovermode='x unified')
    fig1.write_html(f"{output_dir}/graph_housing_rent.html", include_plotlyjs='cdn', full_html=False)
    
    # Graph 2: Median Home Value Over Time by State
    fig2 = px.line(housing_df_filtered, x='year', y='median_home_value', 
                   color='NAME', markers=True,
                   title='Median Home Value Over Time: Top Puerto Rican States',
                   labels={'median_home_value': 'Median Home Value ($)', 
                          'year': 'Year', 'NAME': 'State'},
                   color_discrete_sequence=PR_COLOR_SEQUENCE)
    fig2.update_layout(template='plotly_white', plot_bgcolor=PR_COLORS['gray'], 
                      paper_bgcolor='white', hovermode='x unified')
    fig2.write_html(f"{output_dir}/graph_housing_value.html", include_plotlyjs='cdn', full_html=False)
    
    print("Generated housing cost visualizations")

# ============================================================================
# 2. POVERTY RATES VISUALIZATION
# ============================================================================
def generate_poverty_visualizations():
    """Generate visualizations for poverty rates."""
    poverty_dir = os.path.join(base_dir, 'census_acs5_poverty')
    
    if not os.path.exists(poverty_dir):
        print("Poverty data directory not found. Run download_poverty_data.py first.")
        return
    
    # Load all poverty data files
    poverty_files = glob.glob(os.path.join(poverty_dir, 'acs5_poverty_*.csv'))
    
    if not poverty_files:
        print("No poverty data files found.")
        return
    
    all_poverty = []
    for file in sorted(poverty_files):
        df = pd.read_csv(file)
        all_poverty.append(df)
    
    poverty_df = pd.concat(all_poverty, ignore_index=True)
    
    # Filter for top states
    top_states = ['New York', 'Florida', 'Pennsylvania', 'New Jersey', 'Massachusetts', 
                  'Connecticut', 'Texas', 'California', 'Puerto Rico']
    
    poverty_df_filtered = poverty_df[poverty_df['NAME'].isin(top_states)].copy()
    
    # Convert to numeric
    poverty_df_filtered['poverty_rate'] = pd.to_numeric(
        poverty_df_filtered['poverty_rate'], errors='coerce')
    
    # Graph: Poverty Rate Over Time by State
    fig = px.line(poverty_df_filtered, x='year', y='poverty_rate', 
                  color='NAME', markers=True,
                  title='Poverty Rate Over Time: Top Puerto Rican States',
                  labels={'poverty_rate': 'Poverty Rate (%)', 
                         'year': 'Year', 'NAME': 'State'},
                  color_discrete_sequence=PR_COLOR_SEQUENCE)
    fig.update_layout(template='plotly_white', plot_bgcolor=PR_COLORS['gray'], 
                     paper_bgcolor='white', hovermode='x unified')
    fig.write_html(f"{output_dir}/graph_poverty_rates.html", include_plotlyjs='cdn', full_html=False)
    
    print("Generated poverty rate visualizations")

# ============================================================================
# 3. MIGRATION/MOBILITY VISUALIZATION
# ============================================================================
def generate_migration_visualizations():
    """Generate visualizations for migration and mobility patterns."""
    migration_dir = os.path.join(base_dir, 'census_acs5_migration')
    
    if not os.path.exists(migration_dir):
        print("Migration data directory not found. Run download_year_of_arrival_data.py first.")
        return
    
    # Load all migration data files
    migration_files = glob.glob(os.path.join(migration_dir, 'acs5_migration_*.csv'))
    
    if not migration_files:
        print("No migration data files found.")
        return
    
    all_migration = []
    for file in sorted(migration_files):
        df = pd.read_csv(file)
        all_migration.append(df)
    
    migration_df = pd.concat(all_migration, ignore_index=True)
    
    # Filter for top states
    top_states = ['New York', 'Florida', 'Pennsylvania', 'New Jersey', 'Massachusetts', 
                  'Connecticut', 'Texas', 'California']
    
    migration_df_filtered = migration_df[migration_df['NAME'].isin(top_states)].copy()
    
    # Convert to numeric
    migration_df_filtered['migration_rate'] = pd.to_numeric(
        migration_df_filtered['migration_rate'], errors='coerce')
    migration_df_filtered['moved_from_different_state_rate'] = pd.to_numeric(
        migration_df_filtered['moved_from_different_state_rate'], errors='coerce')
    
    # Graph 1: Overall Migration Rate
    fig1 = px.line(migration_df_filtered, x='year', y='migration_rate', 
                   color='NAME', markers=True,
                   title='Population Mobility Rate (Moved in Past Year): Top Puerto Rican States',
                   labels={'migration_rate': 'Migration Rate (%)', 
                          'year': 'Year', 'NAME': 'State'},
                   color_discrete_sequence=PR_COLOR_SEQUENCE)
    fig1.update_layout(template='plotly_white', plot_bgcolor=PR_COLORS['gray'], 
                      paper_bgcolor='white', hovermode='x unified')
    fig1.write_html(f"{output_dir}/graph_migration_rate.html", include_plotlyjs='cdn', full_html=False)
    
    # Graph 2: Interstate Migration Rate
    fig2 = px.line(migration_df_filtered, x='year', y='moved_from_different_state_rate', 
                   color='NAME', markers=True,
                   title='Interstate Migration Rate (Moved from Different State): Top Puerto Rican States',
                   labels={'moved_from_different_state_rate': 'Interstate Migration Rate (%)', 
                          'year': 'Year', 'NAME': 'State'},
                   color_discrete_sequence=PR_COLOR_SEQUENCE)
    fig2.update_layout(template='plotly_white', plot_bgcolor=PR_COLORS['gray'], 
                      paper_bgcolor='white', hovermode='x unified')
    fig2.write_html(f"{output_dir}/graph_interstate_migration.html", include_plotlyjs='cdn', full_html=False)
    
    print("Generated migration visualizations")

# ============================================================================
# 4. PUERTO RICO ECONOMIC DATA VISUALIZATION
# ============================================================================
def generate_pr_economic_visualizations():
    """Generate visualizations for Puerto Rico economic indicators."""
    pr_econ_dir = os.path.join(base_dir, 'puerto_rico_economic')
    
    if not os.path.exists(pr_econ_dir):
        print("Puerto Rico economic data directory not found. Run download_puerto_rico_economic_data.py first.")
        return
    
    # Try to load combined file first
    combined_file = os.path.join(pr_econ_dir, 'pr_economic_combined.csv')
    
    if os.path.exists(combined_file):
        pr_econ_df = pd.read_csv(combined_file)
    else:
        # Load individual files
        unemployment_file = os.path.join(pr_econ_dir, 'pr_unemployment_rate.csv')
        gdp_file = os.path.join(pr_econ_dir, 'pr_gdp.csv')
        
        if not os.path.exists(unemployment_file) or not os.path.exists(gdp_file):
            print("Puerto Rico economic data files not found.")
            return
        
        unemployment_df = pd.read_csv(unemployment_file)
        gdp_df = pd.read_csv(gdp_file)
        
        # Merge
        pr_econ_df = unemployment_df[['year', 'value']].rename(columns={'value': 'unemployment_rate'})
        pr_econ_df = pr_econ_df.merge(
            gdp_df[['year', 'value']].rename(columns={'value': 'gdp'}),
            on='year', how='outer'
        )
    
    # Graph 1: Unemployment Rate Over Time
    if 'unemployment_rate' in pr_econ_df.columns:
        fig1 = px.line(pr_econ_df, x='year', y='unemployment_rate', markers=True,
                      title='Puerto Rico Unemployment Rate Over Time',
                      labels={'unemployment_rate': 'Unemployment Rate (%)', 'year': 'Year'},
                      color_discrete_sequence=[PR_COLORS['red']])
        fig1.update_traces(line=dict(color=PR_COLORS['red'], width=3),
                          marker=dict(color=PR_COLORS['red'], size=8))
        fig1.update_layout(template='plotly_white', plot_bgcolor=PR_COLORS['gray'], 
                          paper_bgcolor='white')
        fig1.write_html(f"{output_dir}/graph_pr_unemployment.html", include_plotlyjs='cdn', full_html=False)
    
    # Graph 2: GDP Over Time
    if 'gdp' in pr_econ_df.columns:
        fig2 = px.line(pr_econ_df, x='year', y='gdp', markers=True,
                      title='Puerto Rico Real GDP Over Time',
                      labels={'gdp': 'Real GDP (Billions of Chained 2017 Dollars)', 'year': 'Year'},
                      color_discrete_sequence=[PR_COLORS['blue']])
        fig2.update_traces(line=dict(color=PR_COLORS['blue'], width=3),
                          marker=dict(color=PR_COLORS['blue'], size=8))
        fig2.update_layout(template='plotly_white', plot_bgcolor=PR_COLORS['gray'], 
                          paper_bgcolor='white')
        fig2.write_html(f"{output_dir}/graph_pr_gdp.html", include_plotlyjs='cdn', full_html=False)
    
    # Graph 3: Combined View (Unemployment vs GDP Growth)
    if 'unemployment_rate' in pr_econ_df.columns and 'gdp' in pr_econ_df.columns:
        # Calculate GDP growth rate
        pr_econ_df = pr_econ_df.sort_values('year')
        pr_econ_df['gdp_growth'] = pr_econ_df['gdp'].pct_change() * 100
        
        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig3.add_trace(
            go.Scatter(x=pr_econ_df['year'], y=pr_econ_df['unemployment_rate'],
                      name='Unemployment Rate (%)', line=dict(color=PR_COLORS['red'], width=3)),
            secondary_y=False,
        )
        
        fig3.add_trace(
            go.Scatter(x=pr_econ_df['year'], y=pr_econ_df['gdp_growth'],
                      name='GDP Growth Rate (%)', line=dict(color=PR_COLORS['blue'], width=3)),
            secondary_y=True,
        )
        
        fig3.update_xaxes(title_text="Year")
        fig3.update_yaxes(title_text="Unemployment Rate (%)", secondary_y=False, 
                         range=[0, max(pr_econ_df['unemployment_rate']) * 1.1])
        fig3.update_yaxes(title_text="GDP Growth Rate (%)", secondary_y=True)
        
        fig3.update_layout(
            title='Puerto Rico: Unemployment Rate vs GDP Growth',
            template='plotly_white',
            plot_bgcolor=PR_COLORS['gray'],
            paper_bgcolor='white',
            hovermode='x unified'
        )
        
        fig3.write_html(f"{output_dir}/graph_pr_economic_combined.html", include_plotlyjs='cdn', full_html=False)
    
    print("Generated Puerto Rico economic visualizations")

# ============================================================================
# 5. COMPARATIVE VISUALIZATION: PR Economic Push Factors vs Migration
# ============================================================================
def generate_migration_economic_correlation():
    """Create visualization correlating Puerto Rico economic data with migration patterns."""
    # Load Puerto Rico economic data
    pr_econ_dir = os.path.join(base_dir, 'puerto_rico_economic')
    combined_file = os.path.join(pr_econ_dir, 'pr_economic_combined.csv')
    
    if not os.path.exists(combined_file):
        print("Puerto Rico economic data not found. Skipping correlation visualization.")
        return
    
    pr_econ_df = pd.read_csv(combined_file)
    
    # Load Puerto Rican population data (from main dataset)
    pop_dir = os.path.join(base_dir, 'census_acs5')
    pop_files = glob.glob(os.path.join(pop_dir, 'acs5_puerto_rican_pop_*.csv'))
    
    if not pop_files:
        print("Puerto Rican population data not found. Skipping correlation visualization.")
        return
    
    all_pop = []
    for file in sorted(pop_files):
        df = pd.read_csv(file)
        all_pop.append(df)
    
    pop_df = pd.concat(all_pop, ignore_index=True)
    
    # Calculate total Puerto Rican population in mainland US by year
    pop_df['B03001_005E'] = pd.to_numeric(pop_df['B03001_005E'], errors='coerce')
    mainland_pop = pop_df.groupby('year')['B03001_005E'].sum().reset_index()
    mainland_pop.columns = ['year', 'mainland_population']
    
    # Merge with economic data
    merged = pr_econ_df.merge(mainland_pop, on='year', how='inner')
    
    # Calculate population growth rate
    merged = merged.sort_values('year')
    merged['population_growth'] = merged['mainland_population'].pct_change() * 100
    
    # Create dual-axis chart
    if 'unemployment_rate' in merged.columns:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=merged['year'], y=merged['unemployment_rate'],
                      name='PR Unemployment Rate (%)', 
                      line=dict(color=PR_COLORS['red'], width=3)),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=merged['year'], y=merged['population_growth'],
                      name='Mainland Population Growth Rate (%)', 
                      line=dict(color=PR_COLORS['blue'], width=3)),
            secondary_y=True,
        )
        
        fig.update_xaxes(title_text="Year")
        fig.update_yaxes(title_text="Puerto Rico Unemployment Rate (%)", secondary_y=False)
        fig.update_yaxes(title_text="Mainland Population Growth Rate (%)", secondary_y=True)
        
        fig.update_layout(
            title='Puerto Rico Economic Conditions vs Mainland Migration',
            template='plotly_white',
            plot_bgcolor=PR_COLORS['gray'],
            paper_bgcolor='white',
            hovermode='x unified'
        )
        
        fig.write_html(f"{output_dir}/graph_migration_economic_correlation.html", 
                      include_plotlyjs='cdn', full_html=False)
        
        print("Generated migration-economic correlation visualization")

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    print("Generating visualizations for new data sources...")
    print("=" * 60)
    
    generate_housing_visualizations()
    generate_poverty_visualizations()
    generate_migration_visualizations()
    generate_pr_economic_visualizations()
    generate_migration_economic_correlation()
    
    print("=" * 60)
    print(f"All visualizations generated in '{output_dir}/' folder.")

