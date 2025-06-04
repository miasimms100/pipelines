# Import packages
import pandas as pd
from datetime import datetime, date
from pprint import pprint
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

daily_dataframe = pd.read_csv('daily_weather_data.csv')
#['date', 'temperature_2m_max', 'temperature_2m_min', 'sunrise', 'sunset','uv_index_max', 'uv_index_clear_sky_max', 'cloud_cover_mean','precipitation_probability_mean', 'relative_humidity_2m_mean','wind_speed_10m_mean', 'precipitation_hours', 'weekday','rain_prob_rank', 'num_rain_hrs_rank', 'uv_max_rank','uv_clear_sky_rank', 'cloud_cover_rank', 'humidity_rank','max_temp_rank', 'min_temp_rank', 'weekend_preference_rank','wind_speed_rank', 'best_day_rank','best_day_rank_with_weekend_preference']
current_dataframe = pd.read_csv('current_weather_data.csv')
# ['date', 'temperature_2m_max', 'temperature_2m_min', 'sunrise', 'sunset','uv_index_max', 'uv_index_clear_sky_max', 'cloud_cover_mean','precipitation_probability_mean', 'relative_humidity_2m_mean','wind_speed_10m_mean', 'precipitation_hours', 'weekday','rain_prob_rank', 'num_rain_hrs_rank', 'uv_max_rank','uv_clear_sky_rank', 'cloud_cover_rank', 'humidity_rank','max_temp_rank', 'min_temp_rank', 'weekend_preference_rank','wind_speed_rank', 'best_day_rank','best_day_rank_with_weekend_preference']
tourism_data = pd.read_csv('tourism.csv')
#['Place name', 'Address', 'Phone', 'website', 'is_indoor','water', 'play_sweat_it_out', 'small_kid_friendly_under_10','big_kid_friendly_over_10', 'culture', 'nature', 'adult_only']

def convert_to_weekday(date_obj):
    """Convert a date string to a weekday name."""
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return weekdays[date_obj.weekday()]

