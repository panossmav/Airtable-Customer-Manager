from tkinter import *
import tkinter as tk
from tkinter import messagebox as pu
import datetime as dt
from funcs import *
from tkinter import ttk


root = tk.Tk()
root.title('CRMLite Online')
root.geometry('550x550')

def clear_root():
    for widget in root.winfo_children():
        widget.destroy()


def log_in():
    clear_root()
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
    new_window.title(" CRMLite Online Νέα Παραγγελία")
    new_window.geometry('500x500')

    tk.Label(new_window, text='Αριθμός τηλεφώνου πελάτη:').grid(row=0, column=0, sticky='ew')
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

            tk.Label(new_window, text="Κωδικός προϊόντος (SKU):").grid(row=1, column=0, sticky='ew')
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

def create_customer():
    new_window=Toplevel(root)
    new_window.title('CRMLite Online - Εγγραφή πελάτη')
    new_window.geometry('500x500')


    tk.Label(new_window,text='Καταχώρηση πελάτη',font=('Arial',20)).grid(column=0,sticky='ew')


    tk.Label(new_window,text='Τηλέφωνο').grid(column=0,row=1,sticky='ew')
    phone_e = Entry(new_window)
    phone_e.grid(row=2,sticky='ew')

    tk.Label(new_window,text='Όνομα').grid(row=3,sticky='ew')
    name_e = Entry(new_window)
    name_e.grid(row=4,sticky='ew')

    tk.Label(new_window,text='Email').grid(row=5,sticky='ew')
    email_e = Entry(new_window)
    email_e.grid(row=6,sticky='ew')

    if isadmin == True:
        tk.Label(new_window,text='Σημειώσεις').grid(row=7,sticky='ew')
        notes_e = Entry(new_window)
        notes_e.grid(row=8,sticky='ew')
    
    def sbt_create_customer():
        phone = phone_e.get()
        name = name_e.get()
        email = email_e.get()
        notes = notes_e.get()
        if not notes:
            notes = 'None'
        if phone and email and name:
            phone=int(phone)
            find_cust = check_phone(phone)
            if find_cust == True:
                pu.showerror('CRMLite online','Υπάρχει πελάτης με αυτόν τον αριθμό!')
            else:
                act=new_customer(name,phone,email,notes,username)
                pu.showinfo('CRMLite online',f"{act}")
                new_window.destroy()
        else:
            pu.showerror('CRMLite Online','Παρακαλώ συμπληρώστε όνομα,email και τηλέφωνο!')        
    tk.Button(new_window,text='Καταχώρηση',bg='green',fg='white',command=sbt_create_customer).grid(row=9,sticky='ew')

def create_product():
    if isadmin == True:
        new_window=Toplevel(root)
        new_window.title('CRMLite Online | Νέο προϊόν')
        new_window.geometry('600x600')

        tk.Label(new_window,text='Νέο προϊόν',font=("Arial",20)).grid(row=0,sticky='ew')
        tk.Label(new_window,text='Λειτουργία διαχειρηστή',font=('Arial',16),fg='red').grid(row=1,sticky='ew')

        tk.Label(new_window,text='Όνομα προϊόντος').grid(row=2,sticky='ew')
        title_e = Entry(new_window)
        title_e.grid(row=3,sticky='ew')

        tk.Label(new_window,text='Τιμή').grid(row=4,sticky='ew')
        price_e = Entry(new_window)
        price_e.grid(row=5,sticky='ew')
        def sbt_create_product():
            title = title_e.get()
            price = price_e.get()
            try:
                price = float(price)
                if price<0 or not title:
                    raise ValueError
                res=new_product(title,price,username)
                pu.showinfo('CRMLite Online',f"{res}")
                new_window.destroy()
            except ValueError:
                pu.showerror('CRMLite','Σφάλμα εισόδου! Εισάγετε τίτλο και τιμή')
                price_e.delete(0,tk.END)
                title_e.delete(0,tk.END)
        
        
        tk.Button(new_window,text='Καταχώρηση',bg='green',fg='white',command=sbt_create_product).grid(row=6,sticky='ew')
    else:
        pu.showerror('CRMLite Online','Χρειάζεστε δικαιώματα διαχειρηστή για αυτήν την ενέργεια')


