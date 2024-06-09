from textwrap import dedent
import dash
from dash import dcc
from dash import html
import dash_player as player
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pathlib
import base64
import os
import subprocess
import plotly.express as px
import matplotlib.pyplot as plt
import cv2
import plotly.graph_objects as go
import plotly.express as px
import datetime

class AppState:
    def __init__(self):
        self.video_name=None
        self.log_name=None
        self.frame_list= self.get_frame_list()
        self.current_frame=0

    def get_frame_list(self):
        flist=os.listdir('./vimages')
        flist=sorted(flist,key=lambda x: int(x[3:7]))
        flist=[os.path.join('./vimages',x) for x in flist]
        return flist
    
    def get_frame(self):
        print(self.frame_list[self.current_frame])
        img=cv2.imread(self.frame_list[self.current_frame])
        im=cv2.resize(img, (640, 480), 
               interpolation = cv2.INTER_LINEAR)
        #im=img.copy()
        canvas=np.zeros((im.shape[0]*2,im.shape[1],3),dtype=np.uint8)
        canvas[:im.shape[0],:im.shape[1]]=im
        canvas[im.shape[0]:,:im.shape[1]]=im
        #cv2.imwrite('./assets/test.png',canvas)
        
        fig = go.Figure(go.Image(z=canvas[:,:,::-1]))
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="LightSteelBlue",
        )
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        
        
        return fig
    
    def next_frame(self):
        self.current_frame+=1
        print(self.current_frame)
        return self.current_frame
    
    
        

astate=AppState()

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Object Detection Explorer"
server = app.server
app.config.suppress_callback_exceptions = True

fig=astate.get_frame()
n_frames=len(astate.frame_list)
#astate.next_frame()
#astate.next_frame()







app.layout = html.Div(
    children=[
        #dcc.Interval(id="interval-updating-graphs", interval=1000, n_intervals=0),
        html.Div(id="top-bar", className="row"),
        html.Div(
            className="container",
            children=[
                html.Div(
                    id="left-side-column",
                    className="eight columns",
                    children=[
                        html.Img(
                            id="logo-mobile", src=app.get_asset_url("dash-logo.png")
                        ),
                        html.Div(
                            id="header-section",
                            children=[
                                html.H4("Object Detection Explorer"),
                                
                                html.Button(
                                    "Prev", id="prev-button", n_clicks=0
                                ),
                                html.Button(
                                    "Next", id="next-button", n_clicks=0
                                ),
                                dcc.Slider(0, 5000, 1,
                                        value=10,
                                        id='my-slider'
                                ),
                            ],
                        ),
                        
                        html.Div(
                            className="video-outer-container",
                            
                            children=html.Div(
                                className="video-container",
                                style={"width": "100%","height":"500px"},
                                #children=player.DashPlayer(
                                #    id="video-display",
                                #    url="https://www.youtube.com/watch?v=gPtn6hD7o8g",
                                #    controls=True,
                                #    playing=False,
                                #    volume=1,
                                #    width="100%",
                                #    height="100%",
                                #),
                                children=[
                                    dcc.Graph(
                                        id='stacker-graph',
                                        figure=fig,
                                        style={"width": "100%","height":"100%"},
                                        
                                    ), 
                                    #html.Img(id="im-id", src=app.get_asset_url("test.png"),style={"width": "100%","height":"500px"}, ),
                                    

                                ],

                                #children=html.Img(src=r'test.jpg', alt='image'),
                            ),
                        ),
                        html.Div(
                            className="control-section",
                            children=[
                                html.Div(
                                    className="control-element",
                                    children=[
                                        html.Div(
                                            children=["Minimum Confidence Threshold:"]
                                        ),
                                        html.Div(
                                            dcc.Slider(
                                                id="slider-minimum-confidence-threshold",
                                                min=20,
                                                max=80,
                                                marks={
                                                    i: f"{i}%"
                                                    for i in range(20, 81, 10)
                                                },
                                                value=30,
                                                updatemode="drag",
                                            )
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="control-element",
                                    children=[
                                    ],
                                ),
                                html.Div(
                                    className="control-element",
                                    children=[

                                    ],
                                ),
                                html.Div(
                                    className="control-element",
                                    children=[
                                        
                                    ],
                                ),
                            ],
                        ),
                        html.H2(id='fl1',children="File List")
                    ],
                    
                ),
                html.Div(
                    id="right-side-column",
                    className="four columns",
                    children=[
                        html.Div(
                            className="img-container",
                            children=html.Img(
                                id="logo-web", src=app.get_asset_url("dash-logo.png")
                            ),
                        ),
                        html.Div(id="div-visual-mode"),
                        html.Div(id="div-detection-mode"),
                    ],
                ),
            ],
        ),
        
    ]
)

def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    if name[-3:]=='jpg':
        name='test.jpg'
    if name[-3:]=='mp4':
        name='test.mp4'
    with open(os.path.join('D:/Projects/gradio', name), "wb") as fp:
        fp.write(base64.decodebytes(data))
    return name

def process_file(name):
    if name[-3:]=='mp4':
        if not os.path.isdir('vimages'):
            os.mkdir('vimages')
        subprocess.run(['ffmpeg','-i',f'{name}','-vf','fps=8','vimages/out%4d.jpg'])

    
@app.callback(
        Output("stacker-graph", "figure"),
        Input("next-button", "n_clicks"),              
)
def update_graph(nclick):
    print ('n-',nclick)
    ts=datetime.datetime.now()
    fig1=astate.get_frame()
    astate.next_frame()
    print('tt',datetime.datetime.now()-ts)
    return fig1
#
#@app.callback(
#        Output('container-button-basic', 'children'),
#        Input('interval-updating-graphs','n_intervals'))
#def icall(interv):
#    
#    print('interv')
#    return 'The input value was "" and the button has been clicked {} times'.format(
#        interv,
#        
#    )
#

# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8053)