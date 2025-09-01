from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column,Integer,String,create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
ENGINE = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=ENGINE)
Base = declarative_base()

print(DATABASE_URL)

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    username = Column(String,index=True)
    hashed_password = Column(String)
    
    
    
Base.metadata.create_all(ENGINE)




