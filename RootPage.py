import tkinter as tk
from tkinter import *
import sqlite3
import AdminLogin as al

conn = sqlite3.connect('db-sqlite3/data.db')
with conn:
    cursor=conn.cursor()

class RootPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.lbl_status = StringVar(parent)
        self.lbl_status.set("waiting input...")
        Label(self, textvariable=self.lbl_status).grid(row=4, column=0, columnspan=2, sticky='W')

        def reg():
            win = Toplevel()
            win.title("Register")
            win.geometry('500x500')

            unm = StringVar()
            pwd = StringVar()
            Email = StringVar()
            name = StringVar()

            def database():
                global unm1
                unm1 = unm.get()
                pwd1 = pwd.get()
                em1 = Email.get()
                nm1 = name.get()
                if (unm1 == '' or pwd1 == '' or em1 == '' or nm1 == ''):
                    cp = Label(win, text="No input given! Can't Register", fg='brown', width=40, font=("bold", 10))
                    cp.place(x=100, y=100)
                else:
                    cursor.execute('INSERT INTO user (unm,pwd,name,email) VALUES(?,?,?,?)', (unm1, pwd1, em1, nm1))
                    conn.commit()
                    win.destroy()

            label_0 = Label(win, text="Register", width=20, font=("bold", 20))
            label_0.place(x=90, y=53)

            label_1 = Label(win, text="Username", width=20, font=("bold", 10))
            label_1.place(x=80, y=130)

            entry_1 = Entry(win, textvar=unm)
            entry_1.place(x=240, y=130)

            label_1 = Label(win, text="Password", width=20, font=("bold", 10))
            label_1.place(x=80, y=180)

            mobe = Entry(win, textvar=pwd, show="*")
            mobe.place(x=240, y=180)

            label_2 = Label(win, text="Name", width=20, font=("bold", 10))
            label_2.place(x=80, y=230)

            entry_2 = Entry(win, textvar=name)
            entry_2.place(x=240, y=230)

            addr = Label(win, text="Email", width=20, font=("bold", 10))
            addr.place(x=68, y=280)

            addre = Entry(win, textvar=Email)
            addre.place(x=240, y=280)

            Button(win, text='Register', width=20, bg='green', fg='white', command=database).place(x=180, y=340)
            Button(win, text='Cancel', width=20, bg='brown', fg='white', command=win.destroy).place(x=180, y=370)

        label_0 = Label(self, text="Audio Steganography", width=20, font=("bold", 20))
        label_0.place(x=100, y=53)

        label_1 = Label(self, text="Continue by", width=20, font=("default", 14))
        label_1.place(x=100, y=130)

        Button(self, text='Login', width=24, bg='brown', fg='white',
               command=lambda: controller.show_frame(al.AdminLogin)).place(x=123, y=160)

        label_2 = Label(self, text="Or", width=14, font=("default", 9))
        label_2.place(x=175, y=195)

        Button(self, text='Register', width=24, bg='brown', fg='white', command=reg).place(x=123, y=220)
