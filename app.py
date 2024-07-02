from flask import Flask,request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# initialize the database
def init_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''create table if not exists users
                    (id integer primary key, name text, phone text)''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')
    # return <form action="{{ url_for('submit') }}" method="post" ></form>
    #     <label for="name">name: </label>
    #     <input type="text" id="name" name="name" required>
    #     <br>
    #     <label for="phone-no">phone number(us only)</label>
    #     <input type="text" id="phone-no" name="phone-no" required>
    #     <br>
    #     <input type="submit" value = "notify me!">
    # </form>

@app.route('/submit', methods=['post'])
def submit():
    name = request.form['name']
    phone = request.form['phone-no']

    with sqlite3.connect('database.db') as conn:
        c= conn.cursor()
        c.execute('insert into users (name, phone) values (?,?)', (name, phone))
        conn.commit()
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    init_db()
    app.run(debug= True)