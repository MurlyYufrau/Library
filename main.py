import tkinter as tk
import sqlite3
import tkinter.ttk as TTK

# Создать базу данных
conn = sqlite3.connect('library.db')
c = conn.cursor()

# Создать таблицы
c.execute('''CREATE TABLE IF NOT EXISTS books
             (id INTEGER PRIMARY KEY, title TEXT, author_id INTEGER, FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE ON UPDATE CASCADE CONSTRAINT UC_Person UNIQUE (author_id, title) )''')
c.execute('''CREATE TABLE IF NOT EXISTS authors
             (id INTEGER PRIMARY KEY, name TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS readers
             (id INTEGER PRIMARY KEY, name TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS rentals
             (book_id INTEGER, reader_id INTEGER, rental_date DATE, PRIMARY KEY(book_id)
             FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE ON UPDATE CASCADE,
             FOREIGN KEY (reader_id) REFERENCES readers(id) ON DELETE CASCADE ON UPDATE CASCADE)''')

# Вставить данные в таблицы
#c.execute("INSERT INTO authors (name) VALUES (?)", ('Л.Н. Толстой',))
#c.execute("INSERT INTO authors (name) VALUES (?)", ('Ф.М. Достоевский',))
#c.execute("INSERT INTO authors (name) VALUES (?)", ('А.С. Пушкин',))
#c.execute("INSERT INTO books (title, author_id) VALUES (?, ?)", ('Война и мир', 1))
#c.execute("INSERT INTO books (title, author_id) VALUES (?, ?)", ('Преступление и наказание', 2))
#c.execute("INSERT INTO books (title, author_id) VALUES (?, ?)", ('Идиот', 2))
#c.execute("INSERT INTO books (title, author_id) VALUES (?, ?)", ('Евгений Онегин', 3))
#c.execute("INSERT INTO readers (name) VALUES (?)", ('Иван Иванов',))
#c.execute("INSERT INTO readers (name) VALUES (?)", ('Петр Петров',))
#c.execute("INSERT INTO readers (name) VALUES (?)", ('Мария Сидорова',))
#c.execute("INSERT INTO rentals (book_id, reader_id) VALUES (?, ?)", (2,1))

# Сохранить изменения в базе данных
conn.commit()

# Создать графическое приложение
root = tk.Tk()
root.title("Библиотека")

# Создать элементы для отображения списка авторов
authors_frame = tk.LabelFrame(root, text="Авторы")
authors_frame.pack(fill="both", expand="yes")

authors_list = tk.Listbox(authors_frame)
authors_list.pack(fill="both", expand="yes")

# Создать элементы для добавления автора
add_author_frame = tk.LabelFrame(root, text="Добавить Автора")
add_author_frame.pack(fill="both", expand="yes")

add_author_title_label = tk.Label(add_author_frame, text="ФИО:")
add_author_title_label.pack(side="left")

add_author_title_entry = tk.Entry(add_author_frame)
add_author_title_entry.pack(side="left", fill="x", expand="yes")

add_author_button = tk.Button(add_author_frame, text="Добавить")
add_author_button.pack(side="left")

delete_author_button = tk.Button(add_author_frame, text="Удалить")
delete_author_button.pack(side="left")

# Создать элементы для отображения списка книг
books_frame = tk.LabelFrame(root, text="Книги")
books_frame.pack(fill="both", expand="yes")

books_list = tk.Listbox(books_frame)
books_list.pack(side="left", fill="both", expand="yes")

# Создать элементы для добавления книг
add_book_frame = tk.LabelFrame(root, text="Добавить книгу")
add_book_frame.pack(fill="both", expand="yes")

add_book_title_label = tk.Label(add_book_frame, text="Название:")
add_book_title_label.pack(side="left")

add_book_title_entry = tk.Entry(add_book_frame)
add_book_title_entry.pack(side="left", fill="x", expand="yes")

add_book_author_label = tk.Label(add_book_frame, text="Автор:")
add_book_author_label.pack(side="left")

add_book_author_combo = TTK.Combobox(add_book_frame)
add_book_author_combo['values'] = [str(row[0]) + " " + str(row[1]) for row in c.execute("SELECT id, name FROM authors")]
add_book_author_combo.pack(side="left")

add_book_button = tk.Button(add_book_frame, text="Добавить")
add_book_button.pack(side="left")

