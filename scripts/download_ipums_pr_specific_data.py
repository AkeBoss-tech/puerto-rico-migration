"""
Download Puerto Rican-specific data for poverty, housing, income, and other variables
using IPUMS microdata.

This script extracts ACS microdata, filters for Puerto Rican-born individuals,
and aggregates key variables like poverty status, housing costs, income, education, etc.

Requirements:
- pip install ipumspy
- IPUMS API key (get from https://account.ipums.org/api_keys)
- Set IPUMS_API_KEY environment variable or update the script
"""

import os
import pandas as pd
import time
import numpy as np
from ipumspy import IpumsApiClient, MicrodataExtract

# IPUMS API key - set as environment variable or replace with your key
API_KEY = os.getenv('IPUMS_API_KEY', 'YOUR_API_KEY_HERE')

# State FIPS code mapping
STATE_FIPS_TO_NAME = {
    '01': 'Alabama', '02': 'Alaska', '04': 'Arizona', '05': 'Arkansas',
    '06': 'California', '08': 'Colorado', '09': 'Connecticut', '10': 'Delaware',
    '11': 'District of Columbia', '12': 'Florida', '13': 'Georgia', '15': 'Hawaii',
    '16': 'Idaho', '17': 'Illinois', '18': 'Indiana', '19': 'Iowa',
    '20': 'Kansas', '21': 'Kentucky', '22': 'Louisiana', '23': 'Maine',
    '24': 'Maryland', '25': 'Massachusetts', '26': 'Michigan', '27': 'Minnesota',
    '28': 'Mississippi', '29': 'Missouri', '30': 'Montana', '31': 'Nebraska',
    '32': 'Nevada', '33': 'New Hampshire', '34': 'New Jersey', '35': 'New Mexico',
    '36': 'New York', '37': 'North Carolina', '38': 'North Dakota', '39': 'Ohio',
    '40': 'Oklahoma', '41': 'Oregon', '42': 'Pennsylvania', '44': 'Rhode Island',
    '45': 'South Carolina', '46': 'South Dakota', '47': 'Tennessee', '48': 'Texas',
    '49': 'Utah', '50': 'Vermont', '51': 'Virginia', '53': 'Washington',
    '54': 'West Virginia', '55': 'Wisconsin', '56': 'Wyoming', '72': 'Puerto Rico'
}

# Puerto Rico birthplace code in IPUMS
PUERTO_RICO_BPL = 11000

