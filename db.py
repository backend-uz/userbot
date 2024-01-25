from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

database_url = 'sqlite:///database.db'
engine = create_engine(database_url)
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_last_name = Column(String(300))
    username = Column(String(255))
    chat_id = Column(Integer)
    lang = Column(String(3))
    
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def add_user(fname, lname, username, chat_id):
    session = Session()
    flname = ''
    flname += f'{fname} {lname}'
    new_user = User(first_last_name=flname, username=username, chat_id=chat_id)
    session.add(new_user)
    session.commit()
    session.close()
