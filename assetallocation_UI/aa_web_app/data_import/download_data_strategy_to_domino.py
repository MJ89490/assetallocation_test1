import os
from domino import Domino


def call_domino_object():
    domino = Domino(
    "{domino_username}/{domino_project_name}".format(domino_username=os.environ['DOMINO_STARTING_USERNAME'],
                                                     domino_project_name=os.environ['DOMINO_PROJECT_NAME']),
                                                     api_key=os.environ['DOMINO_USER_API_KEY'],
                                                     host=os.environ['DOMINO_API_HOST'])
    return domino


def export_times_data_to_csv(version, signals, returns, positions, fund_name, date_to):
        domino = call_domino_object()

        domino.files_upload("/signals_times_version{fund_name}{version}{date_to}.csv".format(fund_name=fund_name,
                                                                                             version=version,
                                                                                             date_to=date_to),
                            signals.to_csv())
        domino.files_upload("/returns_times_version{fund_name}{version}{date_to}.csv".format(fund_name=fund_name,
                                                                                             version=version,
                                                                                             date_to=date_to),
                            returns.to_csv())
        domino.files_upload("/positions_times_version{fund_name}{version}{date_to}.csv".format(fund_name=fund_name,
                                                                                               version=version,
                                                                                               date_to=date_to),
                            positions.to_csv())


def export_times_positions_data_to_csv(positions, fund_name, strategy_version):
    domino = call_domino_object()
    domino.files_upload("/positions_asset_allocations_chart_times_version{fund_name}{strategy_version}.csv".format(fund_name=fund_name,
                                                                                                                   strategy_version=strategy_version),
                        positions.to_csv())
