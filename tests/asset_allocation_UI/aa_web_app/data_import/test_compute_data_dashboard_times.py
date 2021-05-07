import unittest

from assetallocation_UI.aa_web_app.data_import.compute_data_dashboard_times import ComputeDataDashboardTimes


class TestComputeDataDashboardTimes(unittest.TestCase):

    obj_compute_data_dashboard_times = ComputeDataDashboardTimes(signals='', returns='', positions='')

    def test_compute_mom_signals_each_asset(self):

        pass