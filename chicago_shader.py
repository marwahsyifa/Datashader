import pandas as pd
import datashader as ds
import datashader.transfer_functions as tf
from colorcet import kbc
import plotly.express as px
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Kel_Delapan'

# Read and filter your dataframe
df = pd.read_csv("Crimes_-_2001_to_Present.csv")
dff = df[['Primary Type', 'Latitude', 'Longitude']]
print(dff['Primary Type'].unique())
dff = dff[dff['Primary Type'].isin(['ROBBERY'])]
dff.dropna(subset=['Latitude', 'Longitude'], inplace=True)
print(dff.shape)


# Create a quick mapbox figure with plotly
fig = px.scatter_mapbox(dff[:1], lat='Latitude', lon='Longitude', zoom=10)


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Data Kasus Perampokan di Kota Chicago",
                    style={'textAlign': 'center'}),
            html.A(
                "Data ini di ambil dari Chicago Data Portal yang menyajikan 24 juta laporan kasus kejahatan di kota Chicago dari tahun 2001 - 2022. Beberapa kasus yang telah dilaporkan diantaranya: perampokan; pencurian; penyerangan; prostitusi; dan narkotika. Halaman ini menampilkan visualisasi data kasus perampokan yang terjadi di kota Chicago berbentuk peta beserta titik koordinat kejadian, sehingga dapat menjadi pengetahuan bagi semua orang untuk berhati-hati ketika berada dalam daerah-daerah rawan tersebut.", style={'textAlign': 'center'})
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='our-plot', figure=fig)
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.H1("Document Libraries We Use", style={'textAlign': 'center',
                                                          'textSize': '14px'}),
            html.Div([
                dbc.ListGroup(
                    [
                        dbc.ListGroupItem("Dash", href="https://dash.plotly.com/holoviews",
                                          color="dark", style={'textAlign': 'center'}),
                        dbc.ListGroupItem("Plotly Expres", href="https://plotly.com/python/plotly-express/",
                                          color="dark", style={'textAlign': 'center'}),
                        dbc.ListGroupItem("Pandas", href="https://pandas.pydata.org/",
                                          color="dark", style={'textAlign': 'center'}),
                        dbc.ListGroupItem("Datashader", href="https://datashader.org/",
                                          color="dark", style={'textAlign': 'center'}),
                        dbc.ListGroupItem("Colorcet", href="https://pypi.org/project/colorcet/",
                                          color="dark", style={'textAlign': 'center'}),
                        dbc.ListGroupItem("dash_bootstrap_components", href="https://dash-bootstrap-components.opensource.faculty.ai/docs/components/list_group/",
                                          color="dark", style={'textAlign': 'center'}),
                        dbc.ListGroupItem("Crimes_-_2001_to_Present.csv", href="https://drive.google.com/u/0/uc?id=1Ujywq7OH8xl31h7Uj4SQhZ1RX3hEvpdv&export=download",
                                          color="dark", style={'textAlign': 'center'}),
                    ]
                ),
                html.P(id="counter"),

            ])
        ], width=12)
    ])
])
# Build an abstract canvas representing the space in which to plot data
cvs = ds.Canvas(plot_width=4000, plot_height=4000)

# project the longitude and latitude onto the canvas and
# map the data to pixels as points
aggs = cvs.points(dff, x='Longitude', y='Latitude')
coords_lat, coords_lon = aggs.coords['Latitude'].values, aggs.coords['Longitude'].values

# Set the corners of the image that need to be passed to the mapbox

coordinates = [[coords_lon[0], coords_lat[0]],
               [coords_lon[-1], coords_lat[0]],
               [coords_lon[-1], coords_lat[-1]],
               [coords_lon[0], coords_lat[-1]]]


# Set the image color, and the legend (how) types
# linear (how=linear), logarithmic (how=log), percentile (how=eq_hist)
img = tf.shade(aggs, cmap=kbc, how='eq_hist', alpha=255)[::-1].to_pil()


# Add the datashader image as a mapbox layer image
fig.update_layout(mapbox_style="carto-darkmatter",
                  mapbox_layers=[
                      {
                          "sourcetype": "image",
                          "source": img,
                          "coordinates": coordinates
                      }
                  ]
                  )
if __name__ == "__main__":
    app.run_server(port=5000, host='localhost', debug=True)
