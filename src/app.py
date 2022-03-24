import dash
from dash import dcc, html
from dash.dependencies import Input, Output

import plotly.graph_objects as go
import pandas as pd
import folium


app = dash.Dash(__name__)

def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    return fig


app.layout = html.Div([
    html.H3("Live BRT Data"),
    html.Iframe(src="assets/map.html",
                style={"height": "800px", "width": "100%"}),
    dcc.Graph(id='live-update-map', figure=blank_fig()),
    dcc.Interval(
        id='interval-component',
        interval=15*1000, # in milliseconds
        n_intervals=0,
)
])


@app.callback(Output('live-update-map', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_figures(n):
    df = pd.read_csv('output.csv')

    m = folium.Map(location=[-22.957015, -43.451891], zoom_start=12)
    for lat, long in df[['latitude', 'longitude']].values:
        folium.Marker(location=[lat, long]).add_to(m)

    return m.save('assets/map.html')


app.run_server(debug=False)