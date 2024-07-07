from flask import Flask, request, render_template, redirect, url_for, session
from models.user import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import uuid

app = Flask(__name__)
app.url_map.strict_slashes = False  # Flask will ignore trailing slashes

# Secret key for session management
app.secret_key = 'super_secret_key'

# Database setup
engine = create_engine('mysql+mysqlconnector://football_scout_dev:football_scout_dev_pwd@localhost/football_scout_dev_db')
Session = sessionmaker(bind=engine)
db_session = Session()

# Function to generate cache_id
def generate_cache_id():
    return str(uuid.uuid4())

# Route for rendering the login page
@app.route('/login', methods=['GET'])
def login_page():
    cache_id = generate_cache_id()
    return render_template('login_update4.html', cache_id=cache_id)

# Route for handling the login form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Authentication logic, such as checking the database for the user
    user = db_session.query(User).filter_by(email=username).first()
    if user and user.password == password:  # Placeholder logic, add password hashing comparison
        session['user_id'] = user.id
        return redirect(url_for('homepage', username=user.first_name))
    else:
        return 'Login Failed', 401

# Route for rendering the homepage after login
@app.route('/homepage')
def homepage():
    username = request.args.get('username')
    cache_id = generate_cache_id()
    content = {
        "username": username,
        "notifications": ["Notification 1", "Notification 2", "Notification 3"],
        "lists": ["List 1", "List 2", "List 3"],
        "reports": ["Report 1", "Report 2", "Report 3"]
    }
    return render_template('homepage2.html', content=content, cache_id=cache_id)

# Route for rendering the registration page
@app.route('/register', methods=['GET'])
def register_page():
    cache_id = generate_cache_id()
    return render_template('register.html', cache_id=cache_id)

# Route for handling the registration form submission
@app.route('/register', methods=['POST'])
def register():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    # Create a new User object and save to the database
    new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)  # Add password hashing
    db_session.add(new_user)
    db_session.commit()

    # Log the user in by setting the session
    session['user_id'] = new_user.id

    return redirect(url_for('homepage', username=new_user.first_name))

if __name__ == '__main__':
    app.run(debug=True)

