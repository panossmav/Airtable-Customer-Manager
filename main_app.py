from tkinter import *
import tkinter as tk
from tkinter import messagebox as pu
import datetime as dt
from funcs import *


root = tk.Tk()
root.title('CRMLite Online')
root.geometry('550x550')

def clear_root():
    for widget in root.winfo_children():
        widget.pack_forget()


def log_in():
    tk.Label(root,text='Καλοσωρίσατε!',font=("Arial",18),justify="center").pack()
    tk.Label(root,text='Username: ',font=("Arial",14)).pack()
    user_e=tk.Entry(root)
    user_e.pack()
    tk.Label(root,text='Password',font=('Arial',14)).pack()
    passw_e = Entry(root,show='•')
    passw_e.pack()

    def auth():
        global username
        global isadmin
        username = user_e.get()
        password = passw_e.get()
        success,isadmin = check_user_pass(username,password)
        if success == True:
            home()
        else:
            pu.showerror('CRMLite Online','Ο συνδιασμός είναι λάθος! Δοκιμάστε ξανά')
            passw_e.delete(0,tk.END)
    tk.Button(root,text='Σύνδεση',command=auth).pack()
    

def new_order():
    clear_root()
    tk.Label(root,text='Καταχώρηση νέας παραγγελίας',font=('Arial',14)).grid(row=0,sticky="w")
    tk.Label(root,text='Προϊόντα').grid(row=1,sticky="e")
    add_items = True
    product_entries = []
    product_codes = []
    i = 0
    while add_items == True:
        if add_btn and stop_btn:
            add_btn.pack_forget()
            stop_btn.pack_forget()

        product_entries[i]=Entry(root)
        product_entries[i].grid(row=i+2,sticky="e")
        product_codes[i] = product_entries[i].get()
        if product_entries[i-1]:
            product_entries[i-1].config(state="disabled")
        def add_product_btn():
            add_items = True
        add_btn=tk.Button(root,text='Προσθήκη Προϊόντος',command=add_product_btn)
        add_btn.grid(row=i+3,column=0)
        def stop_add():
            add_items = False
        stop_btn = tk.Button(root,text='Τέλος προσθήκης προϊόντων',command=stop_add)
        stop_btn.grid(row=i+3,column=1)


def home():
    clear_root()
    tk.Label(root,text=f"Όνομα χρήστη: {username}").grid(row=0,sticky='w')
    if isadmin == False:
        tk.Label(root,text='Απλός χρήστης. Περιορισμένη λειτουργία',fg="red").grid(row=1,sticky='w')
    else:
        tk.Label(root,text='Διαχειριστής. Όλες οι λειτουγίες διαθέσιμες',fg="green").grid(row=1,sticky='w')
    tk.Label(root,text=f"Τελευταία ενημέρωση: {now()}").grid(row=2,sticky="w")


log_in()
root.mainloop()