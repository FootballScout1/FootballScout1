from flask import Flask, redirect, url_for, session, flash, render_template, request
from flask_dance.contrib.google import make_google_blueprint, google
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from models.user import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import uuid
from config import Config
from appwrite.client import Client
from appwrite.services.users import Users
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False  # Flask will ignore trailing slashes

# Secret key for session management
app.secret_key = app.config['SECRET_KEY']

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Appwrite client setup
client = Client()
client.set_endpoint(app.config['APPWRITE_ENDPOINT'])  # Appwrite Endpoint
client.set_project(app.config['APPWRITE_PROJECT_ID'])  # Project ID
client.set_key(app.config['APPWRITE_API_KEY'])  # Secret API key

users = Users(client)

# Database setup
engine = create_engine('mysql+mysqlconnector://football_scout_dev:football_scout_dev_pwd@localhost/football_scout_dev_db')
Session = sessionmaker(bind=engine)
db_session = Session()

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)

# OAuth 2 client setup
oauth_client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])

# Google OAuth Blueprint
google_bp = make_google_blueprint(
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    redirect_to='google_login_callback'  # Endpoint to handle Google login callback
)

app.register_blueprint(google_bp, url_prefix="/login")

@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).get(user_id)

def generate_cache_id():
    return str(uuid.uuid4())

# Route for rendering the login page
@app.route('/login', methods=['GET'])
def login_page():
    cache_id = generate_cache_id()
    return render_template('login_update7.html', cache_id=cache_id)

# Route for handling the login form submission (password-based)
@app.route('/login', methods=['POST'])
def login_submit():
    username = request.form.get('username')
    password = request.form.get('password')

    user = db_session.query(User).filter_by(email=username).first()
    if user and user.password == password:
        if user.confirmed:
            login_user(user)
            return redirect(url_for('homepage', username=user.first_name))
        else:
            flash('Please confirm your email address before logging in.', 'warning')
            return redirect(url_for('login_page'))
    else:
        return 'Login Failed', 401

# Route for rendering the homepage after login
@app.route('/homepage')
@login_required
def homepage():
    if google.authorized:
        resp = google.get('/oauth2/v2/userinfo')
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
    return render_template('homepage6.html', content=content, cache_id=cache_id)

# Route for rendering the registration page
@app.route('/register', methods=['GET'])
def register_page():
    cache_id = generate_cache_id()
    return render_template('register.html', cache_id=cache_id)

# Route for handling the registration form submission including sending email verification
@app.route('/register', methods=['POST'])
def register():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
    db_session.add(new_user)
    db_session.commit()

    user = users.create(
        user_id=str(uuid.uuid4()),
        email=email,
        password=password,
        name=f"{first_name} {last_name}"
    )

    send_verification_email(email)

    flash('A confirmation email has been sent to your email address.', 'success')
    return redirect(url_for('login_page'))

# Google OAuth callback route
@app.route('/login/google/callback')
def google_login_callback():
    if not google.authorized:
        return redirect(url_for('google.login'))

    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text
    email = resp.json()['email']

    user = db_session.query(User).filter_by(email=email).first()

    if not user:
        return redirect(url_for('register_page'))

    login_user(user)
    return redirect(url_for('homepage', username=user.first_name))

# GitHub OAuth callback route
@app.route('/login/github')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))

    resp = github.get('/user')
    assert resp.ok, resp.text
    email = resp.json()['email']

    user = db_session.query(User).filter_by(email=email).first()

    if not user:
        return redirect(url_for('register_page'))

    login_user(user)
    return redirect(url_for('homepage', username=user.first_name))

# Token generation and verification functions
def generate_confirmation_token(email):
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except:
        return False
    return email

# Function to send the verification email
def send_verification_email(user_email):
    token = generate_confirmation_token(user_email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    msg = Message(recipients=[user_email], body=html, subject=subject)
    mail.send(msg)

# Email Confirmation
@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('login_page'))

    user = db_session.query(User).filter_by(email=email).first_or_404()

    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        db_session.add(user)
        db_session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('login_page'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

