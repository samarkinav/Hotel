from db.database import DB
import mysql.connector


class DBmodel:
    db = DB()

    def __init__(self):

        self.conn = mysql.connector.connect(host='localhost',
                                            database='db',
                                            user='root',
                                            password='qwerty1234')
        self.c = self.conn.cursor()

        self.conn.commit()

    def insert_client_in_data(self, first_name, last_name, login, password):
        self.c.execute('''INSERT INTO CLIENTS (FirstName,LastName,Login,PersonPassword) VALUES (%s,%s,%s,%s)''',
                       (first_name, last_name, login, password))
        self.conn.commit()



    def room_search(self, datein, dateout, amount):
        self.c.execute('''CREATE TEMPORARY TABLE AVAILABLE
                          SELECT DISTINCT A.Idroom, A.Category, A.Capasity, A.Price, 
                          A.Price * DATEDIFF(%s, %s) AS Total 
                          FROM ROOMS AS A 
                          INNER JOIN ROOMCONDITION AS B 
                          ON A.Idroom = B.Idroom 
                          WHERE (%s NOT BETWEEN DateIn and DateOut)
                          AND (%s NOT BETWEEN DateIn and DateOut) 
                          AND Capasity = %s AND A.Idroom NOT IN (SELECT A.IDROOM FROM ROOMS AS A 
                          INNER JOIN ROOMCONDITION AS B 
                          ON A.Idroom = B.Idroom 
                          WHERE (%s  BETWEEN DateIn and DateOut)
                          OR (%s BETWEEN DateIn and DateOut) 
                          AND Capasity = %s)''', [dateout, datein, datein, dateout, amount, datein, dateout, amount])
        category = []
        total = []
        self.c.execute('''SELECT DISTINCT Category, Total FROM AVAILABLE''')
        available_rooms = self.c.fetchall()
        for row in available_rooms:
            category.append(row[0])
            total.append(row[1])
        self.c.execute('''SELECT Idroom, Category, Total FROM AVAILABLE''')
        available_rooms = self.c.fetchall()
        self.c.execute('''DROP TABLE AVAILABLE''')
        self.conn.commit()
        return [available_rooms, category, total]

    def get_id_client(self, login):
        self.c.execute('''SELECT Idclient FROM CLIENTS WHERE Login = %s''', [login])
        result = self.c.fetchone()[0]
        self.conn.commit()
        return result

    def get_id_food(self, type):
        self.c.execute('''SELECT Idfood FROM TYPEOFFOOD WHERE TypeOfFood = %s''', [type])
        result = self.c.fetchone()[0]
        self.conn.commit()
        return result

    def add_new_reservation(self, login, type, datein, dateout, id_room):
        self.c.execute('''INSERT INTO RESERVATION (Idclient, Idroom, Idfood, DateIn, DateOut) VALUES (%s,%s,%s,%s,%s)''',
                       [self.get_id_client(login), id_room, self.get_id_food(type), datein, dateout])
        self.c.execute('''INSERT INTO ROOMCONDITION VALUES (%s,%s,%s)''', (id_room, datein, dateout))
        self.conn.commit()

    def add_new_client(self, first_name, last_name, login, password):
        self.c.execute('''INSERT INTO CLIENTS (FirstName, LastName, Login, PersonPassword) VALUES (%s,%s,%s,%s)''',
                       [first_name, last_name, login, password])
        self.conn.commit()

    def add_new_room(self, category, capasity, price):
        self.c.execute('''INSERT INTO ROOMS (Category, Capasity, Price) VALUES (%s,%s,%s)''',
                       [category, capasity, price])
        self.conn.commit()

    def get_price_of_food(self, datein, dateout, amount):
        result = []
        self.c.execute('''SELECT TypeOfFood, Price * DATEDIFF(%s, %s) * %s AS Total 
                          FROM TYPEOFFOOD''', [dateout, datein, amount])
        for row in self.c.fetchall():
            result.append(int(row[1]))
        self.conn.commit()
        return result

    def sign_in(self):
        self.c.execute('''SELECT * FROM RESERVATION WHERE Idclient = %s''', [self.db.id_client])
        details = self.c.fetchone()
        self.db.id_room = details[2]
        self.db.id_food = details[3]
        date_in = details[4]
        date_out = details[5]
        self.c.execute('''SELECT A.Amount * (A.Price + B.Price * A.Capasity) 
                          FROM (SELECT DATEDIFF(A.DateOut, A.DateIn) AS Amount, A.Idfood, B.Price, B.Capasity
                          FROM (SELECT * FROM RESERVATION WHERE Idclient = %s) AS A
                          JOIN ROOMS AS B ON A.Idroom = B.Idroom) AS A
                          JOIN TYPEOFFOOD AS B ON A.Idfood = B.Idfood''', [self.db.id_client])
        total_price = self.c.fetchone()[0]
        self.c.execute('''SELECT Category FROM ROOMS WHERE Idroom = %s''', [self.db.id_room])
        category = self.c.fetchone()[0]
        self.c.execute('''SELECT Capasity FROM ROOMS WHERE Idroom = %s''', [self.db.id_room])
        capasity = self.c.fetchone()[0]
        self.c.execute('''SELECT TypeOfFood FROM TYPEOFFOOD WHERE Idfood = %s''', [self.db.id_food])
        food = self.c.fetchone()[0]
        self.conn.commit()
        return [date_in, date_out, category, food, total_price, capasity]

    def view_all_records(self):
        self.c.execute('''SELECT A.DateIn, A.DateOut, A.LastName, A.FirstName, A.Category, A.Capasity, B.TypeOfFood, 
                          INTEGER ((A.Price + B.Price)*DATEDIFF(A.DateOut, A.DateIn)) AS Total
                          FROM (SELECT A.DateIn, A.DateOut, A.LastName, A.FirstName, A.idfood, B.Category, B.Capasity, 
                                B.Price FROM (SELECT A.DateIn, A.DateOut, A.idroom, A.idfood, B.LastName, B.FirstName
                                              FROM RESERVATION AS A JOIN CLIENTS AS B ON A.idclient = B.idclient) AS A
                                JOIN ROOMS AS B
                                ON A.idroom = B.idroom) AS A
                          JOIN TYPEOFFOOD AS B
                          ON A.idfood = B.idfood''')
        return self.c.fetchall()

    def is_admin_found(self, login, password):
        self.c.execute('''SELECT count(*) FROM ADMINISTRATION WHERE  
                             Login = %s and AdminPassword = %s''', [login, password])
        if self.c.fetchone()[0] > 0:
            return True
        else:
            return False

    def is_client_found(self, login, password):
        self.c.execute('''SELECT count(*) FROM CLIENTS WHERE  
                                     Login = %s and PersonPassword = %s''', [login, password])
        if self.c.fetchone()[0] > 0:
            self.find_client(login, password)
            return True
        else:
            return False

    def find_client(self, login, password):
        self.c.execute('''SELECT Idclient, FirstName, LastName FROM CLIENTS WHERE Login = %s AND PersonPassword = %s''',
                       [login, password])
        personal_data = self.c.fetchone()
        self.db.id_client = personal_data[0]
        return personal_data[0], personal_data[1], personal_data[2]

    def is_login_exist(self, login):
        self.c.execute('''SELECT count(*) FROM CLIENTS WHERE  
                                            Login = %s ''', [login])
        if self.c.fetchone()[0] > 0:
            return True
        else:
            return False
