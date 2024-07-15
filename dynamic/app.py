from flask import Flask, request, render_template, redirect, url_for
from models.user import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)

# Database setup
engine = create_engine('mysql+mysqlconnector://football_scout_dev:football_scout_dev_pwd@localhost/football_scout_dev_db')
Session = sessionmaker(bind=engine)
session = Session()

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
    user = session.query(User).filter_by(email=username).first()
    if user and user.password == password:  # Placeholder logic, add password hashing comparison
        return redirect(url_for('homepage', username=user.first_name))
    else:
        return 'Login Failed', 401

# Route for rendering the homepage after login
@app.route('/homepage')
def homepage():
    username = request.args.get('username')
    content = {
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
    session.add(new_user)
    session.commit()

    return redirect(url_for('login_page'))

# Route for testing the post.html template with dynamic data
@app.route('/test_post')
def test_post():
    # Example data for testing purposes
    posts = [
        {"username": "John Doe", "position": "DMF", "club": "Atalanta United", "location": "South Africa",
         "content": "Lorem ipsum dolor sit, amet consectetur adipisicing elit."},
        {"username": "Jane Smith", "position": "GK", "club": "Real Madrid", "location": "Spain",
         "content": "Dolores dolorum eum numquam magni qui at facere nihil voluptates sunt commodi."}
    ]
    return render_template('post.html', posts=posts)

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

    # Process the post data (e.g., save to database, etc.)
    # Placeholder code
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
@app.route('/home_icon')
def home_icon():
    username = request.args.get('username')
    return redirect(url_for('homepage', username=username))

# Route for handling create icon click, redirects to the addpost page
@app.route('/create_icon')
def create_icon():
    return redirect(url_for('add_post_page'))

# Route for handling comment icon click, redirects to the comment page
@app.route('/comment_icon')
def comment_icon():
    return redirect(url_for('comment_page'))

if __name__ == '__main__':
    app.run(debug=True)

