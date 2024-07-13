import os
import subprocess
from flask import Flask,request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
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
    'sprint': 'messaging.sprintpcs.com', # Sprint
    'spectrum': 'vtext.com', #Spectrum
    'uscellular': 'uscc.textmsg.com', #US Cellular
    'metropcs': 'metropcs.sms.us' # Metro PCS
}

def get_gateway_address(phone_number, carrier):
    return f"{phone_number}@{carriers[carrier]}"


@app.route('/')
def index():
    return render_template('index.html')

print("before gatewaty address")
gatewayAddress = get_gateway_address(cell_number, cell_carrier)

@app.route('/submit', methods=['POST'])
def submit():
    print("Start of submit")

    # # Constructing the path to emailtoSMSConfig.py dynamically
    # root_path = Path(__file__).resolve().parent  # Assuming app.py is in the root directory
    # config_path = root_path / 'smsBot' / 'emailtoSMSConfig.py'

    # if not config_path.exists():
    #     print(f"Error: emailtoSMSConfig.py not found at {config_path}")
    #     return redirect(url_for('index'))

    env = os.environ.copy()
    env['PYTHONPATH'] = os.pathsep.join([env.get('PYTHONPATH', ''), os.path.abspath(os.path.dirname(__file__))])


    first_name = request.form['first-name']
    last_name = request.form['last-name']
    cell_number = request.form['phone-no']
    cell_carrier = request.form['carriers']



    print("before creating new Student objext")
    new_student = Student(first_name= first_name, last_name= last_name,
                          cell_number= cell_number, cell_carrier= cell_carrier)
    
    print("Before adding Student")
    db.session.add(new_student)
    db.session.commit()

    # Phone Number and carrier provided by User
    phoneNumber = cell_number 
    carrier = cell_carrier 
    gatewayAddress = get_gateway_address(phoneNumber,carrier)
    
    print("before calling hello.py script")

    try:
        result = subprocess.run(['python', 'smsBot/hello.py', gatewayAddress], capture_output=True, text=True, env=env)
        print(result.stdout)

        if result.returncode != 0:
            print("hello.py encountered an error")
            print(result.stderr)
    except Exception as e:
        print(f"Error running subprocess: {e}")

    
    print("Redirecting to index.html") 
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug = True)