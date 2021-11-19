"""Tests for output module."""
import json
import re
import unittest

from pyhydroquebec.outputter import output_influx, output_json
from datetime import datetime, timedelta

def test_influx_output(capsys):
    """Test influx output function."""

    class MockCustomer:  # pylint: disable=too-few-public-methods
        """Mock class for Customer."""
        contract_id = "foo_customer"
        account_id = "foo_accoutn"
        customer_id = "foo_id"
        balance = "foo_balance"
        current_period = {
            "period_total_bill": "foobar_total_bill", "current_period_data": "current_period_data"
        }
        current_annual_data = {"some_annual_data_key": "foobar_annual_data_value"}
        current_daily_data = {"some_date": {"hour1": {"foobar": "some_data"}}}
        hourly_data = {
            "2021-01-01": {
                "hours": {
                    0: {
                        "average_temperature": 3,
                        "lower_price_consumption": 0.5,
                        "higher_price_consumption": 0,
                        "total_consumption": 0.5
                    },
                    1: {
                        "average_temperature": 4,
                        "lower_price_consumption": 0.53,
                        "higher_price_consumption": 0,
                        "total_consumption": 0.53
                    },
                    2: {
                        "average_temperature": 6,
                        "lower_price_consumption": 0.7,
                        "higher_price_consumption": 0,
                        "total_consumption": 0.7
                    }
                }
            }
        }

    expected = "pyhydroquebec,contract=foo_customer average_temperature=3,lower_price_consumption=0.5," \
        "higher_price_consumption=0,total_consumption=0.5 1609477200000000000\n" \
        "pyhydroquebec,contract=foo_customer average_temperature=4,lower_price_consumption=0.53," \
        "higher_price_consumption=0,total_consumption=0.53 1609480800000000000\n" \
        "pyhydroquebec,contract=foo_customer average_temperature=6,lower_price_consumption=0.7," \
        "higher_price_consumption=0,total_consumption=0.7 1609484400000000000\n"

    mock_customer = MockCustomer()
    output_influx(mock_customer, datetime(2021, 1, 1))
    captured = capsys.readouterr()
    assert re.match(expected, captured.out)


def test_json_output(capsys):
    """Test json output function."""

    data = {
        "overview": {
            "contract_id": "foo_customer",
            "account_id": "foo_accoutn",
            "customer_id": "foo_id",
            "balance": "foo_balance"
        },
        "current_period": {
            "period_total_bill": "foobar_total_bill", "current_period_data": "current_period_data"
        },
        "current_annual_data": {
            "some_annual_data_key": "foobar_annual_data_value"
        },
        "yesterday_data": {
            "date": "some_date",
            "hour1": {
                "foobar": "some_data"
            }
        }
    }

    # \n because of trailing newline in readouterr
    expected = f'{json.dumps(data)}\n'

    class MockCustomer:  # pylint: disable=too-few-public-methods
        """Mock class for Customer."""
        contract_id = "foo_customer"
        account_id = "foo_accoutn"
        customer_id = "foo_id"
        balance = "foo_balance"
        current_period = {
            "period_total_bill": "foobar_total_bill", "current_period_data": "current_period_data"
        }
        current_annual_data = {"some_annual_data_key": "foobar_annual_data_value"}
        current_daily_data = {"some_date": {"hour1": {"foobar": "some_data"}}}

    mock_customer = MockCustomer()
    output_json(mock_customer)
    captured = capsys.readouterr()

    assert captured.out == expected