def download_ipums_pr_specific_data():
    """
    Download and process IPUMS ACS data for Puerto Rican-specific variables.
    
    Extracts data for:
    - Poverty status
    - Housing costs (rent, home value)
    - Income
    - Education
    - Employment
    - And more...
    """
    
    if API_KEY == 'YOUR_API_KEY_HERE':
        print("ERROR: Please set IPUMS_API_KEY environment variable or update the script")
        print("Get your API key from: https://account.ipums.org/api_keys")
        return
    
    # Initialize IPUMS API client
    ipums = IpumsApiClient(API_KEY)
    
    # Define output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'ipums_pr_specific')
    os.makedirs(output_dir, exist_ok=True)
    
    # Years to download (ACS 1-year samples for recent years)
    # Note: For more recent data and better sample sizes, use ACS 5-year samples
    # This example uses 1-year samples for faster processing
    # Start with just 2021 for faster initial run - you can add more years later
    years_to_download = [2021]  # Start with one year for faster processing
    
    # Note: For 2010-2020, you may want to use 5-year samples for better coverage
    # Adjust samples accordingly
    
    for year in years_to_download:
        print(f"\n{'='*60}")
        print(f"Processing {year} ACS Data")
        print(f"{'='*60}")
        
        # Define variables to extract
        # For person-level data:
        variables_person = [
            'BPLD',           # Birthplace Detailed (filter for Puerto Rico = 11000)
            'BPL',            # Birthplace (general)
            'MIGRATE1',       # Migration status
            'YRIMMIG',        # Year of immigration
            'STATEFIP',       # State FIPS code
            'PERWT',          # Person weight
            'POVERTY',        # Poverty status
            'EDUC',           # Educational attainment
            'EDUCD',          # Educational attainment detailed
            'EMPSTAT',        # Employment status
            'LABFORCE',       # Labor force status
            'OCC',            # Occupation (detailed)
            'OCC2010',        # Occupation (2010 classification)
            'IND',            # Industry (detailed)
            'IND1990',        # Industry (1990 classification)
            'INCTOT',         # Total personal income
            'INCEARN',        # Earnings from work
            'LANGUAGED',      # Language spoken at home (detailed)
            'SPEAKENG',       # English speaking ability
            'SEX',            # Sex
            'AGE',            # Age
            'MARST',          # Marital status
            'NCHILD',         # Number of children
            'NCHLT5',         # Number of children under 5
        ]
        
        # For household-level data:
        variables_hh = [
            'HHWT',           # Household weight
            'HHTYPE',         # Household type
            'FAMSIZE',        # Family size
            'NFAMS',          # Number of families in household
            'MULTGEN',        # Multigenerational household
            'RENT',           # Monthly rent
            'RENTGRS',        # Gross rent
            'VALUEH',         # Home value
            'COSTELEC',       # Monthly electricity cost
            'FTOTINC',        # Total family income
            'HHINCOME',       # Household income
            'OWNERSHP',       # Home ownership
            'ROOMS',          # Number of rooms
        ]
        
        # Combine variables (household variables will be on household record)
        all_variables = list(set(variables_person + variables_hh))
        
        # Use ACS 1-year sample for recent years
        # For better coverage, use 5-year samples (e.g., 'us2021a' for 2017-2021)
        sample_name = f'us{year}a'  # ACS 1-year sample
        
        extract = MicrodataExtract(
            collection="usa",
            samples=[sample_name],
            variables=all_variables,
            description=f'Puerto Rican-specific variables for {year}'
        )
        
        try:
            # Submit extract
            print(f"Submitting extract request for {year}...")
            ipums.submit_extract(extract)
            print(f"Extract submitted. Extract ID: {extract.extract_id}")
            
            # Wait for extract to be ready
            print("Waiting for extract to be processed...")
            print("Note: IPUMS extracts can take 10-30+ minutes to process. This is normal.")
            print(f"You can check status at: https://account.ipums.org/extracts with Extract ID: {extract.extract_id}")
            max_wait = 1800  # 30 minutes max wait (larger extracts take longer)
            wait_time = 0
            check_count = 0
            while wait_time < max_wait:
                status = ipums.extract_status(extract)
                check_count += 1
                if check_count % 4 == 0:  # Print status every 4 checks (every minute)
                    print(f"Status check #{check_count}: {status} (waited {wait_time}s / {max_wait}s)")
                else:
                    print(f"Status: {status}")
                
                if status == 'completed':
                    print("✓ Extract ready!")
                    break
                elif status == 'failed':
                    print("✗ Extract failed!")
                    return
                
                time.sleep(15)
                wait_time += 15
            
            if wait_time >= max_wait:
                print("Timeout waiting for extract. Please check status manually.")
                print(f"Extract ID: {extract.extract_id}")
                continue
            
            # Download extract
            print(f"Downloading extract for {year}...")
            download_path = os.path.join(output_dir, f'ipums_acs_{year}')
            os.makedirs(download_path, exist_ok=True)
            ipums.download_extract(extract, download_dir=download_path)
            print(f"Downloaded to {download_path}")
            
            # Process the data
            print(f"Processing data for {year}...")
            process_ipums_pr_data(download_path, year, output_dir)
            
        except Exception as e:
            print(f"Error processing {year}: {e}")
            import traceback
            traceback.print_exc()
            continue

