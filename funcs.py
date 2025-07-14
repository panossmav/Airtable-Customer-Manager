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
            create_user_logs(u,'Logged in.')
            return True  # Auth success
        else:
            return False  # Wrong password
    else:
        return False  # No such user
    


def create_user_logs(u,act):
    logs_table.create(
        {"User":u,
        "Action":act,
        "Date / Time":gr_time.isoformat(sep=' ', timespec='seconds')})


def new_order(p,sku,u):
    formula_n = f"{{Phone}} = {p}"
    check_cust = customers_table.all(formula=formula_n,fields=["Name"])
    if check_cust:
        name = check_cust[0]["fields"].get("Name")
    else:
        name = None

    formula_t = f"{{SKU}} = {sku}"
    check_prod = products_table.all(formula=formula_t, fields=["Title"])
    if check_prod:
        title = check_prod[0]["fields"].get("Title")
    else:
        title = None
    

    if name:
        if title:
            orders_table.create({
                "Customer":name,
                "Status":"Fulfilled",
                "Item":title,
                "Customer Phone":p,
                "Date / Time":gr_time.isoformat(sep=' ', timespec='seconds')
            })
            create_user_logs(u,"Created order (Phone: %d )"%p)
            return "Η παραγγελία καταχωρήθηκε"
        else:
            return "Σφάλμα! Το προϊόν δεν υπάρχει!"
    else:
        return "Σφάλμα! το όνομα δεν υπάρχει!"


def new_customer(n,p,e,notes,user):
    formula = f"{{Phone}} = {p}"
    check_p_ex=customers_table.all(formula=formula,fields=["Phone"])
    if check_p_ex:
        return 'Υπάρχει ήδη πελάτης με αυτό το τηλέφωνο!'
    else:
        customers_table.create({
            "Name":n,
            "Notes":notes,
            "Phone":p,
            "Email":e
        })
        create_user_logs(user,"Add customer (Phone: %d)"%p)
        return 'Ο πελάτης καταχωρήθηκε!'