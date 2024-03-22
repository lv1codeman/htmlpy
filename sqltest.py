import sqlite3
conn = sqlite3.connect('OB010.db')

c = conn.cursor()
# coursedata = [('00005', '全民國防教育軍事訓練-國防政策', '軍訓課')]
# c.executemany('INSERT INTO COURSES VALUES (?,?,?)', coursedata)

keyword = '%科技%'
# c.execute("SELECT * FROM COURSES WHERE CRSNM like '%s'" % keyword)
# print(c.fetchall())
for row in c.execute("SELECT * FROM COURSES WHERE CRSNM like '%s'" % keyword):
    print(row)


conn.commit()
conn.close()
