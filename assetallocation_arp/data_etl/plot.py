# Import packages, classes and functions
import os
import logging
import logging.config
import pandas as pd
import numpy as np
from pybase64 import b64decode
import io
from datetime import datetime
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Select, PreText, HoverTool, FileInput, Button, TableColumn, DateFormatter, \
    DataTable
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
        logger.info("No data retrieved from database - initial graph defaulted to null")
    else:
        logger.info(f"Data retrieved from database for: {name}")

    # Filter data frame for specific ticker
    df = df[df["ticker"] == name]
    # Sort data frame by latest date
    df.sort_values(by=["business_datetime"], inplace=True, ascending=True)
    # Calculate daily return (natural log of today's value / yesterday's value)
    df["log_return"] = np.log(df["value"]).diff()

    # Get basic stats for value and log return columns
    stats.text = str(df[["value", "log_return"]].describe())
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
    price_tooltips = [("Value", "@value"),
                      ("Date", "@business_datetime{%F}"),
                      ("Field", "@description")]

    # Format the tooltip
    return_tooltips = [("Log Return", "@log_return"),
                       ("Date", "@business_datetime{%F}"),
                       ("Field", "@description")]

    # Create figure for graph
    # Initial line chart
    price_fig = figure(plot_width=1000, plot_height=300, x_axis_type="datetime", title="Instrument Price")
    price_fig.line(x="business_datetime",
                   y="value",
                   line_width=2,
                   line_color="orange",
                   legend_field="ticker",
                   source=source)

    # Define figure properties
    price_fig.background_fill_color = "whitesmoke"
    price_fig.xaxis.axis_label = "Time"
    price_fig.yaxis.axis_label = "Price"
    price_fig.xaxis.axis_label_text_font_style = "bold"
    price_fig.yaxis.axis_label_text_font_style = "bold"
    price_fig.legend.location = "top_left"
    price_fig.add_tools(HoverTool(tooltips=price_tooltips, formatters={"@business_datetime": "datetime"}))

    return_fig = figure(plot_width=1000, plot_height=300, x_axis_type="datetime", title="Instrument Log Return")
    return_fig.line(x="business_datetime",
                    y="log_return",
                    line_width=2,
                    line_color="red",
                    legend_field="ticker",
                    source=source)

    # Define figure properties
    return_fig.background_fill_color = "whitesmoke"
    return_fig.xaxis.axis_label = "Time"
    return_fig.yaxis.axis_label = "Log return"
    return_fig.xaxis.axis_label_text_font_style = "bold"
    return_fig.yaxis.axis_label_text_font_style = "bold"
    return_fig.legend.location = "top_left"
    return_fig.add_tools(HoverTool(tooltips=return_tooltips, formatters={"@business_datetime": "datetime"}))

    logger.info("Bokeh charts created")

    return price_fig, return_fig


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
    source_update = get_data(df=db_df, name=instrument)
    col_data_source.data.update(source_update.data)
    col_data_source.selected.indices = []

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
    etl = ETLProcess(df=df_input)
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
    df_tickers, _ = db.get_tickers()
    etl = ETLProcess(df=df_tickers)
    etl.bbg_data()
    etl.clean_data()
    etl.upload_data()

    logger.info("Refresh button handle complete")

    return


# Open data base connection and read current data as data frame
# Get list of instruments from data frame as a unique list
db = Db()
db_df = db.read_from_db()
instrument_list = db_df["ticker"].unique().tolist()

# Create drop down, file input, refresh and stats widgets
drop_down = Select(options=instrument_list, width=200)
refresh_button = Button(label="Refresh", width=200)
file_input = FileInput()
stats = PreText()
columns = [TableColumn(field="ticker", title="ticker"),
           TableColumn(field="description", title="description"),
           TableColumn(field="value", title="value"),
           TableColumn(field="log_return", title="log_return"),
           TableColumn(field="business_datetime", title="business_datetime", formatter=DateFormatter())]

# Get latest data from database and create plot and data table
col_data_source = get_data(df=db_df, name=instrument_list[0])
price_chart, return_chart = make_plot(source=col_data_source)
data_table = DataTable(source=col_data_source, columns=columns, width=800, height=590)

# Register widget attribute change
drop_down.on_change("value", drop_down_handle)
file_input.on_change("value", file_input_handle)
refresh_button.on_click(refresh_button_handle)

# Define layout of dashboard
widgets = row(drop_down, refresh_button, file_input)
charts = column(price_chart, return_chart)
charts_with_table = row(charts, data_table)
layout_with_widgets = column(widgets, charts_with_table, stats)

# Create Dashboard with respective layout
curdoc().add_root(layout_with_widgets)
