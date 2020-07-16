from .currency import Currency


class Fund:
    def __init__(self, currency: Currency, fund_id: int, name: str):
        self._currency = currency
        self._fund_id = fund_id
        self._name = name

    @property
    def fund_id(self):
        return self._fund_id

    @property
    def name(self):
        return self._name

    @property
    def currency(self):
        return self._currency
