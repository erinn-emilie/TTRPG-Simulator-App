import bcrypt
import urllib
from enum import Enum

from sqlalchemy import create_engine, Column, Integer, String, select, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker


driver = "ODBC Driver 17 for SQL Server"  
server = r"localhost\SQLEXPRESS"      
database = "TTRPGDB"

params = urllib.parse.quote_plus(
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()

class Hosts(Base):
    __tablename__ = "Hosts"
    connection_id = Column(Integer, primary_key=True)
    hostname = Column(String(100), nullable=False)
    fk_user_id = Column(Integer, nullable=False)
    password = Column(String(60), nullable=False)
    port = Column(Integer, nullable=False)

class Users(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(60), nullable=False)
    email = Column(String(100), nullable=False)

class DatabaseMessages(Enum):
    NONE = -1
    SUCCESS = 0
    EXISTING_USER = 1
    EXISTING_EMAIL = 2
    CRITICAL_ERROR = 3
    INVAL_CREDS = 4

class Database:
    def add_host_info_to_db(hostname:str, user_id:int, password:str, port:int):
        with SessionLocal() as session:
            new_host = Hosts(
                hostname=hostname,
                fk_user_id=user_id,
                password=password,
                port=port
            )
            session.add(new_host)
            session.commit()

    def create_new_user(username:str, email:str, password:str) -> DatabaseMessages:
        msg = DatabaseMessages.NONE
        pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        try:
            with SessionLocal() as session:
                existing_user = session.execute(
                    select(Users).where(Users.username == username)
                ).scalar_one_or_none()
                if existing_user:
                    msg = DatabaseMessages.EXISTING_USER, -1

                existing_email = session.execute(
                    select(Users).where(Users.email == email)
                ).scalar_one_or_none()
                if existing_email:
                    msg = DatabaseMessages.EXISTING_EMAIL, -1

                session.add(Users(username=username, email=email, password=pw_hash))
                session.commit()
                return Database.check_user(username, password)
            return msg
        except Exception as e:
            msg = DatabaseMessages.CRITICAL_ERROR
            return msg, -1


    def check_user(username:str, password:str):
        msg = DatabaseMessages.NONE
        try:
            with SessionLocal() as session:
                user = session.execute(
                    select(Users).where(Users.username == username)
                ).scalar_one_or_none()

                if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                    msg = DatabaseMessages.SUCCESS
                    return msg, user.user_id
                else:
                    msg = DatabaseMessages.INVAL_CREDS
                    return msg, -1
        except Exception as e:
            msg = DatabaseMessages.CRITICAL_ERROR
            return msg, -1