def process_ipums_pr_data(download_path, year, output_dir):
    """Process downloaded IPUMS microdata and aggregate by state for Puerto Rican population."""
    
    import glob
    
    # Find the data file (usually ends with .dat.gz)
    data_files = glob.glob(os.path.join(download_path, '*.dat.gz'))
    if not data_files:
        data_files = glob.glob(os.path.join(download_path, '*.dat'))
    
    if not data_files:
        print(f"Warning: No data file found in {download_path}")
        return
    
    data_file = data_files[0]
    
    # Find the DDI file for metadata
    ddi_files = glob.glob(os.path.join(download_path, '*.xml'))
    if not ddi_files:
        print(f"Warning: No DDI file found in {download_path}")
        return
    
    ddi_file = ddi_files[0]
    
    # Read the data using ipumspy's reader
    try:
        from ipumspy import readers
        
        print("Reading DDI file...")
        ddi = readers.read_ipums_ddi(ddi_file)
        
        print("Reading microdata (this may take a while)...")
        microdata = readers.read_microdata(ddi, data_file)
        
        print(f"Total records: {len(microdata):,}")
        
        # Filter for Puerto Rican born (BPLD == 11000)
        pr_born = microdata[microdata['BPLD'] == PUERTO_RICO_BPL].copy()
        
        if len(pr_born) == 0:
            print(f"Warning: No Puerto Rican born individuals found in {year} data")
            return
        
        print(f"Puerto Rican born records: {len(pr_born):,}")
        
        # Separate person and household records if needed
        # IPUMS structure: person records have person-level vars, household vars are on person records too
        
        # Create weighted counts
        pr_born['weighted_count'] = pr_born['PERWT']
        
        # Aggregate by state - create multiple output files for different variables
        
        # 1. Poverty Status by State
        if 'POVERTY' in pr_born.columns:
            print("Calculating poverty statistics...")
            poverty_stats = calculate_poverty_stats(pr_born, year)
            poverty_file = os.path.join(output_dir, f'ipums_pr_poverty_{year}.csv')
            poverty_stats.to_csv(poverty_file, index=False)
            print(f"Saved poverty data to {poverty_file}")
        
        # 2. Housing Costs by State
        if 'RENT' in pr_born.columns or 'VALUEH' in pr_born.columns:
            print("Calculating housing statistics...")
            housing_stats = calculate_housing_stats(pr_born, year)
            housing_file = os.path.join(output_dir, f'ipums_pr_housing_{year}.csv')
            housing_stats.to_csv(housing_file, index=False)
            print(f"Saved housing data to {housing_file}")
        
        # 3. Income Statistics by State
        if 'INCTOT' in pr_born.columns or 'FTOTINC' in pr_born.columns:
            print("Calculating income statistics...")
            income_stats = calculate_income_stats(pr_born, year)
            income_file = os.path.join(output_dir, f'ipums_pr_income_{year}.csv')
            income_stats.to_csv(income_file, index=False)
            print(f"Saved income data to {income_file}")
        
        # 4. Education Statistics by State
        if 'EDUC' in pr_born.columns:
            print("Calculating education statistics...")
            education_stats = calculate_education_stats(pr_born, year)
            education_file = os.path.join(output_dir, f'ipums_pr_education_{year}.csv')
            education_stats.to_csv(education_file, index=False)
            print(f"Saved education data to {education_file}")
        
        # 5. Employment Statistics by State
        if 'EMPSTAT' in pr_born.columns or 'LABFORCE' in pr_born.columns:
            print("Calculating employment statistics...")
            employment_stats = calculate_employment_stats(pr_born, year)
            employment_file = os.path.join(output_dir, f'ipums_pr_employment_{year}.csv')
            employment_stats.to_csv(employment_file, index=False)
            print(f"Saved employment data to {employment_file}")
        
        # 6. Demographic Summary by State
        print("Calculating demographic summary...")
        demo_stats = calculate_demographic_summary(pr_born, year)
        demo_file = os.path.join(output_dir, f'ipums_pr_demographics_{year}.csv')
        demo_stats.to_csv(demo_file, index=False)
        print(f"Saved demographics data to {demo_file}")
        
        # 7. Language and English Proficiency by State
        if 'SPEAKENG' in pr_born.columns or 'LANGUAGED' in pr_born.columns:
            print("Calculating language statistics...")
            language_stats = calculate_language_stats(pr_born, year)
            language_file = os.path.join(output_dir, f'ipums_pr_language_{year}.csv')
            language_stats.to_csv(language_file, index=False)
            print(f"Saved language data to {language_file}")
        
        # 8. Family Structure by State
        if 'FAMSIZE' in pr_born.columns or 'HHTYPE' in pr_born.columns:
            print("Calculating family structure statistics...")
            family_stats = calculate_family_stats(pr_born, year)
            family_file = os.path.join(output_dir, f'ipums_pr_family_{year}.csv')
            family_stats.to_csv(family_file, index=False)
            print(f"Saved family structure data to {family_file}")
        
        # 9. Generation Analysis (1st vs. 2nd generation)
        if 'BPL' in pr_born.columns:
            print("Calculating generation statistics...")
            generation_stats = calculate_generation_stats(pr_born, year)
            generation_file = os.path.join(output_dir, f'ipums_pr_generation_{year}.csv')
            generation_stats.to_csv(generation_file, index=False)
            print(f"Saved generation data to {generation_file}")
        
        # 10. Occupation and Industry Details by State
        if 'OCC' in pr_born.columns or 'IND' in pr_born.columns:
            print("Calculating occupation and industry statistics...")
            occupation_stats = calculate_occupation_industry_stats(pr_born, year)
            occupation_file = os.path.join(output_dir, f'ipums_pr_occupation_industry_{year}.csv')
            occupation_stats.to_csv(occupation_file, index=False)
            print(f"Saved occupation/industry data to {occupation_file}")
        
        print(f"\nCompleted processing {year} data")
        
    except Exception as e:
        print(f"Error processing microdata: {e}")
        import traceback
        traceback.print_exc()

