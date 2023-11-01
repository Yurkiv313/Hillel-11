import dataclasses
from abc import ABC, abstractmethod

import requests


@dataclasses.dataclass
class SellBuy:
    sell: float
    buy: float


class RateNotFound(Exception):
    pass


class ProviderBase(ABC):
    name = None

    def __init__(self, currency_from: str, currency_to: str):
        self.currency_from = currency_from
        self.currency_to = currency_to

    @abstractmethod
    def get_rate(self) -> SellBuy:
        pass


class MonoProvider(ProviderBase):
    name = "monobank"

    iso_from_country_code = {
        "UAH": 980,
        "USD": 840,
        "EUR": 978,
    }

    def get_rate(self) -> SellBuy:
        url = "https://api.monobank.ua/bank/currency"
        response = requests.get(url)
        response.raise_for_status()

        currency_from_code = self.iso_from_country_code[self.currency_from]
        currency_to_code = self.iso_from_country_code[self.currency_to]

        for currency in response.json():
            if (
                currency["currencyCodeA"] == currency_from_code
                and currency["currencyCodeB"] == currency_to_code
            ):
                value = SellBuy(
                    sell=float(currency["rateSell"]), buy=float(currency["rateBuy"])
                )
                return value
        raise RateNotFound(
            f"Cannot find rate from {self.currency_from} to {self.currency_to} in provider {self.name}"
        )


class PrivatbankProvider(ProviderBase):
    name = "privatbank"

    def get_rate(self) -> SellBuy:
        url = "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5"
        response = requests.get(url)
        response.raise_for_status()
        for currency in response.json():
            if (
                currency["ccy"] == self.currency_from
                and currency["base_ccy"] == self.currency_to
            ):
                value = SellBuy(
                    buy=float(currency["buy"]), sell=float(currency["sale"])
                )
                return value
        raise RateNotFound(
            f"Cannot find rate from {self.currency_from} to {self.currency_to} in provider {self.name}"
        )


class VkurseProvider(ProviderBase):
    name = "vkurse"

    iso_from_country_code = {
        "UAH": 980,
        "USD": 840,
        "EUR": 978,
    }

    def get_rate(self) -> SellBuy:
        url = "https://vkurse.dp.ua/course.json"
        response = requests.get(url)
        response.raise_for_status()
        json = response.json()

        if self.currency_from == "USD":
            currency = json["Dollar"]
        elif self.currency_from == "EUR":
            currency = json["Euro"]
        else:
            raise RateNotFound(
                f"Cannot find rate from {self.currency_from} to {self.currency_to} in provider {self.name}"
            )

        value = SellBuy(buy=float(currency["sale"]), sell=float(currency["buy"]))
        return value


class NBUProvider(ProviderBase):
    name = "nbu"

    def get_rate(self) -> SellBuy:
        url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
        response = requests.get(url)
        response.raise_for_status()

        for currency in response.json():
            if currency["cc"] == self.currency_from:
                value = SellBuy(
                    sell=float(currency["rate"]), buy=float(currency["rate"])
                )
                return value
        raise RateNotFound(
            f"Cannot find rate from {self.currency_from} in provider {self.name}"
        )


# class MinFinProvider(ProviderBase):
#     name = 'minfin'
#
#     def get_rate(self) -> SellBuy:
#         url = "https://api.minfin.com.ua/mb/25eaaab96d5319587d8a085786f386cff1561ad7/"
#         response = requests.get(url)
#         response.raise_for_status()
#
#         for currency in response.json():
#             if self.currency_from == "USD":
#                 # currency["currency"] == 'usd'
#                 currency = currency["usd"]
#             elif self.currency_from == "EUR":
#                 currency = currency["eur"]
#             if currency["currency"] == self.currency_from:
#                 value = SellBuy(sell=float(currency["ask"]), buy=float(currency["bid"]))
#                 return value
#             raise RateNotFound(
#                 f"Cannot find rate from {self.currency_from} to {self.currency_to} in provider {self.name}"
#             )


PROVIDERS = [MonoProvider, PrivatbankProvider, VkurseProvider, NBUProvider]
