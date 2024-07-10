# FootballScout1/register_and_login_update11.py

from flask import Flask, redirect, url_for, session, flash, render_template, request
from flask_dance.contrib.github import make_github_blueprint, github
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from models.user import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import uuid
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False  # Flask will ignore trailing slashes

# Secret key for session management
app.secret_key = app.config['SECRET_KEY']

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Database setup
engine = create_engine('mysql+mysqlconnector://football_scout_dev:football_scout_dev_pwd@localhost/football_scout_dev_db')
Session = sessionmaker(bind=engine)
db_session = Session()

# Flask-Dance GitHub OAuth configuration
github_bp = make_github_blueprint(client_id=app.config['GITHUB_CLIENT_ID'],
                                  client_secret=app.config['GITHUB_CLIENT_SECRETS'],
                                  redirect_to='github_login')

app.register_blueprint(github_bp, url_prefix='/github_login')

# Function to generate cache_id
def generate_cache_id():
    return str(uuid.uuid4())

# Route for rendering the login page and handling form submission
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    cache_id = generate_cache_id()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Authentication logic, such as checking the database for the user
        user = db_session.query(User).filter_by(email=username).first()
        if user and user.password == password:  # Placeholder logic, add password hashing comparison
            if user.confirmed:
                session['user_id'] = user.id
                return redirect(url_for('homepage', username=user.first_name))
            else:
                flash('Please confirm your email address before logging in.', 'warning')
                return redirect(url_for('login_page'))
        else:
            return 'Login Failed', 401

    return render_template('login_update5.html', cache_id=cache_id)

# Route for rendering the homepage after login
@app.route('/homepage')
def homepage():
    if github.authorized:
        resp = github.get('/user')
        assert resp.ok, resp.text
        email = resp.json()['email']
    else:
        if 'user_id' not in session:
            return redirect(url_for('login_page'))

        user_id = session['user_id']
        user = db_session.query(User).filter_by(id=user_id).first()
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('login_page'))
        email = user.email

    cache_id = generate_cache_id()
    content = {
        "username": email,  # Update with appropriate user data
        "notifications": ["Notification 1", "Notification 2", "Notification 3"],
        "lists": ["List 1", "List 2", "List 3"],
        "reports": ["Report 1", "Report 2", "Report 3"]
    }
    return render_template('homepage5.html', content=content, cache_id=cache_id)

# GitHub OAuth callback route
@app.route('/github_login')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))

    resp = github.get('/user')
    assert resp.ok, resp.text
    email = resp.json()['email']

    user = db_session.query(User).filter_by(email=email).first()
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('login_page'))

    session['user_id'] = user.id
    return redirect(url_for('homepage', username=user.first_name))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5003")

