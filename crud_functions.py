import sqlite3

def create_connection(db_file):
    """Создает соединение с SQLite базой данных."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def initiate_db():
    """Создает таблицу Products, если она еще не создана, и заполняет её начальными данными."""
    database = r"products.db"  # Укажите путь к вашей базе данных
    conn = create_connection(database)

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    price INTEGER NOT NULL
                );
            ''')
            # Вставляем первоначальные данные, если таблица пуста
            cursor.execute("SELECT COUNT(*) FROM Products")
            if cursor.fetchone()[0] == 0:
                cursor.executescript('''
                    INSERT INTO Products (title, description, price) VALUES
                    ('Продукт 1', 'Описание 1', 100),
                    ('Продукт 2', 'Описание 2', 200),
                    ('Продукт 3', 'Описание 3', 300),
                    ('Продукт 4', 'Описание 4', 400);
                ''')
            conn.commit()  # Сохраняем изменения
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    else:
        print("Ошибка! Не удалось создать соединение с базой данных.")

def get_all_products():
    """Получает все продукты из таблицы Products."""
    database = r"products.db"  # Укажите путь к вашей базе данных
    conn = create_connection(database)
    products = []

    if conn is not None:
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, title, description, price FROM Products")
            rows = cur.fetchall()
            for row in rows:
                products.append(row)  # Добавляем каждую строку в список продуктов
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

    return products