def calculate_poverty_stats(df, year):
    """Calculate poverty statistics by state for Puerto Rican population."""
    
    # Filter for population in poverty universe (POVERTY codes vary, typically 0 = N/A, 1-5 = various poverty levels)
    # IPUMS POVERTY codes: 0 = N/A, 1 = below 50%, 2 = 50-99%, 3 = 100-124%, 4 = 125-149%, 5 = 150-184%, 6 = 185-199%, 7 = 200-299%, 8 = 300%+
    # For standard poverty definition, codes 1-3 are below 125% of poverty line
    
    # Create poverty flag (below 125% of poverty line = codes 1, 2, 3)
    df['below_poverty'] = df['POVERTY'].isin([1, 2, 3]).astype(int)
    df['in_poverty_universe'] = (df['POVERTY'] > 0).astype(int)
    
    # Aggregate by state
    state_stats = df.groupby('STATEFIP').agg({
        'weighted_count': 'sum',
        'below_poverty': lambda x: (df.loc[x.index, 'weighted_count'] * x).sum(),
        'in_poverty_universe': lambda x: (df.loc[x.index, 'weighted_count'] * x).sum(),
    }).reset_index()
    
    # Calculate poverty rate
    state_stats['poverty_rate'] = (state_stats['below_poverty'] / state_stats['in_poverty_universe'] * 100).round(2)
    state_stats['below_poverty'] = state_stats['below_poverty'].round().astype(int)
    state_stats['in_poverty_universe'] = state_stats['in_poverty_universe'].round().astype(int)
    
    # Clean up
    state_stats = state_stats.rename(columns={
        'weighted_count': 'total_population',
        'below_poverty': 'below_poverty_level'
    })
    
    # Add state name and year
    state_stats['state'] = state_stats['STATEFIP'].astype(str).str.zfill(2)
    state_stats['NAME'] = state_stats['state'].map(STATE_FIPS_TO_NAME)
    state_stats['year'] = year
    
    # Reorder columns
    state_stats = state_stats[['NAME', 'total_population', 'below_poverty_level', 
                               'in_poverty_universe', 'poverty_rate', 'state', 'year']]
    
    return state_stats.sort_values('total_population', ascending=False)

def calculate_housing_stats(df, year):
    """Calculate housing cost statistics by state for Puerto Rican population."""
    
    # Filter for renter-occupied (RENT > 0) and owner-occupied (VALUEH > 0)
    renters = df[(df['RENT'] > 0) & (df['RENT'] < 999999)].copy()
    owners = df[(df['VALUEH'] > 0) & (df['VALUEH'] < 9999999)].copy()
    
    # Aggregate by state
    state_stats = df.groupby('STATEFIP').agg({
        'weighted_count': 'sum'
    }).reset_index()
    
    # Calculate median rent by state
    if len(renters) > 0:
        rent_medians = []
        for state_fips in state_stats['STATEFIP'].unique():
            state_renters = renters[renters['STATEFIP'] == state_fips]
            if len(state_renters) > 0:
                median_rent = weighted_median(state_renters['RENT'], state_renters['HHWT'])
                rent_medians.append({'STATEFIP': state_fips, 'median_rent': median_rent})
        
        rent_df = pd.DataFrame(rent_medians)
        state_stats = state_stats.merge(rent_df, on='STATEFIP', how='left')
    
    # Calculate median home value by state
    if len(owners) > 0:
        value_medians = []
        for state_fips in state_stats['STATEFIP'].unique():
            state_owners = owners[owners['STATEFIP'] == state_fips]
            if len(state_owners) > 0:
                median_value = weighted_median(state_owners['VALUEH'], state_owners['HHWT'])
                value_medians.append({'STATEFIP': state_fips, 'median_home_value': median_value})
        
        value_df = pd.DataFrame(value_medians)
        state_stats = state_stats.merge(value_df, on='STATEFIP', how='left')
    
    # Add state name and year
    state_stats['state'] = state_stats['STATEFIP'].astype(str).str.zfill(2)
    state_stats['NAME'] = state_stats['state'].map(STATE_FIPS_TO_NAME)
    state_stats['year'] = year
    
    # Rename and reorder
    state_stats = state_stats.rename(columns={'weighted_count': 'total_population'})
    cols = ['NAME', 'total_population']
    if 'median_rent' in state_stats.columns:
        cols.append('median_rent')
    if 'median_home_value' in state_stats.columns:
        cols.append('median_home_value')
    cols.extend(['state', 'year'])
    
    state_stats = state_stats[cols]
    
    return state_stats.sort_values('total_population', ascending=False)

