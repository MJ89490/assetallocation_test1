from typing import Dict


class TickerError(ValueError):
    def __init__(self, tickers: Dict[str, str]):
        self.tickers = tickers
        self.message = 'Tickers do not match.'

    def __str__(self):
        if self.tickers:
            formatted_tickers = ','.join((f' {name} "{val}"' for name, val in self.tickers.items()))
            self.message = f'{self.message}{formatted_tickers}.'

        return self.message


class TickerCategoryError(ValueError):
    def __init__(self, expected_category):
        self.expected_category = expected_category
        self.message = f'{expected_category}_ticker must be of category {expected_category}'

    def __str__(self):
        return self.message
