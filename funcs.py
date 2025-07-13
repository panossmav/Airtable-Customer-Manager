from datetime import *
import pyairtable
import os
import dotenv
from pyairtable import Api
import hashlib
import pytz

gr_time = datetime.now(pytz.timezone("Europe/Athens"))

dotenv.load_dotenv()

api_key = os.getenv("airtable_api") 
base_id = os.getenv("db_id")

api=Api(api_key)
customers_table = api.table(base_id,"Customers")
products_table = api.table(base_id,"Products")
orders_table = api.table(base_id,"Orders")
users_table = api.table(base_id,"App users")
logs_table = api.table(base_id,"User Logs")


def check_user_pass(u, p):
    p_e = hashlib.sha256(p.encode()).hexdigest()
    formula = f"{{Username}} = '{u}'"
    usern = users_table.all(formula=formula, fields=["Password"])
    if usern:
        password = usern[0]["fields"].get("Password")
        if password == p_e:
            return True  # Auth success
        else:
            return False  # Wrong password
    else:
        return False  # No such user
    


def create_user_logs(u,act):
    logs_table.create({"User":u,"Action":act,"Date / Time":gr_time.isoformat(sep=' ', timespec='seconds')})


