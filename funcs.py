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
    acc_type = users_table.all(formula=formula)
    us_type = acc_type[0]["fields"].get("User Type")

    if usern:
        password = usern[0]["fields"].get("Password")
        if password == p_e:
            create_user_logs(u,'Logged in.')
            if us_type == 'admin':
                return True,True  # Auth success and user is an admin
            else:
                return True,False #Auth success and user is NOT an admin
        else:
            return False,False  # Wrong password
    else:
        return False,False  # No such user
    


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
            new_order=orders_table.create({
                "Customer":name,
                "Status":"Fulfilled",
                "Item":title,
                "Customer Phone":p,
                "Date / Time":gr_time.isoformat(sep=' ', timespec='seconds')
            })
            create_user_logs(u,"Created order (Phone: %d )"%p)
            order_num = new_order["fields"].get("Order ID")
            return "Η παραγγελία καταχωρήθηκε. Αριθμός: %d"%order_num
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
    
def edit_customer(o_p,n,n_p,n_e,n_n,u):
    formula = f"{{Phone}} = {o_p}"
    customer = customers_table.all(formula=formula)
    if customer:
        cust_id = customer[0]["id"]
        customers_table.update(cust_id,{
            "Name":n,
            "Phone":n_p,
            "Email":n_e,
            "Notes":n_n
        })
        create_user_logs(u,"Edit customer %d"%o_p)
        return 'Η επεξέργασια πελάτη καταχωρήθηκε'
    else:
        return 'Δεν υπάρχει πελάτης με αυτόν τον αριθμό. Δοκίμαστε ξάνα'


def c_check_name(p):
    formula = f"{{Phone}} = {p}"
    records = customers_table.all(formula=formula)
    if records:
        name = records[0]["fields"].get("Name")
        return name
    else:
        return 'ERROR'
    
def c_check_email(p):
    formula = f"{{Phone}} = {p}"
    records = customers_table.all(formula=formula)
    if records:
        email = records[0]["fields"].get("Email")
        return email
    else:
        return 'ERROR'
    

def c_check_notes(p):
    formula = f"{{Phone}} = {p}"
    records = customers_table.all(formula=formula)
    if records:
        notes = records[0]["fields"].get("Notes")
        return notes
    else:
        return 'ERROR'

def new_product(t,p,u):
    new_p=products_table.create({
        "Title":t,
        "Price":p,
        })
    create_user_logs(u,"Create product.")
    sku = new_p["fields"].get("SKU")
    return f"Το προϊόν προστέθηκε επιτυχώς! SKU: {sku}"
    

def check_orders(id):
    formula=f"{{Order ID}} = {id}"
    res = orders_table.all(formula=formula)
    if res:
        cust = res[0]["fields"].get("Customer")
        stat = res[0]["fields"].get("Status")
        item = res[0]["fields"].get("Item")
        date = res[0]["fields"].get("Date / Time")
        return True,f'Αρ. Παραγγελίας: {id} \n Όνομα: {cust} \n Κατάσταση {stat} \n Προϊόν {item} \n Ημερομηνία: {date}'
    else:
        return False,'Δεν βρέθηκε η παραγγελία'

def modify_status(id,n,u):
    formula=f"{{Order ID}} = {id}"
    res = orders_table.all(formula=formula)
    if res:  
        r_id = res[0]["id"]
        orders_table.update(r_id,{
            "Status":n
        })
        create_user_logs(u,f'Change order {id} status to {n}')
        return 'Η κατάσταση παραγγελίας άλλαξε'
    else:
        return 'Δεν βρέθηκε η παραγγελία'

def modify_product(n_t,n_p,sku,u):
    formula = f"{{SKU}} = {sku}"
    find_prod = products_table.all(formula=formula)
    if find_prod:
        p_id = find_prod[0]["id"]
        products_table.update(p_id,{
            "Title":n_t,
            "Price":n_p
        })
        create_user_logs(u,f"Edit product {sku}")
        return f'Το προϊόν {sku} επεξεργάστηκε.'
    else:
        return f'Δεν βρέθηκε προϊόν με αυτόν τον κωδικό.'

def check_product(sku):
    formula = f"{{SKU}} = {sku}"
    res = products_table.all(formula=formula)
    if res:
        return True
    else:
        return False
    
def old_prod_title(sku):
    formula=f"{{SKU}} ={sku}"
    titles = products_table.all(formula=formula)
    title=titles[0]["fields"].get("Title")
    return title

def old_prod_price(sku):
    formula=f"{{SKU}} ={sku}"
    prices = products_table.all(formula=formula)
    price=prices[0]["fields"].get("Price")
    return price


def new_user(o_u,n_u,pwd,u_t):
    formula = f"{{Username}} = '{n_u}'"
    us_check = users_table.all(formula=formula)
    if us_check:
        return 'Υπάρχει ήδη χρήστης με αυτό το όνομα'
    else:
        users_table.create({
            "Username":n_u,
            "Password":hashlib.sha256(pwd.encode()).hexdigest(),
            "User Type":u_t
        })
        create_user_logs(o_u,f"Create {n_u} as {u_t}")
        return 'Ο χρήσητης αποθηκεύτηκε και μπορεί να συνδεθεί'
    
def del_user(c_u,d_u):
    formula = f"{{Username}} = '{d_u}'"
    res = users_table.all(formula=formula)
    if res:
        user = res[0]["id"]
        users_table.delete(user)
        create_user_logs(c_u,f"Delete user: {d_u}")
        return 'Ο χρήστης διαγράφηκε!'
    else:
        return 'Δεν βρέθηκε χρήστης με αυτό το όνομα!'

    