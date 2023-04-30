# import randominfo as ri
#
# class Person:
#     def __init__(self) -> None:
#         self.first_name = ri.get_first_name()
#         self.last_name = ri.get_last_name()
#         self.birthdate = ri.get_birthdate()
#
# person1 = Person()
# # print(ri.get_email(person1))
# email_list = []
# for i in range(0,20):
#     email_list.append(ri.get_email(person1))
# print(email_list)
#
# import time
# start_time = time.time()
# print(start_time)
# final = []
# dict = {}
# for i in email_list:
#     dict.update({'email':i})
#     final.append(dict)
# end_time = time.time()
# print(end_time)
# print(final)
# print(end_time-start_time)

import sqlite3

conn = sqlite3.connect('database.db')
print("database opened successfully")

# conn.execute('CREATE TABLE if not exists recording (name TEXT, email TEXT)')
# print("Table created successfully")

cur = conn.cursor()
cur.execute('SELECT name FROM sqlite_schema WHERE type ="table" AND name NOT LIKE "sqlite_%";')
# cur.execute("INSERT INTO students (name,addr,city,pin) VALUES ('sharath','ambernath','mumbai','421501')")
# cur.execute("select * from students")
# rows = cur.fetchall()
print(cur.fetchall())
conn.close()