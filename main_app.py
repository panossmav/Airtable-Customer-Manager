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

def home():
    clear_app()
    tk.Label(app,text='Καλωσορίσες %s. \n Επίλεξε μια ενέργεια'%username).pack()

def login_click():
    global username
    username = username_e.get()
    passw = passw_e.get()
    auth = check_user_pass(username,passw)
    if auth == True:
        create_user_logs(username,'Logged in.')
        clear_app()
        home()
    else:
        var = tk.StringVar(value='Λάθος συνδιασμός. Δοκιμάστε ξανά')
        tk.Label(app,textvariable=var).pack()
tk.Button(app,text='Σύνδεση',command=login_click).pack()
app.mainloop()
