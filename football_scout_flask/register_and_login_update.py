from flask import Flask, request, render_template, redirect, url_for
from models.user import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)

# Database setup
engine = create_engine('mysql+mysqlconnector://football_scout_dev:football_scout_dev_pwd@localhost/football_scout_dev_db')
Session = sessionmaker(bind=engine)
session = Session()

# Route for rendering the login page
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login_update.html')

# Route for handling the login form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Authentication logic, such as checking the database for the user
    user = session.query(User).filter_by(email=username).first()
    if user and user.password == password:  # Placeholder logic, add password hashing comparison
        return redirect(url_for('welcome'))
    else:
        return 'Login Failed', 401

# Route for the welcome page
@app.route('/welcome')
def welcome():
    # return 'Welcome to Football Scout!'
    return render_template('homepage.html')

# Route for rendering the registration page
@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

# Route for handling the registration form submission
@app.route('/register', methods=['POST'])
def register():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    # Create a new User object and save to the database
    new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)  # Add password hashing
    session.add(new_user)
    session.commit()

    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)

