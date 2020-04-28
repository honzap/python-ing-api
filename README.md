# ING Bank Python Client

Python interface for ING Bank internet banking.

Provided class enables very simple interface to read data from API 
provided by ING Bank. This service is currently deployed in 
[Czechia](https://ib.ing.cz/transactional-cz/) where the library 
has been tested.

## Usage

For the usage the `requirements.txt` must be installed to the 
environment.
```bash
pip3 install -r requirements.txt
```

### Before Using
Before using the library you should log in into the Internet Banking.
- [Czechia](https://ib.ing.cz/transactional-cz/)

When the login process is done and you're successfully logged in open 
the developer console of the browser. You should there network requests 
and take of of the requests going to bank API. It should contain the 
`/rest` part in the path. Then, find `Request headers` and there 
the `Cookie` header. Copy the whole value of the header and use it to
 set up the `IngClient`. 
 
> Keep in mind that you should stay logged in when you would like to
 run the script. 

### Initialize code
```python
from ing_api import IngClient

# set up cookie
cookie = 'copied value of Cookie header from browser'
api = IngClient(cookie)
```

### Get information about the client
```python
client = api.client()
```

### Get all products of the client
```python
products = api.products()
```

### Get list of transactions (movements)
In the terminology of the API the transactions are called movements.  

```python
product_id = 'uuid'
from_date = datetime.date(1970, 1, 1)
movements = api.movements(product_id, from_date=from_date)
print(movements['count'])
```

Arguments are:
- `product_uuid` - UUID of selected product
- `from_date` - starting date (required)
- `to_date` - ending date of selection (default is today)
- `limit` - number of items which should be loaded once - pagination (default: 25)
- `offset` - offset for pagination (default: 0)

### Get transaction (movement) detail
The information provided in the list of movements is not complete. For 
the detailed information the detail should be called.

```python
movement = api.movement('uuid')
```

## License
The *python-ing-api* is free and open-source software under [MIT License](LICENSE).