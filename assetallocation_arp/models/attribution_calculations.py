def comca_att(workbook, input_data, year, commodity_dict):
    """
    This function calculates the attribution for COMCA. This takes the input data for COMCA instruments and aggregates
    the return for each strategy, instrument and instrument category. This is outputted to an Excel sheet.
    :param workbook: Excel workbook used to output to, xlwings function
    :param input_data: Data to attribute, pandas data frame
    :param year: User inputs year to attribute, integer
    :param commodity_dict: Key-value pairs for commodity categories, dictionary
    :return: n/a
    """
    # Filter data for one calender year
    df_att = input_data.loc[f"01/01/{year}":f"31/12/{year}"]

    # Filter data frame for instrument categories
    df_energy = df_att[commodity_dict["energy"]]
    df_agriculture = df_att[commodity_dict["agriculture"]]
    df_industrial_metals = df_att[commodity_dict["industrial_metals"]]
    df_precious_metals = df_att[commodity_dict["precious_metals"]]
    df_natural_gas = df_att[commodity_dict["natural_gas"]]

    # Append category sums to master data frame
    df_att["energy"] = df_energy.sum(axis=1)
    df_att["agriculture"] = df_agriculture.sum(axis=1)
    df_att["industrial_metals"] = df_industrial_metals.sum(axis=1)
    df_att["precious_metals"] = df_precious_metals.sum(axis=1)
    df_att["natural_gas"] = df_natural_gas.sum(axis=1)

    # Transpose data frame to have a horizontal time series view
    # Calculate year to date for all attributes
    df_att = df_att.transpose()
    df_att["ytd"] = df_att.sum(axis=1)

    # Output attribution data frame to sheet
    workbook.sheets["python_dashboard"].range("A1").value = df_att

    return


def factor_att(workbook, input_data, year, strat_dict):
    """
    This function calculates the attribution for a given model. This takes the input data different strategies, with
    respective weights and aggregates the return. The output is exported to an Excel sheet.
    :param workbook: Excel workbook used to output to, xlwings function
    :param input_data: Raw data to attribute, pandas data frame
    :param year: User inputs year to attribute, integer
    :param strat_dict: Dictionary of lists. Key is type of strategy, position one of value is strategy and position two
                        is the weight. Note cost does not have a strategy name and is set to None.
    :return: n/a
    """
    # Filter data for one calender year
    df_att = input_data.loc[f"01/01/{year}":f"31/12/{year}"]

    # Calculate relative, contribution and total net values
    df_att["relative_quality"] = df_att[strat_dict["quality"][0]] - df_att[strat_dict["main"][0]]
    df_att["relative_value"] = df_att[strat_dict["value"][0]] - df_att[strat_dict["main"][0]]
    df_att["relative_min_vol"] = df_att[strat_dict["min_vol"][0]] - df_att[strat_dict["main"][0]]
    df_att["relative_momentum"] = df_att[strat_dict["momentum"][0]] - df_att[strat_dict["main"][0]]
    df_att["contribution_quality"] = df_att["relative_quality"] * strat_dict["quality"][1]
    df_att["contribution_value"] = df_att["relative_value"] * strat_dict["value"][1]
    df_att["contribution_min_vol"] = df_att["relative_min_vol"] * strat_dict["min_vol"][1]
    df_att["contribution_momentum"] = df_att["relative_momentum"] * strat_dict["momentum"][1]
    df_att["total_net"] = df_att[["contribution_quality", "contribution_value", "contribution_min_vol"]].sum(axis=1)\
                          - (strat_dict["cost"][1] / (10000 * 12))

    # Transpose data frame to have a horizontal time series view
    # Calculate year to date for all attributes
    df_att = df_att.transpose()
    df_att["ytd"] = df_att.sum(axis=1)

    # Output attribution data frame to sheet
    workbook.sheets["python_dashboard"].range("A1").value = df_att

    return
