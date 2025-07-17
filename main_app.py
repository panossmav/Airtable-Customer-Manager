from tkinter import *
import tkinter as tk
from funcs import *
from tkinter import ttk

app=tk.Tk()
app.geometry('500x500')
app.title('Airtable Customer / Order Manager')

tk.Label(app,text='Username: ').pack()
username_e = Entry(app)
username_e.pack()
tk.Label(app,text='Password: ').pack()
passw_e = Entry(app,show='•')
passw_e.pack()


def clear_app():
    for widget in app.winfo_children():
        widget.pack_forget()



def create_order():
    clear_app()
    tk.Label(app,text='Κινητό πελάτη: ').pack()
    phone_e = Entry(app)
    phone_e.pack()
    tk.Label(app,text='Κωδικός προϊόντος: ').pack()
    sku_e = Entry(app)
    sku_e.pack()
    def sbt_order_create():
        phone = int(phone_e.get())
        sku = int(sku_e.get())
        creation = new_order(phone,sku,username)
        fin_var = tk.StringVar(value=creation)
        tk.Label(app,textvariable=fin_var).pack()
    tk.Button(app,text='Καταχώρηση παραγγελίας',command=sbt_order_create).pack()
    tk.Button(app,text='Πίσω -->',command=home).pack()

def create_customer():
    clear_app()
    tk.Label(app,text='Ονοματεπώνυμο: ').pack()
    name_e = Entry(app)
    name_e.pack()
    tk.Label(app,text='Τηλέφωνο: ').pack()
    phone_e = Entry(app)
    phone_e.pack()
    tk.Label(app,text='Email:').pack()
    email_e = Entry(app)
    email_e.pack()
    tk.Label(app,text='Δώσε σημειώσεις (Προαιρετικό):').pack()
    notes_e = Entry(app)
    notes_e.pack()
    def sbt_customer_create():
        name = name_e.get()
        phone = int(phone_e.get())
        email = email_e.get()
        notes = notes_e.get()
        if not(notes):
            notes = 'None'
        res = new_customer(name,phone,email,notes,username)
        res_var = tk.StringVar(value=res)
        tk.Label(app,textvariable=res_var).pack()
    tk.Button(app,text='Καταχώρηση πελάτη',command=sbt_customer_create).pack()
    tk.Button(app,text='Πίσω -->',command=home).pack()

def update_customer():
    clear_app()
    tk.Label(app,text='Τρέχον τηλέφωνο:').pack()
    old_phone_e = Entry(app)
    old_phone_e.pack()

    tk.Label(app,text='Εισάγετε νέα στοιχέια: \n (Αφήστε κενά τα στοιχεία που θέλετε να παραμείνουν ιδια) \n').pack()
    
    tk.Label(app,text='Τηλέφωνο: ').pack()
    new_phone_e = Entry(app)
    new_phone_e.pack()
    tk.Label(app,text='Ονόμα: ').pack()
    new_name_e = Entry(app)
    new_name_e.pack()
    tk.Label(app,text='Email: ').pack()
    new_email_e = Entry(app)
    new_email_e.pack()
    tk.Label(app,text='Σημειώσεις: ').pack()
    new_notes_e = Entry(app)
    new_notes_e.pack()

    def sbt_udt_cust():
        old_phone = int(old_phone_e.get())
        new_phone = new_phone_e.get()
        new_name = new_name_e.get()
        new_email = new_email_e.get()
        new_notes = new_notes_e.get()
        if not new_phone:
            new_phone = old_phone
        else:
            new_phone = int(new_phone)
        if not new_name:
            new_name = c_check_name(old_phone)
        if not new_email:
            new_email = c_check_email(old_phone)
        if not new_notes:
            new_notes = c_check_notes(old_phone)
        res = edit_customer(old_phone,new_name,new_phone,new_email,new_notes,username)
        res_var = tk.StringVar(value=res)
        tk.Label(app,textvariable=res_var).pack()
    tk.Button(app,text='Επεξεργασία',command=sbt_udt_cust).pack()
    tk.Button(app,text='Πίσω -->',command=home).pack()     
        
    
def create_product():
    clear_app()
    tk.Label(app,text='Τίτλος προϊόντος: ').pack()
    tit_e = Entry(app)
    tit_e.pack()
    tk.Label(app,text='Δώσε τιμή').pack()
    pr_e=Entry(app)
    pr_e.pack()


    def sbt_prod_create():
        title = tit_e.get()
        price = float(pr_e.get())
        price = round(price,2)
        res = new_product(title,price,username)
        res_tk = tk.StringVar(value=res)
        tk.Label(app,textvariable=res_tk).pack()

    tk.Button(app,text='Δημιουργία προϊόντος',command=sbt_prod_create).pack()
    tk.Button(app,text='Πίσω -->',command=home).pack()


