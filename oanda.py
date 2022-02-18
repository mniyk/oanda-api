"""OANDA APIを操作するためのモジュール
"""
from datetime import datetime
import logging

from oandapyV20 import API
from oandapyV20.endpoints import instruments


logger = logging.getLogger(__name__)


class Oanda:
    def __init__(self, account_id: str, access_token: str) -> None:
        """初期化

        Args:
            account_id (str): アカウントID
            access_token (str): アクセストークン

        Examples:
            >>> api = Oanda(account_id='test_id', access_token='test_token')
        """
        self.account_id = account_id
        self.access_token = access_token
        self.api = None

    def connect(self, environment: str='practice') -> None:
        """接続

        Args:
            environment (str): 環境

        Examples:
            >>> api.connect('live')
        """
        self.api = API(
            access_token=self.access_token,
            environment=environment)

    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        count: int=None,
        latest_datetime: datetime=None):
        """ローソク足データの取得

        Args:
            symbol (str): 通貨ペア
            timeframe (str): ローソク足時間
            count (int): データ数
            latest_datetime (datetime): 取得する最新の日時
        """
        params = {'granularity': timeframe}

        if count is None and latest_datetime is None:
            raise Exception

        if count is not None:
            params.setdefault('count', count)
        
        if latest_datetime is not None:
            params.setdefault('from', latest_datetime)

        request = instruments.InstrumentsCandles(
            instrument=symbol, params=params)
        
        response = self.api.request(request)

        return response['candles']
