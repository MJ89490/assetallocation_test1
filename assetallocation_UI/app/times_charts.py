import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json


def create_plot():

    # N = 1000
    # x = np.random.randn(N)
    # y = np.random.randn(N)
    # df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
    #
    # trace = go.Scatter(
    #     x=x,
    #     y=y,
    #     mode='markers'
    # )
    # data = [trace]
    # data = [
    #     go.Bar(
    #         x=df['x'], # assign x as the dataframe column 'x'
    #         y=df['y']
    #     )
    # ]

    N = 100
    random_x = np.linspace(0, 1, N)
    random_y0 = np.random.randn(N) + 5
    random_y1 = np.random.randn(N)
    random_y2 = np.random.randn(N) - 5

    # Create traces
    trace0 = go.Scatter(
        x=random_x,
        y=random_y0,
        mode='markers',
        name='markers'
    )
    trace1 = go.Scatter(
        x=random_x,
        y=random_y1,
        mode='lines+markers',
        name='lines+markers'
    )
    trace2 = go.Scatter(
        x=random_x,
        y=random_y2,
        mode='lines',
        name='lines'
    )

    data = [trace0, trace1, trace2]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON