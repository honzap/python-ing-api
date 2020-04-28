"""
ing_api
~~~~~~~~~~~~

This module implements provides a simple interface for ING Bank.

:copyright: (c) 2020 by Jan Pecek.
:license: MIT, see LICENSE for more details.
"""

from datetime import date

import requests


class IngClient:
    """
    ING Client provides simple interface to connect to ING Bank API (currently deployed in CZ)

    Instantiate with: IngClient(cookie)

        cookie - Cookie header copied from web browser

    Usage::

      >>> import datetime
      >>> from ing_api import IngClient
      >>> cookie = 'copied value of Cookie header from browser'
      >>> api = IngClient(cookie)
      >>> # get information about the client
      >>> client = api.client()
      >>> # get all products of the client
      >>> products = api.products()
      >>> # get list of transactions (movements), see more arguments
      >>> product_id = 'uuid'
      >>> from_date = datetime.date(1970, 1, 1)
      >>> movements = api.movements(product_id, from_date=from_date)
      >>> # get transaction (movement) detail
      >>> movement = api.movement('uuid')
    """

    _BASE_URL = 'https://ib.ing.cz/genoma_api/rest'
    _REFERER = 'https://ib.ing.cz/transactional-cz/'

    _USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'

    _HEADERS = {
        'User-Agent': _USER_AGENT,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': _REFERER,
        'Content-Type': 'application/json; charset=utf-8',
        'X-Requested-With': 'XMLHttpRequest'
    }

    _GENOMA_SESSION_NAME = 'genoma-session-id'

    _CLIENT_PATH = '/client'
    _PRODUCTS_PATH = '/products'
    _PRODUCT_PATH = _PRODUCTS_PATH + '/%s'
    _MOVEMENTS_PATH = _PRODUCT_PATH + '/movements'
    _MOVEMENT_PATH = '/movements/%s'

    def __init__(self, cookie):
        self._cookie = cookie
        self._genoma_session_id = self._extract_genoma_session_id(cookie)

    def client(self):
        r"""
        Get logged client information

        :return: JSON object with result
        """
        response = requests.get(self._url(self._CLIENT_PATH), headers=self._headers)
        return response.json()

    def products(self):
        r"""Get list of products

        :return: JSON object with result
        """
        response = requests.get(self._url(self._PRODUCTS_PATH), headers=self._headers)
        return response.json()

    def movements(self, product_uuid, from_date, to_date=date.today(), limit=25, offset=0):
        r"""Get list of movements for specific product

        :param product_uuid: UUID of product
        :type product_uuid: str
        :param from_date: starting date of the selection
        :type from_date: date
        :param to_date: ending date of the selection (default today)
        :type to_date: date
        :param limit: number of items which should be loaded
        :type limit: int
        :param offset: offset for pagination
        :type offset: int
        :return: JSON object with result
        """
        params = {
            'fromDate': from_date.strftime('%d/%m/%Y'),
            'toDate': to_date.strftime('%d/%m/%Y'),
            'limit': limit,
            'offset': offset
        }
        response = requests.get(self._url(self._MOVEMENTS_PATH % product_uuid), params=params, headers=self._headers)
        return response.json()

    def movement(self, movement_uuid):
        r"""Get one movement (transaction) details

        :param movement_uuid: UUID of movement
        :type movement_uuid: str
        :return: JSON object with result
        """
        response = requests.get(self._url(self._MOVEMENT_PATH % movement_uuid), headers=self._headers)
        return response.json()

    def _url(self, path):
        return '%s%s' % (self._BASE_URL, path)

    def _extract_genoma_session_id(self, cookie):
        return [el for el in cookie.split(';') if self._GENOMA_SESSION_NAME in el][0].split('=')[1]

    @property
    def _headers(self):
        headers = self._HEADERS.copy()
        headers['Cookie'] = self._cookie
        headers[self._GENOMA_SESSION_NAME] = self._genoma_session_id
        return headers