def change_order_status():
    options = ['Fulfilled','Refunded','Pending','Unknown']
    new_window=Toplevel(root)
    new_window.geometry('500x500')
    new_window.title('CRMLite online')
    
    tk.Label(new_window,text='Αναζήτηση παραγγελίας',font=('Arial',18)).grid(row=0,sticky='e')
    ord_id_e = Entry(new_window)
    ord_id_e.grid(row=1,sticky='e')

    def sbt_order_search():
        ord_id=ord_id_e.get()
        try:
            ord_id=int(ord_id)
            res,res_msg = check_orders(ord_id)
            if res == True:
                for widgets in new_window.winfo_children():
                    widgets.destroy()
                tk.Label(new_window,text=f"{res_msg}").grid(row=0,sticky='e')
                tk.Label(new_window,text='Αλλαγή κατάστασης σε:\n').grid(row=1,sticky='e')
                new_status_cb = ttk.Combobox(new_window,values=options,state="readonly")
                new_status_cb.grid(row=2,sticky='e')
                new_status_cb.current(0)
                def sbt_update_order():
                    new_status = new_status_cb.get()
                    res_msg_2 = modify_status(ord_id,new_status,username)
                    pu.showinfo('CRMLite Online',f"{res_msg_2}")
                    new_window.destroy()
                tk.Button(new_window,text='Αλλαγή',command=sbt_update_order).grid(row=3,sticky='e')

            else:
                pu.showerror('CRMLite Online','Δεν βρέθηκε παραγγελία με αυτόν τον αριθμό')
        except ValueError:
            pu.showerror('CRMLite Online','Σφάλμα! Ο κωδικός πρέπει να είναι αριθμός')
            ord_id.delete(0,tk.END)
    tk.Button(new_window,text='Αναζήτηση',command=sbt_order_search).grid(row=2,sticky='e')

def create_user():
    if isadmin == True:
        new = Toplevel(root)
        new.title('CRMLite Online | Προσθήκη χρήστη')
        new.geometry('500x500')
        
        tk.Label(new,text='Εγγραφή χρήστη',font=('Arial',18)).grid(row=0,sticky='ew')

        tk.Label(new,text='Username νέου χρήστη').grid(row=1,sticky='ew')
        user_e = Entry(new)
        user_e.grid(row=2,sticky='ew')

        tk.Label(new,text='Password νέου χρήστη').grid(row=3,sticky='ew')
        passw1_e = Entry(new,show='•')
        passw1_e.grid(row=4,sticky='ew')

        tk.Label(new,text='Επανάληψη Password').grid(row=5,sticky='ew')
        passw2_e = Entry(new,show='•')
        passw2_e.grid(row=6,sticky='ew')

        user_types = ['Απλός χρήστης','Διαχειριστής']
        user_type_s = ttk.Combobox(new,values=user_types,state="readonly")
        user_type_s.grid(row=7,sticky='ew')
        user_type_s.current(0)

        def sbt_user_create():
            passw_1 = passw1_e.get()
            passw_2 = passw2_e.get()
            user_new=user_e.get()
            user_type = user_type_s.get()
            if user_type == 'Διαχειριστής':
                user_type = 'admin'
            else:
                user_type = 'user'
            if passw_1 == passw_2:
                passw = passw_1
                free_user,res_msg = new_user(username,user_new,passw,user_type)
                if free_user == True:
                    pu.showinfo('CRMLite online',f"{res_msg}")
                    new.destroy()
                else:
                    pu.showerror('CRMLite Online',f"{res_msg}")
                    user_e.delete(0,tk.END)
                    passw1_e.delete(0,tk.END)
                    passw2_e.delete(0,tk.END)
            else:
                pu.showerror('CRMLite','Οι κωδικοί δεν είναι ίδιοι! Δοκιμάστε ξανά')
                passw1_e.delete(0,tk.END)
                passw2_e.delete(0,tk.END)
        tk.Button(new,text='Προσθήκη',command=sbt_user_create,fg="white",bg="green").grid(row=8,sticky='ew')
    else:
        pu.showerror('CRMLite Online','Δεν έχετε δικαιώματα για αυτήν την ενέργεια')




def change_user_type():
    if isadmin == True:
        new_window = Toplevel(root)
        new_window.title('CRMLite Online | Προσθήκη πελάτη')
        new_window.geometry('500x500')

        tk.Label(new_window,text='Username προς αλλαγή:').grid(row=0,sticky='ew')
        username_e = Entry(new_window)
        username_e.grid(row=1,sticky='ew')
        def locate_user():
            user_m = username_e.get()
            search_status,user_type = search_user(user_m)
            if search_status == True:
                for widget in new_window.winfo_children():
                    widget.destroy()
                tk.Label(new_window,text=f"Χρηστης: {user_m}").grid(row=0,sticky='ew')
                tk.Label(new_window,text='Αλλαγή σε:').grid(row=1,sticky='ew')
                user_types=['Απλός χρήστης','Διαχειριστής']
                user_type_cb = ttk.Combobox(new_window,values=user_types,state='readonly')
                user_type_cb.grid(row=2,sticky='ew')
                if user_type == 'admin':
                    user_type_cb.current(1)
                else:
                    user_type_cb.current(0)
                def sbt_update():
                    new_user_type = user_type_cb.get()
                    if new_user_type == 'Διαχειριστής':
                        new_user_type = 'admin'
                    else:
                        new_user_type = 'user'
                    res = modfiy_user_type(username,user_m,new_user_type)
                    pu.showinfo('CRMLite Online',f"{res}")
                    new_window.destroy()
                tk.Button(new_window,text='Επεξεργασία',command=sbt_update).grid(row=3,sticky='ew')
            else:        
                pu.showerror('CRMLite','Δεν βρέθηκε χρήστης με αυτό το όνομα!')
                username_e.delete(0,tk.END)
        tk.Button(new_window,text='Αναζήτηση χρήστη',command=locate_user).grid(row=2,sticky='ew')
    else:
        pu.showerror('CRMLite','Δεν έχετε δικαίωμα πρόσβασης')

