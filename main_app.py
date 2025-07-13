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


def home():
    clear_app()
    tk.Label(app,text='Καλωσορίσες %s. \n Επίλεξε μια ενέργεια'%username).pack()
    tk.Button(app,text='Νέα παραγγελία',command=create_order).pack()


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
