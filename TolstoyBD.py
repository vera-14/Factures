# -*- coding: utf-8 -*-
import psycopg2
conn = psycopg2.connect(dbname='poems', user='poems_adm',
                        password='jytuby', host='db4.sbras.ru')
cursor = conn.cursor()
cursor.execute('SELECT "TEXT" FROM public."POEM_CONTENT_3"')
lines = cursor.fetchall()
n = 1
with open("MeterRhyme/Tolstoy1.txt", "a", encoding='utf-8') as file:
    for line in lines:
        file.write("$$$")
        file.write(str(n))
        file.write('\n')
        file.write(line[0])
        file.write('\n')
        file.write("***")
        file.write('\n')
        n = n+1

cursor.close()
conn.close()
