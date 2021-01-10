import pandas as pd
import os
import itertools
from pybase64 import b64decode
import io
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.models import Select, PreText, TextInput, Button, HoverTool, FileInput
from bokeh.palettes import Dark2_5 as palette
from db import Db
from etl import ETLProcess
import logging
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


local_proxy = 'http://zsvzen:80'
os.environ['http_proxy'] = local_proxy
os.environ['HTTP_PROXY'] = local_proxy
os.environ['https_proxy'] = local_proxy

db = Db()
# Read .csv as data frame
df = db.read_from_db()
# Convert date column to python datetime
df["business_datetime"] = pd.to_datetime(df["business_datetime"], dayfirst=True)
# Get list of instruments from data frame as a unique list
instrument_list = df["ticker"].unique().tolist()

# Define drop down options
drop_down_options = instrument_list
# Define colours which iterates through the Bokeh palette function, providing a new line colour with each instrument
colors = itertools.cycle(palette)
# Format the tooltip
tooltips = [('Value', '@value'),
            ('Date', '@business_datetime{%F}'),
            ('Field', '@description')]

# Initial line chart
# Create figure for graph
line_chart = figure(plot_width=1000, plot_height=400, x_axis_type="datetime", title="Instrument Price")
# Add line to line, which is the first instrument in our data
line_chart.line(x="business_datetime",
                y="value",
                line_width=0.5,
                line_color=next(colors),
                legend_label=instrument_list[0],
                source=df[df["ticker"] == instrument_list[0]])
# Define chart properties
line_chart.xaxis.axis_label = 'Time'
line_chart.yaxis.axis_label = 'Price (GBP)'
line_chart.legend.location = "top_left"
line_chart.add_tools(HoverTool(tooltips=tooltips,
                               formatters={'@business_datetime': 'datetime'}))

# Create drop down instrument widget
drop_down = Select(options=drop_down_options, width=200)
# Create text entry instrument widget
text_input = TextInput(value="Enter Instrument", width=200)
# Create file input widget - accepting only .csv files
file_input = FileInput()
# Create refresh button widget
refresh_button = Button(label='Refresh', width=200)
# Create stats describe
stats = PreText(text='Statistics', width=500)
stats.text = str(df[df["ticker"] == instrument_list[0]]["value"].describe())


def drop_down_handle(attr, old, new):
    """
    This function handles when the drop down is changed
    :param attr:
    :param old:
    :param new:
    :return:
    """

    line_chart = figure(plot_width=1000, plot_height=400, x_axis_type="datetime", title="Instrument Price")

    line_chart.line(x="business_datetime",
                    y="value",
                    line_width=0.5,
                    line_color=next(colors),
                    legend_label=drop_down.value,
                    source=df[df["ticker"] == drop_down.value]
                    )
    line_chart.xaxis.axis_label = 'Time'
    line_chart.yaxis.axis_label = 'Price (GBP)'
    line_chart.legend.location = "top_left"

    line_chart.add_tools(HoverTool(tooltips=tooltips,
                                   formatters={'@business_datetime': 'datetime'}))

    stats.text = str(df[df["ticker"] == drop_down.value]["value"].describe())

    layout_with_widgets.children[1].children[0] = line_chart


def text_input_handle(attr, old, new):
    """
    This function handles when the text input is changed.
    :param attr:
    :param old:
    :param new:
    :return:
    """
    print(new)


def file_input_handle(att, old, new):
    """
    This function handles when a file is uploaded.
    :param attr:
    :param old:
    :param new:
    :return:
    """
    data_input = b64decode(new)
    f = io.BytesIO(data_input)
    df = pd.read_csv(f)
    etl = ETLProcess(df_input=df)
    etl.bbg_data()
    etl.clean_data()
    etl.upload_data()


def button_handle():
    """
    This function handles when the refresh button is changed.
    :return:
    """
    print('I was refreshed')


# Registering widget attribute change
drop_down.on_change("value", drop_down_handle)
text_input.on_change("value", text_input_handle)
file_input.on_change("value", file_input_handle)
refresh_button.on_click(button_handle)

# Widgets Layout
layout_with_widgets = column(row(drop_down, text_input, file_input, refresh_button), row(line_chart, stats))

# Creating Dashboard
curdoc().add_root(layout_with_widgets)
