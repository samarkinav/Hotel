import mysql.connector


class DB:
    def __init__(self):
        self.conn = mysql.connector.connect(host='localhost',
                                            database='db',
                                            user='root',
                                            password='qwerty1234')
        self.c = self.conn.cursor()

        self.id_client = []
        self.available_rooms = []
        self.id_room = []
        self.id_food = []

        self.flag = True

        if not self.flag:

            self.c.execute('''CREATE TABLE IF NOT EXISTS CLIENTS(
                                    Idclient INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                                    FirstName VARCHAR(30) NOT NULL, 
                                    LastName VARCHAR(20) NOT NULL, 
                                    Login VARCHAR(10) NOT NULL UNIQUE, 
                                    PersonPassword VARCHAR(10) NOT NULL)''')

            self.c.execute('''CREATE TABLE IF NOT EXISTS ROOMS(
                                    Idroom INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                                    Category VARCHAR(15) NOT NULL,
                                    Capasity INTEGER NOT NULL,
                                    Price DECIMAL(15,2) NOT NULL)''')

            self.c.execute('''CREATE TABLE IF NOT EXISTS ROOMCONDITION(
                                    Idroom INT UNSIGNED NOT NULL AUTO_INCREMENT ,
                                    DateIn DATE NOT NULL,
                                    DateOut DATE NOT NULL,
                                    FOREIGN KEY (IDroom) REFERENCES ROOMS(Idroom) ON DELETE CASCADE)''')

            self.c.execute('''CREATE TABLE IF NOT EXISTS TYPEOFFOOD(
                                    Idfood INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                    TypeOfFood VARCHAR(3) NOT NULL,
                                    PRICE DECIMAL(15,2) NOT NULL)''')

            self.c.execute('''CREATE TABLE IF NOT EXISTS RESERVATION(
                                    Idreservation INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                    Idclient INT UNSIGNED,
                                    Idroom INT UNSIGNED,
                                    Idfood INT UNSIGNED,
                                    DateIn DATE NOT NULL,
                                    DateOut DATE NOT NULL,
                                    FOREIGN KEY (Idclient) REFERENCES CLIENTS (Idclient) ON DELETE CASCADE,
                                    FOREIGN KEY (Idroom) REFERENCES ROOMS (Idroom) ON DELETE CASCADE,
                                    FOREIGN KEY (Idfood) REFERENCES TYPEOFFOOD (Idfood) ON DELETE CASCADE)''')

            self.c.execute('''CREATE TABLE IF NOT EXISTS ADMINISTRATION(
                                            Id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                                            FirstName VARCHAR(30) NOT NULL, 
                                            LastName VARCHAR(20) NOT NULL, 
                                            Login VARCHAR(10) NOT NULL UNIQUE, 
                                            AdminPassword VARCHAR(10) NOT NULL)''')

            admins = [
                ('Максим', 'Ермолаев', 'admin1', 'admin1'),
                ('Валерия', 'Самаркина', 'admin2', 'admin2')
            ]
            self.c.executemany("INSERT INTO ADMINISTRATION(FirstName,LastName,Login,AdminPassword) VALUES (%s,%s,%s,%s)",
                               admins)

            clients = [
                ('Иван', 'Орлов', 'person1', 'person1'),
                ('Людмила', 'Игнатенко', 'person2', 'person2'),
                ('Жанна', 'Дегтярева', 'person3', 'person3'),
                ('Игорь', 'Зорин', 'person4', 'person4'),
                ('Евдокия', 'Виницкая', 'person5', 'person5'),
                ('Максим', 'Ермолаев', 'person6', 'person6'),
                ('Валерия', 'Несамаркина', 'person7', 'person7'),
                ('Виктория', 'Баклашева', 'person8', 'person8'),
                ('Андрей', 'Хомутов', 'person9', 'person9'),
                ('Никита', 'Фелитов', 'person10', 'person10'),
                ('Пётр', 'Иванов', 'person11', 'person11'),
                ('Дмитрий', 'Сидоров', 'person12', 'person12'),
                ('Кирилл', 'Петров', 'person13', 'person13'),
                ('Елизавета', 'Жужгова', 'person14', 'person14'),
                ('Юлия', 'Михайлова', 'person15', 'person15'),
                ('Виталий', 'Самаркин', 'person16', 'person16'),
                ('Евгения', 'Евдокимова', 'person17', 'person17'),
                ('Екатерина', 'Новоселова', 'person18', 'person18'),
                ('Ксения', 'Соловьева', 'person19', 'person19'),
                ('Никита', 'Капкаев', 'person20', 'person20'),
                ('Виктория', 'Санникова', 'person21', 'person21'),
                ('Андрей', 'Калистратов', 'person22', 'person22'),
                ('Хаджек', 'Беджек', 'person23', 'person23'),
                ('Самуил', 'Маршак', 'person24', 'person24'),
                ('Денис', 'Родов', 'person25', 'person25'),
                ('Иван', 'Теплин', 'person26', 'person26')
            ]
            self.c.executemany("INSERT INTO CLIENTS (FirstName, LastName, Login, PersonPassword) VALUES (%s,%s,%s,%s)",
                               clients)

            rooms = [
                (1, 'Стандарт', 2, 1300),
                (2, 'Стандарт', 2, 1300),
                (3, 'Стандарт', 3, 2000),
                (4, 'Стандарт', 4, 3000),
                (5, 'Стандарт', 3, 2000),
                (6, 'Стандарт', 1, 1000),
                (7, 'Стандарт', 1, 1000),
                (8, 'Стандарт', 3, 2000),
                (9, 'Стандарт', 2, 1300),
                (10, 'Стандарт', 2, 1300),
                (11, 'Стандарт', 4, 3000),
                (12, 'Полулюкс', 2, 2500),
                (13, 'Полулюкс', 3, 3300),
                (14, 'Полулюкс', 2, 2500),
                (15, 'Люкс', 2, 3700),
                (16, 'Люкс', 3, 4500)
            ]
            self.c.executemany("INSERT INTO ROOMS(Idroom, Category, Capasity, Price) VALUES (%s,%s,%s,%s)",
                               rooms)

            typeoffood = [
                (1, 'RO', 0),
                (2, 'BB', 500),
                (3, 'HB', 1000),
                (4, 'FB', 1500),
                (5, 'AI', 2000)
            ]
            self.c.executemany("INSERT INTO TYPEOFFOOD VALUES (%s,%s,%s)", typeoffood)

            roomcondition = [
                (11, '2020-12-28', '2021-01-01'),
                (1, '2021-01-03', '2021-01-08'),
                (1, '2021-01-15', '2021-01-25'),
                (3, '2020-12-30', '2021-01-03'),
                (3, '2021-01-07', '2021-01-09'),
                (3, '2021-01-27', '2021-01-30'),
                (4, '2020-12-29', '2021-01-01'),
                (4, '2021-01-15', '2021-01-25'),
                (14, '2020-12-28', '2021-01-05'),
                (15, '2020-12-28', '2021-01-06'),
                (12, '2020-12-31', '2021-01-01'),
                (13, '2020-12-30', '2021-01-02'),
                (2, '2021-01-04', '2021-01-10'),
                (5, '2021-01-16', '2021-01-27'),
                (6, '2021-02-28', '2021-03-01'),
                (7, '2021-01-23', '2021-01-28'),
                (8, '2021-01-30', '2021-02-07'),
                (9, '2021-01-30', '2021-02-05'),
                (10, '2021-01-27', '2021-02-09'),
                (11, '2021-01-22', '2021-01-28'),
                (6, '2021-01-29', '2021-01-30'),
                (8, '2021-02-09', '2021-02-25'),
                (7, '2021-02-02', '2021-02-05'),
                (9, '2021-02-18', '2021-02-26'),
                (10, '2021-02-11', '2021-02-15'),
                (11, '2021-02-13', '2021-02-15'),
                (6, '2021-01-24', '2021-01-25'),
                (7, '2021-02-09', '2021-02-15')
            ]
            self.c.executemany(f"INSERT INTO ROOMCONDITION VALUES (%s,%s,%s)", roomcondition)

            reservation = [
                (1, 11, 1, '2020-12-28', '2021-01-01'),
                (2, 1, 2, '2021-01-03', '2021-01-08'),
                (3, 1, 3, '2021-01-15', '2021-01-25'),
                (4, 3, 4, '2020-12-30', '2021-01-03'),
                (5, 3, 5, '2021-01-07', '2021-01-09'),
                (6, 3, 1, '2021-01-27', '2021-01-30'),
                (7, 4, 2, '2020-12-29', '2021-01-01'),
                (8, 4, 3, '2021-01-15', '2021-01-25'),
                (9, 14, 4, '2020-12-28', '2021-01-05'),
                (10, 15, 5, '2020-12-28', '2021-01-06'),
                (11, 12, 1, '2020-12-31', '2021-01-01'),
                (12, 13, 2, '2020-12-30', '2021-01-02'),
                (13, 2, 3, '2021-01-04', '2021-01-10'),
                (14, 6, 1, '2021-02-28', '2021-03-01'),
                (15, 7, 2, '2021-01-23', '2021-01-28'),
                (16, 8, 3, '2021-01-30', '2021-02-07'),
                (17, 9, 4, '2021-01-30', '2021-02-05'),
                (18, 10, 5, '2021-01-27', '2021-02-09'),
                (19, 11, 1, '2021-01-22', '2021-01-28'),
                (20, 6, 2, '2021-01-29', '2021-01-30'),
                (21, 8, 3, '2021-02-09', '2021-02-25'),
                (22, 7, 4, '2021-02-02', '2021-02-05'),
                (23, 9, 5, '2021-02-18', '2021-02-26'),
                (24, 10, 1, '2021-02-11', '2021-02-15'),
                (25, 11, 2, '2021-02-13', '2021-02-15'),
                (26, 6, 3, '2021-01-24', '2021-01-25')
            ]
            self.c.executemany("INSERT INTO RESERVATION(Idclient,Idroom,Idfood,DateIn,DateOut) VALUES (%s,%s,%s,%s,%s)",
                               reservation)

        self.conn.commit()

