import numpy as np
import tensorflow as tf
print(tf.__version__)
import cv2
import time
import PIL.Image as Image
import matplotlib. pyplot as plt
import paho.mqtt.client as mqtt
import logging
import base64
import json

## GUI #######################################################################################################################

# Import required libraries
import pickle
import copy
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html


#global GUI variable
latl = []
lonl = []

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s')



broker="mqtt"

#port
port=1883


# load in the submodel
IMSHOW_SIZE = (700, 500)
IMAGE_SHAPE = (224, 224)
class_names = ['litter','non-litter']
model = tf.keras.models.load_model('/1585347752second')



def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc), flush=True)
	client.subscribe("/data")


def on_message(client, userdata, message):
    tempString = str(message.payload.decode("utf-8"))
    y = json.loads(tempString)
    latl.append(y["Latitude"])
    lonl.append(y["Longitude"])
    #print("message received", flush=True)
    # print('intermediate result:', tempString, flush=True)
    IntermediateResult = np.array(y["IntermediateResult"])
    print('size of intermediate result', IntermediateResult.shape, flush=True)
    result = model.predict(IntermediateResult)
    predicted_id = np.argmax(result, axis=-1)
    print('predicted_i:', predicted_id, flush=True)
    if predicted_id == 0:
        print("litter detected!", flush=True)
    else:
        print("no litter detected", flush=True)

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

# Create global chart template
mapbox_access_token = "pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w"

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-78.05, lat=42.54),
        zoom=7,
    ),
)


# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                dcc.Interval(
                    id='interval-component',
                    interval=1 * 1000000,  # in milliseconds
                    n_intervals=0
                ),
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dash-logo.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "New York Oil and Gas",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Production Overview", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),

        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="main_graph")],
                    className="pretty_container seven columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

# Create callbacks
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
)

# Selectors -> main graph
@app.callback(
    Output("main_graph", "figure"),
    [
        Input('interval-component', 'n_intervals')
    ],
    [ State("main_graph", "relayoutData")],
)
def make_main_figure(
     mainContainer, main_graph_layout
):

#    dff = filter_dataframe(df, well_types, year_slider)

    traces = []


    print("lan en lon test:")
    print(len(latl))
    #for well_type, dff in df.groupby("Well_Type"):
    trace = dict(
        type="scattermapbox",
        lat=latl,
        lon=lonl,
        text= "test",
            #customdata=dff["API_WellNo"],
            #name=WELL_TYPES[well_type],
        marker=dict(size=12, opacity=0.6),
        )
    traces.append(trace)

    # relayoutData is None by default, and {'autosize': True} without relayout action
    if main_graph_layout is not None:
        if "mapbox.center" in main_graph_layout.keys():
            lon = float(main_graph_layout["mapbox.center"]["lon"])
            lat = float(main_graph_layout["mapbox.center"]["lat"])
            zoom = float(main_graph_layout["mapbox.zoom"])
            layout["mapbox"]["center"]["lon"] = lon
            layout["mapbox"]["center"]["lat"] = lat
            layout["mapbox"]["zoom"] = zoom

    figure = dict(data=traces, layout=layout)
    return figure


###########################################################################################################################################





#start of our main loop --------------------------------------------------------------------------------------------

if __name__ == "__main__":

    broker_address = "mqtt"
    # broker_address="iot.eclipse.org"
    print("creating new instance", flush=True)
    client = mqtt.Client("P1")  # create new instance
    client.on_message = on_message  # attach function to callback
    print("connecting to broker", flush=True)
    client.connect(broker_address)  # connect to broker
    client.subscribe("/data")
    client.loop_start()  # start the loop
    print("Subscribing to topic", "/data", flush=True)
    # app.run_server(host= '0.0.0.0',debug=True, port=8050)
    while True:
        time.sleep(1)







