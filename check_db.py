import sqlite3
import pandas as pd

def check_db():
    print("Inside check_db() func")
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM Students')
        rows = c.fetchall()
        for row in rows:
            print(row)


if __name__ == "__main__":
    check_db()