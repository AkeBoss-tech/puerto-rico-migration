"""
Generate visualizations for Puerto Rican-specific data:
1. State comparisons
2. PR-specific vs. overall Hispanic/Latino comparisons
3. Correlation analysis (income, housing, migration patterns)
"""

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

# American/Puerto Rican color theme
PR_COLORS = {
    'red': '#DC143C',
    'red_dark': '#B22234',
    'red_light': '#E4002B',
    'blue': '#0051BA',
    'blue_dark': '#003087',
    'blue_light': '#0066FF',
    'white': '#FFFFFF',
    'gray': '#F5F5F5'
}

PR_COLOR_SEQUENCE = ['#DC143C', '#0051BA', '#B22234', '#0066FF', '#E4002B', '#003087', '#FF6B6B', '#4A90E2']

def load_pr_data():
    """Load all Puerto Rican-specific data files."""
    base_path = 'data/ipums_pr_specific'
    
    data = {}
    files = {
        'poverty': 'ipums_pr_poverty_2021.csv',
        'housing': 'ipums_pr_housing_2021.csv',
        'income': 'ipums_pr_income_2021.csv',
        'education': 'ipums_pr_education_2021.csv',
        'employment': 'ipums_pr_employment_2021.csv',
        'language': 'ipums_pr_language_2021.csv',
        'family': 'ipums_pr_family_2021.csv',
        'demographics': 'ipums_pr_demographics_2021.csv'
    }
    
    for key, filename in files.items():
        filepath = os.path.join(base_path, filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            # Filter out states with very small populations for better visualization
            data[key] = df[df['total_population'] >= 1000].copy()
    
    return data

def load_hispanic_comparison_data():
    """Load Hispanic/Latino comparison data."""
    base_path = 'data/census_acs5_hispanic_comparison'
    
    data = {}
    # Load poverty data
    poverty_file = os.path.join(base_path, 'acs5_hispanic_poverty_2021.csv')
    if os.path.exists(poverty_file):
        data['poverty'] = pd.read_csv(poverty_file)
    
    # Load housing data if available
    housing_file = os.path.join(base_path, 'acs5_hispanic_housing_value_2021.csv')
    if os.path.exists(housing_file):
        data['housing_value'] = pd.read_csv(housing_file)
    
    return data

def load_pr_population_data():
    """Load Puerto Rican population by state data."""
    pop_file = 'data/census_acs5/acs5_puerto_rican_pop_2021.csv'
    if os.path.exists(pop_file):
        df = pd.read_csv(pop_file)
        # Extract state code from state column
        df['state'] = df['state'].astype(str).str.zfill(2)
        return df
    return None

# ============================================================================
# 1. STATE COMPARISONS - Top States by Various Metrics
# ============================================================================

def generate_state_comparison_visualizations(pr_data):
    """Create visualizations comparing states across different metrics."""
    
    # 1. Poverty Rate by State (Top 15)
    if 'poverty' in pr_data:
        poverty_df = pr_data['poverty'].nlargest(15, 'total_population')
        
        fig = px.bar(
            poverty_df,
            x='poverty_rate',
            y='NAME',
            orientation='h',
            title='Puerto Rican Poverty Rates by State (2021)<br><sub>Top 15 States by Population</sub>',
            labels={'poverty_rate': 'Poverty Rate (%)', 'NAME': 'State'},
            color='total_population',
            color_continuous_scale='Reds',
            text='poverty_rate'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(
            template='plotly_white',
            plot_bgcolor=PR_COLORS['gray'],
            paper_bgcolor='white',
            height=600,
            yaxis={'categoryorder': 'total ascending'},
            coloraxis_colorbar=dict(title="Population")
        )
        fig.write_html(f"{output_dir}/graph_pr_poverty_by_state.html", include_plotlyjs='cdn', full_html=False)
        print("Generated: Poverty rates by state")
    
    # 2. Income by State (Top 15)
    if 'income' in pr_data:
        income_df = pr_data['income'].nlargest(15, 'total_population')
        
        fig = px.bar(
            income_df,
            x='median_income',
            y='NAME',
            orientation='h',
            title='Puerto Rican Median Income by State (2021)<br><sub>Top 15 States by Population</sub>',
            labels={'median_income': 'Median Income ($)', 'NAME': 'State'},
            color='total_population',
            color_continuous_scale='Blues',
            text='median_income'
        )
        fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        fig.update_layout(
            template='plotly_white',
            plot_bgcolor=PR_COLORS['gray'],
            paper_bgcolor='white',
            height=600,
            yaxis={'categoryorder': 'total ascending'},
            coloraxis_colorbar=dict(title="Population")
        )
        fig.write_html(f"{output_dir}/graph_pr_income_by_state.html", include_plotlyjs='cdn', full_html=False)
        print("Generated: Income by state")
    
    # 3. Housing Costs by State (Scatter plot: Rent vs Home Value)
    if 'housing' in pr_data:
        housing_df = pr_data['housing'].dropna(subset=['median_rent', 'median_home_value'])
        housing_df = housing_df.nlargest(15, 'total_population')
        
        fig = px.scatter(
            housing_df,
            x='median_rent',
            y='median_home_value',
            size='total_population',
            color='total_population',
            hover_name='NAME',
            title='Puerto Rican Housing Costs by State (2021)<br><sub>Top 15 States by Population</sub>',
            labels={
                'median_rent': 'Median Rent ($)',
                'median_home_value': 'Median Home Value ($)',
                'total_population': 'Population'
            },
            color_continuous_scale='Viridis',
            size_max=30
        )
        fig.update_layout(
            template='plotly_white',
            plot_bgcolor=PR_COLORS['gray'],
            paper_bgcolor='white',
            height=600
        )
        fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        fig.write_html(f"{output_dir}/graph_pr_housing_scatter.html", include_plotlyjs='cdn', full_html=False)
        print("Generated: Housing costs scatter plot")
    
    # 4. Unemployment Rate by State
    if 'employment' in pr_data:
        emp_df = pr_data['employment'].dropna(subset=['unemployment_rate'])
        emp_df = emp_df.nlargest(15, 'total_population')
        
        fig = px.bar(
            emp_df,
            x='unemployment_rate',
            y='NAME',
            orientation='h',
            title='Puerto Rican Unemployment Rates by State (2021)<br><sub>Top 15 States by Population</sub>',
            labels={'unemployment_rate': 'Unemployment Rate (%)', 'NAME': 'State'},
            color='total_population',
            color_continuous_scale='Oranges',
            text='unemployment_rate'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(
            template='plotly_white',
            plot_bgcolor=PR_COLORS['gray'],
            paper_bgcolor='white',
            height=600,
            yaxis={'categoryorder': 'total ascending'},
            coloraxis_colorbar=dict(title="Population")
        )
        fig.write_html(f"{output_dir}/graph_pr_unemployment_by_state.html", include_plotlyjs='cdn', full_html=False)
        print("Generated: Unemployment rates by state")

# ============================================================================
# 2. PR-SPECIFIC vs. HISPANIC/LATINO COMPARISONS
# ============================================================================

def generate_comparison_visualizations(pr_data, hispanic_data):
    """Compare Puerto Rican-specific data with overall Hispanic/Latino data."""
    
    # 1. Poverty Rate Comparison
    if 'poverty' in pr_data and 'poverty' in hispanic_data:
        pr_pov = pr_data['poverty'][['NAME', 'state', 'poverty_rate', 'total_population']].copy()
        pr_pov['Group'] = 'Puerto Rican'
        pr_pov = pr_pov.rename(columns={'poverty_rate': 'rate'})
        
        hisp_pov = hispanic_data['poverty'][['NAME', 'state', 'poverty_rate']].copy()
        hisp_pov['Group'] = 'All Hispanic/Latino'
        hisp_pov = hisp_pov.rename(columns={'poverty_rate': 'rate'})
        
        # Merge and get top states by PR population
        top_states = pr_pov.nlargest(10, 'total_population')['state'].tolist()
        comp_df = pd.concat([
            pr_pov[pr_pov['state'].isin(top_states)][['NAME', 'state', 'rate', 'Group']],
            hisp_pov[hisp_pov['state'].isin(top_states)][['NAME', 'state', 'rate', 'Group']]
        ])
        
        fig = px.bar(
            comp_df,
            x='NAME',
            y='rate',
            color='Group',
            barmode='group',
            title='Poverty Rate Comparison: Puerto Rican vs. All Hispanic/Latino (2021)<br><sub>Top 10 States by Puerto Rican Population</sub>',
            labels={'rate': 'Poverty Rate (%)', 'NAME': 'State'},
            color_discrete_map={
                'Puerto Rican': PR_COLORS['red'],
                'All Hispanic/Latino': PR_COLORS['blue']
            }
        )
        fig.update_layout(
            template='plotly_white',
            plot_bgcolor=PR_COLORS['gray'],
            paper_bgcolor='white',
            height=600,
            xaxis_tickangle=-45
        )
        fig.write_html(f"{output_dir}/graph_pr_vs_hispanic_poverty.html", include_plotlyjs='cdn', full_html=False)
        print("Generated: PR vs Hispanic poverty comparison")
    
    # 2. Income Comparison (if we have income data for Hispanics - would need to add)
    # For now, we'll create a multi-metric comparison chart

# ============================================================================
# 3. CORRELATION ANALYSIS
# ============================================================================

def generate_correlation_analysis(pr_data, pop_data):
    """Analyze correlations between income, housing, and migration patterns."""
    
    # Merge all data by state
    merged = None
    
    if 'income' in pr_data:
        merged = pr_data['income'][['NAME', 'state', 'median_income', 'total_population']].copy()
        
    if 'housing' in pr_data and merged is not None:
        housing_df = pr_data['housing'][['state', 'median_rent', 'median_home_value']]
        merged = merged.merge(housing_df, on='state', how='left')
    
    if 'poverty' in pr_data and merged is not None:
        poverty_df = pr_data['poverty'][['state', 'poverty_rate']]
        merged = merged.merge(poverty_df, on='state', how='left')
    
    if pop_data is not None and merged is not None:
        # Add population data as proxy for migration patterns
        pop_df = pop_data[['state', 'B03001_005E']].copy()
        pop_df.columns = ['state', 'pr_population']
        merged = merged.merge(pop_df, on='state', how='left')
        
        # Calculate log of population for better visualization
        merged['log_population'] = np.log10(merged['pr_population'] + 1)
    
    if merged is None:
        return
    
    # Filter to states with sufficient data
    merged = merged.dropna(subset=['median_income', 'median_rent', 'pr_population'])
    merged = merged[merged['total_population'] >= 1000]
    
    # 1. Income vs. Rent Correlation
    fig = px.scatter(
        merged,
        x='median_income',
        y='median_rent',
        size='pr_population',
        color='poverty_rate',
        hover_name='NAME',
        title='Income vs. Housing Costs: Puerto Rican Population by State (2021)<br><sub>Bubble size = Population, Color = Poverty Rate</sub>',
        labels={
            'median_income': 'Median Income ($)',
            'median_rent': 'Median Rent ($)',
            'pr_population': 'Puerto Rican Population',
            'poverty_rate': 'Poverty Rate (%)'
        },
        color_continuous_scale='RdYlGn_r',
        size_max=30
    )
    
    # Add correlation line
    x = merged['median_income'].values
    y = merged['median_rent'].values
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    
    fig.add_trace(go.Scatter(
        x=x,
        y=p(x),
        mode='lines',
        name='Trend Line',
        line=dict(color='gray', dash='dash', width=2),
        showlegend=True
    ))
    
    # Calculate and display correlation
    corr = np.corrcoef(x, y)[0, 1]
    fig.add_annotation(
        text=f'Correlation: {corr:.2f}',
        xref='paper', yref='paper',
        x=0.05, y=0.95,
        showarrow=False,
        bgcolor='rgba(255, 255, 255, 0.8)'
    )
    
    fig.update_layout(
        template='plotly_white',
        plot_bgcolor=PR_COLORS['gray'],
        paper_bgcolor='white',
        height=600
    )
    fig.write_html(f"{output_dir}/graph_pr_income_rent_correlation.html", include_plotlyjs='cdn', full_html=False)
    print("Generated: Income vs Rent correlation")
    
    # 2. Population vs. Income (Migration patterns)
    fig2 = px.scatter(
        merged,
        x='median_income',
        y='log_population',
        size='total_population',
        color='poverty_rate',
        hover_name='NAME',
        title='Migration Patterns: Population vs. Income (2021)<br><sub>Bubble size = Sample size, Color = Poverty Rate, Y-axis = Log(Population)</sub>',
        labels={
            'median_income': 'Median Income ($)',
            'log_population': 'Puerto Rican Population (Log Scale)',
            'total_population': 'Sample Size',
            'poverty_rate': 'Poverty Rate (%)'
        },
        color_continuous_scale='RdYlGn_r',
        size_max=30
    )
    fig2.update_layout(
        template='plotly_white',
        plot_bgcolor=PR_COLORS['gray'],
        paper_bgcolor='white',
        height=600
    )
    fig2.write_html(f"{output_dir}/graph_pr_population_income_correlation.html", include_plotlyjs='cdn', full_html=False)
    print("Generated: Population vs Income correlation")
    
    # 3. Comprehensive Correlation Matrix
    numeric_cols = ['median_income', 'median_rent', 'median_home_value', 
                    'poverty_rate', 'pr_population', 'total_population']
    numeric_cols = [col for col in numeric_cols if col in merged.columns]
    
    corr_matrix = merged[numeric_cols].corr()
    
    fig3 = px.imshow(
        corr_matrix,
        labels=dict(color="Correlation"),
        title='Correlation Matrix: Puerto Rican Socioeconomic Indicators (2021)',
        color_continuous_scale='RdBu',
        aspect="auto",
        text_auto=True
    )
    fig3.update_layout(
        template='plotly_white',
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=600
    )
    fig3.write_html(f"{output_dir}/graph_pr_correlation_matrix.html", include_plotlyjs='cdn', full_html=False)
    print("Generated: Correlation matrix")

# ============================================================================
# 4. COMPREHENSIVE STATE DASHBOARD
# ============================================================================

def generate_state_dashboard(pr_data):
    """Create a comprehensive dashboard showing multiple metrics by state."""
    
    # Combine key metrics
    metrics = []
    
    if 'income' in pr_data:
        income_df = pr_data['income'][['NAME', 'state', 'median_income']].copy()
        metrics.append(income_df)
    
    if 'poverty' in pr_data:
        poverty_df = pr_data['poverty'][['NAME', 'state', 'poverty_rate']].copy()
        if metrics:
            metrics[0] = metrics[0].merge(poverty_df, on=['NAME', 'state'], how='outer')
        else:
            metrics.append(poverty_df)
    
    if 'housing' in pr_data:
        housing_df = pr_data['housing'][['state', 'median_rent']].copy()
        if metrics:
            metrics[0] = metrics[0].merge(housing_df, on='state', how='outer')
        else:
            metrics.append(housing_df)
    
    if 'employment' in pr_data:
        emp_df = pr_data['employment'][['state', 'unemployment_rate']].copy()
        if metrics:
            metrics[0] = metrics[0].merge(emp_df, on='state', how='outer')
    
    if not metrics:
        return
    
    dashboard_df = metrics[0].copy()
    dashboard_df = dashboard_df.dropna(subset=['NAME'])
    dashboard_df = dashboard_df.nlargest(15, 'median_income') if 'median_income' in dashboard_df.columns else dashboard_df.head(15)
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Median Income', 'Poverty Rate', 'Median Rent', 'Unemployment Rate'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Income
    if 'median_income' in dashboard_df.columns:
        fig.add_trace(
            go.Bar(x=dashboard_df['NAME'], y=dashboard_df['median_income'],
                   name='Income', marker_color=PR_COLORS['blue']),
            row=1, col=1
        )
    
    # Poverty
    if 'poverty_rate' in dashboard_df.columns:
        fig.add_trace(
            go.Bar(x=dashboard_df['NAME'], y=dashboard_df['poverty_rate'],
                   name='Poverty Rate', marker_color=PR_COLORS['red']),
            row=1, col=2
        )
    
    # Rent
    if 'median_rent' in dashboard_df.columns:
        fig.add_trace(
            go.Bar(x=dashboard_df['NAME'], y=dashboard_df['median_rent'],
                   name='Rent', marker_color=PR_COLORS['blue_light']),
            row=2, col=1
        )
    
    # Unemployment
    if 'unemployment_rate' in dashboard_df.columns:
        fig.add_trace(
            go.Bar(x=dashboard_df['NAME'], y=dashboard_df['unemployment_rate'],
                   name='Unemployment', marker_color=PR_COLORS['red_light']),
            row=2, col=2
        )
    
    fig.update_xaxes(tickangle=-45, row=2, col=1)
    fig.update_xaxes(tickangle=-45, row=2, col=2)
    fig.update_layout(
        title_text="Puerto Rican Socioeconomic Dashboard by State (2021)<br><sub>Top 15 States by Income</sub>",
        template='plotly_white',
        plot_bgcolor=PR_COLORS['gray'],
        paper_bgcolor='white',
        height=800,
        showlegend=False
    )
    
    fig.write_html(f"{output_dir}/graph_pr_state_dashboard.html", include_plotlyjs='cdn', full_html=False)
    print("Generated: State dashboard")

if __name__ == "__main__":
    print("="*60)
    print("Generating Puerto Rican-Specific Visualizations")
    print("="*60)
    
    # Load data
    print("\nLoading data...")
    pr_data = load_pr_data()
    hispanic_data = load_hispanic_comparison_data()
    pop_data = load_pr_population_data()
    
    print(f"Loaded {len(pr_data)} PR datasets")
    print(f"Loaded {len(hispanic_data)} Hispanic comparison datasets")
    
    # Generate visualizations
    print("\nGenerating state comparison visualizations...")
    generate_state_comparison_visualizations(pr_data)
    
    print("\nGenerating comparison visualizations...")
    generate_comparison_visualizations(pr_data, hispanic_data)
    
    print("\nGenerating correlation analysis...")
    generate_correlation_analysis(pr_data, pop_data)
    
    print("\nGenerating state dashboard...")
    generate_state_dashboard(pr_data)
    
    print("\n" + "="*60)
    print("All visualizations generated successfully!")
    print(f"Output directory: {output_dir}/")
    print("="*60)
