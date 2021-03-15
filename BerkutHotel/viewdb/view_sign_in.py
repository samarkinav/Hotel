import tkinter as tk
from PIL import ImageTk as ITk
import tkinter.messagebox as mb
from PIL import ImageTk as ITk

from viewdb.viewdb import DBmodel

from view.admin_view import AdminAccountWindow
from view.view_account import PersonalAccountWindow


class SignInWindow(tk.Toplevel):

    def __init__(self, welcome_parent):
        super().__init__(welcome_parent)

        self.parent = welcome_parent

        self.db = DBmodel()

        self.config(bg='#662209')
        self.title('Отель Беркут')
        self.geometry('550x450')
        #self.iconbitmap('..', 'images/Hotel.ico')
        self.resizable(width=True, height=True)

        self.bg = ITk.PhotoImage(file='images/inside.png')
        self.bg_image = tk.Label(self, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        self.grid_rowconfigure(3, minsize=30, weight=60)

        self.frame = tk.LabelFrame(self, bg='#662209', fg="#F5DEB3")
        self.frame.place(relx=0.25, rely=0.2, relwidth=0.5, relheight=0.4)

        self.label_login = tk.Label(self.frame, bg='#662209', fg="#F5DEB3", text='\n\nЛогин')
        self.label_login.place(x=10, y=0)

        self.login_ent = tk.Entry(self.frame, width=26)
        self.login_ent.place(x=10, y=55)
        #self.login_ent.insert(0, 'person1')
        self.login_ent.bind('<KeyRelease>', self.check_data)

        self.label_password = tk.Label(self.frame, bg='#662209', fg="#F5DEB3", text='Пароль')
        self.label_password.place(x=10, y=85)

        self.password_ent = tk.Entry(self.frame, width=26, show="*")
        self.password_ent.place(x=10, y=110)
        #self.password_ent.insert(0, 'person1')
        self.password_ent.bind('<KeyRelease>', self.check_data)

        self.sign_in_btn = tk.Button(self.frame, bg='#662209', fg="#F5DEB3", text='Войти',
                                     width=40, cursor='hand2')
        self.sign_in_btn.pack(side=tk.BOTTOM)
        self.sign_in_btn.bind('<Button-1>', lambda event: self.sign_in(event, self.login_ent.get(),
                                                                       self.password_ent.get()))

        self.back = tk.Button(self, text='На главный экран', cursor='hand2',
                              bg='#662209', fg="#F5DEB3", command=self.back)
        self.back.grid(sticky=tk.NE)

    def back(self):
        self.destroy()
        self.parent.deiconify()

    @staticmethod
    def show_error(msg):
        mb.showerror("Ошибка", msg)

    def sign_in(self, event, login, password):
        if self.sign_in_btn['state'] != 'disabled':
            if self.db.is_admin_found(login, password):
                AdminAccountWindow(self)
                self.withdraw()
            elif self.db.is_client_found(login, password):
                PersonalAccountWindow(self, login, password)
                self.withdraw()
            else:
                self.show_error("Пользователь не зарегистрирован")

    def check_data(self, event):
        if self.login_ent.get().strip() == '' or self.password_ent.get().strip() == '':
            self.sign_in_btn.config(state='disabled')
        else:
            self.sign_in_btn.config(state='normal')