def calculate_income_stats(df, year):
    """Calculate income statistics by state for Puerto Rican population."""
    
    # Filter for valid income values (remove N/A codes, typically negative or very large)
    # IPUMS typically uses codes like 9999999 or negative values for N/A
    valid_income = df[(df['INCTOT'] >= 0) & (df['INCTOT'] < 9999999)].copy()
    
    state_stats = df.groupby('STATEFIP').agg({
        'weighted_count': 'sum'
    }).reset_index()
    
    if len(valid_income) > 0:
        income_medians = []
        income_means = []
        for state_fips in state_stats['STATEFIP'].unique():
            state_income = valid_income[valid_income['STATEFIP'] == state_fips]
            if len(state_income) > 0:
                median_income = weighted_median(state_income['INCTOT'], state_income['PERWT'])
                mean_income = (state_income['INCTOT'] * state_income['PERWT']).sum() / state_income['PERWT'].sum()
                income_medians.append({'STATEFIP': state_fips, 'median_income': median_income})
                income_means.append({'STATEFIP': state_fips, 'mean_income': mean_income})
        
        income_df = pd.DataFrame(income_medians)
        income_df = income_df.merge(pd.DataFrame(income_means), on='STATEFIP')
        state_stats = state_stats.merge(income_df, on='STATEFIP', how='left')
    
    # Add state name and year
    state_stats['state'] = state_stats['STATEFIP'].astype(str).str.zfill(2)
    state_stats['NAME'] = state_stats['state'].map(STATE_FIPS_TO_NAME)
    state_stats['year'] = year
    
    # Rename and reorder
    state_stats = state_stats.rename(columns={'weighted_count': 'total_population'})
    cols = ['NAME', 'total_population']
    if 'median_income' in state_stats.columns:
        cols.append('median_income')
    if 'mean_income' in state_stats.columns:
        cols.append('mean_income')
    cols.extend(['state', 'year'])
    
    state_stats = state_stats[cols]
    
    return state_stats.sort_values('total_population', ascending=False)

def calculate_education_stats(df, year):
    """Calculate education statistics by state for Puerto Rican population."""
    
    # Filter for population 25+ (typical age for education analysis)
    adults = df[df['AGE'] >= 25].copy()
    
    # EDUC codes vary by year, but generally:
    # 0 = N/A, 1 = no schooling, 2 = nursery, 3 = kindergarten, 4-9 = grades 1-8, 
    # 10-11 = grades 9-12, 12 = high school, 13-15 = some college, 16 = bachelor's, 17+ = graduate
    
    # Create education flags
    adults['has_high_school'] = (adults['EDUC'] >= 12).astype(int)
    adults['has_bachelors'] = (adults['EDUC'] >= 16).astype(int)
    
    # Aggregate by state
    state_stats = df.groupby('STATEFIP').agg({
        'weighted_count': 'sum'
    }).reset_index()
    
    adult_stats = adults.groupby('STATEFIP').agg({
        'weighted_count': 'sum',
        'has_high_school': lambda x: (adults.loc[x.index, 'PERWT'] * x).sum(),
        'has_bachelors': lambda x: (adults.loc[x.index, 'PERWT'] * x).sum(),
    }).reset_index()
    
    adult_stats['high_school_rate'] = (adult_stats['has_high_school'] / adult_stats['weighted_count'] * 100).round(2)
    adult_stats['bachelors_rate'] = (adult_stats['has_bachelors'] / adult_stats['weighted_count'] * 100).round(2)
    
    state_stats = state_stats.merge(adult_stats[['STATEFIP', 'high_school_rate', 'bachelors_rate']], 
                                    on='STATEFIP', how='left')
    
    # Add state name and year
    state_stats['state'] = state_stats['STATEFIP'].astype(str).str.zfill(2)
    state_stats['NAME'] = state_stats['state'].map(STATE_FIPS_TO_NAME)
    state_stats['year'] = year
    
    state_stats = state_stats.rename(columns={'weighted_count': 'total_population'})
    state_stats = state_stats[['NAME', 'total_population', 'high_school_rate', 
                               'bachelors_rate', 'state', 'year']]
    
    return state_stats.sort_values('total_population', ascending=False)

