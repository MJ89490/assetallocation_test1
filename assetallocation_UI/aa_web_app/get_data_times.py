from assetallocation_UI.aa_web_app.service.strategy import run_strategy
from assetallocation_arp.data_etl.dal.data_models.strategy import Times, TimesAssetInput, DayOfWeek

class ReceivedDataTimes:
    def __init__(self):
        self.times_form = {}
        self.write_logs = {}

    def received_data_times(self, form_data):
        for idx, val in enumerate(form_data):
            if idx > 1:
                self.times_form[val.split('=', 1)[0]] = val.split('=', 1)[1]

        # Process date under format '12%2F09%2F2000 to 01/01/2000
        self.times_form['input_date_from_times'] = '/'.join(self.times_form['input_date_from_times'].split('%2F'))

        print(self.times_form)

        return self.times_form

    def call_run_times(self, assets_input_times):

       pass
        print('after fund strategy')