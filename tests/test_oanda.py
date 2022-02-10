"""oanda.pyのunittest
"""
import configparser
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
