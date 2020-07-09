from models.effect.data_processing_effect_to_delete import DataProcessingEffect
from models.effect.compute_currencies import CurrencyComputations
import pandas as pd


class ImportDataIMF(DataProcessingEffect):

    def __init__(self):
        super().__init__()
        self.inflation_release = pd.DataFrame()

    def inflation_release_computations(self):
        p = DataProcessingEffect()
        m = p.data_processing_effect()

        dates_index = self.data_currencies_usd.loc[self.start_date_computations:].index.values

        weo_dates = []

        for date in dates_index:
            date = pd.to_datetime(date)
            if date.day <= 19 and date.month == 4 and date.year == 2006:
                weo_date = "Latest"
            if date.month < 4:
                weo_date = "{month}{year}".format(year=date.year - 1, month='Oct')
            elif date.month == 4 and date.day <= 15:
                weo_date = "{month}{year}".format(year=date.year - 1, month='Oct')
            elif date.month >= 4 and date.month < 10:
                weo_date = "{month}{year}".format(year=date.year, month='Apr')
            else:
                assert date.month >= 10, date
                weo_date = "{month}{year}".format(year=date.year, month='Oct')

            weo_dates.append(weo_date)

        self.inflation_release["Inflation Release"] = weo_dates

if __name__ =='__main__':
    obg = ImportDataIMF()
    obg.inflation_release_computations()