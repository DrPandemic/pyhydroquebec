"""PyHydroQuebec Output Module.

This module defines the different output functions:
* text
* influxdb
* json
"""
from datetime import datetime, timedelta
import json

from pyhydroquebec.consts import (OVERVIEW_TPL,
                                  CONSUMPTION_PROFILE_TPL,
                                  YESTERDAY_TPL, ANNUAL_TPL, HOURLY_HEADER, HOURLY_TPL, HQ_TIMEZONE)


def output_text(customer, show_hourly=False):
    """Format data to get a readable output."""
    print(OVERVIEW_TPL.format(customer))
    if customer.current_period['period_total_bill']:
        print(CONSUMPTION_PROFILE_TPL.format(d=customer.current_period))
    if customer.current_annual_data:
        print(ANNUAL_TPL.format(d=customer.current_annual_data))
    yesterday_date = list(customer.current_daily_data.keys())[0]
    data = {'date': yesterday_date}
    data.update(customer.current_daily_data[yesterday_date])
    print(YESTERDAY_TPL.format(d=data))
    if show_hourly:
        print(HOURLY_HEADER)
        for hour, data in customer.hourly_data[yesterday_date]["hours"].items():
            print(HOURLY_TPL.format(d=data, hour=hour))


def output_influx(customer, yesterday=datetime.now(HQ_TIMEZONE) - timedelta(days=1)):
    """Print data using influxDB format."""
    yesterday = yesterday.replace(minute=0, hour=0, second=0, microsecond=0)

    for hour, content in customer.hourly_data[yesterday.strftime("%Y-%m-%d")]['hours'].items():
        msg = "pyhydroquebec,contract={} {} {}"

        data = ",".join(["{}={}".format(key, value) for key, value in content.items()])

        yesterday = yesterday.replace(hour=hour)
        yesterday_str = str(int(yesterday.timestamp() * 1000000000))

        print(msg.format(customer.contract_id, data, yesterday_str))


def output_json(customer, show_hourly=False):
    """Print data as a json."""
    out = {}
    out['overview'] = {
        "contract_id": customer.contract_id,
        "account_id": customer.account_id,
        "customer_id": customer.customer_id,
        "balance": customer.balance
    }
    if customer.current_period['period_total_bill']:
        out["current_period"] = customer.current_period
    if customer.current_annual_data:
        out["current_annual_data"] = customer.current_annual_data
    yesterday_date = list(customer.current_daily_data.keys())[0]
    yesterday_data = {'date': yesterday_date}
    yesterday_data.update(customer.current_daily_data[yesterday_date])
    out["yesterday_data"] = yesterday_data
    if show_hourly:
        out["hourly_data"] = []
        for hour, data in customer.hourly_data[yesterday_date]["hours"].items():
            hourly_object = {"hour": hour}
            hourly_object.update(data)
            out["hourly_data"].append(hourly_object)
    print(json.dumps(out))
