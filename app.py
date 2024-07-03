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

carriers = {
    'AT&T': 'txt.att.net',
    'Verizon': 'vtext.com',
    'T-Mobile': 'tmomail.net',
    'Sprint': 'messaging.sprintpcs.com',
    'Spectrum': 'vtext.com',
    'US Cellular': 'uscc.textmsg.com',
    'Metro PCS': 'metropcs.sms.us'
}

def get_gateway_address(phone_number, carrier):
    return f"{phone_number}@{carriers[carrier]}"

# Phone Number and carrier provided by User
phoneNumber = 2166324947
carrier = 'Spectrum'
gatewayAddress = get_gateway_address(phoneNumber,carrier)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['post'])
def submit():
    name = request.form['name']
    phone = request.form['phone-no']
    carrier = request.form['carrier']

    gatewayAddress = get_gateway_address(phone, carrier)
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('insert into users (name, phone, carrier) values (?,?,?)', (name, phone, carrier))
        conn.commit()
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    init_db()
    app.run(debug = True)