def calculate_employment_stats(df, year):
    """Calculate employment statistics by state for Puerto Rican population."""
    
    # Filter for working age population (16+)
    working_age = df[df['AGE'] >= 16].copy()
    
    # EMPSTAT codes: 0 = N/A, 1 = employed, 2 = unemployed, 3 = not in labor force
    working_age['employed'] = (working_age['EMPSTAT'] == 1).astype(int)
    working_age['unemployed'] = (working_age['EMPSTAT'] == 2).astype(int)
    working_age['in_labor_force'] = (working_age['EMPSTAT'].isin([1, 2])).astype(int)
    
    # Aggregate by state
    state_stats = df.groupby('STATEFIP').agg({
        'weighted_count': 'sum'
    }).reset_index()
    
    emp_stats = working_age.groupby('STATEFIP').agg({
        'employed': lambda x: (working_age.loc[x.index, 'PERWT'] * x).sum(),
        'unemployed': lambda x: (working_age.loc[x.index, 'PERWT'] * x).sum(),
        'in_labor_force': lambda x: (working_age.loc[x.index, 'PERWT'] * x).sum(),
    }).reset_index()
    
    emp_stats['unemployment_rate'] = (emp_stats['unemployed'] / emp_stats['in_labor_force'] * 100).round(2)
    emp_stats['labor_force_participation'] = (emp_stats['in_labor_force'] / 
                                             working_age.groupby('STATEFIP')['PERWT'].sum() * 100).round(2)
    
    state_stats = state_stats.merge(emp_stats[['STATEFIP', 'unemployment_rate', 
                                               'labor_force_participation']], 
                                    on='STATEFIP', how='left')
    
    # Add state name and year
    state_stats['state'] = state_stats['STATEFIP'].astype(str).str.zfill(2)
    state_stats['NAME'] = state_stats['state'].map(STATE_FIPS_TO_NAME)
    state_stats['year'] = year
    
    state_stats = state_stats.rename(columns={'weighted_count': 'total_population'})
    state_stats = state_stats[['NAME', 'total_population', 'unemployment_rate', 
                               'labor_force_participation', 'state', 'year']]
    
    return state_stats.sort_values('total_population', ascending=False)

def calculate_demographic_summary(df, year):
    """Calculate basic demographic summary by state."""
    
    # Calculate median age
    age_stats = []
    for state_fips in df['STATEFIP'].unique():
        state_data = df[df['STATEFIP'] == state_fips]
        if len(state_data) > 0:
            median_age = weighted_median(state_data['AGE'], state_data['PERWT'])
            total_pop = state_data['PERWT'].sum()
            age_stats.append({'STATEFIP': state_fips, 'median_age': median_age, 
                            'total_population': total_pop})
    
    state_stats = pd.DataFrame(age_stats)
    
    # Add state name and year
    state_stats['state'] = state_stats['STATEFIP'].astype(str).str.zfill(2)
    state_stats['NAME'] = state_stats['state'].map(STATE_FIPS_TO_NAME)
    state_stats['year'] = year
    
    state_stats['total_population'] = state_stats['total_population'].round().astype(int)
    state_stats = state_stats[['NAME', 'total_population', 'median_age', 'state', 'year']]
    
    return state_stats.sort_values('total_population', ascending=False)

def calculate_language_stats(df, year):
    """Calculate language and English proficiency statistics by state."""
    
    # Filter for population 5+ (typical age for language analysis)
    language_age = df[df['AGE'] >= 5].copy()
    
    # SPEAKENG codes: 0 = N/A, 1 = only English, 2 = very well, 3 = well, 4 = not well, 5 = not at all
    # We consider codes 2-5 as "speaks language other than English"
    # Codes 2 = speaks very well, 3+ = limited English proficiency
    language_age['speaks_english_only'] = (language_age['SPEAKENG'] == 1).astype(int)
    language_age['speaks_other_language'] = (language_age['SPEAKENG'].isin([2, 3, 4, 5])).astype(int)
    language_age['limited_english'] = (language_age['SPEAKENG'].isin([3, 4, 5])).astype(int)
    
    # Aggregate by state
    state_stats = df.groupby('STATEFIP').agg({
        'weighted_count': 'sum'
    }).reset_index()
    
    lang_stats = language_age.groupby('STATEFIP').agg({
        'speaks_english_only': lambda x: (language_age.loc[x.index, 'PERWT'] * x).sum(),
        'speaks_other_language': lambda x: (language_age.loc[x.index, 'PERWT'] * x).sum(),
        'limited_english': lambda x: (language_age.loc[x.index, 'PERWT'] * x).sum(),
    }).reset_index()
    
    lang_stats['english_only_rate'] = (lang_stats['speaks_english_only'] / 
                                       language_age.groupby('STATEFIP')['PERWT'].sum() * 100).round(2)
    lang_stats['other_language_rate'] = (lang_stats['speaks_other_language'] / 
                                         language_age.groupby('STATEFIP')['PERWT'].sum() * 100).round(2)
    lang_stats['limited_english_rate'] = (lang_stats['limited_english'] / 
                                          language_age.groupby('STATEFIP')['PERWT'].sum() * 100).round(2)
    
    state_stats = state_stats.merge(lang_stats[['STATEFIP', 'english_only_rate', 
                                                'other_language_rate', 'limited_english_rate']], 
                                    on='STATEFIP', how='left')
    
    # Add state name and year
    state_stats['state'] = state_stats['STATEFIP'].astype(str).str.zfill(2)
    state_stats['NAME'] = state_stats['state'].map(STATE_FIPS_TO_NAME)
    state_stats['year'] = year
    
    state_stats = state_stats.rename(columns={'weighted_count': 'total_population'})
    state_stats = state_stats[['NAME', 'total_population', 'english_only_rate', 
                               'other_language_rate', 'limited_english_rate', 'state', 'year']]
    
    return state_stats.sort_values('total_population', ascending=False)

