from flask import Flask, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
# app.secret_key = os.urandom(24)
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
    client_id='GITHUB_CLIENT_ID',
    client_secret='GITHUB_CLIENT_SECRET',
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
    return google.authorize_redirect(redirect_uri)

@app.route('/google_authorize')
def google_authorize():
    token = google.authorize_access_token()
    user = google.parse_id_token(token)
    session['user'] = user
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

