class Fund:
    def __init__(self, currency_id: int, fund_id: int, name: str):
        self._currency_id = currency_id
        self._fund_id = fund_id
        self._name = name
