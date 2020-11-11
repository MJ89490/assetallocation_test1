from typing import List, Union, Optional
import itertools

from assetallocation_arp.common_libraries.dal_enums.asset import Category, Subcategory, subcategory_map
from assetallocation_arp.common_libraries.dal_enums.currency import Currency
from assetallocation_arp.common_libraries.dal_enums.country import Country, country_region
from assetallocation_arp.data_etl.dal.data_models.asset_analytic import AssetAnalytic
from assetallocation_arp.data_etl.dal.data_models.custom_error import TickerError
from assetallocation_arp.common_libraries.dal_enums import fica_asset_input


class Asset:
    def __init__(self, ticker: str):
        """Asset class to hold data from database"""
        self._category = None
        self._country = None
        self._currency = None
        self._description = ''
        self._name = None
        self._ticker = ticker
        self._is_tr = None
        self._subcategory = None
        self._asset_analytics = []

    @property
    def ticker(self) -> str:
        return self._ticker

    @ticker.setter
    def ticker(self, x: str) -> None:
        self._ticker = x

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, x: str) -> None:
        self._name = x

    @property
    def asset_analytics(self) -> List[AssetAnalytic]:
        return self._asset_analytics

    @asset_analytics.setter
    def asset_analytics(self, x: List[AssetAnalytic]) -> None:
        self._asset_analytics = x

    @property
    def category(self) -> Category:
        return self._category

    @category.setter
    def category(self, x: Union[str, Category]) -> None:
        self._category = x if isinstance(x, Category) else Category[x]

    @property
    def country(self) -> Country:
        return self._country

    @country.setter
    def country(self, x: Union[str, Country]) -> None:
        self._country = x if isinstance(x, Country) else Country[x]

    @property
    def region(self) -> str:
        return country_region.get(self.country.name)

    @property
    def subcategory(self) -> str:
        return self._subcategory

    @subcategory.setter
    def subcategory(self, x: str):
        self._subcategory = x

    @property
    def currency(self) -> Currency:
        return self._currency

    @currency.setter
    def currency(self, x: Union[str, Currency]) -> None:
        self._currency = x if isinstance(x, Currency) else Currency[x]

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, x: str) -> None:
        self._description = x

    @property
    def is_tr(self) -> bool:
        return self._is_tr

    @is_tr.setter
    def is_tr(self, x: bool) -> None:
        self._is_tr = x

    def add_analytic(self, asset_analytic: AssetAnalytic) -> None:
        if asset_analytic.asset_ticker == self.ticker:
            self._asset_analytics.append(asset_analytic)
        else:
            raise TickerError({'asset': self.ticker, 'asset_analytic': asset_analytic.asset_ticker})

    def __eq__(self, other: 'Asset'):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False


# noinspection PyAttributeOutsideInit
class FicaAssetInput(Asset):
    def __init__(self, ticker: str, input_category: Union[str, fica_asset_input.Category],
                 curve_tenor: Union[str, fica_asset_input.CurveTenor, None]) -> None:
        """FicaAsset class to hold data from database"""
        super().__init__(ticker)
        self._input_category = input_category
        self._curve_tenor = curve_tenor

    @property
    def curve_tenor(self) -> Optional[fica_asset_input.CurveTenor]:
        return self._curve_tenor

    @curve_tenor.setter
    def curve_tenor(self, x: Union[str, fica_asset_input.CurveTenor]) -> None:
        if self._curve_tenor is not None:
            self._curve_tenor = x if isinstance(x, fica_asset_input.CurveTenor) else fica_asset_input.CurveTenor[x]

    @property
    def input_category(self) -> fica_asset_input.Category:
        return self._input_category

    @input_category.setter
    def input_category(self, x: Union[fica_asset_input.Category, str]) -> None:
        self._input_category = x if isinstance(x, fica_asset_input.Category) else fica_asset_input.Category[x]


# noinspection PyAttributeOutsideInit
class FicaAssetInputGroup:
    def __init__(self, asset_subcategory: Union[str, Subcategory], fica_asset_inputs: List[FicaAssetInput]):
        self.asset_subcategory = asset_subcategory
        self.fica_asset_inputs = fica_asset_inputs

    @property
    def asset_subcategory(self) -> Union[str, Subcategory]:
        return self._asset_subcategory

    @asset_subcategory.setter
    def asset_subcategory(self, x: Union[str, Subcategory]) -> None:
        if isinstance(x, Subcategory):
            self._asset_subcategory = x
        else:
            self._asset_subcategory = subcategory_map[x]

    @property
    def fica_asset_inputs(self) -> List[FicaAssetInput]:
        return self._fica_asset_inputs

    @fica_asset_inputs.setter
    def fica_asset_inputs(self, x: List[FicaAssetInput]) -> None:
        self._fica_asset_inputs = x


