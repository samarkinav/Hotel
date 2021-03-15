import tkinter as tk
import tkinter.messagebox as mb
from PIL import ImageTk as ITk

from viewdb.viewdb import DBmodel


class DetailsWindow(tk.Toplevel):
    def __init__(self, reserve_parent):
        super().__init__(reserve_parent)

        self.parent = reserve_parent

        self.db = DBmodel()

        self.id_room = 0

        self.config(bg='#662209')
        self.title('Отель Беркут')
        self.geometry('550x400')
        #self.iconbitmap('..', 'images/Hotel.ico')
        self.resizable(width=True, height=True)

        self.bg = ITk.PhotoImage(file='images/lux.jpg')
        self.bg_image = tk.Label(self, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        # ========= DETAILS FRAME ===========

        self.frame1 = tk.LabelFrame(self, text='Детали вашего бронирования')
        self.frame1.place(relx=0.04, rely=0.02, relwidth=0.43, relheight=0.8)

        self.grid_rowconfigure(3, minsize=30, weight=60)

        #self.empty_lbl = tk.Label(self.frame1).grid(row=0, column=0)

        self.label_date_in = tk.Label(self.frame1, text='Дата заезда:')
        self.label_date_in.grid(row=1, column=0)

        self.date_in = tk.Label(self.frame1)
        self.date_in.grid(row=1, column=1)

        self.label_date_out = tk.Label(self.frame1, text='Дата выезда:')
        self.label_date_out.grid(row=2, column=0)

        self.date_out = tk.Label(self.frame1)
        self.date_out.grid(row=2, column=1)

        self.label_room = tk.Label(self.frame1, text="Ваши апартаменты: ")
        self.label_room.grid(row=3, column=0)

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

        self.edit_btn = tk.Button(self.frame1, text='Изменить детали \nбронирования',
                                  font=('UnicephalonCyrillic', 10), activebackground='#9E886A',
                                  bg='#662209', fg="#F5DEB3", cursor='hand2', command=self.edit_details)
        self.edit_btn.place(relx=0, rely=0.85, relwidth=1, relheight=0.15)

        # -------------FRAME REGISTRATON----------------------

        self.frame2 = tk.LabelFrame(self, text='Регистрация')
        self.frame2.place(relx=0.5, rely=0.02, relwidth=0.46, relheight=0.8)

        self.error_lbl = tk.Label(self.frame2, text='', fg='red')
        self.error_lbl.pack()

        self.label_first_name = tk.Label(self.frame2, text='Имя')
        self.label_first_name.pack()

        self.first_name = tk.Entry(self.frame2)
        self.first_name.pack()
        self.first_name.bind('<KeyRelease>', self.check_data)

        self.label_second_name = tk.Label(self.frame2, text='Фамилия')
        self.label_second_name.pack()

        self.second_name = tk.Entry(self.frame2)
        self.second_name.pack()
        self.second_name.bind('<KeyRelease>', self.check_data)

        self.label_login = tk.Label(self.frame2, text='Логин')
        self.label_login.pack()

        self.login = tk.Entry(self.frame2)
        self.login.pack()
        self.login.bind('<KeyRelease>', self.check_login)

        self.label_password = tk.Label(self.frame2, text='Пароль')
        self.label_password.pack()

        self.password = tk.Entry(self.frame2)
        self.password.pack()
        self.password.config(show="*")
        self.password.bind('<KeyRelease>', self.check_data)

        self.reservation = tk.Button(self.frame2, text='Забронировать', cursor='hand2',
                                     state='disabled', activebackground='#9E886A',
                                     bg='#662209', fg='#F5DEB3', font=('UnicephalonCyrillic', 10))
        self.reservation.place(relx=0, rely=0.85, relwidth=1, relheight=0.15)
        self.reservation.bind('<Button-1>', self.confirm_reserve)
        self.reservation.bind('<Button-1>', self.check_data, add='+')


        self.sign_in_btn = tk.Button(self, text='Вернуться на главный экран',
                                     bg='#662209', fg="#F5DEB3", cursor='hand2',
                                     command=self.confirm_delete, activebackground='#9E886A',)
        self.sign_in_btn.pack(fill='both', side='bottom')

    def set_details_from_reserve(self, date_in, date_out, room, food, total_price_int, capasity, id_room):
        self.date_in.config(text=f'{self.normal_date(date_in)}')
        self.date_out.config(text=f'{self.normal_date(date_out)}')
        self.room.config(text=room)
        self.capasity.config(text=capasity)
        self.food.config(text=food)
        self.total_price.config(text=f'{total_price_int}')
        self.id_room = id_room

    @staticmethod
    def normal_date(date):
        tuple_date = str(date).split('-')
        return tuple_date[2] + '/' + tuple_date[1] + '/' + tuple_date[0]

    def show_info(self):
        msg = "Номер успешно забронирован!\n Вам доступен личный кабинет"
        mb.showinfo("Поздравляем!", msg)
        self.destroy()
        self.parent.parent.deiconify()

    def back_to_main(self):
        self.destroy()
        self.parent.destroy()
        self.parent.parent.deiconify()

    def edit_details(self):
        self.destroy()
        #self.parent.frame1.place_forget()
        self.parent.frame2.place_forget()
        #self.parent.frame1.place(relx=0.3, rely=0.02, relwidth=0.4, relheight=0.8)
        #self.parent.available_cmbbx.current(newindex=None)
        self.parent.deiconify()

    def confirm_delete(self):
        msg = "Вы уверены, что хотите прервать бронирование?"
        if mb.askyesno(message=msg, parent=self):
            self.back_to_main()

    def record_all(self, first_name, last_name, login, password, date_in, date_out, food):
        #try:
        #login1 = login
        if not self.db.is_client_found(login, password):
            self.db.insert_client_in_data(first_name, last_name, login, password)
        self.db.add_new_reservation(login, food, date_in, date_out, self.id_room)
        self.reservation.config(state='normal')
        self.show_info()

    def check_login(self, event):
        self.check_data(event)
        if self.db.is_login_exist(self.login.get()):
            self.error_lbl.config(text='Логин занят')
        else:
            self.error_lbl.config(text='')

    def check_data(self, event):
        if self.first_name.get().strip() == '' or self.second_name.get().strip() == '' \
            or self.login.get().strip() == '' or self.password.get().strip() == '':
            self.reservation.config(state='disabled')
        else:
            self.reservation.config(state='normal')

    def confirm_reserve(self, event):
        if self.reservation['state'] != 'disabled' and self.error_lbl['text'] != "Логин занят":
            if mb.askyesno('Подтверждение', "Подтвердить бронирование?"):
                self.record_all(self.first_name.get(),
                                self.second_name.get(),
                                self.login.get(),
                                self.password.get(),
                                self.parent.date_in,
                                self.parent.date_out,
                                self.food['text'])

                self.first_name.delete(0, last=tk.END)
                self.second_name.delete(0, last=tk.END)
                self.login.delete(0, last=tk.END)
                self.password.delete(0, last=tk.END)

                self.back_to_main()
