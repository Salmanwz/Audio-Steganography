import tkinter as tk

import AdmHmPg as ah
import AdminLogin as al
import RootPage as rp


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Audio Steganography")
        self.geometry('700x500')
        container = tk.Frame(self)
        self.cuser = ''

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (rp.RootPage, al.AdminLogin, ah.AdmHmPg):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(rp.RootPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


app = SeaofBTCapp()
app.mainloop()
