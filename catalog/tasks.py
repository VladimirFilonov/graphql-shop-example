import requests
from time import sleep
from catalog.models import CurrencyRate
from catalog_queue.queue_manager import TaskQueue
from datetime import datetime


def get_currency_rate(currency):
    pair = "{}RUB".format(currency.upper())
    response = requests.get(
        "https://www.freeforexapi.com/api/live?pairs={}".format(pair)
    )
    data = response.json()
    return data['rates'][pair]['rate']

def update_currency_rates():
    queryset = CurrencyRate.objects.all()
    for rate in queryset:
        rate.rate = get_currency_rate(rate.currency)
        rate.save(update_fields=['rate'])
    return True


def fake_scheduler():
    queue = TaskQueue()
    print(datetime.now())
    sleep(1)
    queue.enqueue(fake_scheduler)