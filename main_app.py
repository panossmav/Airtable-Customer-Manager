from tkinter import *
import tkinter as tk
from funcs import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox


app=tk.Tk()
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
    title = tk.Label(app, text="Νέα Παραγγελία", font=("Helvetica", 18, "bold"))
    title.pack(pady=15)

    form_frame = tk.Frame(app, padx=20, pady=20, bd=2, relief=tk.RIDGE)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Κινητό πελάτη:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5, padx=5)
    phone_e = tk.Entry(form_frame, font=("Arial", 12))
    phone_e.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="Κωδικός προϊόντος (SKU):", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5, padx=5)
    sku_e = tk.Entry(form_frame, font=("Arial", 12))
    sku_e.grid(row=1, column=1, pady=5, padx=5)

    result_var = tk.StringVar()
    result_label = tk.Label(app, textvariable=result_var, font=("Arial", 12), fg="green")
    result_label.pack(pady=10)

    def sbt_order_create():
        try:
            phone = int(phone_e.get())
            sku = int(sku_e.get())
        except ValueError:
            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε έγκυρους αριθμούς για το τηλέφωνο και το SKU.")
            return
        
        creation, nostock = new_order(phone, sku, username)
        result_var.set(creation)
        if nostock:
            messagebox.showwarning("Προσοχή", "Το απόθεμα για το προϊόν τελείωσε!")

    btn_frame = tk.Frame(app)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Καταχώρηση Παραγγελίας", command=sbt_order_create, width=20).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Πίσω", command=home, width=20).grid(row=0, column=1, padx=10)


def create_customer():
    clear_app()
    title = tk.Label(app, text="Καταχώρηση Νέου Πελάτη", font=("Helvetica", 18, "bold"))
    title.pack(pady=15)

    form_frame = tk.Frame(app, padx=20, pady=20, bd=2, relief=tk.RIDGE)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Ονοματεπώνυμο:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5, padx=5)
    name_e = tk.Entry(form_frame, font=("Arial", 12), width=30)
    name_e.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="Τηλέφωνο:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5, padx=5)
    phone_e = tk.Entry(form_frame, font=("Arial", 12), width=30)
    phone_e.grid(row=1, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="Email:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5, padx=5)
    email_e = tk.Entry(form_frame, font=("Arial", 12), width=30)
    email_e.grid(row=2, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="Σημειώσεις (προαιρετικό):", font=("Arial", 12)).grid(row=3, column=0, sticky="e", pady=5, padx=5)
    notes_e = tk.Entry(form_frame, font=("Arial", 12), width=30)
    notes_e.grid(row=3, column=1, pady=5, padx=5)

    result_var = tk.StringVar()
    result_label = tk.Label(app, textvariable=result_var, font=("Arial", 12), fg="green")
    result_label.pack(pady=10)

    def sbt_customer_create():
        name = name_e.get().strip()
        phone_str = phone_e.get().strip()
        email = email_e.get().strip()
        notes = notes_e.get().strip() or "None"

        if not name or not phone_str or not email:
            messagebox.showerror("Σφάλμα", "Τα πεδία όνομα, τηλέφωνο και email είναι υποχρεωτικά.")
            return
        try:
            phone = int(phone_str)
        except ValueError:
            messagebox.showerror("Σφάλμα", "Το τηλέφωνο πρέπει να είναι αριθμός.")
            return
        
        res = new_customer(name, phone, email, notes, username)
        result_var.set(res)

    btn_frame = tk.Frame(app)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Καταχώρηση Πελάτη", command=sbt_customer_create, width=20).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Πίσω", command=home, width=20).grid(row=0, column=1, padx=10)


