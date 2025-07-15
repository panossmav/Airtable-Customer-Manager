from tkinter import *
import tkinter as tk
from funcs import *

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
    tk.Label(app,text='SKU').pack()
    sku_e = Entry(app)
    sku_e.pack()

    def sbt_prod_create():
        title = tit_e.get()
        price = float(pr_e.get())
        price = round(price,2)
        sku = int(sku_e.get())
        res = new_product(title,price,sku,username)
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




def home():
    clear_app()
    tk.Label(app,text='Καλωσορίσες %s. \n Επίλεξε μια ενέργεια'%username).pack()
    tk.Button(app,text='Νέα παραγγελία',command=create_order).pack()
    tk.Button(app,text='Καταχώρηση πελάτη',command=create_customer).pack()
    tk.Button(app,text='Επεξεργασία πελάτη',command=update_customer).pack()
    tk.Button(app,text='Δημιουργία προϊόντος',command=create_product).pack()
    tk.Button(app,text='Επεξεργασία κατάστασης παραγγελίας',command=modify_order).pack()




def login_click():
    global username
    username = username_e.get()
    passw = passw_e.get()
    auth = check_user_pass(username,passw)
    if auth == True:
        clear_app()
        home()
    else:
        var = tk.StringVar(value='Λάθος συνδιασμός. Δοκιμάστε ξανά')
        tk.Label(app,textvariable=var).pack()
tk.Button(app,text='Σύνδεση',command=login_click).pack()
app.mainloop()
