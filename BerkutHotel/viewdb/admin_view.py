import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from PIL import ImageTk as ITk

from viewdb.viewdb import DBmodel


class AdminAccountWindow(tk.Toplevel):
    def __init__(self, sign_in_parent):
        super().__init__(sign_in_parent)

        self.parent = sign_in_parent

        self.db = DBmodel()

        self.title("Окно администратора")
        self.geometry("900x400+300+200")
        self.resizable(False, False)
        self.config(bg='#662209')

        self.bg = ITk.PhotoImage(file='images/inside.png')
        self.bg_image = tk.Label(self, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        # ========== FRAMES ===========

        self.combobox = ttk.Combobox(self, values=['Полная информация',
                                                   'Зарегистрированные пользователи',
                                                   'Информация о номерах'],
                                     width=35, justify=tk.CENTER, state='readonly')
        self.combobox.pack()
        self.combobox.bind('<<ComboboxSelected>>', self.show_table)
        self.combobox.current(0)

        self.info_btn_frame = tk.Frame(self, bg='#662209', bd=2)
        self.info_btn_frame.pack()

        self.clients_btn_frame = tk.Frame(self, bg='#662209', bd=2)
        #self.clients_btn_frame.grid(row=1, column=0)

        self.rooms_btn_frame = tk.Frame(self, bg='#662209', bd=2)
        #self.rooms_btn_frame.grid(row=1, column=0)

        self.combobox_filter = ttk.Combobox(self.info_btn_frame, values=['Прошедшие брони', 'Активные брони',
                                                                         'Предстоящие брони', 'Все бронирования'],
                                            justify=tk.CENTER, state='readonly')
        self.combobox_filter.grid(row=0, column=0)
        self.combobox_filter.bind('<<ComboboxSelected>>', self.filter_table)
        self.combobox_filter.current(3)

        # ========= ПОЛНАЯ ИНФОРМАЦИЯ =============

        # self.btn_info_delete = tk.Button(self.info_btn_frame, text='Удалить бронь',
        #                                  bg='#006400', fg="#F5DEB3", bd=1, cursor='hand2',
        #                                  compound=tk.TOP, command=self.delete_info_records)
        # self.btn_info_delete.grid(row=0, column=1)
        #
        # self.btn_info_edit = tk.Button(self.info_btn_frame, text='Редактировать бронь',
        #                                bg='#006400', fg="#F5DEB3", bd=1, cursor='hand2',
        #                                compound=tk.TOP, command=self.info_edit)
        # self.btn_info_edit.grid(row=0, column=2)

        self.btn_info_search = tk.Button(self.info_btn_frame, text='Поиск',
                                         bg='#662209', fg="#F5DEB3", bd=1, cursor='hand2',
                                         compound=tk.TOP, command=self.open_search_info_dialog)
        #self.btn_info_search.grid(row=0, column=3)

        self.btn_info_refresh = tk.Button(self.info_btn_frame, text='Вернуться к полной таблице',
                                          bg='#662209', fg="#F5DEB3", bd=1, cursor='hand2',
                                          compound=tk.TOP, command=self.view_info_refresh)

        # ============ КЛИЕНТЫ ==============

        # self.btn_clients_add = tk.Button(self.clients_btn_frame, text='Добавить клиента',
        #                                  bg='#006400', fg="#F5DEB3",
        #                                  bd=1, cursor='hand2', compound=tk.TOP, command=self.add_info_dialog)
        # self.btn_clients_add.grid(row=0, column=0)

        self.btn_clients_delete = tk.Button(self.clients_btn_frame, text='Удалить клиента',
                                            bg='#662209', fg="#F5DEB3",
                                            bd=1, cursor='hand2', compound=tk.TOP, command=self.delete_clients_records)
        self.btn_clients_delete.grid(row=0, column=1)

        self.btn_clients_edit = tk.Button(self.clients_btn_frame, text='Редактировать данные клиента',
                                          bg='#662209', fg="#F5DEB3",
                                          bd=1, cursor='hand2', compound=tk.TOP, command=self.clients_edit)
        self.btn_clients_edit.grid(row=0, column=2)

        self.btn_clients_search = tk.Button(self.clients_btn_frame, text='Поиск по фамилии',
                                            bg='#662209', fg="#F5DEB3",
                                            bd=1, cursor='hand2', compound=tk.TOP,
                                            command=self.open_search_clients_dialog)
        self.btn_clients_search.grid(row=0, column=3)

        self.btn_clients_refresh = tk.Button(self.clients_btn_frame, text='Вернуться к полной таблице',
                                             bg='#662209', fg="#F5DEB3",
                                             bd=1, cursor='hand2', compound=tk.TOP, command=self.view_clients_refresh)

        # ============ АПАРТАМЕНТЫ ==============

        self.btn_rooms_add = tk.Button(self.rooms_btn_frame, text='Добавить номер',
                                       bg='#662209', fg="#F5DEB3", bd=1, cursor='hand2',
                                       compound=tk.TOP, command=self.add_rooms_dialog)
        self.btn_rooms_add.grid(row=0, column=0)

        self.btn_rooms_delete = tk.Button(self.rooms_btn_frame, text='Удалить номер',
                                          bg='#662209', fg="#F5DEB3",
                                          bd=1, cursor='hand2', compound=tk.TOP, command=self.delete_rooms_records)
        self.btn_rooms_delete.grid(row=0, column=1)

        self.btn_rooms_edit = tk.Button(self.rooms_btn_frame, text='Редактировать',
                                        bg='#662209', fg="#F5DEB3", bd=1, cursor='hand2',
                                        compound=tk.TOP, command=self.rooms_edit)
        self.btn_rooms_edit.grid(row=0, column=2)

        self.btn_rooms_search = tk.Button(self.rooms_btn_frame, text='Поиск по категории',
                                          bg='#662209', fg="#F5DEB3", bd=1, cursor='hand2',
                                          compound=tk.TOP, command=self.open_search_rooms_dialog)
        self.btn_rooms_search.grid(row=0, column=3)

        self.btn_rooms_refresh = tk.Button(self.rooms_btn_frame, text='Вернуться к полной таблице',
                                           bg='#662209', fg="#F5DEB3", cursor='hand2', bd=1,
                                           compound=tk.TOP, command=self.view_rooms_refresh)

        # ===============  ===============

        self.treeframe = tk.Frame(self, bg='#662209')
        self.treeframe.pack()

        self.info_table()
        self.view_info_refresh()

        self.back_to_welcome_btn = tk.Button(self, text='На главный экран',
                                             cursor='hand2', bg='#662209', fg="#F5DEB3",
                                             command=self.back_to_welcome, activebackground='#9E886A',)
        self.back_to_welcome_btn.pack(fill=tk.X, side=tk.BOTTOM)

    def back_to_welcome(self):
        self.destroy()
        self.parent.destroy()
        self.parent.parent.deiconify()

    def show_table(self, event):
        if self.combobox.get() == 'Полная информация':
            self.clients_btn_frame.pack_forget()
            self.rooms_btn_frame.pack_forget()

            self.info_btn_frame.pack()

            self.combobox_filter.grid(row=0, column=0, sticky='we')

            self.info_table()
            self.view_info_refresh()
        elif self.combobox.get() == 'Зарегистрированные пользователи':
            self.info_btn_frame.pack_forget()
            self.rooms_btn_frame.pack_forget()

            self.combobox_filter.grid_forget()

            self.clients_btn_frame.pack()

            self.clients_table()
            self.view_clients_refresh()
        else:
            self.info_btn_frame.pack_forget()
            self.clients_btn_frame.pack_forget()

            self.combobox_filter.grid_forget()

            self.rooms_btn_frame.pack()

            self.rooms_table()
            self.view_rooms_refresh()

    # ============= ФИЛЬТРЫ =================

    def filter_table(self, event):
        self.info_table()

        if self.combobox_filter.get() == 'Все бронирования':
            self.view_info_refresh()
            self.btn_info_search.grid(row=0, column=3)
        elif self.combobox_filter.get() == 'Прошедшие брони':
            self.filter_past_reserve()
            self.btn_info_search.grid_forget()
        elif self.combobox_filter.get() == 'Активные брони':
            self.filter_now_reserve()
            self.btn_info_search.grid_forget()
        else:
            self.filter_future_reserve()
            self.btn_info_search.grid_forget()

    def filter_past_reserve(self):
        self.db.c.execute('''SELECT * FROM DOP WHERE DateOut < CURDATE()''')

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def filter_now_reserve(self):
        self.db.c.execute('''SELECT * FROM DOP WHERE DateIn < CURDATE() AND DateOut > CURDATE()''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def filter_future_reserve(self):
        self.db.c.execute('''SELECT * FROM DOP WHERE DateIn > CURDATE()''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    # ============ ШАПКИ ==============

    def info_table(self):
        self.treeframe.pack_forget()

        self.treeframe = tk.Frame(self, bg='#d7d8e0')
        self.treeframe.pack()

        self.tree = ttk.Treeview(self.treeframe, columns=('ID', 'DateIn', 'DateOut', 'Nights',
                                                          'LastName', 'FirstName', 'Category',
                                                          'Capasity', 'TypeOfFood', 'Total'),
                                 height=15, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('DateIn', width=80, anchor=tk.CENTER)
        self.tree.column('DateOut', width=80, anchor=tk.CENTER)
        self.tree.column('Nights', width=90, anchor=tk.CENTER)
        self.tree.column('LastName', width=100, anchor=tk.CENTER)
        self.tree.column('FirstName', width=100, anchor=tk.CENTER)
        self.tree.column('Category', width=110, anchor=tk.CENTER)
        self.tree.column('Capasity', width=85, anchor=tk.CENTER)
        self.tree.column('TypeOfFood', width=80, anchor=tk.CENTER)
        self.tree.column('Total', width=120, anchor=tk.CENTER)

        self.tree.heading('ID', text='№')
        self.tree.heading('DateIn', text='Дата заезда')
        self.tree.heading('DateOut', text='Дата выезда')
        self.tree.heading('Nights', text='Кол-во ночей')
        self.tree.heading('LastName', text='Фамилия')
        self.tree.heading('FirstName', text='Имя')
        self.tree.heading('Category', text='Категория номера')
        self.tree.heading('Capasity', text='Вместимость')
        self.tree.heading('TypeOfFood', text='Тип питания')
        self.tree.heading('Total', text='Итоговая стоимость')

        self.tree.grid(row=2, column=0)

        scroll = tk.Scrollbar(self.treeframe, command=self.tree.yview)
        scroll.grid(row=2, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scroll.set)

    def clients_table(self):
        self.treeframe.pack_forget()

        self.treeframe = tk.Frame(self, bg='#d7d8e0')
        self.treeframe.pack()

        self.tree = ttk.Treeview(self.treeframe, columns=('Idclient', 'FirstName', 'LastName', 'Login'),
                                 height=15, show='headings')

        self.tree.column('Idclient', width=30, anchor=tk.CENTER)
        self.tree.column('FirstName', width=150, anchor=tk.CENTER)
        self.tree.column('LastName', width=150, anchor=tk.CENTER)
        self.tree.column('Login', width=150, anchor=tk.CENTER)
        # self.tree.column('PersonPassword', width=100, anchor=tk.CENTER)

        self.tree.heading('Idclient', text='№')
        self.tree.heading('FirstName', text='Имя')
        self.tree.heading('LastName', text='Фамилия')
        self.tree.heading('Login', text='Логин')
        # self.tree.heading('PersonPassword', text='Пароль')

        self.tree.grid(row=2, column=0)

        scroll = tk.Scrollbar(self.treeframe, command=self.tree.yview)
        scroll.grid(row=2, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scroll.set)

    def rooms_table(self):
        self.treeframe.pack_forget()

        self.treeframe = tk.Frame(self, bg='#d7d8e0')
        self.treeframe.pack()

        self.tree = ttk.Treeview(self.treeframe, columns=('Idroom', 'Category', 'Capasity', 'Price'),
                                 height=15, show='headings')

        self.tree.column('Idroom', width=30, anchor=tk.CENTER)
        self.tree.column('Category', width=150, anchor=tk.CENTER)
        self.tree.column('Capasity', width=150, anchor=tk.CENTER)
        self.tree.column('Price', width=150, anchor=tk.CENTER)

        self.tree.heading('Idroom', text='№')
        self.tree.heading('Category', text='Категория номера')
        self.tree.heading('Capasity', text='Вместимость')
        self.tree.heading('Price', text='Цена за сутки, руб')

        self.tree.grid(row=2, column=0)

        scroll = tk.Scrollbar(self.treeframe, command=self.tree.yview)
        scroll.grid(row=2, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scroll.set)

    # ============ ПОКАЗАТЬ ТАБЛИЦЫ =============

    def view_info_refresh(self):
        self.btn_info_search.grid(row=0, column=3)
        self.btn_info_refresh.grid_forget()

        try:
            self.db.c.execute('''DROP TABLE DOP''')
        except:
            pass
        self.db.c.execute('''create temporary table dop
                             SELECT A.Idreservation AS ID, A.DateIn AS DateIn, A.DateOut AS DateOut,
                             DATEDIFF(DateOut, DateIn) AS NIGHTS, A.LastName AS LastName,
                             A.FirstName AS FirstName, A.Category AS Category, A.Capasity AS Capasity,
                             B.TypeOfFood AS TypeOfFood,
                             (A.Price + B.Price)*DATEDIFF(DateOut, DateIn) AS Total
                             FROM (SELECT A.Idreservation, A.DateIn, A.DateOut, A.LastName, A.FirstName, A.idfood,
                             B.Category, B.Capasity, B.Price
                             FROM (SELECT A.Idreservation, A.DateIn, A.DateOut, A.idroom, A.idfood, B.LastName, B.FirstName
                             FROM RESERVATION AS A JOIN CLIENTS AS B ON A.idclient = B.idclient)
                             AS A JOIN ROOMS AS B ON A.idroom = B.idroom)
                             AS A JOIN TYPEOFFOOD AS B ON A.idfood = B.idfood
                             ORDER BY ID''')
        self.db.c.execute('''SELECT * FROM DOP''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def view_clients_refresh(self):
        self.btn_clients_search.grid(row=0, column=3)
        self.btn_clients_refresh.grid_forget()

        self.db.c.execute('''SELECT * FROM CLIENTS''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def view_rooms_refresh(self):
        self.btn_rooms_search.grid(row=0, column=3)
        self.btn_rooms_refresh.grid_forget()

        self.db.c.execute('''SELECT * FROM ROOMS''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    # def view_records(self, value):              #Починить
    #     self.btn_info_search.pack(side=tk.LEFT)
    #     self.btn_refresh.pack_forget()
    #
    #     arg = ('%' + value + '%',)
    #     self.db.c.execute('''SELECT * FROM ?''', arg)
    #     [self.tree.delete(i) for i in self.tree.get_children()]
    #     [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    # ========== ДОБАВИТЬ ===========

    def add_info_dialog(self):
        # AddInfo(self)
        pass

    def add_clients_dialog(self):
        # AddClient(self)
        pass

    def add_client(self, firstname, lastname, login, password):
        self.db.add_new_client(firstname, lastname, login, password)
        self.view_clients_refresh()

    def add_rooms_dialog(self):
        AddRoom(self)

    def add_room(self, category, capasity, price):
        self.db.add_new_room(category, capasity, price)
        self.view_rooms_refresh()
        #self.destroy()

    # ========= УДАЛЕНИЕ ============

    def delete_info_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''SET SQL_SAFE_UPDATES=0;DELETE FROM DOP WHERE ID=%s;SET SQL_SAFE_UPDATES=1''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_info_refresh()

    def delete_clients_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''SELECT count(*) FROM RESERVATION WHERE Idclient=%s''',
                              (self.tree.set(selection_item, '#1'),))

        if self.db.c.fetchone()[0] > 0:
            msg = 'Внимание!\nВ базе находятся бронирования, привязанные к данному клиенту\n' \
                  'Вы уверены, что хотите удалить запись?'
            if mb.askyesno('Удаление', msg):
                for selection_item in self.tree.selection():
                    self.db.c.execute('''DELETE FROM CLIENTS WHERE Idclient=%s''', (self.tree.set(selection_item, '#1'),))
        else:
            for selection_item in self.tree.selection():
                self.db.c.execute('''DELETE FROM CLIENTS WHERE Idclient=%s''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_clients_refresh()

    def delete_rooms_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''SELECT count(*) FROM RESERVATION WHERE Idroom=%s''',
                              (self.tree.set(selection_item, '#1'),))

        if self.db.c.fetchone()[0] > 0:
            msg = 'Внимание!\nВ базе находятся клиенты, привязанные к данному номеру\n' \
                  'Вы уверены, что хотите удалить запись?'
            if mb.askyesno('Удаление', msg):
                for selection_item in self.tree.selection():
                    self.db.c.execute('''DELETE FROM ROOMS WHERE Idroom=%s''', (self.tree.set(selection_item, '#1'),))
        else:
            for selection_item in self.tree.selection():
                self.db.c.execute('''DELETE FROM ROOMS WHERE Idroom=%s''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_rooms_refresh()

    # ========= РЕДАКТИРОВАНИЕ ============

    def clients_edit(self):
        EditClient(self)

    def update_clients_record(self, first_name, last_name, login):
        self.db.c.execute('''UPDATE CLIENTS SET FirstName=%s, LastName=%s, Login=%s WHERE Idclient=%s''',
                          (first_name, last_name, login, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_clients_refresh()

    def rooms_edit(self):
        EditRoom(self)

    def update_room(self, category, capasity, price):
        self.db.c.execute('''UPDATE ROOMS SET Category=%s, Capasity=%s, Price=%s WHERE Idroom=%s''',
                          (category, capasity, price, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_rooms_refresh()

    # ========= ПОИСК ============

    def search_info_records(self, search_value):
        self.btn_info_refresh.grid(row=0, column=4)
        self.btn_info_search.grid_forget()

        self.db.c.execute('''SELECT * FROM DOP WHERE LastName LIKE %s OR FirstName LIKE %s OR Category LIKE %s''', [search_value,search_value,search_value])
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def search_clients_records(self, value):
        self.btn_clients_refresh.grid(row=0, column=4)
        self.btn_clients_search.grid_forget()

        last_name = ('%' + value + '%',)
        self.db.c.execute('''SELECT * FROM CLIENTS WHERE LastName LIKE %s''', last_name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def search_rooms_records(self, value):
        self.btn_rooms_refresh.grid(row=0, column=4)
        self.btn_rooms_search.grid_forget()

        category = ('%' + value + '%',)
        self.db.c.execute('''SELECT * FROM ROOMS WHERE Category LIKE %s''', category)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_search_info_dialog(self):
        SearchReservation(self)

    def open_search_clients_dialog(self):
        SearchClientByLastName(self)

    def open_search_rooms_dialog(self):
        SearchRoomByCategory(self)


class AddRoom(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.title('Добавить номер')
        self.geometry('400x220+400+300')
        self.config(bg='#662209')
        self.resizable(False, False)

        label_category = tk.Label(self, text='Категория',  bg='#662209', fg="#F5DEB3",)
        label_category.place(x=50, y=50)

        self.entry_category = ttk.Entry(self)
        self.entry_category.place(x=200, y=50)

        label_capasity = tk.Label(self, text='Вместимость, чел', bg='#662209', fg="#F5DEB3")
        label_capasity.place(x=50, y=80)

        self.entry_capasity = ttk.Entry(self)
        self.entry_capasity.place(x=200, y=80)

        label_price = tk.Label(self, text='Цена за сутки, руб',  bg='#662209', fg="#F5DEB3",)
        label_price.place(x=50, y=110)

        self.entry_price = ttk.Entry(self)
        self.entry_price.place(x=200, y=110)

        self.btn_ok = tk.Button(self, bg='#662209', fg="#F5DEB3", text='Добавить', cursor='hand2', width=10)
        self.btn_ok.place(x=100, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.parent.add_room(self.entry_category.get(),
                                                                          self.entry_capasity.get(),
                                                                          self.entry_price.get()))

        self.btn_cancel = tk.Button(self, bg='#662209', fg="#F5DEB3", text='Закрыть',
                                    cursor='hand2', command=self.destroy, width=10)
        self.btn_cancel.place(x=200, y=170)


class EditRoom(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.db = DBmodel()

        self.title('Редактировать номер')
        self.geometry('400x220+400+300')
        self.config(bg='#662209')
        self.resizable(False, False)

        label_category = tk.Label(self, text='Категория', bg='#662209', fg="#F5DEB3")
        label_category.place(x=50, y=50)

        self.entry_category = tk.Entry(self)
        self.entry_category.place(x=200, y=50)

        label_capasity = tk.Label(self, text='Вместимость, чел', bg='#662209', fg="#F5DEB3")
        label_capasity.place(x=50, y=80)

        self.entry_capasity = tk.Entry(self)
        self.entry_capasity.place(x=200, y=80)

        label_price = tk.Label(self, text='Цена за сутки, руб', bg='#662209', fg="#F5DEB3")
        label_price.place(x=50, y=110)

        self.entry_price = tk.Entry(self)
        self.entry_price.place(x=200, y=110)

        self.default_data()

        btn_edit = tk.Button(self, text='Редактировать', bg='#662209', fg="#F5DEB3")
        btn_edit.place(x=100, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.parent.update_room(self.entry_category.get(),
                                                                          self.entry_capasity.get(),
                                                                          self.entry_price.get()))

        self.btn_cancel = tk.Button(self, bg='#662209', fg="#F5DEB3", text='Закрыть',
                                    cursor='hand2', command=self.destroy, width=10)
        self.btn_cancel.place(x=200, y=170)

    def default_data(self):
        self.db.c.execute('''SELECT * FROM ROOMS WHERE Idroom=%s''',
                          [self.parent.tree.set(self.parent.tree.selection()[0], '#1')])
        row = self.db.c.fetchone()
        self.entry_category.insert(0, row[1])
        self.entry_capasity.insert(0, row[2])
        self.entry_price.insert(0, row[3])


class EditClient(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.db = DBmodel()

        self.title('Редактировать данные клиента')
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

        self.default_data()

        self.btn_edit = tk.Button(self, text='Редактировать', bg='#662209', fg="#F5DEB3", cursor='hand2')
        self.btn_edit.place(x=100, y=170)
        self.btn_edit.bind('<Button-1>', self.edit_data)

        self.btn_cancel = tk.Button(self, bg='#662209', fg="#F5DEB3", text='Закрыть',
                                    cursor='hand2', command=self.destroy, width=10)
        self.btn_cancel.place(x=200, y=170)

    def default_data(self):
        self.db.c.execute('''SELECT * FROM CLIENTS WHERE Idclient=%s''',
                          [self.parent.tree.set(self.parent.tree.selection()[0], '#1')])
        row = self.db.c.fetchone()
        self.entry_last_name.insert(0, row[2])
        self.entry_name.insert(0, row[1])
        self.entry_login.insert(0, row[3])

    def check_login(self, event):
        if self.db.is_login_exist(self.entry_login.get()):
            self.btn_edit.config(state='disabled')
        else:
            self.btn_edit.config(state='normal')

    def check_data(self, event):
        if self.entry_name.get().strip() == '' or \
                self.entry_last_name.get().strip() == '' or self.entry_login.get().strip() == '':
            self.btn_edit.config(state='disabled')
        else:
            self.btn_edit.config(state='normal')

    def edit_data(self, event):
        if self.btn_edit['state'] == 'normal':
            self.parent.update_clients_record(self.entry_name.get(),
                                              self.entry_last_name.get(),
                                              self.entry_login.get())
            self.destroy()
            mb.showinfo('Данные обновлены', 'Данные успешно обновлены!')


class SearchRoomByCategory(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)

        self.parent = root

        self.title('Поиск по категории')
        self.geometry('190x100')
        self.config(bg='#662209')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Категория номера', bg='#662209', fg="#F5DEB3",
                                width=20, anchor='center')
        label_search.grid(row=0, column=0, columnspan=2, sticky='we')

        self.entry_search = tk.Entry(self, width=20)
        self.entry_search.grid(row=1, column=0, columnspan=2, sticky='we')

        btn_search = tk.Button(self,  bg='#662209', fg="#F5DEB3", text='Поиск', cursor='hand2', width=10)
        btn_search.grid(row=2, column=0, sticky='we')
        btn_search.bind('<Button-1>', lambda event: self.parent.search_rooms_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

        btn_cancel = tk.Button(self,  bg='#662209', fg="#F5DEB3", text='Отмена',
                               cursor='hand2', command=self.destroy, width=10)
        btn_cancel.grid(row=2, column=1, sticky='we')


class SearchClientByLastName(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)

        self.parent = root

        self.title('Поиск по фамилии')
        self.geometry('190x100')
        self.config(bg='#662209')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Фамилия', bg='#662209', fg="#F5DEB3",
                                width=20, anchor='center')
        label_search.grid(row=0, column=0, columnspan=2, sticky='we')

        self.entry_search = tk.Entry(self, width=20)
        self.entry_search.grid(row=1, column=0, columnspan=2, sticky='we')

        btn_search = tk.Button(self,  bg='#662209', fg="#F5DEB3", text='Поиск', cursor='hand2', width=10)
        btn_search.grid(row=2, column=0, sticky='we')
        btn_search.bind('<Button-1>', lambda event: self.parent.search_clients_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

        btn_cancel = tk.Button(self,  bg='#662209', fg="#F5DEB3", text='Отмена',
                               cursor='hand2', command=self.destroy, width=10)
        btn_cancel.grid(row=2, column=1, sticky='we')


class SearchReservation(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)

        self.parent = root

        self.title('Поиск')
        self.geometry('190x100')
        self.config(bg='#662209')
        self.resizable(False, False)

        label_search = tk.Label(self, text='', bg='#662209', fg="#F5DEB3",
                                width=20, anchor='center')
        label_search.grid(row=0, column=0, columnspan=2, sticky='we')

        self.entry_search = tk.Entry(self, width=20)
        self.entry_search.grid(row=1, column=0, columnspan=2, sticky='we')

        btn_search = tk.Button(self,  bg='#662209', fg="#F5DEB3", text='Поиск', cursor='hand2', width=10)
        btn_search.grid(row=2, column=0, sticky='we')
        btn_search.bind('<Button-1>', lambda event: self.parent.search_info_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

        btn_cancel = tk.Button(self,  bg='#662209', fg="#F5DEB3", text='Отмена',
                               cursor='hand2', command=self.destroy, width=10)
        btn_cancel.grid(row=2, column=1, sticky='we')