def update_customer():
    clear_app()
    title = tk.Label(app, text="Επεξεργασία Πελάτη", font=("Helvetica", 18, "bold"))
    title.pack(pady=15)

    info_lbl = tk.Label(app, text="Εισάγετε το τρέχον τηλέφωνο του πελάτη που θέλετε να ενημερώσετε:", font=("Arial", 12))
    info_lbl.pack(pady=5)

    old_phone_e = tk.Entry(app, font=("Arial", 12), width=30)
    old_phone_e.pack(pady=5)

    tk.Label(app, text="Νέα Στοιχεία (αφήστε κενά για να μείνουν ίδια):", font=("Arial", 12, "italic")).pack(pady=10)

    form_frame = tk.Frame(app, padx=20, pady=10, bd=2, relief=tk.RIDGE)
    form_frame.pack(pady=5)

    tk.Label(form_frame, text="Νέο Τηλέφωνο:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5, padx=5)
    new_phone_e = tk.Entry(form_frame, font=("Arial", 12), width=30)
    new_phone_e.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="Νέο Όνομα:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5, padx=5)
    new_name_e = tk.Entry(form_frame, font=("Arial", 12), width=30)
    new_name_e.grid(row=1, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="Νέο Email:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5, padx=5)
    new_email_e = tk.Entry(form_frame, font=("Arial", 12), width=30)
    new_email_e.grid(row=2, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="Νέες Σημειώσεις:", font=("Arial", 12)).grid(row=3, column=0, sticky="e", pady=5, padx=5)
    new_notes_e = tk.Entry(form_frame, font=("Arial", 12), width=30)
    new_notes_e.grid(row=3, column=1, pady=5, padx=5)

    result_var = tk.StringVar()
    result_label = tk.Label(app, textvariable=result_var, font=("Arial", 12), fg="green")
    result_label.pack(pady=10)

    def sbt_udt_cust():
        old_phone_str = old_phone_e.get().strip()
        if not old_phone_str:
            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε το τρέχον τηλέφωνο του πελάτη.")
            return
        try:
            old_phone = int(old_phone_str)
        except ValueError:
            messagebox.showerror("Σφάλμα", "Το τρέχον τηλέφωνο πρέπει να είναι αριθμός.")
            return

        new_phone_str = new_phone_e.get().strip()
        new_name = new_name_e.get().strip()
        new_email = new_email_e.get().strip()
        new_notes = new_notes_e.get().strip()

        if not new_phone_str:
            new_phone = old_phone
        else:
            try:
                new_phone = int(new_phone_str)
            except ValueError:
                messagebox.showerror("Σφάλμα", "Το νέο τηλέφωνο πρέπει να είναι αριθμός.")
                return
        
        if not new_name:
            new_name = c_check_name(old_phone)
        if not new_email:
            new_email = c_check_email(old_phone)
        if not new_notes:
            new_notes = c_check_notes(old_phone)

        res = edit_customer(old_phone, new_name, new_phone, new_email, new_notes, username)
        result_var.set(res)

    btn_frame = tk.Frame(app)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Επεξεργασία", command=sbt_udt_cust, width=20).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Πίσω", command=home, width=20).grid(row=0, column=1, padx=10)
       
    
def create_product():
    clear_app()
    title = tk.Label(app, text="Δημιουργία Προϊόντος", font=("Helvetica", 18, "bold"))
    title.pack(pady=15)

    form_frame = tk.Frame(app, padx=20, pady=20, bd=2, relief=tk.RIDGE)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Τίτλος προϊόντος:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5, padx=5)
    tit_e = tk.Entry(form_frame, font=("Arial", 12), width=30)
    tit_e.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="Τιμή:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5, padx=5)
    pr_e = tk.Entry(form_frame, font=("Arial", 12), width=30)
    pr_e.grid(row=1, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="Απόθεμα (0 για μη παρακολούθηση):", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5, padx=5)
    st_e = tk.Entry(form_frame, font=("Arial", 12), width=30)
    st_e.grid(row=2, column=1, pady=5, padx=5)

    result_var = tk.StringVar()
    result_label = tk.Label(app, textvariable=result_var, font=("Arial", 12), fg="green")
    result_label.pack(pady=10)

    def sbt_prod_create():
        title = tit_e.get().strip()
        price_str = pr_e.get().strip()
        stock_str = st_e.get().strip()

        if not title or not price_str or not stock_str:
            messagebox.showerror("Σφάλμα", "Παρακαλώ συμπληρώστε όλα τα πεδία.")
            return
        try:
            price = round(float(price_str), 2)
            stock = int(stock_str)
        except ValueError:
            messagebox.showerror("Σφάλμα", "Η τιμή πρέπει να είναι αριθμός με ή χωρίς δεκαδικά, και το απόθεμα ακέραιος αριθμός.")
            return

        res = new_product(title, price, username, stock)
        result_var.set(res)

    btn_frame = tk.Frame(app)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Δημιουργία Προϊόντος", command=sbt_prod_create, width=20).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Πίσω", command=home, width=20).grid(row=0, column=1, padx=10)


