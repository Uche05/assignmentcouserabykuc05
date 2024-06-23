import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output

# Load SpaceX launch data
spacex_df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv')

# Create a Dash application
app = dash.Dash(__name__)

# TASK 1: Add a Launch Site Drop-down Input Component
site_options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]

site_dropdown = dcc.Dropdown(id='site-dropdown', 
                             options=site_options,
                             value='ALL',
                             placeholder='Select a Launch Site here',
                             searchable=True)

# TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def render_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Success Counts for All Launch Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, values='class', names='class', title=f'Success Counts for {entered_site}')
    return fig

# TASK 3: Add a Range Slider to Select Payload
payload_slider = dcc.RangeSlider(id='payload-slider',
                                 min=0, max=10000, step=1000,
                                 marks={i: str(i) for i in range(0, 10001, 1000)},
                                 value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()])

# TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def render_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version', 
                         title='Payload Success Rate for All Sites', 
                         labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Outcome'})
    else:
        filtered_site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_site_df, x='Payload Mass (kg)', y='class', color='Booster Version', 
                         title=f'Payload Success Rate for {entered_site}', 
                         labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Outcome'})
        
    fig.update_layout(yaxis=dict(tickvals=[0, 1], ticktext=['Failure', 'Success']))
    return fig

# Define the layout of the application
app.layout = html.Div([
    html.H1("SpaceX Launch Data Analysis"),
    
    html.Div([
        html.Div([site_dropdown], className='six columns'),
        html.Div([payload_slider], className='six columns'),
    ], className='row'),
    
    html.Div([
        html.Div([dcc.Graph(id='success-pie-chart')], className='six columns'),
        html.Div([dcc.Graph(id='success-payload-scatter-chart')], className='six columns'),
    ], className='row'),
])

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)
