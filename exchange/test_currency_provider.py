import responses
from unittest.mock import MagicMock, patch
from exchange.currency_provider import MonoProvider, SellBuy


# Create your tests here.


def test_mono_currency_provider():
    print("foo")
    provider = MonoProvider("USD", "UAH")
    rate_mocked = MagicMock(return_value=SellBuy(sell=27.0, buy=27.0))
    provider.get_rate = rate_mocked
    rate = provider.get_rate()
    assert rate == SellBuy(sell=27.0, buy=27.0)
    rate_mocked.assert_called()


@responses.activate
def test_mono_with_data():
    responses.get(
        "https://api.monobank.ua/bank/currency",
        json=[
            {
                "currencyCodeA": 840,
                "currencyCodeB": 980,
                "rateBuy": 28.0,
                "rateSell": 28.0,
            }
        ],
    )
    provider = MonoProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=28.0, buy=28.0)
