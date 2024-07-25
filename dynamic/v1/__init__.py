import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

# Database setup
# db = "sqlite:///footDB.db"
# engine = create_engine(db, pool_pre_ping=True)

# Database setup
# engine = create_engine('mysql+mysqlconnector://football_scout_dev:football_scout_dev_pwd@localhost/football_scout_dev_db')

# Extract the PostgreSQL connection details from environment variables
user = os.getenv('FOOTBALL_SCOUT_DEV_PGSQL_USER', 'football_scout_dev')
password = os.getenv('FOOTBALL_SCOUT_DEV_PGSQL_PWD', '8i0QuEi2hDvNDyUgmQpBY0tA2ztryywF')
host = os.getenv('FOOTBALL_SCOUT_DEV_PGSQL_HOST', 'dpg-cqarnd08fa8c73asb9h0-a.oregon-postgres.render.com')
database = os.getenv('FOOTBALL_SCOUT_DEV_PGSQL_DB', 'football_scout_dev_db')

# Create the engine using the PostgreSQL connection string
DATABASE_URL = f'postgresql://{user}:{password}@{host}/{database}'
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

