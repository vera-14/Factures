# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect('factures.db')  # Исходная база данных, хранящая номера, описание фактур и примеры
cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS samples""")  # Обновляем бд
cur.execute("""CREATE TABLE IF NOT EXISTS samples(
   id INT PRIMARY KEY,
   strophica TEXT,
   stopnost INT,
   meter TEXT,
   example1 TEXT,
   number1 INT,
   year1 INT,
   name1 TEXT,
   example2 TEXT,
   number2 INT,
   year2 INT,
   name2 TEXT,
   example3 TEXT,
   number3 INT,
   year3 INT,
   name3 TEXT);
""")
conn.commit()

f = open('current_db_pushkin.txt', 'r', encoding='utf-8')  # открываем текстовый файл с таблицей примеров фактур
cont = f.read()
f.close()

rows = cont.split('@#')  # Разбиваем файл на строки, затем строки на поля
formatted = [tuple(x.split('@')) for x in rows]

# Загружаем в бд поочередно строки из массива
for i in range(len(formatted, )):
    cur.executemany("INSERT INTO samples VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (formatted[i],))
    conn.commit()

sql = """
UPDATE samples
SET meter = 'ямб' 
WHERE meter = 'я'
"""
cur.execute(sql)
conn.commit()

sql = """
UPDATE samples
SET meter = 'хорей' 
WHERE meter = 'х'
"""
cur.execute(sql)
conn.commit()

sql = """
UPDATE samples
SET meter = 'дактиль' 
WHERE meter = 'д'
"""
cur.execute(sql)
conn.commit()

sql = """
UPDATE samples
SET meter = 'амфибрахий' 
WHERE meter = 'ам'
"""
cur.execute(sql)
conn.commit()

sql = """
UPDATE samples
SET meter = 'анапест' 
WHERE meter = 'ан'
"""
cur.execute(sql)
conn.commit()

cur.execute("SELECT * FROM samples;")  # Выводим все результаты
all_results = cur.fetchall()
#print(all_results)