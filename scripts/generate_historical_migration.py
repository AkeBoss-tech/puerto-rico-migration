import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

def generate_historical_migration():
    """
    Generate interactive graph for Puerto Rican Migration to New York City (1941-1956)
    Based on data from: New York City Department of City Planning Bulletin (1957)
    """
    
    # Data from Table 1: Puerto Rican Migration to New York City, 1941 - 1956
    data = {
        'Year': [1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 
                 1951, 1952, 1953, 1954, 1955, 1956],
        'Net_Out_Migration_PR': [643, 1679, 3204, 11201, 13573, 39911, 24551, 
                                  32775, 25698, 34703, 52899, 59103, 69124, 21531, 
                                  45464, 52315],
        'Net_Migration_NYC': [600, 1600, 3000, 10600, 12900, 37900, 23300, 
                              29500, 23100, 29500, 42300, 45500, 51800, 16100, 
                              31600, 33900],
        'NYC_Percent_Total': [95, 95, 95, 95, 95, 95, 95, 90, 90, 85, 80, 77, 75, 75, 70, 65]
    }
    
    df = pd.DataFrame(data)
    
    # Create a figure with secondary y-axis
    fig = go.Figure()
    
    # Add Net Out-Migration from Puerto Rico (bar chart)
    fig.add_trace(go.Bar(
        x=df['Year'],
        y=df['Net_Out_Migration_PR'],
        name='Net Out-Migration from Puerto Rico',
        marker_color='#e74c3c',
        opacity=0.7,
        yaxis='y'
    ))
    
    # Add Net Migration to NYC (line chart)
    fig.add_trace(go.Scatter(
        x=df['Year'],
        y=df['Net_Migration_NYC'],
        mode='lines+markers',
        name='Net Migration to New York City',
        line=dict(color='#3498db', width=3),
        marker=dict(size=8, color='#3498db'),
        yaxis='y'
    ))
    
    # Add NYC as Percent of Total (secondary y-axis, line chart)
    fig.add_trace(go.Scatter(
        x=df['Year'],
        y=df['NYC_Percent_Total'],
        mode='lines+markers',
        name='NYC as % of Total Migration',
        line=dict(color='#2ecc71', width=3, dash='dash'),
        marker=dict(size=8, color='#2ecc71'),
        yaxis='y2'
    ))
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Puerto Rican Migration to New York City, 1941-1956',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis=dict(
            title='Year',
            tickmode='linear',
            tick0=1941,
            dtick=2
        ),
        yaxis=dict(
            title='Number of Migrants',
            side='left',
            range=[0, max(df['Net_Out_Migration_PR'].max(), df['Net_Migration_NYC'].max()) * 1.1]
        ),
        yaxis2=dict(
            title='Percentage (%)',
            overlaying='y',
            side='right',
            range=[0, 100]
        ),
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='rgba(0, 0, 0, 0.2)',
            borderwidth=1
        ),
        annotations=[
            dict(
                text='Source: New York City Department of City Planning, Welfare and Health Council to New York City, Puerto Rico Planning Board (1957)',
                xref='paper',
                yref='paper',
                x=0.5,
                y=-0.15,
                showarrow=False,
                font=dict(size=10, color='gray')
            )
        ],
        margin=dict(b=80)
    )
    
    # Save to HTML
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'graph10_historical_migration.html')
    
    fig.write_html(output_file, include_plotlyjs='cdn', full_html=False)
    print(f"Historical migration graph saved to {output_file}")

if __name__ == "__main__":
    generate_historical_migration()