delete_book_button = tk.Button(add_book_frame, text="Удалить")
delete_book_button.pack(side="left")

# Создать элементы для отображения списка читателей
readers_frame = tk.LabelFrame(root, text="Читатели")
readers_frame.pack(fill="both", expand="yes")

readers_list = tk.Listbox(readers_frame)
readers_list.pack(side="left", fill="both", expand="yes")

# Создать элементы для добавления читателей
add_reader_frame = tk.LabelFrame(root, text="Добавить читателя")
add_reader_frame.pack(fill="both", expand="yes")

add_reader_name_label = tk.Label(add_reader_frame, text="Имя:")
add_reader_name_label.pack(side="left")

add_reader_name_entry = tk.Entry(add_reader_frame)
add_reader_name_entry.pack(side="left", fill="x", expand="yes")

add_reader_button = tk.Button(add_reader_frame, text="Добавить")
add_reader_button.pack(side="left")

delete_reader_button = tk.Button(add_reader_frame, text="Удалить")
delete_reader_button.pack(side="left")

# Создать элементы для управления прокатом книг
rentals_frame = tk.LabelFrame(root, text="Прокат книг")
rentals_frame.pack(fill="both", expand="yes")

rentals_list = tk.Listbox(rentals_frame)
rentals_list.pack(side="left", fill="both", expand="yes")

rentals_readers_combobox = TTK.Combobox(rentals_frame)
rentals_readers_combobox['values'] = [row[0] for row in c.execute("SELECT name FROM readers")]
rentals_readers_combobox.pack(side="top", fill="both")

rentals_books_combobox = TTK.Combobox(rentals_frame)
rentals_books_combobox['values'] = [row[0] for row in c.execute("SELECT title FROM books")]
rentals_books_combobox.pack(side="top", fill="both")

rent_book_button = tk.Button(rentals_frame, text="Выдать книгу")
rent_book_button.pack(side="bottom", fill="both")

return_book_button = tk.Button(rentals_frame, text="Вернуть книгу")
return_book_button.pack(side="bottom", fill="both")

# Создать функции для управления книгами
def display_books():
    """Отобразить список книг в базе данных."""
    # Очистить список книг
    books_list.delete(0, tk.END)

    # Заполнить список книг из базы данных
    for row in c.execute("SELECT books.id, title, name FROM books INNER JOIN authors ON authors.id = books.author_id"):
        books_list.insert(tk.END, " ".join([str(column) for column in row]))

def display_authors():
    authors_list.delete(0, tk.END)

    # Заполнить список книг из базы данных
    for row in c.execute("SELECT authors.id, name FROM authors"):
        authors_list.insert(tk.END, " ".join([str(column) for column in row]))

def add_book():
    """Добавить книгу в базу данных."""
    # Получить данные из полей ввода
    title = add_book_title_entry.get()
    author_selected = add_book_author_combo.get()

    # Проверить, не пусты ли поля ввода
    if not title or not author_selected:
        return

    author_id = author_selected.split()[0]

    # Вставить данные в базу данных
    c.execute("INSERT INTO books (title, author_id) VALUES (?, ?)", (title, author_id))

    # Сохранить изменения в базе данных
    conn.commit()

    # Очистить поля ввода
    add_book_title_entry.delete(0, tk.END)

    # Оюновить интерфейсь
    refresh()

# Создать функции для управления читателями
def display_readers():
    """Отобразить список читателей в базе данных."""
    # Очистить список читателей
    readers_list.delete(0, tk.END)

    # Заполнить список читателей из базы данных
    for row in c.execute("SELECT * FROM readers"):
        readers_list.insert(tk.END, " ".join([str(column) for column in row]))

def add_reader():
    """Добавить читателя в базу данных."""
    # Получить данные из полей ввода
    name = add_reader_name_entry.get()

    # Проверить, не пусто ли поле ввода
    if not name:
        return

    # Вставить данные в базу данных
    c.execute("INSERT INTO readers (name) VALUES (?)", (name,))

    # Сохранить изменения в базе данных
    conn.commit()

    # Очистить поле ввода
    add_reader_name_entry.delete(0, tk.END)

    # Оюновить интерфейсь
    refresh()

