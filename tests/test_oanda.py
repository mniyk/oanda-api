"""oanda.pyのunittest
"""
import configparser
import logging
import unittest

from oanda.oanda import Oanda


logging.basicConfig(
    level=logging.DEBUG,
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

logger = logging.getLogger(__name__)


class TestOanda(unittest.TestCase):
    def setUp(self) -> None:
        config = configparser.ConfigParser()
        config.read('settings.ini')

        self.api = Oanda(
            account_id=config.get('OANDA', 'ACCOUNT_ID'),
            access_token=config.get('OANDA', 'ACCESS_TOKEN'))

        self.api.connect('live')

    def test_get_candles(self) -> None:
        latest_datetime = '2022-03-18T00:00:00.000000000Z'

        candles = self.api.get_candles(
            'USD_JPY', 'M15', latest_datetime=latest_datetime, count=5000)

        logger.debug(candles)

    def test_get_pip(self) -> None:
        logger.debug(self.api.get_pip('USD_JPY'))

    def test_send_order(self) -> None:
        logger.debug(self.api.send_order('USD_JPY', 1, 1))

    def test_close_order(self) -> None:
        logger.debug(self.api.close_order('14361'))

    def test_send_profit(self) -> None:
        order = self.api.send_order('USD_JPY', 1, 1)

        logger.debug(
            self.api.send_profit(
                'USD_JPY', order['id'], 1, order['price'], 20))

    def test_send_loss(self) -> None:
        order = self.api.send_order('USD_JPY', 1, 1)
        
        logger.debug(
            self.api.send_loss(
                'USD_JPY', order['id'], 1, order['price'], 20))