daily_dataframe['date'] = daily_dataframe['date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S+00:00").date())
daily_dataframe['weekday'] = daily_dataframe['date'].apply(convert_to_weekday)
daily_dataframe = daily_dataframe.fillna(0)
daily_dataframe['rain_prob_rank'] = daily_dataframe['precipitation_probability_mean'].rank(method='min', ascending=False)
daily_dataframe['num_rain_hrs_rank'] = daily_dataframe['precipitation_hours'].rank(method='min', ascending=False)
daily_dataframe['uv_max_rank'] = daily_dataframe['uv_index_max'].rank(method='min', ascending=False)
daily_dataframe['uv_clear_sky_rank'] = daily_dataframe['uv_index_clear_sky_max'].rank(method='min', ascending=False)
daily_dataframe['cloud_cover_rank'] = daily_dataframe['cloud_cover_mean'].rank(method='min', ascending=False)
daily_dataframe['humidity_rank'] = daily_dataframe['relative_humidity_2m_mean'].rank(method='min', ascending=False)
daily_dataframe['max_temp_rank'] = daily_dataframe['temperature_2m_max'].rank(method='min')
daily_dataframe['min_temp_rank'] = daily_dataframe['temperature_2m_min'].rank(method='min')
daily_dataframe['weekend_preference_rank'] = daily_dataframe['date'].apply(lambda x : x.weekday())
daily_dataframe['wind_speed_rank'] = daily_dataframe['wind_speed_10m_mean'].rank(method='min', ascending=False)
daily_dataframe['best_day_rank'] = daily_dataframe.apply(lambda row: row['rain_prob_rank'] + row['num_rain_hrs_rank'] +row['uv_max_rank'] + row['uv_clear_sky_rank'] +row['cloud_cover_rank'] + row['humidity_rank'] +row['max_temp_rank'] + row['min_temp_rank'] + row['wind_speed_rank'], axis=1)
daily_dataframe['best_day_rank_with_weekend_preference'] = daily_dataframe.apply(lambda row: row['rain_prob_rank'] + row['num_rain_hrs_rank'] +row['uv_max_rank'] + row['uv_clear_sky_rank'] +row['cloud_cover_rank'] + row['humidity_rank'] +row['max_temp_rank'] + row['min_temp_rank'] + row['wind_speed_rank'] + row['weekend_preference_rank'], axis=1)
daily_dataframe['sunrise'] = daily_dataframe['sunrise'].apply(lambda x :  (datetime.fromtimestamp(x)).time())
daily_dataframe['sunset'] = daily_dataframe['sunset'].apply(lambda x :  (datetime.fromtimestamp(x)).time())

best_day_sort=daily_dataframe.sort_values(by = "best_day_rank", ascending=True) 

# Extracting the warmest and coolest days
best_outdoor_date = best_day_sort.iloc[15]['date']
best_indoor_date = best_day_sort.iloc[0]['date']

# print(f"Best Outdoor Day: {best_outdoor_date}")
# print(f"Best Indoor Day: {best_indoor_date}")

date_range_dropDown = daily_dataframe['date'].tolist()
line_graph_column_list = ['temperature_2m_max', 'temperature_2m_min']

best_outdoor_date_card_content = [
    dbc.CardHeader("Best Outdoor Activity Day"),
    dbc.CardBody(
        [
            html.H5(f"{best_day_sort.iloc[15]['weekday']}, {best_day_sort.iloc[15]['date']}", className="card-title"),
            html.P(
                f"Temperature: {best_day_sort.iloc[15]['temperature_2m_max']}°F ", 
                className="card-text",
                ),
            html.P(
                f"Rain Probability is: {best_day_sort.iloc[6]['precipitation_probability_mean']}%", 
                className="card-text",
                ),
            html.P(
                f"Cloud Coverage is: {best_day_sort.iloc[6]['cloud_cover_rank']}", 
                className="card-text",
                ),
            html.P(
                f"Humidity is: {best_day_sort.iloc[6]['relative_humidity_2m_mean']}", 
                className="card-text",
                ),
        ]
    ),
]
best_indoor_date_card_content = [
    dbc.CardHeader("Best Indoor Activity Day"),
    dbc.CardBody(
        [
            html.H5(f"{best_day_sort.iloc[0]['weekday']}, {best_day_sort.iloc[0]['date']}", className="card-title"),
            html.P(
                f"Temperature: {best_day_sort.iloc[15]['temperature_2m_max']}°F ", 
                className="card-text",
                ),
            html.P(
                f"Rain Probability is: {best_day_sort.iloc[6]['precipitation_probability_mean']}%", 
                className="card-text",
                ),
            html.P(
                f"Cloud Coverage is: {best_day_sort.iloc[6]['cloud_cover_rank']}", 
                className="card-text",
                ),
            html.P(
                f"Humidity is: {best_day_sort.iloc[6]['relative_humidity_2m_mean']}", 
                className="card-text",
                ),
        ]
    ),
]

fig = px.line(daily_dataframe, x='date', y='temperature_2m_max', title='Your Graph Title')
# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CYBORG]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.H2('Visit the Ville: Planning Dashboard', className="text-primary text-center")
    ]),
    dbc.Row([
        dbc.Col([
            html.H2('Days in Town:', className="text-primary text-center fs-3"),
            dcc.Dropdown(
                options=date_range_dropDown,
                multi=True, placeholder='Select Visiting Dates',
                id='date-range-dropdown',
                className='mb-3'),
                ]),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                best_outdoor_date_card_content,
                className="mb-3",
                color="primary",
                style={"width": "18rem"}
            )
        ], width=6),
        dbc.Col([
            dbc.Card(
                best_indoor_date_card_content,
                className="mb-3",
                color="warning",
                style={"width": "18rem"}
            )
        ], width=6)
    ]),
    dbc.Row([html.H6('Places to Visit in the Ville:', className="text-primary text-center fs-3")
    ]),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                data=tourism_data.to_dict('records'), 
                hidden_columns=['is_indoor', 'water', 'play_sweat_it_out', 'small_kid_friendly_under_10','big_kid_friendly_over_10', 'culture', 'nature', 'adult_only'], 
                page_size=5, style_table={'overflowX': 'auto'})
        ], width=12),
    ]),
    dbc.Row([
        html.H6('Weather Data Visualization:', className="text-primary text-center fs-3"),
        dbc.Col([
            dcc.Graph(id="graph", figure=fig),
            dcc.Checklist(id="checklist",
                          options=line_graph_column_list,
                          value=['temperature_2m_max', 'temperature_2m_min'],
                          inline=True),
                          ])
        ]),
    ], fluid=True)

# Add controls to build the interaction
@callback(
    Output(component_id='my-first-graph-final', component_property='figure'),
    Input(component_id='radio-buttons-final', component_property='value'),
)
@app.callback(
    Output("graph", "figure"),
    Input("checklist", "value"))


def update_graph(col_chosen):
    fig = px.histogram(daily_dataframe, x='date', y=col_chosen, title='Temperature for the week',  histfunc='avg')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8051)
