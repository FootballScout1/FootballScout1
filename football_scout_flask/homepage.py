from flask import Flask, render_template
from models.user import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)

# Database setup
engine = create_engine('mysql+mysqlconnector://football_scout_dev:football_scout_dev_pwd@localhost/football_scout_dev_db')
Session = sessionmaker(bind=engine)
db_session = Session()

@app.route('/')
def homepage():
    # Sample dynamic data
    user = db_session.query(User).first()
    dynamic_content = {
        'username': user.first_name + ' ' + user.last_name,
        'notifications': ['Notification 1', 'Notification 2', 'Notification 3'],
        'lists': ['List 1', 'List 2', 'List 3'],
        'reports': ['Report 1', 'Report 2', 'Report 3'],
    }
    return render_template('homepage_update.html', content=dynamic_content)

if __name__ == '__main__':
    app.run(debug=True)

