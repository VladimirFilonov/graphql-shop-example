# https://www.freeforexapi.com/api/live?pairs=USDRUB
import requests 
from redis import Redis
from rq import Queue
from rq.decorators import job
from rq_scheduler import Scheduler
from datetime import datetime, timedelta

redis_conn = Redis()

@job("default", connection=redis_conn)
def get_currency_rate(currency):
    pair = "{}RUB".format(currency)
    response = requests.get(
        "https://www.freeforexapi.com/api/live?pairs={}".format(pair)
    )
    data = response.json()
    return data['rates'][pair]['rate']

#sheduler = Scheduler(connection=redis_conn)
#sheduler.enqueue_at(datetime(2019, 7, 4, 21, 7), get_currency_rate, 'USD')