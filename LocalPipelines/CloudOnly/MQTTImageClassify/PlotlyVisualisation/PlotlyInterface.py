from threading import Thread

import numpy as np
import time
import logging

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

import redis




#global GUI variable
latl = []
lonl = []
locationID = []

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s')


###########################################################################################################################################

# connect with redis server
r = redis.Redis(host="redis", port=6379, db=0)
redisSubscriber = r.pubsub()
# subscribe to classical music
redisSubscriber.subscribe('mqtt_data')

def subscriber():
    while True:
        message = redisSubscriber.get_message()
        if message:
            StringReceived = str(message['data'])
            print("stringreceived: "+StringReceived, flush=True)
            if len(StringReceived) > 1:

                StringList = (StringReceived.strip("'")).split(",")
                print("latitude: ", flush=True)
                latituderec = round(float(StringList[1]),6)
                longituderec = round(float(StringList[2]),6)
                if latituderec in latl:
                    indices = [i for i, x in enumerate(latl) if x == latituderec]
                    print("already in it lat!", flush=True)
                    for index in indices:
                        if lonl[index] == longituderec:
                            print("already in it long!", flush=True)
                            print("langl", flush=True)
                            print(latl,flush=True)
                            print("long", flush=True)
                            print(lonl, flush=True)
                else:
                    latl.append(latituderec)
                    lonl.append(longituderec)







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
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Detected litter",
    height=800,
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=4.320352, lat=51.065772),
        zoom=4,
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

                html.H1(
                    "Detected litter: Cloud vs Edge",
                    style={"margin-bottom": "0px", "automargin":"True"},
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),

        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="main_graph"),                 dcc.Interval(
                    id='interval-component',
                    interval=1 * 500,  # in milliseconds
                    n_intervals=0
                )],
                    className="pretty_container twelve columns",

                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

## Create callbacks
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

    traces = []


    print("lan en lon test:", flush=True)
    print(latl, flush=True)
    print(lonl, flush=True)
    # for i in range(0, len(latl)):
    trace = dict(
            type="scattermapbox",
            lat=latl,
            lon= lonl,
            text= locationID,
            marker=dict(size=12, opacity=0.6),
            )
    traces.append(trace)
    print(traces, flush=True)
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





#start of our main loop --------------------------------------------------------------------------------------------

if __name__ == "__main__":

    check_messages = Thread(target=subscriber, daemon=True)
    check_messages.start()
    app.run_server(host= '0.0.0.0',debug=True, port=8050)
