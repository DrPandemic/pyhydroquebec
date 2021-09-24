"""Prometheus Server which collected Hydroquebec Data.

Waits for Prometheus HTTP requests.
"""
from aiohttp import web
from datetime import datetime, timedelta
import os

from pyhydroquebec.client import HydroQuebecClient
from pyhydroquebec.consts import DAILY_MAP, CURRENT_MAP, HQ_TIMEZONE


class PrometheusServer:
    def __init__(self):
        self.username = os.environ['PYHQ_USER']
        self.password = os.environ['PYHQ_PASSWORD']
        self.contract = os.environ['PYHQ_CONTRACT']
        self.log_level = os.environ.get('PYHQ_LOG_LEVEL', 'INFO')
        self.client = HydroQuebecClient(self.username,
                                        self.password,
                                        30,
                                        log_level=self.log_level)

    async def daily(self, request):
        await self.client.login()

        customer = None
        for client_customer in self.client.customers:
            if str(client_customer.contract_id) == str(self.contract):
                customer = client_customer

        if customer is None:
            self.logger.warning('Contract %s not found', contract_data['id'])
            return

        yesterday = datetime.now(HQ_TIMEZONE) - timedelta(days=1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        await customer.fetch_hourly_data(yesterday_str)
        if not customer.hourly_data:
            self.logger.warning('Failed to fetch data')

        content = ""

        data = customer.hourly_data[yesterday_str]['hours']
        # Since Prometheus can't ingest "old" data, we'll be lying about it's timestamp and insert it 24h late.
        # https://github.com/prometheus/prometheus/issues/7396#issuecomment-649451086
        today = datetime.now(HQ_TIMEZONE).replace(hour=0, minute=0, second=0, microsecond=0)
        timestamp = (today + timedelta(hours=yesterday.hour)).timestamp() * 1000
        result = []
        for metric_name in DAILY_MAP:
            result.append(self.add_metric(metric_name, data[yesterday.hour], timestamp))

        return web.Response(text="".join(result))

    def headers(self, metric_type):
        if metric_type == "lower_price_consumption":
            return """
# HELP hydroquebec_hourly_lower_price_consumption The number of kWh used at lower price in 1 hour.
# TYPE hydroquebec_hourly_lower_price_consumption histogram
        """
        elif metric_type == "higher_price_consumption":
            return """
# HELP hydroquebec_hourly_higher_price_consumption The number of kWh used at higher price in 1 hour.
# TYPE hydroquebec_hourly_higher_price_consumption histogram
        """
        elif metric_type == "total_consumption":
            return """
# HELP hydroquebec_hourly_total_consumption The number of kWh used in 1 hour.
# TYPE hydroquebec_hourly_total_consumption histogram
        """
        elif metric_type == "average_temperature":
            return """
# HELP hydroquebec_hourly_average_temperature The average temperature over 1 hour.
# TYPE hydroquebec_hourly_average_temperature gauge
        """
        else:
            return ""

    def add_metric(self, metric_type, data, timestamp):
        header = self.headers(metric_type).strip(" ")
        return "{}hydroquebec_hourly_{} {} {:.0f}\n".format(header,
                                                            metric_type,
                                                            data[metric_type],
                                                            timestamp)

    def run(self):
        app = web.Application()
        app.add_routes([web.get('/daily', self.daily)])
        web.run_app(app)
