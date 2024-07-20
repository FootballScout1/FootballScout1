import os
from flask import Flask, request, render_template, redirect, url_for, jsonify, g, session
from models.user import User
from models.post import Post
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import storage
from dynamic.v1.views import app_views
from dotenv import load_dotenv
from werkzeug.exceptions import NotFound
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

# Get the absolute path to the project directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Set the upload folder path
UPLOAD_FOLDER = os.path.join(basedir, 'uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Set a secret key for session management
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key_here')

# Allow CORS for all domains
CORS(app, resources={r"/*": {"origins": "*"}})

# Register blueprint once
if not app.blueprints.get('app_views'):
    app.register_blueprint(app_views)

# Database setup
db = "sqlite:///footDB.db"
engine = create_engine(db, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
session_db = Session()

@app.before_request
def load_user():
    user_id = get_current_user_id()  # Function to get the current user ID
    if user_id:
        user = storage.get(User, user_id)
        if user:
            g.user_content = user.to_dict()
        else:
            g.user_content = {}
    else:
        g.user_content = {}

def get_current_user_id():
    """Get the current user ID from the session."""
    return session.get('user_id')

@app.teardown_appcontext
def teardown_db(exception):
    """Close storage session"""
    storage.close()

# Custom 404 error handler
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

# Sample route to demonstrate 404 handling
@app.route('/dynamic/v1/sample')
def sample_route():
    # Example route
    return jsonify({"message": "This is a sample route"}), 200

# Route for redirecting the root URL to the login page
@app.route('/')
def index():
   return redirect(url_for('login_page'))

# Route for rendering the login page
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Route for handling the login form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Authentication logic, such as checking the database for the user
    user = session_db.query(User).filter_by(email=username).first()
    if user and user.password == password:  # Placeholder logic, add google auth api and password hashing comparison later
        session['user_id'] = user.id  # Store user ID in session
        return redirect(url_for('homepage', username=user.first_name))
    else:
        return 'Login Failed', 401

# Route for rendering the homepage after login
@app.route('/homepage')
def homepage():
    username = request.args.get('username')
    user = session_db.query(User).filter_by(first_name=username).first()
    if not user:
        # handle the case where user is not found
        return 'User not found', 404
    content = {
        "id": user.id,
        "username": username,
        "notifications": ["Notification 1", "Notification 2", "Notification 3"],
        "lists": ["List 1", "List 2", "List 3"],
        "reports": ["Report 1", "Report 2", "Report 3"]
    }
    return render_template('homepage.html', content=content)

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
    session_db.add(new_user)
    session_db.commit()

    # Fetch the newly created user to get their details
    user = session_db.query(User).filter_by(email=email).first()

    return redirect(url_for('homepage', username=user.first_name))

# Route to render the static post.html template
@app.route('/test_post')
def test_post():
    username = request.args.get('username')
    content = {
        "username": username,
        "notifications": ["Notification 1", "Notification 2", "Notification 3"],
        "lists": ["List 1", "List 2", "List 3"],
        "reports": ["Report 1", "Report 2", "Report 3"]
    }
    return render_template('post.html', content=content)

# Route for rendering the addpost.html template
@app.route('/addpost', methods=['GET'])
def add_post_page():
    content = {
        "username": "default_user",
    }
    return render_template('addpost.html', content=content)

# Route for handling the add post form submission
@app.route('/addpost', methods=['POST'])
def add_post():
    # Extract post data from form
    title = request.form.get('title')
    content = request.form.get('content')
    return redirect(url_for('test_post'))  # Redirect to a test route or homepage

# Route for rendering the comment.html template
@app.route('/comment')
def comment_page():
    # Example data for testing purposes
    comments = [
        {"username": "John Doe", "comment": "Great post!"},
        {"username": "Jane Smith", "comment": "Nice job!"},
    ]
    return render_template('comment.html', comments=comments)

# Route for handling home icon click, redirects to the homepage
@app.route('/home_icon/<user_id>', methods=['GET'])
def home_icon(user_id):
    # Fetch user data based on user_id
    user_data = session_db.query(User).filter_by(id=user_id).first()

    if user_data:
        content = {
            "username": user_data.first_name,
            "profile_picture": user_data.profile_picture,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "email": user_data.email,
            "id": user_data.id
        }
    return redirect(url_for('homepage', username=user_data.first_name))

# Route for handling create icon click, redirects to the addpost page
@app.route('/create_icon')
def create_icon():
    return redirect(url_for('add_post_page'))

# Route for handling comment icon click, redirects to the comment page
@app.route('/comment_icon')
def comment_icon():
    return redirect(url_for('comment_page'))

if __name__ == "__main__":
    host = os.getenv('FOOTBALL_SCOUT_API_HOST', '0.0.0.0')
    port = int(os.getenv('FOOTBALL_SCOUT_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True, debug=True)

