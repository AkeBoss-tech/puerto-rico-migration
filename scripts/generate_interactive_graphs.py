import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Ensure output directory exists
output_dir = 'docs'
os.makedirs(output_dir, exist_ok=True)

# Load data
file_path = 'data/usa_00001.csv'
df = pd.read_csv(file_path)

# Data Cleaning & Prep
df['INCTOT_CLEAN'] = df['INCTOT'].apply(lambda x: x if x < 999999 else None)
df['SEX_LABEL'] = df['SEX'].map({1: 'Male', 2: 'Female'})
emp_map = {1: 'Employed', 2: 'Unemployed', 3: 'Not in Labor Force'}
df['EMPSTAT_LABEL'] = df['EMPSTAT'].map(emp_map)
df['IS_PR_BORN'] = df['BPL'] == 110

def group_education(code):
    if code <= 2: return 'No Schooling/Pre-school'
    if code <= 6: return 'Grades 1-12'
    if code <= 9: return '1-3 Years College'
    if code >= 10: return '4+ Years College'
    return 'Unknown'

df['EDUC_GROUP'] = df['EDUC'].apply(group_education)

# --- Graph 1: Total Population Trend ---
yearly_pop = df.groupby('YEAR')['PERWT'].sum().reset_index()
fig1 = px.line(yearly_pop, x='YEAR', y='PERWT', markers=True, 
              title='Total Sample Population Trend (Weighted)',
              labels={'PERWT': 'Population', 'YEAR': 'Year'})
fig1.update_layout(template='plotly_white')
fig1.write_html(f"{output_dir}/graph1_pop_trend.html", include_plotlyjs='cdn', full_html=False)

# --- Graph 2: Puerto Rico Born Population ---
pr_data = df[df['IS_PR_BORN']]
if not pr_data.empty:
    pr_yearly = pr_data.groupby('YEAR')['PERWT'].sum().reset_index()
    fig2 = px.bar(pr_yearly, x='YEAR', y='PERWT', 
                  title='Puerto Rico Born Population Living in US Mainland',
                  labels={'PERWT': 'Population', 'YEAR': 'Year'},
                  text_auto=True, color_discrete_sequence=['#3498db'])
    fig2.update_layout(template='plotly_white')
    fig2.write_html(f"{output_dir}/graph2_pr_pop.html", include_plotlyjs='cdn', full_html=False)

# --- Graph 3: Median Income Comparison ---
income_comp = df[df['INCTOT_CLEAN'].notna()].groupby(['YEAR', 'IS_PR_BORN'])['INCTOT_CLEAN'].median().reset_index()
income_comp['Group'] = income_comp['IS_PR_BORN'].map({True: 'PR Born', False: 'Total Population'})
fig3 = px.line(income_comp, x='YEAR', y='INCTOT_CLEAN', color='Group', markers=True,
               title='Median Personal Income: PR Born vs. Total Population',
               labels={'INCTOT_CLEAN': 'Median Income (USD)', 'YEAR': 'Year'})
fig3.update_layout(template='plotly_white')
fig3.write_html(f"{output_dir}/graph3_income.html", include_plotlyjs='cdn', full_html=False)

# --- Graph 4: Age Distribution (Box Plot as interactive alternative to Violin) ---
fig4 = px.box(df, x='YEAR', y='AGE', color='IS_PR_BORN', 
              title='Age Distribution: Total vs PR Born',
              labels={'IS_PR_BORN': 'PR Born', 'AGE': 'Age'},
              color_discrete_map={True: '#e74c3c', False: '#95a5a6'})
# Rename legend
new_names = {'True': 'PR Born', 'False': 'Total Population'}
fig4.for_each_trace(lambda t: t.update(name = new_names[t.name],
                                      legendgroup = new_names[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, new_names[t.name])
                                     )
                  )
fig4.update_layout(template='plotly_white')
fig4.write_html(f"{output_dir}/graph4_age_dist.html", include_plotlyjs='cdn', full_html=False)

# --- Graph 5: Employment Status Stacked Bar ---
if not pr_data.empty:
    emp_counts = pr_data.groupby(['YEAR', 'EMPSTAT_LABEL'])['PERWT'].sum().reset_index()
    # Calculate percentage
    emp_counts['TOTAL_YEAR'] = emp_counts.groupby('YEAR')['PERWT'].transform('sum')
    emp_counts['PERCENT'] = (emp_counts['PERWT'] / emp_counts['TOTAL_YEAR']) * 100
    
    fig5 = px.bar(emp_counts, x='YEAR', y='PERCENT', color='EMPSTAT_LABEL',
                  title='Employment Status Distribution (PR Born)',
                  labels={'PERCENT': 'Percentage (%)', 'EMPSTAT_LABEL': 'Status'},
                  text_auto='.1f',
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig5.update_layout(template='plotly_white')
    fig5.write_html(f"{output_dir}/graph5_employment.html", include_plotlyjs='cdn', full_html=False)

# --- Graph 6: Education Trends ---
if not pr_data.empty:
    educ_counts = pr_data.groupby(['YEAR', 'EDUC_GROUP'])['PERWT'].sum().reset_index()
    educ_counts['TOTAL_YEAR'] = educ_counts.groupby('YEAR')['PERWT'].transform('sum')
    educ_counts['PERCENT'] = (educ_counts['PERWT'] / educ_counts['TOTAL_YEAR']) * 100
    
    fig6 = px.line(educ_counts, x='YEAR', y='PERCENT', color='EDUC_GROUP', markers=True,
                   title='Education Level Trends (PR Born)',
                   labels={'PERCENT': 'Percentage (%)', 'EDUC_GROUP': 'Education Level'})
    fig6.update_layout(template='plotly_white')
    fig6.write_html(f"{output_dir}/graph6_education.html", include_plotlyjs='cdn', full_html=False)

print("All interactive graphs generated in 'docs/' folder.")

