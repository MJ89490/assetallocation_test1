class Ticker:
    def __init__(self, ticker_10y: str, ticker_15y: str, ticker_1y: str, ticker_20y: str, ticker_2y: str,
                 ticker_30y: str, ticker_3m: str, ticker_3y: str, ticker_4y: str, ticker_5y: str, ticker_6y: str,
                 ticker_7y: str, ticker_8y: str, ticker_9y: str, ticker_type: str):
        """Ticker class to hold data from database"""
        self._ticker_10y = ticker_10y
        self._ticker_15y = ticker_15y
        self._ticker_1y = ticker_1y
        self._ticker_20y = ticker_20y
        self._ticker_2y = ticker_2y
        self._ticker_30y = ticker_30y
        self._ticker_3m = ticker_3m
        self._ticker_3y = ticker_3y
        self._ticker_4y = ticker_4y
        self._ticker_5y = ticker_5y
        self._ticker_6y = ticker_6y
        self._ticker_7y = ticker_7y
        self._ticker_8y = ticker_8y
        self._ticker_9y = ticker_9y
        self._type = ticker_type
