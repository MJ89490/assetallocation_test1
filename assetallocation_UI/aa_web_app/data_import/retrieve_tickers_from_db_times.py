from assetallocation_arp.data_etl.dal.arp_proc_caller import TimesProcCaller


def _select_asset_tickers_with_names_and_subcategories_from_db():
    apc = TimesProcCaller()

    asset_tickers_names_subcategories = apc.select_asset_tickers_names_subcategories()

    return asset_tickers_names_subcategories.set_index(asset_tickers_names_subcategories.ticker)


def select_tickers():
    """
    Select all asset tickers with names and subcategories that exist in the database
    :return: all asset tickers with names and subcategories
    """

    asset_tickers_names_subcategories = _select_asset_tickers_with_names_and_subcategories_from_db()

    return asset_tickers_names_subcategories.ticker


def select_names_subcategories(user_ticker):
    """
    Select all asset tickers with names and subcategories that exist in the database
    :return: all asset tickers with names and subcategories
    """

    asset_tickers_names_subcategories = _select_asset_tickers_with_names_and_subcategories_from_db()

    ticker_selected_data = asset_tickers_names_subcategories.loc[user_ticker]

    name, subcategory = ticker_selected_data.loc["name"], ticker_selected_data.loc["subcategory"]

    return name, subcategory

