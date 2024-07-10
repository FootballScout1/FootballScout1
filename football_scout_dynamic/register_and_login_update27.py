from flask import Flask, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth
import os
from config import Config
import jwt

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']

# OAuth configuration
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid profile email'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)
github = oauth.register(
    name='github',
    client_id=app.config['GITHUB_CLIENT_ID'],
    client_secret=app.config['GITHUB_CLIENT_SECRET'],
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'}
)

@app.route('/')
def home():
    return 'Welcome to the Football Scout App'

@app.route('/login')
def login():
    return 'Login Page'

@app.route('/register')
def register():
    return 'Register Page'

@app.route('/google_login')
def google_login():
    redirect_uri = url_for('google_authorize', _external=True)
    print(f"Redirect URI for Google Login: {redirect_uri}")  # Debug print statement
    return google.authorize_redirect(redirect_uri)

@app.route('/google_authorize')
def google_authorize():
    try:
        token = google.authorize_access_token()
        id_token = token['id_token']
        decoded_id_token = jwt.decode(id_token, options={"verify_signature": False})
        nonce = decoded_id_token.get('nonce')
        user = google.parse_id_token(token, nonce)
        session['user'] = user
        print(f"User info: {user}")  # Debug print statement
        return redirect('/')
    except Exception as e:
        print(f"Error during Google authorization: {e}")  # Debug print statement
        return redirect('/')

@app.route('/github_login')
def github_login():
    redirect_uri = url_for('github_authorize', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/github_authorize')
def github_authorize():
    token = github.authorize_access_token()
    user = github.get('user')
    session['user'] = user
    return redirect('/')

if __name__ == '__main__':
    app.run(host=os.getenv('FOOTBALL_SCOUT_API_HOST', '127.0.0.1'),
            port=int(os.getenv('FOOTBALL_SCOUT_API_PORT', 5000)),
            debug=True)