def modify_order():
    clear_app()
    title = tk.Label(app, text="Επεξεργασία Κατάστασης Παραγγελίας", font=("Helvetica", 18, "bold"))
    title.pack(pady=15)

    tk.Label(app, text="Αριθμός παραγγελίας:", font=("Arial", 12)).pack(pady=5)
    id_e = tk.Entry(app, font=("Arial", 12), width=30)
    id_e.pack(pady=5)

    result_var = tk.StringVar()
    result_label = tk.Label(app, textvariable=result_var, font=("Arial", 12), fg="green")
    result_label.pack(pady=10)

    def find_order():
        order_id_str = id_e.get().strip()
        if not order_id_str:
            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε αριθμό παραγγελίας.")
            return
        try:
            o_id = int(order_id_str)
        except ValueError:
            messagebox.showerror("Σφάλμα", "Ο αριθμός παραγγελίας πρέπει να είναι ακέραιος.")
            return
        
        db_search, result = check_orders(o_id)
        if db_search:
            clear_app()
            tk.Label(app, text=f"Παραγγελία #{o_id}", font=("Helvetica", 16, "bold")).pack(pady=10)
            result_var.set(result)
            tk.Label(app, textvariable=result_var, font=("Arial", 12)).pack(pady=5)

            tk.Label(app, text="Νέο Status:", font=("Arial", 12)).pack(pady=10)
            status_e = tk.Entry(app, font=("Arial", 12), width=30)
            status_e.pack(pady=5)

            def sbt_found():
                status = status_e.get().strip()
                if not status:
                    messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε νέο status.")
                    return
                res = modify_status(o_id, status, username)
                messagebox.showinfo("Ενημέρωση", res)
                modify_order()  # Επαναφορτώνει τη φόρμα

            btn_frame = tk.Frame(app)
            btn_frame.pack(pady=10)
            tk.Button(btn_frame, text="Αλλαγή Κατάστασης", command=sbt_found, width=20).grid(row=0, column=0, padx=10)
            tk.Button(btn_frame, text="Πίσω", command=modify_order, width=20).grid(row=0, column=1, padx=10)
        else:
            result_var.set(result)

    btn_frame = tk.Frame(app)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Αναζήτηση Παραγγελίας", command=find_order, width=20).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Πίσω", command=home, width=20).grid(row=0, column=1, padx=10)