def calculate_family_stats(df, year):
    """Calculate family structure statistics by state."""
    
    # Use household-level data - need to deduplicate by household
    # Get unique households (can use SERIAL for household ID if available, or group by key vars)
    # For simplicity, we'll aggregate at person level but use household variables
    
    # Family size
    if 'FAMSIZE' in df.columns:
        df['family_size'] = df['FAMSIZE']
    
    # Household type indicators
    # HHTYPE codes vary, but generally: 1 = family household, 2 = nonfamily household
    if 'HHTYPE' in df.columns:
        df['is_family_household'] = (df['HHTYPE'] == 1).astype(int)
    
    # Multigenerational household
    if 'MULTGEN' in df.columns:
        # MULTGEN: 0 = not multigenerational, 1 = multigenerational
        df['is_multigenerational'] = (df['MULTGEN'] == 1).astype(int)
    
    # Number of children
    if 'NCHILD' in df.columns:
        df['has_children'] = (df['NCHILD'] > 0).astype(int)
        df['has_young_children'] = (df['NCHLT5'] > 0).astype(int) if 'NCHLT5' in df.columns else 0
    
    # Aggregate by state (household-weighted)
    state_stats = df.groupby('STATEFIP').agg({
        'weighted_count': 'sum',
        'HHWT': 'first',  # Household weight
    }).reset_index()
    
    # Calculate averages by state
    family_means = []
    for state_fips in df['STATEFIP'].unique():
        state_data = df[df['STATEFIP'] == state_fips]
        if len(state_data) > 0:
            stats = {'STATEFIP': state_fips}
            
            if 'FAMSIZE' in state_data.columns:
                stats['avg_family_size'] = weighted_mean(state_data['FAMSIZE'], state_data['HHWT'])
            
            if 'is_family_household' in state_data.columns:
                stats['family_household_rate'] = (state_data['is_family_household'] * state_data['HHWT']).sum() / state_data['HHWT'].sum() * 100
            
            if 'is_multigenerational' in state_data.columns:
                stats['multigenerational_rate'] = (state_data['is_multigenerational'] * state_data['HHWT']).sum() / state_data['HHWT'].sum() * 100
            
            if 'has_children' in state_data.columns:
                stats['households_with_children_rate'] = (state_data['has_children'] * state_data['HHWT']).sum() / state_data['HHWT'].sum() * 100
            
            family_means.append(stats)
    
    family_df = pd.DataFrame(family_means)
    state_stats = state_stats.merge(family_df, on='STATEFIP', how='left')
    
    # Round numeric columns
    for col in ['avg_family_size', 'family_household_rate', 'multigenerational_rate', 'households_with_children_rate']:
        if col in state_stats.columns:
            state_stats[col] = state_stats[col].round(2)
    
    # Add state name and year
    state_stats['state'] = state_stats['STATEFIP'].astype(str).str.zfill(2)
    state_stats['NAME'] = state_stats['state'].map(STATE_FIPS_TO_NAME)
    state_stats['year'] = year
    
    state_stats = state_stats.rename(columns={'weighted_count': 'total_population'})
    # Select relevant columns
    cols = ['NAME', 'total_population']
    if 'avg_family_size' in state_stats.columns:
        cols.append('avg_family_size')
    if 'family_household_rate' in state_stats.columns:
        cols.append('family_household_rate')
    if 'multigenerational_rate' in state_stats.columns:
        cols.append('multigenerational_rate')
    if 'households_with_children_rate' in state_stats.columns:
        cols.append('households_with_children_rate')
    cols.extend(['state', 'year'])
    
    state_stats = state_stats[cols]
    
    return state_stats.sort_values('total_population', ascending=False)

