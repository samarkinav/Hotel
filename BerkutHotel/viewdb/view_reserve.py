import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from tkcalendar import *
from PIL import ImageTk as ITk

import datetime

from viewdb.viewdb import DBmodel

from view.view_details import DetailsWindow


class ReservationWindow(tk.Toplevel):
    values_of_food = ['RO', 'BB', 'HB', 'FB', 'AI']
    room_category = ['Стандарт', 'Полулюкс', 'Люкс']

    def __init__(self, welcome_parent):
        super().__init__(welcome_parent)

        self.parent = welcome_parent

        self.db = DBmodel()

        self.id_room = 0
        self.available_rooms = []
        self.category = []
        self.price_of_category = []
        self.food_price_int = 0
        self.room_price_int = 0
        self.total_price_int = 0
        self.date_in = ''
        self.date_out = ''

        self.config(bg='#662209')
        self.title('Отель Беркут')
        self.geometry('550x400')
        #self.iconbitmap('..', 'images/Hotel.ico')
        self.resizable(width=True, height=True)

        self.bg = ITk.PhotoImage(file='images/food.jpg')
        self.bg_image = tk.Label(self, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        self.grid_rowconfigure(3, minsize=30, weight=60)

        # ============ RESERVE FRAME =============

        self.frame1 = tk.LabelFrame(self, text='Бронирование', font=('UnicephalonCyrillic', 11))
        self.frame1.place(relx=0.3, rely=0.02, relwidth=0.4, relheight=0.8)

        self.input_date_in = tk.Label(self.frame1, text='Дата заезда').place(relx=0.1, rely=0.05,
                                                                             relwidth=0.4, relheight=0.07)

        self.date_in_ent = tk.Button(self.frame1, bd=0, font=('UnicephalonCyrillic', 12), cursor='hand2',
                                     bg='white', text=f'{self.normal_date(datetime.date.today())}')
        self.date_in_ent.place(relx=0.1, rely=0.12, relwidth=0.6, relheight=0.1)
        self.date_in_ent.bind('<Button-1>', self.select_date_in)

        self.input_date_out = tk.Label(self.frame1, text='Дата отъезда').place(relx=0.1, rely=0.25,
                                                                               relwidth=0.4, relheight=0.07)

        self.date_out_ent = tk.Button(self.frame1, bd=0, font=('UnicephalonCyrillic', 12),
                                      bg='white', cursor='hand2',
                                      text=f'{self.normal_date(datetime.date.today()+datetime.timedelta(days=1))}')
        self.date_out_ent.place(relx=0.1, rely=0.32, relwidth=0.6, relheight=0.1)
        self.date_out_ent.bind('<Button-1>', self.select_date_out)

        self.amount_lbl = tk.Label(self.frame1, text='Количество гостей').place(relx=0.1, rely=0.50,
                                                                                relwidth=0.6, relheight=0.07)

        self.amount_of_person_cmmbx = ttk.Combobox(self.frame1, state='readonly', cursor='hand2',
                                                   values=['1 взрослый', '2 взрослых', '3 взрослых', '4 взрослых'],
                                                   font=('UnicephalonCyrillic', 10), justify=tk.CENTER)
        self.amount_of_person_cmmbx.place(relx=0.1, rely=0.57, relwidth=0.6, relheight=0.1)
        self.amount_of_person_cmmbx.current(0)
        self.amount_of_person_cmmbx.bind("<<ComboboxSelected>>", )

        self.find_btn = tk.Button(self.frame1, text='Найти номер', font=('UnicephalonCyrillic', 11),
                                  bg='#662209', fg="#F5DEB3", bd=2, cursor='hand2',
                                  activebackground='#9E886A', activeforeground='#F5DEB3')
        self.find_btn.place(relx=0, rely=0.85, relwidth=1, relheight=0.15)
        self.find_btn.bind('<Button-1>', self.show_options)

        # ----------------------FRAME OPTIONS-------------------

        self.frame2 = tk.LabelFrame(self, text='Подходящие варианты', font=('UnicephalonCyrillic', 11))

        #self.empty_lbl = tk.Label(self.frame2, text='      ').grid(row=0, column=0)

        self.available_lbl = tk.Label(self.frame2, text='Выберите\nапартаменты: ')
        self.available_lbl.grid(row=1, column=1)

        self.available_cmbbx = ttk.Combobox(self.frame2, values=self.room_category,
                                            width=12, state='readonly', justify=tk.CENTER)
        self.available_cmbbx.grid(row=1, column=2)
        self.available_cmbbx.bind("<<ComboboxSelected>>", self.changed_category)

        self.price_lbl = tk.Label(self.frame2, text='Стоимость, руб: ', justify=tk.CENTER)
        self.price_lbl.grid(row=2, column=1)

        self.room_price = tk.Label(self.frame2, text='0', justify=tk.LEFT)
        self.room_price.grid(row=2, column=2, pady=10)

        self.type_of_food_lbl = tk.Label(self.frame2, text='Тип питания:', justify=tk.CENTER)
        self.type_of_food_lbl.grid(row=3, column=1, pady=10)

        self.type_of_food_cmbbx = ttk.Combobox(self.frame2, state='readonly', width=5,
                                               values=self.values_of_food, justify=tk.CENTER)
        self.type_of_food_cmbbx.grid(row=3, column=2)
        self.type_of_food_cmbbx.bind("<<ComboboxSelected>>", self.changed_category)
        self.type_of_food_cmbbx.current(0)

        self.price_of_food_lbl = tk.Label(self.frame2, text='Стоимость, руб:', justify=tk.CENTER)
        self.price_of_food_lbl.grid(row=4, column=1)

        self.food_price = tk.Label(self.frame2, text='0', justify=tk.LEFT)
        self.food_price.grid(row=4, column=2)

        self.total_price_label = tk.Label(self.frame2, text='Итоговая\nстоимость, руб:',
                                          font=('UnicephalonCyrillic', 10))
        self.total_price_label.place(relx=0.01, rely=0.65, relwidth=0.5, relheight=0.2)

        self.total_price = tk.Label(self.frame2, text='0', font=('UnicephalonCyrillic', 10))
        self.total_price.place(relx=0.51, rely=0.65, relwidth=0.3, relheight=0.2)

        self.reserve_btn = tk.Button(self.frame2, text='Перейти к оформлению', cursor='hand2',
                                     command=self.check_data, bg='#662209', fg="#F5DEB3",
                                     font=('UnicephalonCyrillic', 11), bd=0, activebackground='#9E886A',)
        self.reserve_btn.place(relx=0, rely=0.85, relwidth=1, relheight=0.15)

        self.sign_in_btn = tk.Button(self, text='Вернуться на главный экран', activebackground='#9E886A',
                                     bg='#662209', fg="#F5DEB3", cursor='hand2', command=self.confirm_delete)
        self.sign_in_btn.pack(fill='both', side='bottom')

        self.cal = Calendar(self, setmode='day', date_pattern='dd/mm/yyyy', cursor='hand2',
                            showweeknumbers=False, weekendbackground='white')

        self.frame1.place(relx=0.02, rely=0.02, relwidth=0.4, relheight=0.8)

    def run_details_window(self):
        details_window = DetailsWindow(self)
        details_window.set_details_from_reserve(self.date_in,
                                                self.date_out,
                                                self.available_cmbbx.get(),
                                                self.type_of_food_cmbbx.get(),
                                                self.total_price_int,
                                                self.amount_of_person_cmmbx.current()+1,
                                                self.id_room)
        self.withdraw()

    def select_date_in(self, event):
        if self.date_in_ent['state'] == 'normal':
            self.date_in_ent.config(state='disabled')
            self.date_out_ent.config(state='disabled')
            #self.amount_of_person_cmmbx.place_forget()

            self.cal.config(mindate=datetime.date.today())
            # self.cal.config(maxdate=self.max_date)

            self.cal.place(relx=0.44, rely=0.25)
            self.cal.bind('<<CalendarSelected>>', self.record_date_in)
        else:
            self.cal.place_forget()
            self.date_in_ent.config(state='normal')
            self.date_out_ent.config(state='normal')
            self.amount_of_person_cmmbx.place(relx=0.1, rely=0.57, relwidth=0.6, relheight=0.1)

    def select_date_out(self, event):
        if self.date_out_ent['state'] == 'normal':
            self.date_in_ent.config(state='disabled')
            self.date_out_ent.config(state='disabled')
            #self.amount_of_person_cmmbx.place_forget()

            min_date = self.reversed_date(self.future_day(self.date_in_ent['text']))
            self.cal.config(mindate=min_date)
            self.cal.config(maxdate=None)

            self.cal.place(relx=0.44, rely=0.37)
            self.cal.bind('<<CalendarSelected>>', self.record_date_out)
        else:
            self.cal.place_forget()
            self.date_in_ent.config(state='normal')
            self.date_out_ent.config(state='normal')
            self.amount_of_person_cmmbx.place(relx=0.1, rely=0.57, relwidth=0.6, relheight=0.1)

    def future_day(self, date):
        future = date.split("/")
        future_date = datetime.date(int(future[2]), int(future[1]), int(future[0])) + datetime.timedelta(days=1)
        return self.normal_date(future_date)

    @staticmethod
    def normal_date(date):
        tuple_date = str(date).split('-')
        return tuple_date[2] + '/' + tuple_date[1] + '/' + tuple_date[0]

    @staticmethod
    def reversed_date(date: str):
        date = date.split("/")
        return datetime.date(int(date[2]), int(date[1]), int(date[0]))

    def record_date_in(self, event):
        selected_date = self.cal.get_date()
        self.date_in_ent.config(text=selected_date)

        if self.reversed_date(self.date_in_ent['text']) >= self.reversed_date(self.date_out_ent['text']):
            self.date_out_ent.config(text=self.future_day(self.date_in_ent['text']))

        self.date_in_ent.config(state='normal')
        self.date_out_ent.config(state='normal')
        self.amount_of_person_cmmbx.config(state='readonly')
        self.cal.place_forget()

    def record_date_out(self, event):
        selected_date = self.cal.get_date()
        self.date_out_ent.config(text=selected_date)

        self.date_in_ent.config(state='normal')
        self.date_out_ent.config(state='normal')
        self.amount_of_person_cmmbx.config(state='readonly')
        self.cal.place_forget()

    def confirm_delete(self):
        msg = "Вы уверены, что хотите прервать бронирование?"
        if mb.askyesno(message=msg, parent=self):
            self.destroy()
            self.parent.deiconify()

    def date_convert(self):
        date_in = self.date_in_ent['text'].split("/")
        date_out = self.date_out_ent['text'].split("/")

        self.date_in = f'{date_in[2]}-{date_in[1]}-{date_in[0]}'
        self.date_out = f'{date_out[2]}-{date_out[1]}-{date_out[0]}'

    def amount_cmbbx_changed(self):
        pass

    def show_options(self, event):
        if self.find_btn['state'] != 'disabled':
            self.frame2.place_forget()

            self.date_convert()

            self.get_available_room(self.date_in, self.date_out, self.amount_of_person_cmmbx.get()[0])

            if not self.category:
                self.find_btn.config(state='disabled')
                self.find_btn.config(state='normal')
                mb.showwarning("Очень жаль..", "К сожалению, подходящих номеров нет :c")
            else:
                self.available_cmbbx.config(values=self.category)
                self.available_cmbbx.current(0)
                self.changed_category(event)
                self.type_of_food_cmbbx.current(0)
                self.food_price.config(text='0')

                self.frame1.place(relx=0.02, rely=0.02, relwidth=0.4, relheight=0.8)
                self.frame2.place(relx=0.45, rely=0.02, relwidth=0.5, relheight=0.8)

    def get_available_room(self, datein, dateout, amount):
        [self.available_rooms, self.category, self.price_of_category] = self.db.room_search(datein, dateout, amount)

    def changed_category(self, event):
        for i in range(len(self.price_of_category)):
            if self.available_cmbbx.get() == self.category[i]:
                self.room_price_int = int(self.price_of_category[i])
                self.id_room = self.get_id_room(self.category[i])

        food = ['RO', 'BB', 'HB', 'FB', 'AI']
        for i in range(5):
            if self.type_of_food_cmbbx.get() == food[i]:
                self.food_price_int = int(self.db.get_price_of_food(self.date_in,
                                                                    self.date_out,
                                                                    self.amount_of_person_cmmbx.get())[i])

        self.room_price.config(text=f"{self.room_price_int}")
        self.food_price.config(text=f"{self.food_price_int}")
        self.total_price_int = self.room_price_int + self.food_price_int
        self.total_price.config(text=f"{self.total_price_int}")

    def get_id_room(self, category):
        result = 0
        for row in self.available_rooms:
            if row[1] == category:
                result = row[0]
        return result

    def check_data(self):
        if self.available_cmbbx.get() == '':
            mb.showerror("Апартаменты не выбраны!", "Выберите апартаменты!")
        else:
            self.run_details_window()
