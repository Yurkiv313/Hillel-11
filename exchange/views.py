from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from exchange.forms import RateForm
from exchange.models import Rate


def main_view(request):
    response_data = {
        "current_rates": [
            {
                "id": rate.id,
                "date": rate.date,
                "vendor": rate.provider,
                "currency_a": rate.currency_from,
                "currency_b": rate.currency_to,
                "sell": rate.sell,
                "buy": rate.buy,
            }
            for rate in Rate.objects.all()
        ]
    }
    return JsonResponse(response_data)


def exchange_rate(request):
    form = RateForm(request.POST or None)

    if request.method == "GET":
        return render(request, "exchange_rate.html", {"form": form})
    if request.method == "POST":
        amount = float(request.POST["amount"])
        from_currency = request.POST["from_currency"]
        to_currency = request.POST["to_currency"]
        results = Rate.objects.filter(
            currency_from=from_currency, currency_to=to_currency
        ).order_by("buy")
        result = (
            Rate.objects.filter(currency_from=from_currency, currency_to=to_currency)
            .order_by("buy")
            .first()
        )
        if result is None:
            return HttpResponse("ERROR")
        rate = result.buy if result.currency_from == from_currency else result.sell
        amount_in_to_currency = amount * float(rate)

        return render(
            request,
            "exchange_rate.html",
            {
                "form": form,
                "amount_in_to_currency": amount_in_to_currency,
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
            },
        )
    else:
        return HttpResponse("ERROR")
