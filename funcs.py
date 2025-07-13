from datetime import *
import pyairtable
import os
import dotenv
from pyairtable import Api

dotenv.load_dotenv()

api_key = os.getenv("airtable_api") 
base_id = os.getenv("db_id")

api=Api(api_key)
customers_table = api.table(base_id,"Customers")
products_table = api.table(base_id,"Products")
orders_table = api.table(base_id,"Orders")
users_table = api.table(base_id,"App users")
logs_table = api.table(base_id,"User Logs")


