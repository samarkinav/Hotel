import tkinter as tk
import tkinter.messagebox as mb
from PIL import ImageTk as ITk

from viewdb.viewdb import DBmodel


class PersonalAccountWindow(tk.Toplevel):
    def __init__(self, sign_in_parent, login, password):
        super().__init__(sign_in_parent)

        self.parent = sign_in_parent

        self.db = DBmodel()

        self.id_client = []

        self.config(bg='#662209')
        self.title('Отель Беркут')
        self.geometry('700x500')
        #self.iconbitmap('..', 'images/Hotel.ico')
        self.resizable(width=True, height=True)

        self.bg = ITk.PhotoImage(file='images/standard.jpg')
        self.bg_image = tk.Label(self, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        self.welcome_lbl = tk.Label(self, bg='#662209', text='Добро пожаловать, Человек Человечиков!',
                                    font=('Hanging Letters', 15, 'bold'), fg='#F5DEB3')
        self.welcome_lbl.pack()

        self.frame1 = tk.LabelFrame(self, text='Детали вашего бронирования',
                                    font=('Hanging Letters', 10))
        self.frame1.place(relx=0.3, rely=0.2, relwidth=0.4, relheight=0.6)

        self.grid_rowconfigure(3, minsize=30, weight=60)

        self.empty_lbl = tk.Label(self.frame1)
        self.empty_lbl.grid(row=0, column=0)

        self.label_date_in = tk.Label(self.frame1, text='Дата заезда:')
        self.label_date_in.grid(row=1, column=0)

        self.date_in = tk.Label(self.frame1)
        self.date_in.grid(row=1, column=1)

        self.label_date_out = tk.Label(self.frame1, text='Дата выезда:')
        self.label_date_out.grid(row=2, column=0)

        self.date_out = tk.Label(self.frame1)
        self.date_out.grid(row=2, column=1)

        self.label_room = tk.Label(self.frame1, text="Ваши апартаменты: ")
        self.label_room.grid(row=3, column=0, padx=20)

        self.room = tk.Label(self.frame1)
        self.room.grid(row=3, column=1)

        self.lbl_capasity = tk.Label(self.frame1, text="Кол-во человек:")
        self.lbl_capasity.grid(row=4, column=0)

        self.capasity = tk.Label(self.frame1)
        self.capasity.grid(row=4, column=1)

        self.label_food = tk.Label(self.frame1, text="Ваш тип питания: ")
        self.label_food.grid(row=5, column=0)

        self.food = tk.Label(self.frame1)
        self.food.grid(row=5, column=1)

        self.total_price_lbl = tk.Label(self.frame1, text='Итоговая стоимость: ')
        self.total_price_lbl.grid(row=6, column=0)

        self.total_price = tk.Label(self.frame1)
        self.total_price.grid(row=6, column=1)

        self.empty_lbl_2 = tk.Label(self.frame1)
        self.empty_lbl_2.grid(row=7, column=0)

        self.edit_firstname_btn = tk.Button(self.frame1, text="Редактировать личные данные", cursor='hand2',
                                            bg='#662209', fg="#F5DEB3", command=self.edit)
        self.edit_firstname_btn.place(relx=0.1, rely=0.8, relwidth=0.8, relheight=0.1)

        self.back = tk.Button(self, text='На главный экран', cursor='hand2',
                              bg='#662209', fg="#F5DEB3", command=self.back_to_main)
        self.back.pack(side=tk.BOTTOM, fill='both')

        self.show_details(login, password)

    def back_to_main(self):
        self.destroy()
        self.parent.destroy()
        self.parent.parent.deiconify()

    def show_details(self, login, password):
        FirstName = self.db.find_client(login, password)[1]
        LastName = self.db.find_client(login, password)[2]
        self.id_client = self.db.find_client(login, password)[0]
        self.welcome_lbl.config(text=f'Добро пожаловать, {FirstName} {LastName}!')

        [date_in, date_out, category, food, total_price, capasity] = self.db.sign_in()
        self.date_in.config(text=f"{self.normal_date(date_in)}")
        self.date_out.config(text=f"{self.normal_date(date_out)}")
        self.room.config(text=f"{category}")
        self.capasity.config(text=f"{capasity}")
        self.food.config(text=f"{food}")
        self.total_price.config(text=f"{int(total_price)}")

    @staticmethod
    def normal_date(date):
        tuple_date = str(date).split('-')
        return tuple_date[2] + '/' + tuple_date[1] + '/' + tuple_date[0]

    def edit(self):
        Edit(self, self.id_client)


class Edit(tk.Toplevel):
    def __init__(self, parent, id_client):
        super().__init__(parent)

        self.id_client = id_client
        self.parent = parent
        self.db = DBmodel()

        self.title('Редактировать личные данные')
        self.geometry('400x220+400+300')
        self.config(bg='#662209')
        self.resizable(False, False)

        label_last_name = tk.Label(self, text='Фамилия', bg='#662209', fg="#F5DEB3")
        label_last_name.place(x=50, y=50)

        self.entry_last_name = tk.Entry(self)
        self.entry_last_name.place(x=200, y=50)
        self.entry_last_name.bind('<KeyRelease>', self.check_data)

        label_name = tk.Label(self, text='Имя', bg='#662209', fg="#F5DEB3")
        label_name.place(x=50, y=80)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=80)
        self.entry_name.bind('<KeyRelease>', self.check_data)

        label_login = tk.Label(self, text='Логин', bg='#662209', fg="#F5DEB3")
        label_login.place(x=50, y=110)

        self.entry_login = tk.Entry(self)
        self.entry_login.place(x=200, y=110)
        self.entry_login.bind('<KeyRelease>', self.check_data)
        self.entry_login.bind('<KeyRelease>', self.check_login, add='+')

        label_password = tk.Label(self, text='Пароль', bg='#662209', fg="#F5DEB3")
        label_password.place(x=50, y=140)

        self.entry_password = tk.Entry(self)
        self.entry_password.place(x=200, y=140)
        self.entry_password.bind('<KeyRelease>', self.check_data)

        self.default_data()

        self.btn_edit = tk.Button(self, text='Редактировать', bg='#662209', fg="#F5DEB3")
        self.btn_edit.place(x=100, y=170)
        self.btn_edit.bind('<Button-1>', self.edit_data)

        self.btn_cancel = tk.Button(self, bg='#662209', fg="#F5DEB3", text='Отмена',
                                    cursor='hand2', command=self.destroy, width=10)
        self.btn_cancel.place(x=200, y=170)

    def default_data(self):
        self.db.c.execute('''SELECT * FROM CLIENTS WHERE Idclient=%s''', [self.id_client])
        row = self.db.c.fetchone()
        self.entry_last_name.insert(0, row[2])
        self.entry_name.insert(0, row[1])
        self.entry_login.insert(0, row[3])
        self.entry_password.insert(0, row[4])

    def update_client_in_data(self, first_name, last_name, login, password):
        self.db.c.execute('''UPDATE CLIENTS SET FirstName=%s, LastName=%s, Login=%s, PersonPassword=%s WHERE Idclient=%s''',
                         [first_name, last_name, login, password, self.id_client])
        self.db.conn.commit()
        self.destroy()
        mb.showinfo('Данные обновлены', 'Данные успешно обновлены!')
        self.parent.show_details(login, password)

    def check_login(self, event):
        if self.db.is_login_exist(self.entry_login.get()):
            self.btn_edit.config(state='disabled')
        else:
            self.btn_edit.config(state='normal')

    def check_data(self, event):
        if self.entry_name.get().strip() == '' or self.entry_last_name.get().strip() == '' \
            or self.entry_login.get().strip() == '' or self.entry_password.get().strip() == '':
            self.btn_edit.config(state='disabled')
        else:
            self.btn_edit.config(state='normal')

    def edit_data(self, event):
        if self.btn_edit['state'] == 'normal':
            self.update_client_in_data(self.entry_name.get(),
                                       self.entry_last_name.get(),
                                       self.entry_login.get(),
                                       self.entry_password.get())
