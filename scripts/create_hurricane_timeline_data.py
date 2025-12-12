"""
Create hurricane and disaster timeline data for Puerto Rico.

This script creates a template CSV file with major hurricanes and disasters
affecting Puerto Rico that may have influenced migration patterns.

This data should be manually researched and filled in, as it requires
compilation from multiple sources (NOAA, FEMA, news reports, etc.).

Requirements:
- None (creates template file)
"""

import os
import pandas as pd

def create_hurricane_timeline_template():
    """
    Create a template CSV file for hurricane/disaster timeline data.
    
    Users should research and fill in the details for each event.
    """
    # Define output directory and file
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'puerto_rico_disasters')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'pr_disaster_timeline.csv')
    
    # Template data with known major events
    # Users should research and add details, dates, impacts, etc.
    template_data = [
        {
            'event_name': 'Hurricane Maria',
            'date': '2017-09-20',
            'year': 2017,
            'month': 9,
            'category': 'Hurricane',
            'severity': 'Category 5',
            'estimated_deaths': 2977,  # Official estimate, may vary
            'economic_damage_billions_usd': 90,
            'homes_destroyed': 70000,
            'homes_damaged': 300000,
            'power_outage_duration_days': 328,  # Some areas
            'notes': 'Most destructive hurricane in modern Puerto Rico history. Massive migration spike to mainland.',
            'migration_impact': 'Very High',
            'mainland_destinations': 'Florida, New York, Pennsylvania, Connecticut, Massachusetts'
        },
        {
            'event_name': 'Hurricane Irma',
            'date': '2017-09-06',
            'year': 2017,
            'month': 9,
            'category': 'Hurricane',
            'severity': 'Category 5',
            'estimated_deaths': 3,
            'economic_damage_billions_usd': 1,
            'homes_destroyed': None,
            'homes_damaged': None,
            'power_outage_duration_days': 11,
            'notes': 'Hit just before Maria. Primarily affected northern coast.',
            'migration_impact': 'Medium',
            'mainland_destinations': None
        },
        {
            'event_name': 'Hurricane Fiona',
            'date': '2022-09-18',
            'year': 2022,
            'month': 9,
            'category': 'Hurricane',
            'severity': 'Category 1',
            'estimated_deaths': 25,
            'economic_damage_billions_usd': 8,
            'homes_destroyed': None,
            'homes_damaged': None,
            'power_outage_duration_days': 18,
            'notes': 'Caused island-wide power outage. Significant flooding.',
            'migration_impact': 'Medium',
            'mainland_destinations': None
        },
        {
            'event_name': 'Hurricane Georges',
            'date': '1998-09-21',
            'year': 1998,
            'month': 9,
            'category': 'Hurricane',
            'severity': 'Category 3',
            'estimated_deaths': None,
            'economic_damage_billions_usd': 3.5,
            'homes_destroyed': 28000,
            'homes_damaged': 72000,
            'power_outage_duration_days': None,
            'notes': 'Major damage across the island. Significant migration impact.',
            'migration_impact': 'High',
            'mainland_destinations': None
        },
        {
            'event_name': 'Hurricane Hugo',
            'date': '1989-09-18',
            'year': 1989,
            'month': 9,
            'category': 'Hurricane',
            'severity': 'Category 3',
            'estimated_deaths': None,
            'economic_damage_billions_usd': 2,
            'homes_destroyed': None,
            'homes_damaged': None,
            'power_outage_duration_days': None,
            'notes': 'Severe damage to infrastructure and agriculture.',
            'migration_impact': 'Medium',
            'mainland_destinations': None
        },
        {
            'event_name': 'Puerto Rico Economic Crisis',
            'date': '2006-01-01',
            'year': 2006,
            'month': 1,
            'category': 'Economic',
            'severity': 'Crisis',
            'estimated_deaths': None,
            'economic_damage_billions_usd': None,
            'homes_destroyed': None,
            'homes_damaged': None,
            'power_outage_duration_days': None,
            'notes': 'Beginning of economic recession. Peak unemployment in 2010-2012. Debt crisis 2014-2016.',
            'migration_impact': 'Very High',
            'mainland_destinations': None
        },
        {
            'event_name': 'Puerto Rico Debt Crisis',
            'date': '2014-01-01',
            'year': 2014,
            'month': 1,
            'category': 'Economic',
            'severity': 'Crisis',
            'estimated_deaths': None,
            'economic_damage_billions_usd': None,
            'homes_destroyed': None,
            'homes_damaged': None,
            'power_outage_duration_days': None,
            'notes': 'Debt default, austerity measures, government services cut. Accelerated migration.',
            'migration_impact': 'Very High',
            'mainland_destinations': None
        },
        {
            'event_name': '2020 Earthquakes',
            'date': '2020-01-07',
            'year': 2020,
            'month': 1,
            'category': 'Earthquake',
            'severity': 'Magnitude 6.4',
            'estimated_deaths': None,
            'economic_damage_billions_usd': None,
            'homes_destroyed': None,
            'homes_damaged': None,
            'power_outage_duration_days': None,
            'notes': 'Series of earthquakes in January 2020, largest M6.4. Power outages.',
            'migration_impact': 'Low',
            'mainland_destinations': None
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(template_data)
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    
    print(f"Created hurricane/disaster timeline template at: {output_file}")
    print("\nThis is a template file. Please research and fill in missing data.")
    print("Sources to check:")
    print("- NOAA National Hurricane Center: https://www.nhc.noaa.gov/")
    print("- FEMA disaster declarations")
    print("- Puerto Rico government reports")
    print("- Academic studies on migration patterns")
    print("- Census Bureau migration data (correlate with disaster dates)")
    print("\nConsider adding:")
    print("- Precise dates and durations")
    print("- Detailed migration data by destination state")
    print("- Economic indicators (unemployment, GDP impact)")
    print("- Recovery timeline")
    print("- Additional events (hurricanes, floods, droughts, etc.)")
    
    return output_file

if __name__ == "__main__":
    create_hurricane_timeline_template()

