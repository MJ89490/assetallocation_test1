import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json


def create_plot():
    data = [
        go.Scatter(
            x=[0, 1, 2, 3, 4, 5, 6, 7, 8],
            y=[0, 1, 2, 3, 4, 5, 6, 7, 8]
        )
    ]
    layout = go.Layout(
        autosize=False,
        width=400,
        height=400,
        paper_bgcolor='#7f7f7f',
        plot_bgcolor='#c7c7c7'
    )

    fig = go.Figure(data=data, layout=layout)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

    # N = 10
    # random_x = np.linspace(0, 1, N)
    # random_y0 = np.random.randn(N) + 5
    # random_y1 = np.random.randn(N)
    # random_y2 = np.random.randn(N) - 5
    #
    # # Create traces
    # trace0 = go.Scatter(
    #     x=random_x,
    #     y=random_y0,
    #     mode='markers',
    #     name='markers'
    # )
    # trace1 = go.Scatter(
    #     x=random_x,
    #     y=random_y1,
    #     mode='lines+markers',
    #     name='lines+markers'
    # )
    # trace2 = go.Scatter(
    #     x=random_x,
    #     y=random_y2,
    #     mode='lines',
    #     name='lines'
    # )
    # data = [trace0, trace1, trace2]
    # layout = go.Layout(
    # autosize=False,
    # width=500,
    # height=500,)
    #
    # fig = go.Figure(data=data, layout=layout)
    #
    #
    # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #
    # return graphJSON