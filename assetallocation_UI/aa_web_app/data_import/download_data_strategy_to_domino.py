import os
from domino import Domino


def call_domino_object():
    domino = Domino(
    "{domino_username}/{domino_project_name}".format(domino_username=os.environ['DOMINO_STARTING_USERNAME'],
                                                     domino_project_name=os.environ['DOMINO_PROJECT_NAME']),
                                                     api_key=os.environ['DOMINO_USER_API_KEY'],
                                                     host=os.environ['DOMINO_API_HOST'])
    return domino


def export_times_data_to_csv(self, version):
        domino = self.call_domino_object()

        domino.files_upload("/signals_times_version{version}.csv".format(version=version), self.signals.to_csv())
        domino.files_upload("/returns_times_version{version}.csv".format(version=version), self.returns.to_csv())
        domino.files_upload("/positions_times_version{version}.csv".format(version=version), self.positions.to_csv())


def export_times_positions_data_to_csv(self):
        domino = self.call_domino_object()
        domino.files_upload("/positions_charts_times_version.csv", self.positions.to_csv())
