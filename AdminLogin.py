import sqlite3
import tkinter as tk
from tkinter import *

import AdmHmPg as ah
import RootPage as rp

conn = sqlite3.connect('db-sqlite3/data.db')
with conn:
    cursor = conn.cursor()


class AdminLogin(tk.Frame):
    cuser = ''

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        unm = StringVar()
        pwd = StringVar()

        def AdmLogCheck():
            unm1 = unm.get()
            pwd1 = pwd.get()
            self.cuser = unm1

            row = cursor.execute("SELECT `unm`,`pwd` FROM user WHERE unm=? and pwd=?", (unm1, pwd1))
            row = cursor.fetchall()
            le = len(row)
            if le > 0:
                AdminLogin.cuser = unm1
                print(AdminLogin.cuser)
                controller.show_frame(ah.AdmHmPg)
            else:
                wp = Label(self, text="Wrong Username or Password!", fg='red', width=40, font=("bold", 10))
                wp.place(x=100, y=100)

        label_0 = Label(self, text="User Login", width=20, font=("bold", 20))
        label_0.place(x=100, y=53)

        label_1 = Label(self, text="Username :", width=20, font=("bold", 10))
        label_1.place(x=80, y=130)

        unm = Entry(self)
        unm.place(x=240, y=130)

        plbl = Label(self, text="Password :", width=20, font=("bold", 10))
        plbl.place(x=80, y=180)

        pwd = Entry(self, show="*")
        pwd.place(x=240, y=180)

        Button(self, text='Login', width=13, bg='green', fg='white', command=AdmLogCheck).place(x=123, y=230)
        Button(self, text='Cancel', width=13, bg='brown', fg='white',
               command=lambda: controller.show_frame(rp.RootPage)).place(x=273, y=230)