def calculate_generation_stats(df, year):
    """Calculate generation statistics (1st vs. 2nd generation) by state."""
    
    # BPL codes: 11000 = Puerto Rico, others are different places
    # For Puerto Rican analysis:
    # - 1st generation: BPLD == 11000 (Puerto Rico-born)
    # - 2nd generation: Need to check parent's birthplace (can use MOMLOC/POPLOC if available)
    # For simplicity, we'll focus on 1st generation (Puerto Rico-born) vs. all others
    # Note: This is a simplified approach - true 2nd generation requires parent birthplace data
    
    # All individuals in this dataset are Puerto Rico-born (we filtered earlier)
    # So this is all 1st generation. For true 2nd generation analysis, you'd need
    # to filter by Hispanic origin (HISPAN) and parent birthplace
    
    # For now, we'll note that this is 1st generation data
    # A more complete analysis would require additional variables
    
    state_stats = df.groupby('STATEFIP').agg({
        'weighted_count': 'sum'
    }).reset_index()
    
    # Mark all as first generation (Puerto Rico-born)
    state_stats['first_generation_count'] = state_stats['weighted_count']
    state_stats['first_generation_rate'] = 100.0  # All are 1st gen in this dataset
    
    # Add state name and year
    state_stats['state'] = state_stats['STATEFIP'].astype(str).str.zfill(2)
    state_stats['NAME'] = state_stats['state'].map(STATE_FIPS_TO_NAME)
    state_stats['year'] = year
    
    state_stats = state_stats.rename(columns={'weighted_count': 'total_population'})
    state_stats = state_stats[['NAME', 'total_population', 'first_generation_count', 
                               'first_generation_rate', 'state', 'year']]
    
    # Note: This is simplified. For true intergenerational analysis, need to use HISPAN
    # and filter for Puerto Rican origin rather than birthplace
    
    return state_stats.sort_values('total_population', ascending=False)

def calculate_occupation_industry_stats(df, year):
    """Calculate occupation and industry statistics by state."""
    
    # Filter for employed population
    employed = df[df['EMPSTAT'] == 1].copy()
    
    if len(employed) == 0:
        # Return empty stats if no employed
        state_stats = df.groupby('STATEFIP').agg({'weighted_count': 'sum'}).reset_index()
        state_stats['state'] = state_stats['STATEFIP'].astype(str).str.zfill(2)
        state_stats['NAME'] = state_stats['state'].map(STATE_FIPS_TO_NAME)
        state_stats['year'] = year
        state_stats = state_stats.rename(columns={'weighted_count': 'total_population'})
        return state_stats[['NAME', 'total_population', 'state', 'year']]
    
    # Aggregate by state
    state_stats = df.groupby('STATEFIP').agg({
        'weighted_count': 'sum'
    }).reset_index()
    
    # Count employed by state
    employed_counts = employed.groupby('STATEFIP')['PERWT'].sum().reset_index()
    employed_counts.columns = ['STATEFIP', 'employed_count']
    
    state_stats = state_stats.merge(employed_counts, on='STATEFIP', how='left')
    state_stats['employment_rate'] = (state_stats['employed_count'] / 
                                     state_stats['weighted_count'] * 100).round(2)
    
    # Top occupation categories (simplified - would need detailed occupation classification)
    # Top industry categories (simplified - would need detailed industry classification)
    
    # For now, just provide employment counts
    # Detailed occupation/industry breakdowns would require more complex categorization
    
    # Add state name and year
    state_stats['state'] = state_stats['STATEFIP'].astype(str).str.zfill(2)
    state_stats['NAME'] = state_stats['state'].map(STATE_FIPS_TO_NAME)
    state_stats['year'] = year
    
    state_stats = state_stats.rename(columns={'weighted_count': 'total_population'})
    state_stats['employed_count'] = state_stats['employed_count'].round().astype(int)
    state_stats = state_stats[['NAME', 'total_population', 'employed_count', 
                               'employment_rate', 'state', 'year']]
    
    return state_stats.sort_values('total_population', ascending=False)

def weighted_mean(values, weights):
    """Calculate weighted mean."""
    return (values * weights).sum() / weights.sum()

def weighted_median(values, weights):
    """Calculate weighted median."""
    # Sort by values
    sorted_indices = values.sort_values().index
    sorted_values = values.loc[sorted_indices]
    sorted_weights = weights.loc[sorted_indices]
    
    # Cumulative weights
    cum_weights = sorted_weights.cumsum()
    total_weight = sorted_weights.sum()
    
    # Find median
    median_index = cum_weights[cum_weights >= total_weight / 2].index[0]
    return sorted_values.loc[median_index]

if __name__ == "__main__":
    download_ipums_pr_specific_data()

