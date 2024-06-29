from flask import Flask,request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY_KEY, name TEXT, phone TEXT)''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    phone = request.form['phone-no']

    with sqlite3.connect('database.db') as conn:
        c= conn.cursor()
        c.execute('INSERT INTO users (name, phone) VALUES (?,?)', (name, phone))
        conn.commit()
    
    return redirect(url_for('index.html'))

if __name__ == "__main__":
    init_db()
    app.run(debug= True)