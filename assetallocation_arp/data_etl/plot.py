# Import packages, classes and functions
import os
import logging
import logging.config
import pandas as pd
from pybase64 import b64decode
import io
from datetime import datetime
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import column, gridplot
from bokeh.models import ColumnDataSource, Select, PreText, HoverTool, FileInput, Button
from db import Db
from etl import ETLProcess

# Get logging config from .ini file
logging.config.fileConfig(f"{os.path.dirname(os.path.abspath(__file__))}/logging.ini", disable_existing_loggers=False)
logger = logging.getLogger("sLogger")

# Define proxy settings to run local Bokeh server
local_proxy = "http://zsvzen:80"
os.environ["http_proxy"] = local_proxy
os.environ["HTTP_PROXY"] = local_proxy
os.environ["https_proxy"] = local_proxy
logger.info("Proxy settings defined")


def get_data(df, name):
    """
    This function takes a data frame and name entry and return data in ColumnDataSource format for Bokeh
    :param df: Data as pandas data frame
    :param name: Ticker/instrument name as string
    :return: ColumnDataSource format data
    """
    # If data frame is empty, default output to be a "null" data frame which can be shown in Bokeh
    if df.empty:
        df = pd.DataFrame({"ticker": ["N/A", "N/A"],
                           "value": [0, 0],
                           "business_datetime": [datetime.today().strftime("%Y/%m/%d"),
                                                 datetime.today().strftime("%Y/%m/%d")],
                           "description": ["N/A", "N/A"]
                           })
        logger.info("Null table retrieved from database")
    else:
        logger.info("Non-null table retrieved from database")

    # Filter data frame for specific ticker
    df = df[df.ticker == name]
    # Get basic stats for value column of data frame
    stats.text = str(df["value"].describe())

    logger.info("Data frame converted to ColumnDataSource")

    return ColumnDataSource(df)


def make_plot(source):
    """
    This function takes the source data and creates a Bokeh line chart (time series) of time vs. price for each
    instrument.
    :param source: Input data in ColumnDataSource format
    :return: Line chart figure in Bokeh format
    """
    # Format the tooltip
    tooltips = [("Value", "@value"),
                ("Date", "@business_datetime{%F}"),
                ("Field", "@description")]

    # Create figure for graph
    # Initial line chart
    line_chart = figure(plot_width=1000, plot_height=400, x_axis_type="datetime", title="Instrument Price")
    line_chart.line(x="business_datetime",
                    y="value",
                    line_width=0.5,
                    line_color="red",
                    source=source)

    # Define figure properties
    line_chart.xaxis.axis_label = "Time"
    line_chart.yaxis.axis_label = "Price"
    line_chart.legend.location = "top_left"
    line_chart.add_tools(HoverTool(tooltips=tooltips, formatters={"@business_datetime": "datetime"}))

    logger.info("Bokeh line chart created")

    return line_chart


def drop_down_handle(attr, old, new):
    """
    This function handles when the drop down Bokeh widget is changed.
    :param attr:
    :param old:
    :param new:
    :return: n/a
    """
    # Define the value chosen from the drop down
    instrument = drop_down.value

    # Get filtered data frame database in ColumnDataSource format
    # Update source data
    source_update = get_data(df=df, name=instrument)
    source.data.update(source_update.data)

    logger.info(f"{instrument} chosen from drop down")

    return


def file_input_handle(attr, old, new):
    """
    This function handles when a file is uploaded to the FileInput Bokeh widget.
    :param attr:
    :param old:
    :param new:
    :return:
    """
    # Read user input .csv file as pandas data frame
    data_input = b64decode(new)
    data_input_bytes = io.BytesIO(data_input)
    df_input = pd.read_csv(data_input_bytes)
    logger.info(".csv file read as data frame")

    # Run data frame through ETL class
    etl = ETLProcess(df_input=df_input)
    etl.clean_input()
    etl.bbg_data()
    etl.clean_data()
    etl.upload_data()
    logger.info("File input handle complete")

    return


def refresh_button_handle():
    """
    This function handles when the refresh button Bokeh widget is changed.
    :return:
    """
    # Run data frame through ETL class
    db = Db()
    # Get tickers from database and retrieve latest prices for these
    df_tickers = db.get_tickers()
    etl = ETLProcess(df_input=df_tickers)
    etl.bbg_data()
    etl.clean_data()
    etl.upload_data()

    logger.info("Refresh button handle complete")

    return


# Open data base connection and read current data as data frame
# Get list of instruments from data frame as a unique list
db = Db()
df = db.read_from_db()
instrument_list = df["ticker"].unique().tolist()

# Create drop down, file input, refresh and stats widgets
drop_down = Select(title="Instrument", options=instrument_list)
refresh_button = Button(label="Refresh")
file_input = FileInput()
stats = PreText()

# Get latest data from database and create plot
source = get_data(df=df, name=instrument_list[0])
line_chart = make_plot(source=source)

# Registering widget attribute change
drop_down.on_change("value", drop_down_handle)
file_input.on_change("value", file_input_handle)
refresh_button.on_click(refresh_button_handle)

# Define layout of dashboard
layout_with_widgets = gridplot([[column(drop_down, refresh_button, file_input, stats), line_chart]])

# Create Dashboard with respective layout
curdoc().add_root(layout_with_widgets)