def modify_cust_info():
    new_window = Toplevel(root)
    new_window.title('CRMLite | Επεξεργασία Πελάτη')
    new_window.geometry('500x500')

    tk.Label(new_window,text='Αριθμός τηλεφώνου').grid(row=0,sticky='ew')
    old_phone_e = Entry(new_window)
    old_phone_e.grid(row=1,sticky='ew')
    def search_customer():
        old_phone = old_phone_e.get()
        try:
            old_phone = int(old_phone)
            res = check_phone(old_phone)
            if res == True:
                for widget in new_window.winfo_children():
                    widget.destroy()
                c_name,c_phone,c_email,c_notes=fetch_customer_info(old_phone)
                tk.Label(new_window,text='Όνομα: ').grid(row=0,column=0)
                name_entry = Entry(new_window)
                name_entry.grid(row=0,column=1)
                name_entry.insert(0,c_name)

                tk.Label(new_window,text='Email: ').grid(row=1,column=0)
                email_entry = Entry(new_window)
                email_entry.grid(row=1,column=1)
                email_entry.insert(0,c_email)

                tk.Label(new_window,text='Κινητό:').grid(row=2,column=0)
                phone_entry = Entry(new_window)
                phone_entry.grid(row=2,column=1)
                phone_entry.insert(0,c_phone)

                tk.Label(new_window,text='Σημειώσεις:').grid(row=3,column=0)
                notes_entry = Entry(new_window)
                notes_entry.grid(row=3,column=1)
                notes_entry.insert(0,c_notes)

                def sbt_edit():
                    name = name_entry.get()
                    email = email_entry.get()
                    phone = phone_entry.get()
                    notes = notes_entry.get()
                    try:
                        phone = int(phone)
                        taken = check_phone(phone)
                        if taken == True:
                            if int(phone) == int(old_phone):
                                pass
                            else:
                                raise ValueError
                        
                        result,res_msg = edit_customer(old_phone,name,phone,email,notes,username)
                        if result == True:
                            pu.showinfo('CRMLite Online',f"{res_msg}")
                        else:
                            pu.showerror('CRMLite Online',f"{res_msg}")
                    except ValueError:
                        pu.showerror('CRMLite online','Εισάγετε έναν έγκυρο αριθμό!')
                tk.Button(new_window,text='Επεξεργασία',command=sbt_edit).grid(row=4)
        except ValueError:
            pu.showerror('CRMLite','Παρακαλώ εισάγετε έγκυρο αριθμό')
    tk.Button(new_window,text=f"Αναζήτηση πελάτη",command=search_customer).grid(row=2,sticky='ew')

    

def home():
    clear_root()
    tk.Label(root,text=f"Όνομα χρήστη: {username}").grid(row=0,column=0)
    tk.Button(root,text=f"Αποσύνδεση",command=log_in).grid(row=0,column=1)
    if isadmin == False:
        tk.Label(root,text='Απλός χρήστης. Περιορισμένη λειτουργία',fg="red").grid(row=1,sticky='w')
    else:
        tk.Label(root,text='Διαχειριστής. Όλες οι λειτουγίες διαθέσιμες',fg="green").grid(row=1,column=0)
        tk.Label(root,text=f"Συνολικοί πελάτες: {total_cust()}").grid(row=1,column=1)
        tk.Label(root,text=f"Συνολικός τζίρος: {total_net()}").grid(row=1,column=2)
    tk.Label(root,text=f"Τελευταία ενημέρωση: {now()}").grid(row=2,sticky="w")
    tk.Button(root,text='Νέα Παραγγελία',command=create_order).grid(row=3,sticky='ew')
    tk.Button(root,text='Καταχώρηση πελάτη',command=create_customer).grid(row=4,sticky='ew')
    tk.Button(root,text='Καταχώρηση προϊόντος',command=create_product).grid(row=5,sticky='ew')
    tk.Button(root,text='Αλλαγή κατάστασης παραγγελίας',command=change_order_status).grid(row=6,sticky='ew')
    tk.Button(root,text='Προσθήκη χρήστη εφαρμογής',command=create_user).grid(row=6,sticky='ew')
    tk.Button(root,text='Αλλαγή τύπου χρήστη',command=change_user_type).grid(row=7,sticky='ew')
    #Επεξεργασία πελατόν κρυφή μέχρι να γινει resolve το issue #5 
    tk.Button(root,text='Επεξεργασία πελάτη',command=modify_cust_info).grid(row=8,sticky='ew')
    

log_in()
root.mainloop()