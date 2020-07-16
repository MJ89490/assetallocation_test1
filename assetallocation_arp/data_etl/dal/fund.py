from .currency import Currency


class Fund:
    def __init__(self, currency: Currency, name: str):
        self._currency = currency
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def currency(self):
        return self._currency
