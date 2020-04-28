import datetime

from ing_api import IngClient

# set up cookie
cookie = 'copied value of Cookie header from browser'

api = IngClient(cookie)

# get information about the client
client = api.client()

# get all products of the client
products = api.products()

# get list of transactions (movements), see more arguments
product_id = 'uuid'
from_date = datetime.date(1970, 1, 1)
movements = api.movements(product_id, from_date=from_date)

# get transaction (movement) detail
movement = api.movement('uuid')
