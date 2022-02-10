"""OANDA APIを操作するためのモジュール
"""
import logging


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
