import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import sqlite3
import dblib
import langpack

class AddNew(tk.Toplevel):
    def __init__(self, parent, selected_language):
        super().__init__()
        self.selected_language = selected_language
        self.i18n = langpack.I18N(self.selected_language)
        self.db = dblib.UserDataManager()
        self.parent = parent
        self.geometry("400x300+710+200")
        self.title(self.i18n.text_add_new_button_user)
        self.iconbitmap("python.ico")

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.role = tk.StringVar()
        self.email = tk.StringVar()
        self.phone = tk.IntVar()

        self.create_widgets()
        self.bind_widgets()
        self.txt_username.focus_set()
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def save_user(self):
        try:
            if len(self.username.get()) == 0:
                msg.showerror(title=self.i18n.message_username_error, message=self.i18n.message_username_error)
            elif self.db.user_detail(self.username.get()) is not None:
                msg.showerror(title=self.i18n.message_username_exist, message=self.i18n.message_username_exist)
            elif len(self.password.get()) == 0:
                msg.showerror(title=self.i18n.message_password_error, message=self.i18n.message_password_error)
            elif len(self.role.get()) == 0:
                msg.showerror(title=self.i18n.message_role_error, message=self.i18n.message_role_error)
            elif len(self.email.get()) == 0:
                msg.showerror(title=self.i18n.message_email_error, message=self.i18n.message_email_error)
            elif len(str(self.phone.get())) == 0:
                msg.showerror(title=self.i18n.message_phone_error, message=self.i18n.message_phone_error)
            else:
                self.db.add_user(role=self.role.get(), username=self.username.get(),
                                  password=self.password.get(), email=self.email.get(), phone=self.phone.get())
                msg.showinfo(self.i18n.message_save_success_user, self.i18n.message_save_success_user)
                self.clear_text_boxes()
                self.txt_username.focus_set()
        except (tk.TclError, sqlite3.Error) as err:
            msg.showerror(title=self.i18n.message_save_error_user, message=self.i18n.message_save_error_user + "\n" + str(err))

    def clear_text_boxes(self):
        self.txt_username.delete(0, "end")
        self.txt_password.delete(0, "end")
        self.txt_role.delete(0, "end")
        self.txt_email.delete(0, "end")
        self.txt_phone.delete(0, "end")

    def create_widgets(self):
        self.lbl_username = ttk.Label(self, text=self.i18n.text_username)
        self.lbl_username.grid(column=0, row=0, padx=15, pady=15, sticky="w")

        self.lbl_password = ttk.Label(self, text=self.i18n.text_password)
        self.lbl_password.grid(column=0, row=1, padx=15, pady=(0, 15), sticky="w")

        self.lbl_role = ttk.Label(self, text=self.i18n.text_role)
        self.lbl_role.grid(column=0, row=2, padx=15, pady=(0, 15), sticky="w")

        self.lbl_email = ttk.Label(self, text=self.i18n.text_email)
        self.lbl_email.grid(column=0, row=3, padx=15, pady=(0, 15), sticky="w")

        self.lbl_phone = ttk.Label(self, text=self.i18n.text_phone)
        self.lbl_phone.grid(column=0, row=4, padx=15, pady=(0, 15), sticky="w")

        self.txt_username = ttk.Entry(self, textvariable=self.username, width=35)
        self.txt_username.grid(column=1, row=0, padx=(0, 15), pady=15)

        self.txt_password = ttk.Entry(self, textvariable=self.password, width=35)
        self.txt_password.grid(column=1, row=1, padx=(0, 15), pady=(0, 15))

        self.txt_role = ttk.Entry(self, textvariable=self.role, width=35)
        self.txt_role.grid(column=1, row=2, padx=(0, 15), pady=(0, 15))

        self.txt_email = ttk.Entry(self, textvariable=self.email, width=35)
        self.txt_email.grid(column=1, row=3, padx=(0, 15), pady=(0, 15))

        self.txt_phone = ttk.Entry(self, textvariable=self.phone, width=35)
        self.txt_phone.grid(column=1, row=4, padx=(0, 15), pady=(0, 15))

        self.btn_save = ttk.Button(self, text=self.i18n.text_save_button_user, command=self.save_user)
        self.btn_save.grid(column=0, row=5, columnspan=2, pady=(0, 15), sticky="e")

    def bind_widgets(self):
        self.txt_phone.bind("<Return>", self.save_user)

    def close_window(self):
        self.parent.deiconify()
        self.destroy()