def edit_prod():
    clear_app()
    title = tk.Label(app, text="Επεξεργασία Προϊόντος", font=("Helvetica", 18, "bold"))
    title.pack(pady=15)

    tk.Label(app, text="Εισάγετε SKU προϊόντος:", font=("Arial", 12)).pack(pady=5)
    sku_e = tk.Entry(app, font=("Arial", 12), width=30)
    sku_e.pack(pady=5)

    result_var = tk.StringVar()
    result_label = tk.Label(app, textvariable=result_var, font=("Arial", 12), fg="green")
    result_label.pack(pady=10)

    def sbt_ed_pr():
        sku_str = sku_e.get().strip()
        if not sku_str:
            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε SKU.")
            return
        try:
            sku = int(sku_str)
        except ValueError:
            messagebox.showerror("Σφάλμα", "Το SKU πρέπει να είναι αριθμός.")
            return

        if check_product(sku):
            clear_app()
            title2 = tk.Label(app, text=f"Επεξεργασία Προϊόντος SKU: {sku}", font=("Helvetica", 16, "bold"))
            title2.pack(pady=15)
            old_title = old_prod_title(sku)
            old_price = old_prod_price(sku)
            tk.Label(app, text=f"Τίτλος: {old_title}", font=("Arial", 12)).pack(pady=5)
            tk.Label(app, text=f"Τιμή: {old_price}", font=("Arial", 12)).pack(pady=5)

            tk.Label(app, text="Εισάγετε αλλαγές (αφήστε κενά για διατήρηση):", font=("Arial", 12, "italic")).pack(pady=10)

            form_frame = tk.Frame(app, padx=20, pady=10, bd=2, relief=tk.RIDGE)
            form_frame.pack(pady=5)

            tk.Label(form_frame, text="Νέος τίτλος:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5, padx=5)
            n_title_e = tk.Entry(form_frame, font=("Arial", 12), width=30)
            n_title_e.grid(row=0, column=1, pady=5, padx=5)

            tk.Label(form_frame, text="Νέα τιμή:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5, padx=5)
            n_p_e = tk.Entry(form_frame, font=("Arial", 12), width=30)
            n_p_e.grid(row=1, column=1, pady=5, padx=5)

            def sbt_found_prod():
                n_title = n_title_e.get().strip()
                n_price_str = n_p_e.get().strip()
                if not n_title:
                    n_title = old_title
                if not n_price_str:
                    n_price = old_price
                else:
                    try:
                        n_price = float(n_price_str)
                    except ValueError:
                        messagebox.showerror("Σφάλμα", "Η τιμή πρέπει να είναι αριθμός.")
                        return
                res = modify_product(n_title, n_price, sku, username)
                result_var.set(res)

            btn_frame = tk.Frame(app)
            btn_frame.pack(pady=10)
            tk.Button(btn_frame, text="Υποβολή Αλλαγής", command=sbt_found_prod, width=20).grid(row=0, column=0, padx=10)
            tk.Button(btn_frame, text="Πίσω", command=edit_prod, width=20).grid(row=0, column=1, padx=10)
        else:
            result_var.set("Δεν βρέθηκε προϊόν με αυτό το SKU.")

    btn_frame = tk.Frame(app)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Αναζήτηση Προϊόντος", command=sbt_ed_pr, width=20).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Πίσω", command=home, width=20).grid(row=0, column=1, padx=10)


        


def create_user():
    clear_app()
    title = tk.Label(app, text="Δημιουργία Νέου Χρήστη", font=("Helvetica", 18, "bold"))
    title.pack(pady=15)

    form_frame = tk.Frame(app, padx=20, pady=20, bd=2, relief=tk.RIDGE)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Νέο Username:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5, padx=5)
    n_user_e = tk.Entry(form_frame, font=("Arial", 12), width=30)
    n_user_e.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="Κωδικός πρόσβασης:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5, padx=5)
    pwd_e1 = tk.Entry(form_frame, font=("Arial", 12), width=30, show='•')
    pwd_e1.grid(row=1, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="Επανάληψη κωδικού:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5, padx=5)
    pwd_e2 = tk.Entry(form_frame, font=("Arial", 12), width=30, show='•')
    pwd_e2.grid(row=2, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="Τύπος χρήστη:", font=("Arial", 12)).grid(row=3, column=0, sticky="e", pady=5, padx=5)
    u_type_c = ttk.Combobox(form_frame, values=["Διαχειριστής", "Απλός Χρήστης"], font=("Arial", 12), width=28)
    u_type_c.grid(row=3, column=1, pady=5, padx=5)
    u_type_c.current(1)

    result_var = tk.StringVar()
    result_label = tk.Label(app, textvariable=result_var, font=("Arial", 12), fg="green")
    result_label.pack(pady=10)

    def sbt_create_user():
        n_user = n_user_e.get().strip()
        pwd_1 = pwd_e1.get()
        pwd_2 = pwd_e2.get()
        u_type = u_type_c.get()

        if pwd_1 != pwd_2:
            messagebox.showerror("Σφάλμα", "Ο κωδικός και η επιβεβαίωση διαφέρουν.")
            return
        if not n_user or not pwd_1:
            messagebox.showerror("Σφάλμα", "Παρακαλώ συμπληρώστε όλα τα πεδία.")
            return

        u_type_val = "admin" if u_type == "Διαχειριστής" else "user"
        res = new_user(username, n_user, pwd_1, u_type_val)
        result_var.set(res)

    btn_frame = tk.Frame(app)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Προσθήκη Χρήστη", command=sbt_create_user, width=20).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Πίσω", command=home, width=20).grid(row=0, column=1, padx=10)



