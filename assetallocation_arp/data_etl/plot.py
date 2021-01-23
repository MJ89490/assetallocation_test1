# Import packages, classes and functions
import logging
import logging.config
import os

logging.config.fileConfig(f"{os.path.dirname(os.path.abspath(__file__))}/logging.ini", disable_existing_loggers=False)
logger = logging.getLogger('sLogger')

import pandas as pd
import itertools
from pybase64 import b64decode
import io
from datetime import datetime
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row, column, gridplot
from bokeh.models import ColumnDataSource, Select, PreText, HoverTool, FileInput, Button
from bokeh.palettes import Dark2_5 as palette
from db import Db
from etl import ETLProcess


# Logs
logger.info('An info message')


# Define proxy settings to run local Bokeh server
local_proxy = 'http://zsvzen:80'
os.environ['http_proxy'] = local_proxy
os.environ['HTTP_PROXY'] = local_proxy
os.environ['https_proxy'] = local_proxy

# Define database class
# Read .csv as data frame
db = Db()
df = db.read_from_db()
# Get list of instruments from data frame as a unique list
instrument_list = df["ticker"].unique().tolist()


def get_data(df, name):
    if df.empty:
        df = pd.DataFrame({"ticker": ["N/A", "N/A"],
                           "value": [0, 0],
                           "business_datetime": [datetime.today().strftime('%Y/%m/%d'),
                                                 datetime.today().strftime('%Y/%m/%d')],
                           "description": ["N/A", "N/A"]
                           })
    else:
        pass

    df = df[df.ticker == name]

    stats.text = str(df["value"].describe())

    source = ColumnDataSource(df)

    return source


def make_plot(source):
    # Define colours which iterates through the Bokeh palette function, providing a new line colour with each instrument
    # Format the tooltip
    colors = itertools.cycle(palette)
    tooltips = [('Value', '@value'),
                ('Date', '@business_datetime{%F}'),
                ('Field', '@description')]

    # Initial line chart
    # Create figure for graph
    # Add line to line, which is the first instrument in our data
    line_chart = figure(plot_width=1000, plot_height=400, x_axis_type="datetime", title="Instrument Price")
    line_chart.line(x="business_datetime",
                    y="value",
                    line_width=0.5,
                    line_color=next(colors),
                    source=source)

    # Define chart properties
    line_chart.xaxis.axis_label = 'Time'
    line_chart.yaxis.axis_label = 'Price'
    line_chart.legend.location = "top_left"
    line_chart.add_tools(HoverTool(tooltips=tooltips, formatters={'@business_datetime': 'datetime'}))



    return line_chart


def drop_down_handle(attr, old, new):
    """
    This function handles when the drop down is changed
    :param attr:
    :param old:
    :param new:
    :return:
    """
    instrument = drop_down.value

    source_update = get_data(df=df, name=instrument)

    source.data.update(source_update.data)

    return


def file_input_handle(attr, old, new):
    """
    This function handles when a file is uploaded.
    :param attr:
    :param old:
    :param new:
    :return:
    """
    # Read user input .csv file as pandas data frame
    data_input = b64decode(new)
    data_input_bytes = io.BytesIO(data_input)
    df_input = pd.read_csv(data_input_bytes)

    # Run data frame through ETL class
    etl = ETLProcess(df_input=df_input)
    etl.clean_input()
    etl.bbg_data()
    etl.clean_data()
    etl.upload_data()

    return


def button_handle():
    """
    This function handles when the refresh button is changed
    :return:
    """
    # Run data frame through ETL class
    db = Db()
    # Read .csv as data frame
    df_tickers = db.get_tickers()
    etl = ETLProcess(df_input=df_tickers)
    etl.bbg_data()
    etl.clean_data()
    etl.upload_data()

    return


# Create drop down, file input, refresh and stats widgets
drop_down = Select(title="Instrument", options=instrument_list)
refresh_button = Button(label='Refresh')
file_input = FileInput()
stats = PreText()

source = get_data(df=df, name=instrument_list[0])
line_chart = make_plot(source=source)

# Registering widget attribute change
drop_down.on_change("value", drop_down_handle)
file_input.on_change("value", file_input_handle)
refresh_button.on_click(button_handle)


# Widgets Layout
# layout_with_widgets = column(row(drop_down), row(file_input, refresh_button), row(line_chart), row(stats))
layout_with_widgets = gridplot([[column(drop_down, refresh_button, file_input, stats), line_chart]])
# layout_with_widgets.children[2].children[0] = line_chart
# layout_with_widgets.children[3].children[0] = stats

# Creating Dashboard
curdoc().add_root(layout_with_widgets)
