from flask import Flask,request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)

# Configure the databse URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Student Model Definition
class Student(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    cell_number = db.Column(db.String(15), nullable=False)
    cell_carrier = db.Column(db.String(50), nullable=False)

#Initialize Database
with app.app_context():
    db.create_all()

carriers = {
    'att': 'txt.att.net', # AT&T
    'verizon': 'vtext.com', # Verizon
    'tmobile': 'tmomail.net', # T-Mobile
    'sprint': 'messaging.sprintpcs.com', #Sprint
    'spectrum': 'vtext.com', #Spectrum
    'uscellular': 'uscc.textmsg.com', #US Cellular
    'metropcs': 'metropcs.sms.us' # Metro PCS
}

def get_gateway_address(phone_number, carrier):
    return f"{phone_number}@{carriers[carrier]}"


# Phone Number and carrier provided by User
phoneNumber = 2166324947
carrier = 'spectrum'
gatewayAddress = get_gateway_address(phoneNumber,carrier)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    cell_number = request.form['phone-no']
    cell_carrier = request.form['carriers']

    gatewayAddress = get_gateway_address(cell_number, cell_carrier)
    new_student = Student(first_name= first_name, last_name= last_name,
                          cell_number= cell_number, cell_carrier= cell_carrier  )
    
    db.session.add(new_student)
    db.session.commit()
    # with sqlite3.connect('database.db') as conn:
        # c = conn.cursor()
        # c.execute('insert into users (first_name, last_name, phone, carrier) values (?,?,?,?)', 
                #  (first_name, last_name, phone, carrier))
        # conn.commit()
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug = True)