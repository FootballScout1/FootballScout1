# FootballScout1/test_smtp_github.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, url_for, redirect, request
from flask_dance.contrib.github import make_github_blueprint, github
from config import Config

# Create a Flask application instance
app = Flask(__name__)
app.config.from_object(Config)

# Load GitHub blueprint with correct config
github_bp = make_github_blueprint(
    client_id=app.config['GITHUB_CLIENT_ID'],
    client_secret=app.config['GITHUB_CLIENT_SECRETS'],
)
app.register_blueprint(github_bp, url_prefix='/github_login')

# SMTP settings from configuration
smtp_server = Config.MAIL_SERVER
smtp_port = Config.MAIL_PORT
sender_email = Config.MAIL_USERNAME
receiver_email = 'ukonud4@gmail.com'
password = Config.MAIL_PASSWORD
EMAIL_USE_TLS = Config.MAIL_USE_TLS

def send_email(subject, body):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    part1 = MIMEText(body, "plain")
    message.attach(part1)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")

@app.route('/login/github')
def login():
    return redirect(url_for('github.login'))

@app.route('/github_login')
def github_login():
    resp = github.get('/user')
    assert resp.ok, resp.text
    return 'You are logged in as ' + resp.json()['login']

if __name__ == "__main__":
    app.run(debug=True)