# Создать функции для управления прокатом книг
def display_rentals():
    """Отобразить список выданных книг в базе данных."""
    # Очистить список выданных книг
    rentals_list.delete(0, tk.END)

    # Заполнить список выданных книг из базы данных
    for row in c.execute("SELECT rentals.book_id, books.title, readers.name FROM rentals INNER JOIN books ON books.id = rentals.book_id INNER JOIN readers ON readers.id = rentals.reader_id"):
        rentals_list.insert(tk.END, " ".join([str(column) for column in row]))

    # Заполнить список читателей из базы данных
    rentals_readers_combobox['values'] = [str(row[0]) + " " + str(row[1]) for row in c.execute("SELECT id, name FROM readers")]

    # Заполнить список книг из базы данных
    rentals_books_combobox['values'] = [str(row[0]) + " " + str(row[1]) for row in c.execute("SELECT id, title FROM books")]

def rent_book():
    """Выдать книгу читателю."""
    # Получить данные из полей ввода
    book_selected = rentals_books_combobox.get()
    reader_selected = rentals_readers_combobox.get()

    # Проверить, выбраны ли книга и читатель
    if not book_selected or not reader_selected:
        return

    book_id = book_selected.split()[0]
    reader_id = reader_selected.split()[0]

    # Вставить данные в базу данных
    c.execute("INSERT INTO rentals (book_id, reader_id, rental_date) VALUES (?, ?, date('now'))",
              (book_id, reader_id))

    # Сохранить изменения в базе данных
    conn.commit()

    # Оюновить интерфейсь
    refresh()

def return_book():
    """Вернуть книгу в библиотеку."""
    # Получить данные из полей ввода
    rental_id = rentals_list.curselection()

    # Проверить, выбрана ли выданная книга
    if not rental_id:
        return

    selected_index = rental_id[0]
    selected_item = rentals_list.get(selected_index)

    index = selected_item.split()[0]

    # Удалить данные из базы данных
    c.execute("DELETE FROM rentals WHERE id = ?", (index))

    # Сохранить изменения в базе данных
    conn.commit()

    # Оюновить интерфейсь
    refresh()

def delete_reader():
    reader_selected = readers_list.curselection()

    # Проверить, выбрана ли выданная книга
    if not reader_selected:
        return

    selected_index = reader_selected[0]
    selected_item = readers_list.get(selected_index)

    index = selected_item.split()[0]

    c.execute("DELETE FROM readers WHERE id = ?", (index))

    # Сохранить изменения в базе данных
    conn.commit()

    # Оюновить интерфейсь
    refresh()

def delete_book():
    book_selected = books_list.curselection()

    # Проверить, выбрана ли выданная книга
    if not book_selected:
        return

    selected_index = book_selected[0]
    selected_item = books_list.get(selected_index)

    index = selected_item.split()[0]

    c.execute("DELETE FROM books WHERE id = ?", (index))

    # Сохранить изменения в базе данных
    conn.commit()

    # Оюновить интерфейс
    refresh()

def add_author():
    """Добавить автора в базу данных."""
    # Получить данные из полей ввода
    name = add_author_title_entry.get()

    # Проверить, не пусто ли поле ввода
    if not name:
        return

    # Вставить данные в базу данных
    c.execute("INSERT INTO authors (name) VALUES (?)", (name,))

    # Сохранить изменения в базе данных
    conn.commit()

    # Очистить поле ввода
    add_author_title_entry.delete(0, tk.END)

    # Оюновить интерфейсь
    refresh()

def delete_author():
    author_selected = authors_list.curselection()

    print(author_selected)

    # Проверить, выбрана ли автор
    if not author_selected:
        return

    selected_index = author_selected[0]
    selected_item = authors_list.get(selected_index)

    index = selected_item.split()[0]

    c.execute("DELETE FROM authors WHERE id = ?", (index))

    # Сохранить изменения в базе данных
    conn.commit()

    # Оюновить интерфейс
    refresh()

def refresh():
    display_books()
    display_readers()
    display_rentals()
    display_authors()

add_book_button.config(command=add_book)
add_reader_button.config(command=add_reader)
add_author_button.config(command=add_author)
rent_book_button.config(command=rent_book)
return_book_button.config(command=return_book)
delete_reader_button.config(command=delete_reader)
delete_book_button.config(command=delete_book)
delete_author_button.config(command=delete_author)

refresh()

root.mainloop()
conn.close()