def modify_order():
    clear_app()
    tk.Label(app,text='Αριθμός παραγγελίας: ').pack()
    id_e = Entry(app)
    id_e.pack()
    def find_order():
        o_id = int(id_e.get())
        db_search,result = check_orders(o_id)
        def found():
            tk.Label(app,text='Νέο Status:').pack()
            status_e = Entry(app)
            status_e.pack()
            def sbt_found():
                status = status_e.get()
                res = modify_status(o_id,status,username)
                res_var = tk.StringVar(value=res)
                tk.Label(app,textvariable=res_var).pack()
            tk.Button(app,text='Αλλαγή κατάστασης',command=sbt_found).pack()
            tk.Button(app,text='Πίσω -->',command=modify_order).pack()
        if db_search == True:
            clear_app()
            result=tk.StringVar(value=result)
            tk.Label(app,textvariable=result).pack()
            found()
        else:
            result=tk.StringVar(value=result)
            tk.Label(app,textvariable=result).pack()            
    tk.Button(app,text='Αναζήτηση παραγγελίας',command=find_order).pack()
    tk.Button(app,text='Πίσω -->',command=home).pack()

def edit_prod():
    clear_app()
    tk.Label(app,text='SKU').pack()
    sku_e = Entry(app)
    sku_e.pack()
    def sbt_ed_pr():
        sku = int(sku_e.get())
        def found_prod():
            clear_app()
            tk.Label(app,text=f"SKU: {sku} \n Τίτλος: {old_prod_title(sku)} \n Τιμή: {old_prod_price(sku)}").pack()
            tk.Label(app,text='Εισάγετε αλλαγές \n Αφηστε κενό για διατήρηση')
            tk.Label(app,text='Νέος τίτλος').pack()
            n_title_e = Entry(app)
            n_title_e.pack()
            tk.Label(app,text='Νέα τιμή').pack()
            n_p_e = Entry(app)
            n_p_e.pack()
            def sbt_found_prod():
                n_title = n_title_e.get()
                n_price = n_price.get()
                if not n_title:
                    n_title = old_prod_title(sku)
                if not n_price:
                    n_price = old_prod_price(sku)
                else:
                    n_price = float(n_price)
                res = modify_product(n_title,n_price,sku,username)
                res_var = tk.StringVar(value=res)
                tk.Label(app,textvariable=res_var).pack()
            tk.Button(app,text='Υποβολή αλλαγής',command=sbt_found_prod).pack()
            tk.Button(app,text='Πίσω <-',command=edit_prod).pack()

        prod_check = check_product(sku)
        if prod_check == True:
            found_prod()
        else:
            tk.Label(app,text='Δεν βρέθηκε προϊόν με αυτό το SKU').pack()
    
    tk.Button(app,text='Αναζήτση παραγγελίας',command=sbt_ed_pr).pack()
    tk.Button(app,text='Πίσω -->',command=home).pack()

        


def create_user():
    clear_app()
    tk.Label(app,text='Νεο username').pack()
    n_user_e = Entry(app)
    n_user_e.pack()
    tk.Label(app,text='Κωδικός πρόσβασης').pack()
    pwd_e1 = Entry(app,show='•')
    pwd_e1.pack()
    tk.Label(app,text='Επανάληψη κωδικού πρόσβασης').pack()
    pwd_e2 = Entry(app,show='•')
    pwd_e2.pack()
    tk.Label(app,text='Τύπος χρήστη').pack()
    u_type_c = ttk.Combobox(app,values=["Διαχειριστής","Απλός Χρήστης"])
    u_type_c.pack()
    def sbt_create_user():
        n_user = n_user_e.get()
        pwd_1 = pwd_e1.get()
        pwd_2 = pwd_e2.get()
        u_type = u_type_c.get()
        if pwd_1 == pwd_2:
            pwd = pwd_1
            if u_type == "Διαχειριστής":
                u_type = "admin"
            else:
                u_type = "user"
            res = new_user(username,n_user,pwd,u_type)
            res = tk.StringVar(value=res)
            tk.Label(app,textvariable=res).pack()
        else:
            tk.Label(app,text='Ο κωδικός και η επιβεβαίωση διαφέρουν. Δοκιμάστε ξανά.').pack()
    tk.Button(app,text='Προσθήκη χρήστη',command=sbt_create_user).pack()
    tk.Button(app,text='Πίσω -->',command=home).pack()




def home():
    clear_app()
    tk.Label(app,text='Καλωσορίσες %s. \n Επίλεξε μια ενέργεια'%username).pack()
    if isadmin == True:
        tk.Button(app,text='Προσθήκη χρήστη',command=create_user).pack()
    tk.Button(app,text='Νέα παραγγελία',command=create_order).pack()
    tk.Button(app,text='Καταχώρηση πελάτη',command=create_customer).pack()
    tk.Button(app,text='Επεξεργασία πελάτη',command=update_customer).pack()
    tk.Button(app,text='Δημιουργία προϊόντος',command=create_product).pack()
    tk.Button(app,text='Επεξεργασία κατάστασης παραγγελίας',command=modify_order).pack()
    tk.Button(app,text='Επεξεργασία προϊόντος',command=edit_prod).pack()
    



def login_click():
    global username
    global isadmin
    username = username_e.get()
    passw = passw_e.get()
    auth,isadmin = check_user_pass(username,passw)
    if auth == True:
        clear_app()
        home()
    else:
        var = tk.StringVar(value='Λάθος συνδιασμός. Δοκιμάστε ξανά')
        tk.Label(app,textvariable=var).pack()
tk.Button(app,text='Σύνδεση',command=login_click).pack()
app.mainloop()
