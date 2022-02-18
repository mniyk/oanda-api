"""OANDA APIを操作するためのモジュール
"""
from datetime import datetime
import logging

from oandapyV20 import API
from oandapyV20.endpoints import accounts, instruments, orders, trades


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

        Examples:
            >>> latest_datetime = datetime.utcnow().timestamp()
            >>> candles = self.api.get_candles(
                'USD_JPY', 'M15', latest_datetime=latest_datetime, count=5000)
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

    def get_pip(self, symbol: str):
        """PIPの取得

        Args:
            symbol (str): 通貨ペア

        Examples:
            >>> self.api.get_pip('USD_JPY')
        """
        request = accounts.AccountInstruments(
            accountID=self.account_id, params={'instruments': symbol})

        response = self.api.request(request)

        pip = 10 ** response['instruments'][0]['pipLocation']

        return pip

    def send_order(self, symbol: str, direction: int, units: int):
        """注文の送信

        Args:
            symbol (str): 通貨ペア
            direction (int): 売買方向
            units (int): 発注数

        Returns:
            dict: 取引内容

        Examples:
            >>> self.api.send_order('USD_JPY', 1, 1)
        """
        data = {
            'order': {
                'instrument': symbol, 
                'units': units * direction, 
                'type': 'MARKET',
                'positionFill': 'DEFAULT'}}

        request = orders.OrderCreate(accountID=self.account_id, data=data)

        response = self.api.request(request)

        if 'orderCancelTransaction' not in response:
            order = {
                'symbol': response['orderFillTransaction']['instrument'],
                'utc': response['orderFillTransaction']['time'],
                'id': response['lastTransactionID'],
                'price': float(response['orderFillTransaction']['price']),
                'units': float(response['orderFillTransaction']['units'])}

            return order
        else:
            raise Exception

    def close_order(self, order_id: str):
        """取引の決済

        Args:
            order_id (str): 取引ID

        Examples:
            >>> 
        """
        request = trades.TradeClose(self.account_id, order_id)

        response = self.api.request(request)

        order = {
            'symbol': response['orderFillTransaction']['instrument'],
            'utc': response['orderFillTransaction']['time'],
            'id': response['lastTransactionID'],
            'price': float(response['orderFillTransaction']['price']),
            'units': float(response['orderFillTransaction']['units']),
            'profit_loss': float(response['orderFillTransaction']['pl']), 
            'open_order_id': order_id}

        return order

    
    def send_profit(
        self, 
        symbol: str, 
        order_id: str, 
        direction: int, 
        price: float, 
        profit_pip: int):
        """指値の送信

        Args:
            symbol (str): 通貨ペア
            trade_id (str): 取引ID
            direction (int): 売買方向
            price (float): 発注時の価格
            profit_pip (int): 指値PIP

        Examples:
            >>> order = self.api.send_order('USD_JPY', 1, 1)
            >>> self.api.send_profit(
                    'USD_JPY', order['id'], 1, order['price'], 20)
        """
        pip = self.get_pip(symbol)
        profit_pip = profit_pip * pip

        profit_rate = (
            price + profit_pip if direction == 1 else price - profit_pip)
        profit_rate = f'{profit_rate:.3f}'

        data = {
            'order': {
                'type': 'TAKE_PROFIT', 
                'tradeID': order_id, 
                'timeInForce': 'GTC', 
                'price': profit_rate}}

        request = orders.OrderCreate(self.account_id, data=data)

        response = self.api.request(request)

        return response

    def send_loss(
        self, 
        symbol: str, 
        order_id: str, 
        direction: int, 
        price: float, 
        loss_pip: int):
        """指値の送信

        Args:
            symbol (str): 通貨ペア
            trade_id (str): 取引ID
            direction (int): 売買方向
            price (float): 発注時の価格
            loss_pip (int): 逆指値PIP
        
        Examples:
            >>> order = self.api.send_order('USD_JPY', 1, 1)
            >>> self.api.send_loss(
                    'USD_JPY', order['id'], 1, order['price'], 20)
        """
        pip = self.get_pip(symbol)
        loss_pip = loss_pip * pip

        loss_rate = price - loss_pip if direction == 1 else price + loss_pip
        loss_rate = f'{loss_rate:.3f}'

        data = {
            'order': {
                'type': 'STOP_LOSS', 
                'tradeID': order_id, 
                'timeInForce': 'GTC', 
                'price': loss_rate}}

        order = orders.OrderCreate(self.account_id, data=data)
        
        response = self.api.request(order)

        return response
