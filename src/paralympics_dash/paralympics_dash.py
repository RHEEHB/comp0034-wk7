# Version after the final activity in week 6
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import requests
from figures import line_chart, bar_gender, scatter_geo

# Variable that contains the external_stylesheet to use, in this case Bootstrap styling from dash bootstrap
# components (dbc)
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Define a variable that contains the meta tags
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Pass the stylesheet variable to the Dash app constructor
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags)

# Variables that define the three rows and their contents
def create_card(event_id):
    """
    Generate a card for the event specified by event_id.

    Uses the REST API route.

    Args:
        event_id:

    Returns:
        card: dash boostrap components card for the event
    """
    # Use python requests to access your REST API on your localhost
    # Make sure you run the REST APP first and check your port number if you changed it from the default 5000
    url = f"http://127.0.0.1:5000/events/{event_id}"
    event_response = requests.get(url)
    ev = event_response.json()

    # Variables for the card contents
    logo = f'logos/{ev['year']}_{ev['host']}.jpg'
    dates = f'{ev['start']} to {ev['end']}'
    host = f'{ev['host']} {ev['year']}'
    highlights = f'Highlights: {ev['highlights']}'
    participants = f'{ev['participants']} athletes'
    events = f'{ev['events']} events'
    countries = f'{ev['countries']} countries'

    card = dbc.Card([
        dbc.CardBody(
            [
                html.H4([html.Img(src=app.get_asset_url(logo), width=35, className="me-1"),
                         host]),
                html.Br(),
                html.H6(dates, className="card-subtitle"),
                html.P(highlights, className="card-text"),
                html.P(participants, className="card-text"),
                html.P(events, className="card-text"),
                html.P(countries, className="card-text"),
            ]
        ),
    ],
        style={"width": "18rem"},
    )
    return card

dropdown = dbc.Select(
    id="type-dropdown",  # id uniquely identifies the element, will be needed later
    options=[
        {"label": "Events", "value": "events"},
        # The value is in the format of the column heading in the data
        {"label": "Sports", "value": "sports"},
        {"label": "Countries", "value": "countries"},
        {"label": "Athletes", "value": "participants"},
    ],
    value="events"  # The default selection
)

checklist = dbc.Checklist(
    options=[
        {"label": "Summer", "value": "summer"},
        {"label": "Winter", "value": "winter"},
    ],
    value=["summer"],  # Values is a list as you can select both winter and summer
    id="checklist-input",
)

line = line_chart("sports")
bar = bar_gender("winter")
map = scatter_geo()
card = create_card(12)
row_one = dbc.Row([
    dbc.Col([
        html.H1("Paralympics Dashboard"), 
        html.P("Use the charts to help answer the questions."),
             ], width=12)
])

row_two = dbc.Row([
    dbc.Col(children=[
        dropdown
    ], width=2),
    dbc.Col(children=[
        checklist,
    ], width={"size": 2, "offset": 4}),
], align="start")

row_three = dbc.Row([
    dbc.Col(children=[
        dcc.Graph(id="line", figure=line)
    ], width=6),
    dbc.Col(children=[
        dcc.Graph(id="bar", figure=bar),
    ], width=6),
], align="start")

row_four = dbc.Row([
    dbc.Col(children=[
        dcc.Graph(id="map", figure=map),
    ], width=8),
    dbc.Col(children=[
        card,
    ], width=4),
], align="start")

# Add an HTML layout to the Dash app.

# The layout is wrapped in a DBC Container()
app.layout = dbc.Container([
    row_one,
    row_two,
    row_three,
    row_four,
])

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
    # Runs on port 8050 by default. If you have a port conflict, add the parameter port=   e.g. port=8051
