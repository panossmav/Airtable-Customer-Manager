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
    

def create_order():
    new_window = Toplevel(root)
    new_window.title("Νέα Παραγγελία")

    tk.Label(new_window, text='Αριθμός τηλεφώνου πελάτη:').grid(row=0, column=0, sticky='e')
    phone_e = Entry(new_window)
    phone_e.grid(row=0, column=1, sticky='w')

    def sbt_find_cust():
        phone = phone_e.get()
        if not phone:
            pu.showerror('CRMLite Online', 'Παρακαλώ εισάγετε έναν αριθμό τηλεφώνου!')
            return

        try:
            phone_int = int(phone)
        except ValueError:
            pu.showerror('CRMLite Online', 'Μη έγκυρος αριθμός τηλεφώνου!')
            return

        if check_phone(phone_int):
            for widget in new_window.winfo_children():
                widget.destroy()

            name, phone, email, notes = fetch_customer_info(phone_int)
            tk.Label(new_window, text=f"Ο πελάτης βρέθηκε!\nΌνομα: {name}\nΤηλέφωνο: {phone}\nEmail: {email}\nΣημειώσεις: {notes}", justify='left').grid(row=0, column=0, columnspan=3, sticky='w', padx=10, pady=10)

            tk.Label(new_window, text="Κωδικός προϊόντος (SKU):").grid(row=1, column=0, sticky='e')
            sku_entry = Entry(new_window)
            sku_entry.grid(row=1, column=1, sticky='w')

            product_frame = tk.Frame(new_window)
            product_frame.grid(row=3, column=0, columnspan=3, sticky='w', padx=10, pady=10)

            total_price_var = tk.DoubleVar(value=0.00)
            row_counter = [0]  # Μετρητής για εμφάνιση προϊόντων

            def sbt_add_product():
                sku = sku_entry.get()
                if not sku:
                    pu.showerror('CRMLite Online', 'Παρακαλώ δώστε κωδικό προϊόντος!')
                    return
                try:
                    sku_int = int(sku)
                except ValueError:
                    pu.showerror('CRMLite Online', 'Ο κωδικός προϊόντος πρέπει να είναι αριθμός!')
                    return

                if check_product(sku_int):
                    title, price = fetch_product_info(sku_int)
                    tk.Label(product_frame, text=f"{title}, {price:.2f}€, Κωδ: {sku_int}").grid(row=row_counter[0], column=0, sticky='w')
                    total_price_var.set(total_price_var.get() + price)
                    total_label.config(text=f"Σύνολο: {total_price_var.get():.2f} €")
                    row_counter[0] += 1
                    sku_entry.delete(0, 'end')
                else:
                    pu.showerror('CRMLite Online', f"Δεν βρέθηκε προϊόν με κωδικό {sku_int}!")

            tk.Button(new_window, text="Προσθήκη", command=sbt_add_product).grid(row=1, column=2, sticky='w')

            total_label = tk.Label(new_window, text="Σύνολο: 0.00 €", font=('Arial', 12, 'bold'))
            total_label.grid(row=2, column=0, columnspan=3, sticky='w', padx=10, pady=5)

            # Κουμπί Καταχώρηση Παραγγελίας
            def submit_order():
                price = total_price_var.get()
                result, msg = new_order(phone_int, price, username)
                if result:
                    pu.showinfo('CRMLite Online', msg)
                    new_window.destroy()
                else:
                    pu.showerror('CRMLite Online', msg)

            tk.Button(new_window, text="Καταχώρηση Παραγγελίας", command=submit_order, bg="green", fg="white").grid(row=4, column=0, columnspan=3, pady=10)

        else:
            pu.showerror('CRMLite Online', f"Δεν βρέθηκε πελάτης με τον αριθμό {phone}. \nΠροσθέστε πελάτη και δοκιμάστε ξανά.")

    tk.Button(new_window, text='Αναζήτηση πελάτη', command=sbt_find_cust).grid(row=0, column=2, sticky='w')


def home():
    clear_root()
    tk.Label(root,text=f"Όνομα χρήστη: {username}").grid(row=0,sticky='w')
    if isadmin == False:
        tk.Label(root,text='Απλός χρήστης. Περιορισμένη λειτουργία',fg="red").grid(row=1,sticky='w')
    else:
        tk.Label(root,text='Διαχειριστής. Όλες οι λειτουγίες διαθέσιμες',fg="green").grid(row=1,sticky='w')
    tk.Label(root,text=f"Τελευταία ενημέρωση: {now()}").grid(row=2,sticky="w")
    tk.Button(root,text='Νέα Παραγγελία',command=create_order).grid(column=3,sticky='e')


log_in()
root.mainloop()