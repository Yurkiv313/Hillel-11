import datetime

from celery import shared_task

from .currency_provider import PROVIDERS
from .models import Rate


@shared_task
def pull_rate():
    date = datetime.date.today()
    for provider_class in PROVIDERS:
        provider_eur = provider_class(
            "EUR",
            "UAH",
        )
        print("EUR", provider_eur.name)

        eur = Rate.objects.filter(
            currency_from="EUR",
            currency_to="UAH",
            provider=provider_eur.name,
            date=date,
        )
        if not eur.exists():
            print("Record for EUR and", provider_eur.name, "not found, creating.")
            euro_rate = provider_eur.get_rate()
            eur = Rate.objects.create(
                currency_from="EUR",
                currency_to="UAH",
                sell=euro_rate.sell,
                buy=euro_rate.buy,
                provider=provider_eur.name,
                date=date,
            )
            print("Created euro exchange rate with ID", eur.id)

        provider_usd = provider_class("USD", "UAH")
        print("USD", provider_usd.name)

        usd = Rate.objects.filter(
            currency_from="USD",
            currency_to="UAH",
            provider=provider_usd.name,
            date=date,
        )
        if not usd.exists():
            print("Record for USD and", provider_usd.name, "not found, creating.")

            usd_rate = provider_usd.get_rate()
            usd = Rate.objects.create(
                currency_from="USD",
                currency_to="UAH",
                provider=provider_usd.name,
                date=date,
                sell=usd_rate.sell,
                buy=usd_rate.buy,
            )
            print("Created USD exchange rate with ID", usd.id)
