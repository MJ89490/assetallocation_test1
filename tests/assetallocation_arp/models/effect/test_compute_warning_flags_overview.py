import os
import numpy as np
import pandas as pd
from unittest import TestCase

from assetallocation_arp.models.effect.compute_warning_flags_overview import ComputeWarningFlagsOverview
from assetallocation_arp.models.effect.compute_currencies import ComputeCurrencies


class TestComputeWarningFlagsOverview(TestCase):

    def setUp(self):
        all_data = pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "all_date.csv")), sep=',', engine='python')
        all_data = all_data.set_index(pd.to_datetime(all_data.Date, format='%Y-%m-%d'))
        del all_data['Date']
        self.obj_import_data = ComputeCurrencies(asset_inputs=pd.read_csv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "effect", "outputs_origin", "asset_inputs.csv")), sep=',', engine='python'),
                                                 bid_ask_spread=10,
                                                 frequency_mat='weekly',
                                                 end_date_mat='23/09/2020',
                                                 signal_day_mat='WED',
                                                 all_data=all_data)
        self.obj_import_data.process_all_data_effect()
        self.obj_import_data.start_date_calculations = pd.to_datetime('12-01-2000', format='%d-%m-%Y')
        self.process_usd_eur_data_effect = self.obj_import_data.process_usd_eur_data_effect()
        self.obj_compute_warning_flags = ComputeWarningFlagsOverview(pd.to_datetime('23-09-2020', format='%d-%m-%Y'), "weekly")

    def test_compute_warning_flags_rates(self):
        flags = self.obj_compute_warning_flags.compute_warning_flags_rates(self.process_usd_eur_data_effect['three_month_implied_usd'], self.process_usd_eur_data_effect['three_month_implied_eur'])
        assert np.allclose(np.array(flags), np.array(-0.0812800000))
