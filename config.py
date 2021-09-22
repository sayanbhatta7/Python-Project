from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


DEBUG = True
try:
    client = MongoClient('mongodb://%s:%s@127.0.0.1' % ('admin', 'admin'))
    DATABASE = client['BankSystem']               # Database Name

except ConnectionFailure as e:
    print("Connection Error:", e)