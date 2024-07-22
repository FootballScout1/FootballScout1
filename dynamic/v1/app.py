import logging
import os
from flask import Flask, request, render_template, abort, redirect, url_for, jsonify, g, session
from models.user import User
from models.post import Post
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import storage
from dynamic.v1.views import app_views, get_comment
from dotenv import load_dotenv
from werkzeug.exceptions import NotFound
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import uuid
from dynamic.lazydict import update_obj_dict

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

# Get the absolute path to the project directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Set the upload folder path
UPLOAD_FOLDER = os.path.join(basedir, 'uploads')

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Set a secret key for session management
app.secret_key = os.getenv('SECRET_KEY', 'later')

# Allow CORS for all domains
CORS(app, resources={r"/*": {"origins": "*"}})

# Register blueprint once
if not app.blueprints.get('app_views'):
    app.register_blueprint(app_views)

# Database setup
# db = "sqlite:///footDB.db"
# engine = create_engine(db, pool_pre_ping=True)

# Database setup
# engine = create_engine('mysql+mysqlconnector://football_scout_dev:football_scout_dev_pwd@localhost/football_scout_dev_db')

# Database setup
# Extract the PostgreSQL connection details from environment variables
user = os.getenv('FOOTBALL_SCOUT_DEV_PGSQL_USER', 'football_scout_dev')
password = os.getenv('FOOTBALL_SCOUT_DEV_PGSQL_PWD', '8i0QuEi2hDvNDyUgmQpBY0tA2ztryywF')
host = os.getenv('FOOTBALL_SCOUT_DEV_PGSQL_HOST', 'dpg-cqarnd08fa8c73asb9h0-a.oregon-postgres.render.com')
database = os.getenv('FOOTBALL_SCOUT_DEV_PGSQL_DB', 'football_scout_dev_db')

# Create the engine using the PostgreSQL connection string
DATABASE_URL = f'postgresql://{user}:{password}@{host}/{database}'
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session_db = Session()


PRIMARY_USER_ID = 'db392ac7-72e1-4e14-9eef-60c50e086310'
SECONDARY_USER_ID = 'f17ae849-dc33-416e-8fd9-8e5bc554a664'

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

def get_available_user_id():
    # Check the availability of PRIMARY_USER_ID and fallback to SECONDARY_USER_ID if necessary
    return PRIMARY_USER_ID if PRIMARY_USER_ID else SECONDARY_USER_ID

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
    user_id = user_id = get_available_user_id()
    return redirect(url_for('home_icon', user_id=user_id, cache_id=uuid.uuid4()))

# Route for rendering the login page
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html', cache_id=uuid.uuid4())

# Route for handling the login form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Authentication logic, such as checking the database for the user
    user = session_db.query(User).filter_by(email=username).first()
    if user and user.password == password:  # Placeholder logic, add google auth api and password hashing comparison later
        session['user_id'] = user.id  # Store user ID in session
        return redirect(url_for('homepage', username=user.first_name, cache_id=uuid.uuid4()))
    else:
        return 'Login Failed', 401

# Route for rendering the default homepage without login (root)
@app.route('/homepage_default')
def homepage_default():
    user_id = get_available_user_id()
    content = {
                "id": user_id,
                "username": "Guest",
                "profile_picture": url_for('static', filename='images/soccer-stadium-full-people.jpg'),
                "notifications": [],
                "lists": [],
                "reports": []
            }
    return render_template('homepage.html', user_id=content['id'], cache_id=uuid.uuid4())