# noinspection PyAttributeOutsideInit
class FxAssetInput:
    def __init__(self, ppp_ticker: str, cash_rate_ticker: str, currency: str) -> None:
        """TimesAssetInput class to hold data from database"""
        self.ppp_ticker = ppp_ticker
        self.cash_rate_ticker = cash_rate_ticker
        self.currency = currency

        self.ppp_asset = None
        self.cash_rate_asset = None

    @property
    def cash_rate_asset(self) -> Asset:
        return self._cash_rate_asset

    @cash_rate_asset.setter
    def cash_rate_asset(self, x: Asset) -> None:
        self._cash_rate_asset = x

    @property
    def ppp_asset(self) -> Asset:
        return self._ppp_asset

    @ppp_asset.setter
    def ppp_asset(self, x: Asset) -> None:
        self._ppp_asset = x

    @staticmethod
    def get_crosses(fx_asset_inputs: List['FxAssetInput']) -> List[str]:
        currencies = [i.currency for i in fx_asset_inputs]
        return list(itertools.combinations(currencies, 2))

    @staticmethod
    def get_spot_tickers(fx_asset_inputs: List['FxAssetInput']) -> List[str]:
        crosses = FxAssetInput.get_crosses(fx_asset_inputs)
        return [''.join(x) + ' Curncy' for x in crosses]

    @staticmethod
    def get_carry_tickers(fx_asset_inputs: List['FxAssetInput']) -> List[str]:
        crosses = FxAssetInput.get_crosses(fx_asset_inputs)
        return [''.join(x) + 'CR Curncy' for x in crosses]


# noinspection PyAttributeOutsideInit
class TimesAssetInput:
    def __init__(
            self, asset_subcategory: Union[str, Subcategory], s_leverage: int, signal_ticker: str,
            future_ticker: str, cost: float
    ) -> None:
        """TimesAssetInput class to hold data from database
        :param asset_subcategory:
        """
        self.asset_subcategory = asset_subcategory
        self.signal_ticker = signal_ticker
        self.future_ticker = future_ticker
        self.cost = cost
        self.s_leverage = s_leverage
        self._signal_asset = None
        self._future_asset = None

    @property
    def asset_subcategory(self) -> Subcategory:
        return self._asset_subcategory

    @asset_subcategory.setter
    def asset_subcategory(self, x: Union[str, Subcategory]) -> None:
        if isinstance(x, Subcategory):
            self._asset_subcategory = x
        else:
            self._asset_subcategory = subcategory_map[x]

    @property
    def signal_asset(self) -> Asset:
        return self._signal_asset

    @signal_asset.setter
    def signal_asset(self, x: Asset) -> None:
        if x.ticker == self.signal_ticker:
            self._signal_asset = x
        else:
            raise TickerError({'asset': x.ticker, 'signal': self.signal_ticker})

    @property
    def future_asset(self) -> Asset:
        return self._future_asset

    @future_asset.setter
    def future_asset(self, x: Asset) -> None:
        if x.ticker == self.future_ticker:
            self._future_asset = x
        else:
            raise TickerError({'asset': x.ticker, 'future': self.future_ticker})

    @property
    def s_leverage(self) -> int:
        return self._s_leverage

    @s_leverage.setter
    def s_leverage(self, x: int) -> None:
        self._s_leverage = x

    @property
    def signal_ticker(self) -> str:
        return self._signal_ticker

    @signal_ticker.setter
    def signal_ticker(self, x: str) -> None:
        self._signal_ticker = x

    @property
    def future_ticker(self) -> str:
        return self._future_ticker

    @future_ticker.setter
    def future_ticker(self, x: str) -> None:
        self._future_ticker = x

    @property
    def cost(self) -> float:
        return self._cost

    @cost.setter
    def cost(self, x: float) -> None:
        self._cost = x


# noinspection PyAttributeOutsideInit
class EffectAssetInput(Asset):
    def __init__(self, ticker: str, ndf_code: str, spot_code: str, position_size: float) -> None:
        """EffectAsset class to hold data from database"""
        super().__init__(ticker)
        self.ndf_code = ndf_code
        self.spot_code = spot_code
        self.position_size = position_size

    @property
    def ndf_code(self) -> str:
        return self._ndf_code

    @ndf_code.setter
    def ndf_code(self, x: str) -> None:
        self._ndf_code = x

    @property
    def spot_code(self) -> str:
        return self._spot_code

    @spot_code.setter
    def spot_code(self, x: str) -> None:
        self._spot_code = x

    @property
    def position_size(self) -> float:
        return self._position_size

    @position_size.setter
    def position_size(self, x: float) -> None:
        self._position_size = x


# noinspection PyAttributeOutsideInit
class MavenAssetInput:
    def __init__(
            self, asset_subcategory: Union[str, Subcategory], description: str, bbg_tr_ticker: str,
            bbg_er_ticker: str, currency: str, cash_ticker: str, asset_class: str, true_excess: bool,
            asset_weight: float, transaction_cost: float
    ) -> None:
        """TimesAssetInput class to hold data from database
        :param asset_subcategory:
        """
        self.asset_subcategory = asset_subcategory
        self.description = description
        self.bbg_tr_ticker = bbg_tr_ticker
        self.bbg_er_ticker = bbg_er_ticker
        self.currency = currency
        self.cash_ticker = cash_ticker
        self.asset_class = asset_class
        self.true_excess = true_excess
        self.asset_weight = asset_weight
        self.transaction_cost = transaction_cost
        self.bbg_tr_asset = Asset(bbg_tr_ticker)
        self.bbg_er_asset = Asset(bbg_er_ticker)
        self.cash_asset = Asset(cash_ticker)

    # TODO write template for generating pset from __init__ parameters
