from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv('DBURL')
db_name = os.getenv('DBNAME')
db_user = os.getenv('DBUSER')
db_password = os.getenv('DBPASSWD')

DATABASE_URL = f'postgresql+psycopg2://{db_user}:{db_password}@{db_url}/{db_name}'
print(DATABASE_URL)

engine = create_engine(DATABASE_URL)
session_local = sessionmaker(bind=engine, autocommit=False, autoflush=False)
db_session = scoped_session(session_local)

def session_factory():
    return session_local()
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()