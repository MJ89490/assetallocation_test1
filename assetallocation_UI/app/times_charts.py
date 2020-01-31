import plotly.graph_objs as go
import json
import plotly

def chart_performance():

    long_dates=[ '01 October 2019'
                ,'02 October 2019'
                ,'03 October 2019'
                ,'04 October 2019'
                ,'07 October 2019'
                ,'08 October 2019'
                ,'09 October 2019'
                ,'10 October 2019'
                ,'11 October 2019'
                ,'14 October 2019'
                ,'15 October 2019'
                ,'16 October 2019'
                ,'17 October 2019'
                ,'18 October 2019'
                ,'21 October 2019'
                ,'22 October 2019'
                ,'23 October 2019'
                ,'24 October 2019'
                ,'25 October 2019'
                ,'28 October 2019'
                ,'29 October 2019'
                ,'30 October 2019'
                ,'31 October 2019'
                ,'01 November 2019'
                ,'04 November 2019'
                ,'05 November 2019'
                ,'06 November 2019'
                ,'07 November 2019'
                ,'08 November 2019'
                ,'11 November 2019'
                ,'12 November 2019'
                ,'13 November 2019'
                ,'14 November 2019'
                ,'15 November 2019'
                ,'18 November 2019'
                ,'19 November 2019'
                ,'20 November 2019'
                ,'21 November 2019'
                ,'22 November 2019'
                ,'25 November 2019'
                ,'26 November 2019'
                ]
    EUR=[   0.024274825
            ,0.024204681
            ,0.024171547
            ,0.024151617
            ,0.024179115
            ,0.024224208
            ,0.024182653
            ,0.02408567
            ,0.023979159
            ,0.024019207
            ,0.024006867
            ,0.023890842
            ,0.023683559
            ,0.023528043
            ,0.023594928
            ,0.023691237
            ,0.023676481
            ,0.023769996
            ,0.023894028
            ,0.023822907
            ,0.02377344
            ,0.023713101
            ,0.023650694
            ,0.02358623
            ,0.023719108
            ,0.023949783
            ,0.023938895
            ,0.023998145
            ,0.024060064
            ,0.024035353
            ,0.024095065
            ,0.024122447
            ,0.024042413
            ,0.023914799
            ,0.023823282
            ,0.023812665
            ,0.023853065
            ,0.023908605
            ,0.024084176
            ,0.024138546
            ,0.024079545
            ]

    AUD=[   0.023492661
            ,0.023488191
            ,0.023365271
            ,0.023283445
            ,0.023403907
            ,0.023420276
            ,0.023426818
            ,0.023321667
            ,0.023208107
            ,0.023288012
            ,0.023347448
            ,0.023323572
            ,0.02308786
            ,0.022982533
            ,0.022941709
            ,0.022982413
            ,0.022986116
            ,0.023155209
            ,0.023178275
            ,0.023068074
            ,0.022923516
            ,0.022848464
            ,0.022787237
            ,0.022665491
            ,0.02282398
            ,0.022768898
            ,0.022848438
            ,0.022754688
            ,0.022960792
            ,0.022969985
            ,0.023011418
            ,0.023076149
            ,0.023241608
            ,0.023139071
            ,0.023146317
            ,0.023091814
            ,0.023204566
            ,0.02325692
            ,0.023252458
            ,0.023297309
            ,0.02326584
            ]

    fig = go.Figure()
    # Create and style traces
    fig.add_trace(go.Scatter(x=long_dates, y=EUR, name='EUR',
                             line=dict(color='royalblue', width=2)))
    fig.add_trace(go.Scatter(x=long_dates, y=AUD, name='AUD',
                             line=dict(color='yellow', width=2)))

    # Edit the layout
    fig.update_layout( xaxis_title='',
                      yaxis_title='Level',
                      font=dict(family="Arial", size=9),
                      width=750,
                      height=340
                       )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def bar_chart():
    years =[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
     2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]


    fig = go.Figure()
    fig.add_trace(go.Bar(x=years,
                         y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                            350, 430, 474, 526, 488, 537, 500, 439],
                         name='Rest of world',
                         marker_color='rgb(55, 83, 109)'
                         ))
    fig.add_trace(go.Bar(x=years,
                         y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                            299, 340, 403, 549, 499],
                         name='China',
                         marker_color='rgb(26, 118, 255)'
                         ))

    fig.update_layout(
        title='US Export of Plastic Scrap',
        xaxis_tickfont_size=14,
        width=750,
        height=340,
        yaxis=dict(
            title='USD (millions)',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)








































    # return graphJSONimport plotly
    # import plotly.graph_objs as go
    #
    # import pandas as pd
    # import numpy as np
    # import json
    #
    # def create_plot():
    #     N = 100
    #     random_x = np.linspace(0, 1, N)
    #     random_y0 = np.random.randn(N) + 5
    #     random_y1 = np.random.randn(N)
    #     random_y2 = np.random.randn(N) - 5
    #
    #     # Create traces
    #     trace0 = go.Scatter(
    #         x=random_x,
    #         y=random_y0,
    #         mode='markers',
    #         name='markers'
    #     )
    #     trace1 = go.Scatter(
    #         x=random_x,
    #         y=random_y1,
    #         mode='lines+markers',
    #         name='lines+markers'
    #     )
    #     trace2 = go.Scatter(
    #         x=random_x,
    #         y=random_y2,
    #         mode='lines',
    #         name='lines'
    #     )
    #
    #     layout = go.Layout(
    #         title="Scatter Graph",
    #         xaxis_title="x Axis Title",
    #         yaxis_title="y Axis Title",
    #         font=dict(
    #             family="Merriweather, serif",
    #             size=18),
    #         width=900,
    #         height=800,
    #     )
    #
    #
    #
    #     data = [trace0, trace1, trace2]
    #     fig = go.Figure(data=data, layout=layout)
    #     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #
    #     return graphJSON
    #
    #
    #
    #     # N = 40
    #     # x = np.linspace(0, 1, N)
    #     # y = np.random.randn(N)
    #     # df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
    #     #
    #     #
    #     # data = [
    #     #     go.Bar(
    #     #         x=df['x'], # assign x as the dataframe column 'x'
    #     #         y=df['y']
    #     #     )
    #     # ]
    #     #
    #     # graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    #     #
    #     # return graphJSON
    #
    #     # N = 40
    #     # x = np.linspace(0, 1, N)
    #     # y = np.random.randn(N)
    #     # df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
    #     #
    #     # data = [
    #     #     go.Bar(
    #     #         x=df['x'], # assign x as the dataframe column 'x'
    #     #         y=df['y']
    #     #     )
    #     # ]
    #     #
    #     # layout = go.Layout(
    #     #     width=350,
    #     #     height=350,
    #     # )
    #     # fig = go.Figure(data=data, layout=layout)
    #     #
    #     # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #     # return graphJSON
    #     # data = [
    #     #     go.Scatter(
    #     #         x=[0, 1, 2, 3, 4, 5, 6, 7, 8],
    #     #         y=[0, 1, 2, 3, 4, 5, 6, 7, 8]
    #     #     )
    #     # ]
    #     # layout = go.Layout(
    #     #     width=300,
    #     #     height=300,
    #     #     plot_bgcolor='#c7c7c7'
    #     # )
    #     #
    #     # fig = go.Figure(data=data, layout=layout)
    #     #
    #     # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #     # return graphJSON
    #
    #     # N = 10
    #     # random_x = np.linspace(0, 1, N)
    #     # random_y0 = np.random.randn(N) + 5
    #     # random_y1 = np.random.randn(N)
    #     # random_y2 = np.random.randn(N) - 5
    #     #
    #     # # Create traces
    #     # trace0 = go.Scatter(
    #     #     x=random_x,
    #     #     y=random_y0,
    #     #     mode='markers',
    #     #     name='markers'
    #     # )
    #     # trace1 = go.Scatter(
    #     #     x=random_x,
    #     #     y=random_y1,
    #     #     mode='lines+markers',
    #     #     name='lines+markers'
    #     # )
    #     # trace2 = go.Scatter(
    #     #     x=random_x,
    #     #     y=random_y2,
    #     #     mode='lines',
    #     #     name='lines'
    #     # )
    #     # data = [trace0, trace1, trace2]
    #     # layout = go.Layout(
    #     # autosize=False,
    #     # width=500,
    #     # height=500,)
    #     #
    #     # fig = go.Figure(data=data, layout=layout)
    #     #
    #     #
    #     # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #     #