#импортируем библиотеку Ткинтер
#добавляем удобную для себя формулировку в коде
import tkinter as tk
from tkinter import ttk
#импорт модуля для БД
import sqlite3





#создание класса главного окна
class Main(tk.Frame): #tk.Frame - наследование, область окна

    def __init__(self, root):  #конструктор класса
        super().__init__(root) #родитель класса
        self.init_main() #привязка функции
        self.db = db #привязка переменной
        self.view_records() #привязка функции


    def init_main(self): #инициализация виджетов главного окна
        toolbar = tk.Frame(bg='#dcf5f9', bd=2) #установка тени под меню (цвет и отступ)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        #1. кнопка добавления
        self.img_add = tk.PhotoImage(file='./img/go_contact.png') #добавление иконки дочерн.окна
        btn_add = tk.Button(toolbar, text='Добавить', bg='#dcf5f9',
                            bd=0, image=self.img_add, command = self.open_second) #вид кнопки
        btn_add.pack(side=tk.RIGHT) #положение иконки на окне


        #2. кнопка удаления
        self.img_del = tk.PhotoImage(file='./img/ungo_contact.png') #добавление иконки дочерн.окна
        btn_del = tk.Button(toolbar, bg='#dcf5f9',
                            bd=0, image=self.img_del, command = self.delete_records) #вид кнопки
        btn_del.pack(side=tk.RIGHT) #положение иконки на окне

        #3. кнопка поиска
        self.img_srch = tk.PhotoImage(file='./img/gowhere.png') #добавление иконки дочерн.окна
        btn_srch = tk.Button(toolbar, text='Найти', bg='#dcf5f9',
                            bd=0, image=self.img_srch, command = self.open_search) #вид кнопки
        btn_srch.pack(side=tk.LEFT) #положение иконки на окне


        #4. кнопка изменения
        self.img_refresh = tk.PhotoImage(file='./img/load.png') #добавление иконки дочерн.окна
        btn_refresh = tk.Button(toolbar, bg='#dcf5f9',
                            bd=0, image=self.img_refresh, command = self.open_refresh_second) #вид кнопки
        btn_refresh.pack(side=tk.RIGHT) #положение иконки на окне
        

        #5. кнопка обновления
        self.img_upd = tk.PhotoImage(file='./img/goupd.png') #добавление иконки дочерн.окна
        btn_upd = tk.Button(toolbar, text='Обновить', bg='#dcf5f9',
                            bd=0, image=self.img_upd, command = self.view_records) #вид кнопки
        btn_upd.pack(side=tk.LEFT) #положение иконки на окне



        #таблица, столбцы на окне
        self.tree = ttk.Treeview(root, 
                                 columns=('id', 'name', 'phone', 'email', 'salary'),
                                 height=45, show='headings')

        #положение столбцов и наименование
        self.tree.column('id', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=100, anchor=tk.CENTER)

        #наименование столбцов
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='ФИО работника')
        self.tree.heading('phone', text='Номер телефона')
        self.tree.heading('email', text='Почта')
        self.tree.heading('salary', text='Зарплата')

        self.tree.pack(side=tk.RIGHT) #положение иконки добавления


    def records(self, name, phone, email, salary): #добавление данных
        self.db.insert_data(name, phone, email, salary)
        self.view_records()
  

    def view_records(self): #отображение данных в окне Treeview
        self.db.cur.execute('SELECT * FROM Users') #выбор всех столбцов в таблице
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in self.db.cur.fetchall()]


    def search_records(self, name): #поиск данных
        self.db.cur.execute('SELECT * FROM Users WHERE name LIKE ?', ('%' + name + '%', )) #значение поиска
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in self.db.cur.fetchall()]


    def refresh_records(self, name, phone, email, salary): #изменение данных
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''
            UPDATE Users
            SET name = ?, phone = ?, email = ?, salary = ?
            WHERE id = ?
        ''', (name, phone, email, salary, id))
        self.db.conn.commit() #сохранение
        self.view_records() #открытие функции


    def delete_records(self): #удаление данных
        for row in self.tree.selection():
            self.db.cur.execute('DELETE FROM Users WHERE id = ?',
                                (self.tree.set(row, '#1'), ))
        self.db.conn.commit() #сохранение
        self.view_records() #открытие функции


    def open_second(self): #вызов дочернего окна для добавления
        Second()


    def open_refresh_second(self): #вызов дочернего окна для изменения
        Refresh()

    
    def open_search(self): #вызов дочернего окна для поиска данных
        Search()





#создание класса дочернего окна (добавление данных)
class Second(tk.Toplevel):

    def __init__(self):  #конструктор класса
        super().__init__(root) #родитель класса
        self.init_second() #привязка функции
        self.view = app #приложение

    def init_second(self): #инициализация виджетов второго окна
        self.title('Добавление нового сотрудника') #заголовок
        self.geometry('450x200') #размеры окна 
        self.configure(bg='#dcf5f9') #цвет
        self.iconbitmap('./ico/go_contact.ico') #замена иконки
        self.resizable(False, False) #для отсутствия поломки пользователем
        self.grab_set() #все события
        self.focus_set() #фокус

        #наименование данных
        label_name = tk.Label(self, text='ФИО:', bg='#dcf5f9')
        label_name.place(x=50, y=25)
        label_phone = tk.Label(self, text='Номер телефона:', bg='#dcf5f9')
        label_phone.place(x=50, y=55)
        label_email = tk.Label(self, text='Почта:', bg='#dcf5f9' )
        label_email.place(x=50, y=85)
        label_salary = tk.Label(self, text='Зарплата:', bg='#dcf5f9' )
        label_salary.place(x=50, y=115)

        #ввод данных
        self.enter_name = tk.Entry(self, bg='#f6fcfe', width=26)
        self.enter_name.place(x=200, y=25)
        self.enter_phone = tk.Entry(self, bg='#f6fcfe')
        self.enter_phone.place(x=200, y=55)
        self.enter_email = tk.Entry(self, bg='#f6fcfe') 
        self.enter_email.place(x=200, y=85)
        self.enter_salary = tk.Entry(self, bg='#f6fcfe') 
        self.enter_salary.place(x=200, y=115)

        btn_cancel = tk.Button(self, text='Отмена', bg='#b3e9fa', command=self.destroy) #добавление кнопки закрытия
        btn_cancel.place(x=270, y=150) #положение кнопки

        self.btn_add = tk.Button(self, text='Добавить',  bg='#b3e9fa', command=self.destroy) #кнопка добавления
        self.btn_add.bind('<Button-1>', lambda ev: self.view.records(self.enter_name.get(),                                                                     
                                                                self.enter_phone.get(),
                                                                self.enter_email.get(),
                                                                self.enter_salary.get())) #функция кнопки
        self.btn_add.place(x=200, y=150) #положение кнопки





#создание класса дочернего окна (изменение данных)
class Refresh(Second):

    def __init__(self): #конструктор класса
        super().__init__() #родитель класса
        self.init_refresh() #привязка функции
        self.db = db #привязка переменной
        self.default_data() #привязка функции

    def init_refresh(self): #инициализация виджетов третьего окна
        self.title('Изменение текущего сотрудника') #заголовок
        self.btn_add.destroy() #закрытие
        self.btn_refresh = tk.Button(self, text='Изменить',  bg='#b3e9fa', command=self.destroy) #добавление кнопки изменения
        self.btn_refresh.bind('<Button-1>', lambda ev: self.view.refresh_records(self.enter_name.get(),
                                                                            self.enter_phone.get(),
                                                                            self.enter_email.get(),
                                                                            self.enter_salary.get())) #функции кнопки
        self.btn_refresh.bind('<Button-1>', lambda ev: self.destroy(), add = '+')
        self.btn_refresh.place(x=200, y=150) #положение кнопки 


        self.geometry('400x200') #размеры окна 
        self.configure(bg='#dcf5f9') #цвет
        self.iconbitmap('./ico/goload.ico') #замена иконки
        self.resizable(False, False) #для отсутствия поломки пользователем
        self.grab_set() #все события
        self.focus_set() #фокус

    def default_data(self): #наличие начальных данных при изменении
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute('SELECT * FROM Users WHERE id = ?', (id, ))
        row = self.db.cur.fetchone()
        self.enter_name.insert(0, row[1])  #id каждого столбца
        self.enter_phone.insert(0, row[2]) 
        self.enter_email.insert(0, row[3]) 
        self.enter_salary.insert(0, row[4])        





#создание класса дочернего окна для поиска
class Search(tk.Toplevel):

    def __init__(self):  #конструктор класса
        super().__init__(root) #родитель класса
        self.init_search() #привязка функции
        self.view = app

    def init_search(self): #инициализация виджетов второго окна
        self.title('Поиск сотрудника') #заголовок
        self.geometry('400x150') #размеры окна 
        self.configure(bg='#dcf5f9') #цвет
        self.iconbitmap('./ico/gowhere.ico') #замена иконки
        self.resizable(False, False) #для отсутствия поломки пользователем
        self.grab_set() #все события
        self.focus_set() #фокус

        #наименование данных
        label_name = tk.Label(self, text='ФИО:', bg='#dcf5f9')
        label_name.place(x=50, y=50)

        #ввод данных
        self.enter_name = tk.Entry(self, bg='#f6fcfe', width=33)
        self.enter_name.place(x=120, y=50)

        btn_cancel = tk.Button(self, text='Отмена', bg='#b3e9fa', command=self.destroy) #добавление кнопки закрытия
        btn_cancel.place(x=180, y=85) #положение кнопки

        self.btn_add = tk.Button(self, text='Найти',  bg='#b3e9fa', command=self.destroy) #кнопка поиска
        self.btn_add.bind('<Button-1>', lambda ev: self.view.search_records(self.enter_name.get())) #функция кнопки
        self.btn_add.place(x=120, y=85) #положение кнопки





#добавление базы данных (БД)
class DataBase():

    def __init__(self): #конструктор класса
        self.conn = sqlite3.connect('employee.db') #подключение к бд
        self.cur = self.conn.cursor()
        #создание таблицы
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Users (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            phone TEXT NOT NULL,
                            email TEXT NOT NULL,
                            salary TEXT NOT NULL
                        )''')
        self.conn.commit() #сохраняем подключение

    def insert_data(self, name, phone, email, salary):
        #ввод в базу данных
        self.cur.execute('''
                        INSERT INTO Users (name, phone, email, salary)
                        VALUES (?, ?, ?, ?)''', (name, phone, email, salary))
        self.conn.commit() #сохранение
        




#при запуске программы
if __name__ == '__main__':
    root = tk.Tk() #создание окна
    db = DataBase() #переменная для подключения к БД
    app = Main(root) #присоединяем класс окна к переменной 
    root.iconbitmap('./ico/comp.ico') #замена пера на свою иконку
    root.title('Сотрудники компании PRO') #заголовok
    root.configure(bg='#edf6f8') #цвет фона
    root.geometry('745x450') #размеры окна 
    root.resizable(False, False) #для отсутствия поломки пользователем
    root.mainloop() #показ окна