import psycopg2
from faker import Faker

# Підключення до PostgreSQL
DB_CONFIG = {
    "dbname": "postgres",        
    "user": "postgres",          
    "password": "password",  
    "host": "localhost",
    "port": "5432"
}

try:
    # Підключення до БД
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("Успішно підключено до PostgreSQL")

    # Створення таблиці 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        );
    """)
    conn.commit()
    print("Таблицю створено")

    # Генерація та додавання  випадкових записів 
    fake = Faker()
    print("\nГенерація та наповнення даними")
    for _ in range(5):
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s);",
            (fake.name(), fake.email())
        )
    conn.commit()
    print("5 записів успішно додано.")

    # Вибірка даних
    cursor.execute("SELECT * FROM users;")
    users = cursor.fetchall()
    print("\nВибірка даних (SELECT)")
    for user in users:
        print(f"ID: {user[0]} | Ім'я: {user[1]} | Email: {user[2]}")

    # Зміна даних 
    if users:
        target_id = users[0][0]
        cursor.execute(
            "UPDATE users SET name = %s WHERE id = %s;",
            ("Оновлений Користувач", target_id)
        )
        conn.commit()
        print(f"\nЗміна даних (UPDATE)")
        print(f"Ім'я користувача з ID={target_id} змінено на 'Оновлений Користувач'.")

    # Видалення даних
    if len(users) > 1:
        delete_id = users[1][0]
        cursor.execute("DELETE FROM users WHERE id = %s;", (delete_id,))
        conn.commit()
        print(f"\nВидалення даних")
        print(f"Запис з ID={delete_id} успішно видалено.")

    # Закриття ресурсів
    cursor.close()
    conn.close()
    print("\nЗ'єднання з БД закрито")

except Exception as ex:
    print(f"\nПомилка під час роботи з БД: {ex}")