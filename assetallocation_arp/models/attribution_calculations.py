def comca_att(workbook, input_data, year):
    """
    This function calculates the attribution for COMCA. This takes the input data for COMCA instruments and aggregates
    the return for each strategy, instrument and instrument category. This is outputted to an Excel sheet.
    :param workbook: Excel workbook used to output to, xlwings function
    :param input_data: Data to attribute, pandas data frame
    :param year: User inputs year to attribute, integer
    :return: n/a
    """
    # Filter data for given year
    date_from = f"01/01/{year}"
    date_to = f"31/12/{year}"
    df_att = input_data.loc[date_from:date_to]

    # Filter data frame for instrument category sums
    df_energy = df_att[["CL", "CO", "HO", "XB", "QS"]]
    df_agriculture = df_att[["BO", "C ", "CT", "KC", "KW", "LC", "LH", "S ", "SB", "SM", "W "]]
    df_industrial_metals = df_att[["HG", "LA", "LN", "LX"]]
    df_precious_metals = df_att[["GC", "SI"]]
    df_natural_gas = df_att[["NG"]]

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


def factor_att(workbook, input_data, year, ac_weights, dev_weights, eafe_weights):
    """
    This function calculates the attribution for FACTOR. This takes the input data for FACTOR strategies and categories
    and aggregates the return. This is outputted to an Excel sheet.
    :param workbook: Excel workbook used to output to, xlwings function
    :param input_data: Data to attribute, pandas data frame
    :param year: User inputs year to attribute, integer
    :param ac_weights: weights for AC, list
    :param dev_weights: weights for DEV, list
    :param eafe_weights: weights for EAFE, list
    :return: n/a
    """
    # Filter data for given year
    date_from = f"01/01/{year}"
    date_to = f"31/12/{year}"
    df_att = input_data.loc[date_from:date_to]

    # Calculate EAFE relative, contribution and total net values
    df_att["eafe_relative_quality"] = df_att["M1EAQU"] - df_att["M1EA"]
    df_att["eafe_relative_value"] = df_att["M1EAEV"] - df_att["M1EA"]
    df_att["eafe_relative_minvol"] = df_att["M00IEA$O"] - df_att["M1EA"]
    df_att["eafe_relative_momentum"] = df_att["M1EAMM"] - df_att["M1EA"]
    df_att["eafe_contribution_quality"] = df_att["eafe_relative_quality"] * ac_weights[0]
    df_att["eafe_contribution_value"] = df_att["eafe_relative_value"] * ac_weights[1]
    df_att["eafe_contribution_minvol"] = df_att["eafe_relative_minvol"] * ac_weights[2]
    df_att["eafe_contribution_momentum"] = df_att["eafe_relative_momentum"] * ac_weights[3]
    df_att["eafe_total_net"] = df_att[["eafe_contribution_quality", "eafe_contribution_value",
                                       "eafe_contribution_minvol"]].sum(axis=1) - (ac_weights[5] / (10000 * 12))

    # Calculate AC relative, contribution and total net values
    df_att["ac_relative_quality"] = df_att["M1WDQU"] - df_att["M1WD"]
    df_att["ac_relative_value"] = df_att["M1WDOV"] - df_att["M1WD"]
    df_att["ac_relative_minvol"] = df_att["M00IWD$O"] - df_att["M1WD"]
    df_att["ac_relative_momentum"] = df_att["M1WD000$"] - df_att["M1WD"]
    df_att["ac_contribution_quality"] = df_att["ac_relative_quality"] * dev_weights[0]
    df_att["ac_contribution_value"] = df_att["ac_relative_value"] * dev_weights[1]
    df_att["ac_contribution_minvol"] = df_att["ac_relative_minvol"] * dev_weights[2]
    df_att["ac_contribution_momentum"] = df_att["ac_relative_momentum"] * dev_weights[3]
    df_att["ac_total_net"] = df_att[["ac_contribution_quality", "ac_contribution_value",
                                     "ac_contribution_minvol"]].sum(axis=1) - (dev_weights[5] / (10000 * 12))

    # Calculate DEV relative, contribution and total net values
    df_att["dev_relative_quality"] = df_att["M1WOQU"] - df_att["M1WO"]
    df_att["dev_relative_value"] = df_att["M1WOEV"] - df_att["M1WO"]
    df_att["dev_relative_minvol"] = df_att["M00IWO$O"] - df_att["M1WO"]
    df_att["dev_relative_momentum"] = df_att["M1WOMOM"] - df_att["M1WO"]
    df_att["dev_contribution_quality"] = df_att["dev_relative_quality"] * eafe_weights[0]
    df_att["dev_contribution_value"] = df_att["dev_relative_value"] * eafe_weights[1]
    df_att["dev_contribution_minvol"] = df_att["dev_relative_minvol"] * eafe_weights[2]
    df_att["dev_contribution_momentum"] = df_att["dev_relative_momentum"] * eafe_weights[3]
    df_att["dev_total_net"] = df_att[["dev_contribution_quality", "dev_contribution_value",
                                      "dev_contribution_minvol"]].sum(axis=1) - (eafe_weights[5] / (10000 * 12))

    # Transpose data frame to have a horizontal time series view
    # Calculate year to date for all attributes
    df_att = df_att.transpose()
    df_att["ytd"] = df_att.sum(axis=1)

    # Output attribution data frame to sheet
    workbook.sheets["python_dashboard"].range("A1").value = df_att

    return
