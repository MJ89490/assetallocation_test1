from typing import Dict


class IncorrectTickerError(ValueError):
    def __init__(self, tickers: Dict[str, str]):
        self.tickers = tickers
        self.message = 'Tickers do not match.'

    def __str__(self):
        if self.tickers:
            formatted_tickers = ','.join((f' {name} "{val}"' for name, val in self.tickers.items()))
            self.message = f'{self.message}{formatted_tickers}.'

        return self.message