def delete_user():
    clear_app()
    tk.Label(app,text='Όνομα χρήστη που επιθυμείτε να διαγράψετε').pack()
    d_u_e = Entry(app)
    d_u_e.pack()
    def sbt_del():
        d_u = d_u_e.get()
        res = del_user(username,d_u)
        res_var = tk.StringVar(value=res)
        tk.Label(app,textvariable=res_var).pack()
    tk.Button(app,text='Διαγραφή',command=sbt_del).pack()
    tk.Button(app,text='Πίσω -->',command=home).pack()


def delete_customer():
    clear_app()
    title = tk.Label(app, text="Διαγραφή Πελάτη", font=("Helvetica", 18, "bold"))
    title.pack(pady=15)

    tk.Label(app, text="Τηλέφωνο πελάτη προς διαγραφή:", font=("Arial", 12)).pack(pady=10)
    p_e = tk.Entry(app, font=("Arial", 12), width=30)
    p_e.pack(pady=5)

    result_var = tk.StringVar()
    result_label = tk.Label(app, textvariable=result_var, font=("Arial", 12), fg="green")
    result_label.pack(pady=10)

    def sbt_del_c():
        p_str = p_e.get().strip()
        if not p_str:
            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε τηλέφωνο πελάτη.")
            return
        res = del_cust(username, p_str)
        result_var.set(res)

    btn_frame = tk.Frame(app)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Διαγραφή", command=sbt_del_c, width=20).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Πίσω", command=home, width=20).grid(row=0, column=1, padx=10)



def add_inv():
    clear_app()
    tk.Label(app,text='SKU').pack()
    sku_e = Entry(app)
    sku_e.pack()
    tk.Label(app,text='Αριθμός νέων παραλαβών').pack()
    n_inve = Entry(app)
    n_inve.pack()
    def sbt_add_inv():
        sku = int(sku_e.get())
        n_inv = int(n_inve.get())
        res = update_inv(username,sku,n_inv)
        res_var = tk.StringVar(value=res)
        tk.Label(app,textvariable=res_var).pack()
    tk.Button(app,text='Επεξεργασία',command=sbt_add_inv).pack()
    tk.Button(app,text='Πίσω -->',command=home).pack()    

