from tkinter import *
from PIL import ImageTk as ITk #pip install pillow

from view.view_sign_in import SignInWindow
from view.view_reserve import ReservationWindow


class WelcomeWindow(Tk):

    def blinking(self):
        text = 'Добро пожаловать в отель "БЕРКУТ"!'

        if text[self.i] != '!':
            self.show_text += text[self.i]
            self.i += 1
        else:
            self.show_text = ''
            self.i = 0

        if self.flag == 1:
            self.welcome_lbl.config(fg='#9E886A', text=self.show_text)
            self.flag = 0
        else:
            self.welcome_lbl.config(fg='#F5DEB3', text=self.show_text)
            self.flag = 1

        self.after(400, self.blinking)

    def __init__(self):
        super().__init__()

        self.title('Отель Беркут')
        self.geometry('900x500')
        self.resizable(width=False, height=False)
        #self.iconbitmap('..', 'images/Hotel.ico')
        self.config(bg='#662209')

        self.flag = 0

        #=====BG IMAGE=====
        self.bg = ITk.PhotoImage(file='images/inside.png')
        self.bg_image = Label(self, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        self.grid_rowconfigure(3, minsize=30, weight=60)

        self.frame = Frame(self, relief=RAISED, bg='#662209')
        self.frame.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.4)

        self.welcome_lbl = Label(self.frame, bg='#662209', fg='#F5DEB3',
                                 text='Добро пожаловать в отель "БЕРКУТ"!',
                                 font=('Impact', '20', "bold"))
        self.welcome_lbl.pack(side='top', pady=10)

        self.i = 0
        self.show_text = ''
        self.blinking()

        self.book_btn = Button(self.frame, text='\nЗабронировать\n    номер  \n', font=('Goudy old style', 12),
                               bg='#662209', fg="#F5DEB3", cursor='hand2',
                               command=self.run_reservation_window, activebackground='#9E886A')
        self.book_btn.place(relx=0.05, rely=0.5, relwidth=0.35, relheight=0.35)

        self.or_lbl = Label(self.frame, text='или', bg='#662209', fg='#F5DEB3')
        self.or_lbl.place(relx=0.48, rely=0.6)

        self.sign_in_btn = Button(self.frame, text='Войти в\n личный\n кабинет', font=('Goudy old style', 12),
                                  bg='#662209', fg="#F5DEB3", cursor='hand2',
                                  command=self.run_sign_in, activebackground='#9E886A')
        self.sign_in_btn.place(relx=0.6, rely=0.5, relwidth=0.35, relheight=0.35)

        self.admin_btn = Button(self, text='Войти как администратор',
                                bg='#662209', fg="#F5DEB3", cursor='hand2',
                                command=self.run_sign_in, activebackground='#9E886A')
        self.admin_btn.pack(fill='both', side='bottom')

    def run_reservation_window(self):
        self.withdraw()
        reservation_window = ReservationWindow(self)

    def run_sign_in(self):
        self.withdraw()
        sign_in_window = SignInWindow(self)
