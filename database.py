from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

# Get the absolute path of the current directory
current_dir = os.path.abspath(os.path.dirname(__file__))

# Define the relative path to the database file
relative_db_path = "mydatabase/user.db"

# Create the SQLite URL using the relative path
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(current_dir, relative_db_path)}"



engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