def net_profit_customer():
    clear_app()
    title = tk.Label(app, text="Καθαρό Κέρδος Πελάτη", font=("Helvetica", 18, "bold"))
    title.pack(pady=15)

    tk.Label(app, text="Τηλέφωνο πελάτη:", font=("Arial", 12)).pack(pady=10)
    p_e = tk.Entry(app, font=("Arial", 12), width=30)
    p_e.pack(pady=5)

    result_var = tk.StringVar()
    result_label = tk.Label(app, textvariable=result_var, font=("Arial", 12), fg="green")
    result_label.pack(pady=10)

    def sbt_n_p_c():
        p_str = p_e.get().strip()
        if not p_str:
            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε τηλέφωνο.")
            return
        try:
            p = int(p_str)
        except ValueError:
            messagebox.showerror("Σφάλμα", "Το τηλέφωνο πρέπει να είναι αριθμός.")
            return
        res = net_pr_cust(p, username)
        result_var.set(res)

    btn_frame = tk.Frame(app)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Προβολή", command=sbt_n_p_c, width=20).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Πίσω", command=home, width=20).grid(row=0, column=1, padx=10)





def home():
    clear_app()

    bg_color = "#f0f2f5"
    section_bg = "#ffffff"
    btn_color = "#4a90e2"
    btn_hover = "#357ABD"
    font = ("Segoe UI", 11)
    title_font = ("Segoe UI", 16, "bold")
    card_title_font = ("Segoe UI", 12, "bold")

    app.configure(bg=bg_color)

 
    title = tk.Label(app, text=f"📊 Airtable CRM Dashboard\nΚαλωσόρισες {username}", font=title_font,
                     bg=bg_color, fg="#222")
    title.pack(pady=20)


    stats_frame = tk.Frame(app, bg=bg_color)
    stats_frame.pack(pady=5)

    def stat_card(parent, title, value):
        card = tk.Frame(parent, bg=section_bg, bd=1, relief="solid", padx=20, pady=10)
        tk.Label(card, text=title, font=card_title_font, bg=section_bg).pack(anchor="w")
        tk.Label(card, text=value, font=("Segoe UI", 14, "bold"), bg=section_bg, fg="#007acc").pack(anchor="w")
        return card
    customers_total = int(total_cust())
    net_total = total_net()

    stat_card(stats_frame, "Σύνολο Πελατών", customers_total).grid(row=0, column=0, padx=10)
    stat_card(stats_frame, "Συνολικός Τζίρος", f"{net_total}€").grid(row=0, column=1, padx=20)


    sections_frame = tk.Frame(app, bg=bg_color)
    sections_frame.pack(pady=15)

    def action_section(title, buttons):
        frame = tk.LabelFrame(sections_frame, text=title, font=card_title_font,
                              bg=section_bg, fg="#333", padx=15, pady=10, bd=2)
        for text, cmd in buttons:
            b = tk.Button(frame, text=text, command=cmd,
                          font=font, bg=btn_color, fg="white",
                          activebackground=btn_hover, width=30, height=2)
            b.pack(pady=5)
        return frame


    cust_order_section = action_section("👥 Πελάτες & Παραγγελίες", [
        ("🛒 Νέα Παραγγελία", create_order),
        ("📤 Καταχώρηση Πελάτη", create_customer),
        ("✏️ Επεξεργασία Πελάτη", update_customer),
        ("📦 Δημιουργία Προϊόντος", create_product),
        ("🛠️ Επεξεργασία Προϊόντος", edit_prod),
        ("📥 Επεξεργασία Αποθέματος", add_inv),
        ("🔁 Επεξεργασία Κατάστασης Παραγγελίας", modify_order)
    ])
    cust_order_section.grid(row=0, column=0, padx=15)


    if isadmin:
        admin_section = action_section("🔐 Διαχειριστικές Λειτουργίες", [
            ("👤 Προσθήκη Χρήστη", create_user),
            ("🗑️ Διαγραφή Χρήστη", delete_user),
            ("🚫 Διαγραφή Πελάτη", delete_customer),
            ("📈 Τζίρος ανά Πελάτη", net_profit_customer)
        ])
        admin_section.grid(row=0, column=1, padx=15)


    footer = tk.Label(app, text="© 2025 - Airtable Customer Manager", bg=bg_color, fg="gray", font=("Segoe UI", 9))
    footer.pack(pady=20)


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
