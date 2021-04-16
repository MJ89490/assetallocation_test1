# Import packages, classes and functions
import os
import logging
import logging.config
import numpy as np
from datetime import datetime, timedelta
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Select, PreText, HoverTool, Button, TableColumn, DateFormatter, \
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


def get_data(df, name) -> ColumnDataSource:
    """
    This function takes a data frame and name entry and return data in ColumnDataSource format for Bokeh
    :param df: Data as pandas data frame
    :param name: Ticker/instrument name as string
    :return: ColumnDataSource format data
    """
    logger.info(f"Data retrieved for: {name}")
    # Filter data frame for specific ticker
    # Sort data frame by latest date
    df = df[df["ticker"] == name]
    df.sort_values(by=["business_datetime"], inplace=True, ascending=True)

    try:
        # Calculate daily return (natural log of today's value / yesterday's value)
        df["log_return"] = np.log(df["value"]).diff()
    except AttributeError:
        df["log_return"] = 100

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
    price_fig = figure(plot_width=1000, plot_height=300, x_axis_type="datetime", title="Daily Instrument Price")
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

    return_fig = figure(plot_width=1000, plot_height=300, x_axis_type="datetime", title="Daily Instrument Return")
    return_fig.line(x="business_datetime",
                    y="log_return",
                    line_width=0.5,
                    line_color="red",
                    legend_field="ticker",
                    source=source)

    # Define figure properties
    return_fig.background_fill_color = "whitesmoke"
    return_fig.xaxis.axis_label = "Time"
    return_fig.yaxis.axis_label = "Natural logarithmic return"
    return_fig.xaxis.axis_label_text_font_style = "bold"
    return_fig.yaxis.axis_label_text_font_style = "bold"
    return_fig.legend.location = "top_left"
    return_fig.add_tools(HoverTool(tooltips=return_tooltips, formatters={"@business_datetime": "datetime"}))
    logger.info("Bokeh charts created")

    return price_fig, return_fig


def drop_down_handle(attr, old, new) -> None:
    """
    This function handles when the drop down Bokeh widget is changed.
    :param attr:
    :param old:
    :param new:
    :return:
    """
    # Define the value chosen from the drop down
    instrument = drop_down.value

    # Get filtered data frame database in ColumnDataSource format
    # Update source data
    source_update = get_data(df=df_db, name=instrument)
    col_data_source.data.update(source_update.data)
    col_data_source.selected.indices = []
    logger.info(f"{instrument} chosen from drop down")

    return


def refresh_button_handle() -> None:
    """
    This function handles when the refresh button Bokeh widget is changed.
    :return:
    """
    logger.info("Refresh button handle started")
    if df_db["business_datetime"].max().date() != datetime.today().date() - timedelta(days=1):
        # Run data frame through ETL class
        db = Db()
        # Get tickers from database and retrieve latest prices for these
        df_tickers = db.get_tickers()
        etl = ETLProcess(df_tickers=df_tickers)
        etl.bbg_data()
        df_clean = etl.clean_data()
        db.df_to_staging_asset_analytic(df_clean)
        db.call_proc(proc_name="staging.load_asset_analytics", proc_params=[])

    else:
        logging.info("Data is up to date - no refresh is required")
    logger.info("Refresh button handle complete")

    return


def data_validation_handle() -> None:
    """
    This function handles when the data validation button Bokeh widget is changed.
    :return:
    """
    logger.info("Data validation handle started")
    db = Db()
    # Get analytic data and run data validation against this
    df_analytic, _ = db.get_analytic()
    etl = ETLProcess(df=df_analytic)
    etl.data_validation()
    logger.info("Data validation button handle complete")

    return


# Open data base connection and read current data as data frame
# Get list of instruments from data frame as a unique list
db = Db()
df_db, instrument_list = db.get_analytic()

# Create drop down, file input, refresh and stats widgets
drop_down = Select(options=instrument_list, width=200)
refresh_button = Button(label="Refresh", width=200)
data_val_button = Button(label="Data Validation", width=200)
stats = PreText()
columns = [TableColumn(field="ticker", title="ticker"),
           TableColumn(field="description", title="description"),
           TableColumn(field="value", title="value"),
           TableColumn(field="log_return", title="log_return"),
           TableColumn(field="business_datetime", title="business_datetime", formatter=DateFormatter())]

# Get latest data from database and create plot and data table
col_data_source = get_data(df=df_db, name=instrument_list[0])
price_chart, return_chart = make_plot(source=col_data_source)
data_table = DataTable(source=col_data_source, columns=columns, width=800, height=590)

# Register widget attribute change
drop_down.on_change("value", drop_down_handle)
refresh_button.on_click(refresh_button_handle)
data_val_button.on_click(data_validation_handle)

# Define layout of dashboard
widgets = row(drop_down, refresh_button, data_val_button)
charts = column(price_chart, return_chart)
charts_with_table = row(charts, data_table)
layout_with_widgets = column(widgets, charts_with_table, stats)

# Create Dashboard with respective layout
curdoc().add_root(layout_with_widgets)

# bokeh serve assetallocation_arp/data_etl/plot.py

# TODO
# Log times must be UTC .. not British Summer (or other)! - check .ini file