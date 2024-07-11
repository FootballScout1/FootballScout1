from flask import Flask, redirect, url_for, session, flash, render_template, request
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.github import make_github_blueprint, github
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from models.user import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import uuid
from config import Config
from appwrite.client import Client
from appwrite.services.users import Users

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
client.set_project(app.config['APPWRITE_PROJECT_ID'])  # project ID
client.set_key(app.config['APPWRITE_API_KEY'])  # secret API key

users = Users(client)

# Database setup
engine = create_engine('mysql+mysqlconnector://football_scout_dev:football_scout_dev_pwd@localhost/football_scout_dev_db')
Session = sessionmaker(bind=engine)
db_session = Session()

# Flask-Dance Google OAuth configuration
google_bp = make_google_blueprint(client_id=app.config['GOOGLE_CLIENT_ID'],
                                  client_secret=app.config['GOOGLE_CLIENT_SECRET'],
                                  scope=[
                                      "openid",
                                      "https://www.googleapis.com/auth/userinfo.email",
                                      "https://www.googleapis.com/auth/userinfo.profile"],
                                  redirect_to='google_login')

app.register_blueprint(google_bp, url_prefix='/google_login')

# Flask-Dance GitHub OAuth configuration
github_bp = make_github_blueprint(client_id=app.config['GITHUB_CLIENT_ID'],
                                  client_secret=app.config['GITHUB_CLIENT_SECRET'],
                                  redirect_to='github_login')

app.register_blueprint(github_bp, url_prefix='/github_login')

# Function to generate cache_id
def generate_cache_id():
    return str(uuid.uuid4())

# Route for rendering the login page
@app.route('/login', methods=['GET'])
def login_page():
    cache_id = generate_cache_id()
    return render_template('login_update10.html', cache_id=cache_id)

# Route for handling the login form submission (password-based)
@app.route('/login', methods=['POST'])
def login():
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

# Route for rendering the homepage after login
@app.route('/homepage')
def homepage():
    if google.authorized:
        resp = google.get('/oauth2/v2/userinfo')
        assert resp.ok, resp.text
        email = resp.json()['email']
    elif github.authorized:
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
    return render_template('homepage10.html', content=content, cache_id=cache_id)

# Route for rendering the registration page
@app.route('/register', methods=['GET'])
def register_page():
    cache_id = generate_cache_id()
    return render_template('register10.html', cache_id=cache_id)

# Route for handling the registration form submission including sending email verification
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

    # Create user in Appwrite
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
@app.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))

    # Fetch token from Google's token endpoint
    token = google_bp.session.fetch_token(
        google_bp.token_url,
        client_secret=google_bp.client_secret,
        authorization_response=request.url,
        scope=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile"
        ]
    )

    # Fetch user info from Google
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text
    email = resp.json().get('email')
    if not email:
        flash('Email not found in Google response', 'error')
        return redirect(url_for('login_page'))

    user = db_session.query(User).filter_by(email=email).first()

    if not user:
        # If user doesn't exist, redirect to registration page
        return redirect(url_for('register_page'))

    # Log the user in by setting the session
    session['user_id'] = user.id
    return redirect(url_for('homepage', username=user.first_name))

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
        # If user doesn't exist, redirect to registration page
        return redirect(url_for('register_page'))

    # Log the user in by setting the session
    session['user_id'] = user.id
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
    msg = Message(recipients=[user_email], body=html, subject=subject, sender='your-email@example.com')
    mail.send(msg)

# Route for email confirmation
@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('login_page'))

    user = db_session.query(User).filter_by(email=email).first()

    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        db_session.add(user)
        db_session.commit()
        flash('You have confirmed your account. Thanks!', 'success')

    return redirect(url_for('login_page'))

if __name__ == "__main__":
    app.run(debug=True)

