"""oanda.pyのunittest
"""
import configparser
from datetime import datetime
from itertools import count
import logging
import unittest

from oanda import Oanda


logging.basicConfig(
    level=logging.INFO,
    format='\t'.join([
        '%(asctime)s',
        '%(levelname)s',
        '%(filename)s',
        '%(funcName)s',
        '%(processName)s',
        '%(process)d',
        '%(threadName)s',
        '%(thread)d',
        '%(message)s']))
logger = logging.Logger(__name__)


class TestOanda(unittest.TestCase):
    def setUp(self) -> None:
        config = configparser.ConfigParser()
        config.read('settings.ini')

        self.api = Oanda(
            account_id=config.get('OANDA', 'ACCOUNT_ID'),
            access_token=config.get('OANDA', 'ACCESS_TOKEN'))

        self.api.connect('live')

    def test_get_candles(self) -> None:
        latest_datetime = datetime.utcnow().timestamp()

        candles = self.api.get_candles(
            'USD_JPY', 'M15', latest_datetime=latest_datetime, count=5000)

        print(candles)

    def test_get_pip(self) -> None:
        self.api.get_pip('USD_JPY')

    def test_send_order(self) -> None:
        print(self.api.send_order('USD_JPY', 1, 1))
