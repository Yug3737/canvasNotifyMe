import sqlite3
import pandas as pd

def check_db():
    print("Inside check_db() func")
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users')
        rows = c.fetchall()
        for row in rows:
            print(row)

# conn = sqlite3.connect("test_databases")
# cursor_obj = conn.cursor()

# table = ''' create table IF NOT EXISTS instructor(ID INTEGER PRIMARY KEY NOT NULL, FNAME VARCHAR(20), LNAME VARCHAR(20), CITY VARCHAR(20), CCODE CHAR(2));'''

# cursor_obj.execute(table)

# print("table is ready")

# cursor_obj.execute('''insert into INSTRUCTOR values (1, 'Rav', 'Ahuja', 'TORONTO', 'CA')''')
# cursor_obj.execute('''insert into INSTRUCTOR values (2, 'Raul', 'Chong', 'Markham', 'CA'), (3, 'Hima', 'Vasudevan', 'Chicago', 'US')''')

# conn.commit()

if __name__ == "__main__":
    check_db()