# Route for rendering the homepage after login
@app.route('/homepage')
def homepage():
    """
    Renders the homepage
    """
    username = request.args.get('username')

    logger.debug(f"Fetching user with username: {username}")

    if username:
        user = session_db.query(User).filter_by(first_name=username).first()
        if user:
            content = {
                "id": user.id,
                "username": username,
                "profile_picture": user.profile_picture,
                "notifications": ["Notification 1", "Notification 2", "Notification 3"],
                "lists": ["List 1", "List 2", "List 3"],
                "reports": ["Report 1", "Report 2", "Report 3"],
            }
        else:
            logger.error(f"User with username '{username}' not found, using default content")
            user_id = get_available_user_id()
            content = {
                "id": user_id,
                "username": "Guest",
                "profile_picture": url_for('static', filename='images/soccer-stadium-full-people.jpg'),
                "notifications": [],
                "lists": [],
                "reports": []
            }
            return redirect(url_for('home_icon', user_id=content['id'], cache_id=uuid.uuid4()))
    else:
        logger.debug("No username provided, using default content")
        user_id = get_available_user_id()
        content = {
            "id": user_id,
            "username": "Guest",
            "profile_picture": url_for('static', filename='images/soccer-stadium-full-people.jpg'),
            "notifications": [],
            "lists": [],
            "reports": []
        }
        return redirect(url_for('home_icon', user_id=content['id'], cache_id=uuid.uuid4()))
    try:
        logger.debug("Fetching all posts")
        all_posts = list(storage.all(Post).values())
        all_posts_info = list()
        for post in all_posts:
            post_dict = post.to_dict()
            update_obj_dict(post, post_dict)
            post_dict.update({
                'comments_count': len(post.comments),
                'likes_count': len(post.likes)
            })
            all_posts_info.append(post_dict)

        logger.debug(f"Rendering homepage with {len(all_posts_info)} posts")
        return render_template('homepage.html', posts=all_posts_info[95:105], content=content, cache_id=uuid.uuid4())

    except Exception as e:
        logger.exception("An error occurred while rendering the homepage")
        return 'An internal error occurred', 500

# Route for rendering the registration page
@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html', cache_id=uuid.uuid4())

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

    return redirect(url_for('homepage', username=user.first_name, cache_id=uuid.uuid4()))

# Route to render the static post.html template
@app.route('/test_post/<user_id>/<post_id>')
def test_post(user_id, post_id):

    # Fetch user data based on user_id
    user = storage.get(User, user_id)
    post = storage.get(Post, post_id)
    if not user or not post:
        return "User or Post not found", 404

    return render_template('post.html', user_id=user_id, post_id=post_id, cache_id=uuid.uuid4())

# Route for rendering the addpost.html template
@app.route('/addpost/<user_id>', methods=['GET'])
def add_post_page(user_id):

    user = storage.get(User, user_id)
    if not user:
        return "User not found", 404
    return render_template('addpost.html', user_id=user_id, content=user.to_dict(), cache_id=uuid.uuid4())

# Route for handling the add post form submission
@app.route('/addpost/<user_id>', methods=['POST'])
def add_post(user_id):

    user = storage.get(User, user_id)
    if not user:
        return "User not found", 404
    return redirect(url_for('test_post', user_id=user_id, content=user.to_dict(), cache_id=uuid.uuid4()))  # Redirect to the posts page

# Route for rendering the comment.html template
@app.route('/comment/<user_id>/<post_id>')
def comment_page(user_id, post_id):

    # Fetch user data based on user_id
    user = storage.get(User, user_id)
    post = storage.get(Post, post_id)
    if not user or not post:
        return "User or Post not found", 404

    return render_template('comment.html', user_id=user_id, post_id=post_id, content=user.to_dict(), cache_id=uuid.uuid4())

# Route for handling home icon click, redirects to the homepage
@app.route('/home_icon/<user_id>', methods=['GET'])
def home_icon(user_id):
    # Fetch user data based on user_id
    user_data = session_db.query(User).filter_by(id=user_id).first()
    # cache_id = uuid.uuid4()
    if user_data:
        content = {
            "username": user_data.first_name,
            "profile_picture": user_data.profile_picture,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "email": user_data.email,
            "id": user_data.id
        }
    return redirect(url_for('homepage', username=user_data.first_name, cache_id=uuid.uuid4()))

# Route for handling create icon click, redirects to the addpost page
@app.route('/create_icon/<user_id>')
def create_icon(user_id):
    
    user = storage.get(User, user_id)
    if not user:
        return "User not found", 404
    return redirect(url_for('add_post_page', user_id=user_id, content=user.to_dict(), cache_id=uuid.uuid4()))  # Redirect to the addpost page

# Route for handling comment icon click, redirects to the comment page
@app.route('/comment_icon/<user_id>/<post_id>')
def comment_icon(user_id, post_id):

    user = storage.get(User, user_id)
    post = storage.get(Post, post_id)
    if not user or not post:
        return "User or Post not found", 404
    return render_template('comment.html', user_id=user_id, post_id=post_id, content=user.to_dict(), cache_id=uuid.uuid4())

if __name__ == "__main__":
    host = os.getenv('FOOTBALL_SCOUT_API_HOST', '0.0.0.0')
    port = int(os.getenv('FOOTBALL_SCOUT_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True, debug=True)

