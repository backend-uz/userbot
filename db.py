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
    
    
class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    chat_id = chat_id = Column(Integer)
    belongto = Column(String(300))
    filepath = Column(String(100))
    caption = Column(String())
    postedtime = Column(String(50))
    exptime = Column(String(50))
    edit = Column(Boolean())
    
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
    
    
def add_task(chat_id, belongto, filepath, caption, postedtime, exptime, edit):
    session = Session()
    new_task = Tasks(chat_id=chat_id, belongto=belongto, filepath=filepath, caption=caption, postedtime=postedtime, exptime=exptime, edit=edit)
    session.add(new_task)
    session.commit()
    added_id = new_task.id
    session.close()
    return added_id