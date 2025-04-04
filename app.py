import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
print("Loading data...")
df = pd.read_excel("FringeDataCombined.xlsx")

# Clean and prepare the data
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df = df.dropna(subset=['Latitude', 'Longitude', 'Year'])

# Convert accessibility levels to numeric for consistent sorting (assuming higher is better)
# Map accessibility levels to traffic light colors
def map_access_to_color(access_level):
    # Inspect the type of access_level values
    if isinstance(access_level, (int, float)):
        if access_level <= 1:
            return "red"
        elif access_level == 2:
            return "orange"
        else:
            return "green"
    else:  # Handle string or other types
        access_str = str(access_level).lower()
        if "low" in access_str or "poor" in access_str or "1" in access_str:
            return "red"
        elif "medium" in access_str or "partial" in access_str or "2" in access_str:
            return "orange"
        else:
            return "green"

# Add a color column based on accessibility level
df['access_color'] = df['Accessibility level'].apply(map_access_to_color)

# Create options for dropdowns
venue_options = [{'label': v, 'value': v} for v in sorted(df['Venue address'].unique())]
# Convert all accessibility levels to strings for display
accessibility_options = sorted([{'label': str(lvl), 'value': lvl} for lvl in df['Accessibility level'].unique()], 
                                key=lambda x: str(x['label']))
year_options = [{'label': str(int(y)), 'value': int(y)} for y in sorted(df['Year'].unique())]

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Edinburgh Fringe Accessibility"

# Define the layout with a clean, modern design
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Edinburgh Fringe Festival Venue Accessibility Dashboard",
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '10px'}),
        html.P("Explore venue accessibility using the traffic light system: Green (High), Orange (Medium), Red (Low)",
               style={'textAlign': 'center', 'color': '#7f8c8d', 'marginBottom': '20px'})
    ], style={'padding': '15px'}),

    # Filters section
    html.Div([
        # Year filter
        html.Div([
            html.Label("Select Year(s):", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='year_dropdown',
                options=year_options,
                multi=True,
                placeholder="Select year(s)..."
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '20px'}),

        # Venue filter
        html.Div([
            html.Label("Select Venue(s):", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='venue_dropdown',
                options=venue_options,
                multi=True,
                placeholder="Select venue(s)..."
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '20px'}),

        # Accessibility filter
        html.Div([
            html.Label("Filter by Accessibility:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='accessibility_dropdown',
                options=accessibility_options,
                multi=True,
                placeholder="Select accessibility level(s)..."
            )
        ], style={'width': '30%', 'display': 'inline-block'})
    ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px', 'marginBottom': '20px'}),

    # Stats summary
    html.Div([
        html.Div(id='venue_count', style={'textAlign': 'center', 'fontSize': '18px'})
    ], style={'padding': '10px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px', 'marginBottom': '20px'}),

    # Map
    html.Div([
        dcc.Graph(id='map_figure')
    ], style={'padding': '20px'})

], style={'fontFamily': 'Arial, sans-serif', 'margin': '0 auto', 'maxWidth': '1200px'})

@app.callback(
    [Output('map_figure', 'figure'),
     Output('venue_count', 'children')],
    [
        Input('venue_dropdown', 'value'),
        Input('accessibility_dropdown', 'value'),
        Input('year_dropdown', 'value')
    ]
)
def update_map(selected_venues, selected_accessibility, selected_years):
    # Make a copy of the original dataframe
    dff = df.copy()

    # Apply filters
    if selected_venues:
        dff = dff[dff['Venue address'].isin(selected_venues)]
    if selected_accessibility:
        dff = dff[dff['Accessibility level'].isin(selected_accessibility)]
    if selected_years:
        dff = dff[dff['Year'].isin(selected_years)]
    
    # Count venues by accessibility level for stats
    venue_counts = dff.groupby('access_color')['Venue address'].nunique().to_dict()
    green_count = venue_counts.get('green', 0)
    orange_count = venue_counts.get('orange', 0)
    red_count = venue_counts.get('red', 0)
    total_venues = dff['Venue address'].nunique()
    
    # Define custom marker colors based on accessibility level
    color_map = {
        'red': '#FF0000',     # Red for low accessibility
        'orange': '#FFA500',  # Orange/Yellow for medium accessibility
        'green': '#00FF00'    # Green for high accessibility
    }
    
    # Create the map with custom markers
    fig = go.Figure()
    
    # Add a scatter mapbox trace for each accessibility level to control colors
    for color in ['green', 'orange', 'red']:
        color_df = dff[dff['access_color'] == color]
        if not color_df.empty:
            fig.add_trace(go.Scattermapbox(
                lat=color_df['Latitude'],
                lon=color_df['Longitude'],
                mode='markers',
                marker=dict(
                    size=12,
                    color=color_map[color],
                    opacity=0.8
                ),
                text=color_df.apply(
                    lambda row: (
                        f"<b>{row['Venue address']}</b><br>"
                        f"Year: {int(row['Year'])}<br>"
                        f"Performances: {row['Performances #']}<br>"
                        f"Accessibility Level: {row['Accessibility level']}<br>"
                        f"Details: { (str(row['Venue accessibility'])[:100] + '...') if len(str(row['Venue accessibility'])) > 100 else str(row['Venue accessibility']) }"
                    ),
                    axis=1
                ),
                hoverinfo='text',
                name=f"{color.capitalize()} Accessibility"
            ))
    
    # Update the map layout
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(
            center=dict(lat=55.9533, lon=-3.1883),  # Edinburgh center
            zoom=12
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(255,255,255,0.8)',
            title="Accessibility Level"
        ),
        height=600
    )
    
    # Create stats summary
    stats = html.Div([
        html.Span(f"Total Venues: {total_venues} | ", style={'fontWeight': 'bold'}),
        html.Span("High Accessibility: ", style={'fontWeight': 'bold'}),
        html.Span(f"{green_count}", style={'color': 'green', 'fontWeight': 'bold'}),
        html.Span(" | Medium Accessibility: ", style={'fontWeight': 'bold'}),
        html.Span(f"{orange_count}", style={'color': 'orange', 'fontWeight': 'bold'}),
        html.Span(" | Low Accessibility: ", style={'fontWeight': 'bold'}),
        html.Span(f"{red_count}", style={'color': 'red', 'fontWeight': 'bold'})
    ])

    return fig, stats

if __name__ == '__main__':
    print("Starting server...")
    app.run_server(debug=True) 