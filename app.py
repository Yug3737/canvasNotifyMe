import os
import subprocess
from flask import Flask,request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy.orm import DeclarativeBase
from supabase import  create_client, Client

SUPABASE_PROJECT_URL = os.environ.get("SUPABASE_PROJECT_URL")
SUPABASE_SECRET_KEY = os.environ.get("SUPABASE_SECRET_SERVICE_ROLE_API_KEY")

if not SUPABASE_PROJECT_URL:
    raise ValueError("SUPABASE_PROJECT_URL is not set`")
elif not SUPABASE_SECRET_KEY:
    raise ValueError("SUPABASE_SECRET_KEY is not set")


supabase = create_client(SUPABASE_PROJECT_URL, SUPABASE_SECRET_KEY)

app = Flask(__name__)

data = supabase.table("Student").select("*").execute()
print("data", data)


# Ensure the environment variables are set
if not os.getenv('SENDER_EMAIL') or not os.getenv('YUGPATEL8767_APP_KEY'):
    raise EnvironmentError("SENDER_EMAIL or YUGPATEL8767_APP_KEY environment variables are not set.")

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


@app.route('/submit', methods=['POST'])
def submit():
    print("Start of submit")

    env = os.environ.copy()
    env['PYTHONPATH'] = os.pathsep.join([env.get('PYTHONPATH', ''), os.path.abspath(os.path.dirname(__file__))])


    first_name = request.form['first-name']
    last_name = request.form['last-name']
    cell_number = request.form['phone-no']
    cell_carrier = request.form['carriers']


    try:

        print("Before adding Student")
        data = supabase.table("Student").insert({
            "first_name": first_name,
            "last_name": last_name, 
            "cell_number": cell_number,
            "cell_carrier": cell_carrier}).execute()

    except Exception as e:
        print(f"Error adding Student to database: {e}")
        return redirect(url_for('index'))

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