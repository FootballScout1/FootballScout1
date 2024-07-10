from flask import Flask, redirect, url_for, session, flash, render_template
from flask_dance.contrib.google import make_google_blueprint, google
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
app.secret_key = 'super_secret_key'

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Database setup
engine = create_engine('mysql+mysqlconnector://football_scout_dev:football_scout_dev_pwd@localhost/football_scout_dev_db')
Session = sessionmaker(bind=engine)
db_session = Session()

# Flask-Dance Google OAuth configuration
google_bp = make_google_blueprint(client_id='your-client-id',
                                  client_secret='your-client-secret',
                                  redirect_to='google_login')

app.register_blueprint(google_bp, url_prefix='/google_login')


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
    # Placeholder logic for password-based login
    return 'Login Failed', 401


# Route for rendering the homepage after login
@app.route('/homepage')
def homepage():
    if not google.authorized:
        return redirect(url_for('google.login'))

    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text
    email = resp.json()['email']

    user = db_session.query(User).filter_by(email=email).first()

    if user:
        cache_id = generate_cache_id()
        content = {
            "username": user.first_name,
            "notifications": ["Notification 1", "Notification 2", "Notification 3"],
            "lists": ["List 1", "List 2", "List 3"],
            "reports": ["Report 1", "Report 2", "Report 3"]
        }
        return render_template('homepage2.html', content=content, cache_id=cache_id)
    else:
        flash('User not found.', 'error')
        return redirect(url_for('login_page'))


# Route for rendering the registration page
@app.route('/register', methods=['GET'])
def register_page():
    cache_id = generate_cache_id()
    return render_template('register.html', cache_id=cache_id)


# Google OAuth callback route
@app.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))

    resp = google.get('/oauth2/v2/userinfo')
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


if __name__ == '__main__':
    app.run(debug=True)

