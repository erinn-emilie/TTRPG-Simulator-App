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
    fk_user_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False)
    password = Column(String(60), nullable=False)
    port = Column(Integer, nullable=False)

class Users(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(60), nullable=False)
    email = Column(String(100), nullable=False)

class Maps(Base):
    __tablename__ = "Maps"
    map_id = Column(Integer, primary_key=True)
    fk_user_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False)
    map_name = Column(String(100), nullable=False)
    map_dict = Column(String(), nullable=False)

class DatabaseMessages(Enum):
    NONE = -1
    SUCCESS = 0
    EXISTING_USER = 1
    EXISTING_EMAIL = 2
    CRITICAL_ERROR = 3
    INVAL_CREDS = 4
    EXISTING_MAP = 5
    NO_SESSION_FOUND = 6

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

    def get_host_info(username:str, password:str):
        msg = DatabaseMessages.NONE
        try:
            with SessionLocal() as session:
                user = session.execute(
                    select(Users).where(Users.username == username)
                ).scalar_one_or_none()
                if(user):
                    info = session.execute(
                        select(Hosts).where(Hosts.fk_user_id == user.user_id)
                    ).scalar_one_or_none()
                    if(info):
                        if(bcrypt.checkpw(password.encode("utf-8"), info.password.encode("utf-8"))):
                            msg = DatabaseMessages.SUCCESS
                            return msg, session.hostname, session.port
                        else:
                            msg = DatabaseMessages.NO_SESSION_FOUND
                    else:
                        msg = DatabaseMessages.NO_SESSION_FOUND
                else:
                    msg = DatabaseMessages.NO_SESSION_FOUND
            return msg, "", ""
        except Exception as e:
            msg = DatabaseMessages.CRITICAL_ERROR
            return msg, "", ""



    def add_map_to_db(user_id:int, map_name:str, map_dict:dict):
        msg = DatabaseMessages.NONE
        try:
            with SessionLocal() as session:
                existing_map = session.execute(
                    select(Maps).where(Maps.map_name == map_name)
                ).scalar_one_or_none()
                if existing_map:
                    msg = DatabaseMessages.EXISTING_MAP
                else:
                    new_map = Maps(
                        map_name=map_name,
                        fk_user_id=user_id,
                        map_dict=str(map_dict)
                    )
                    session.add(new_map)
                    session.commit()
                    msg = DatabaseMessages.SUCCESS
            return msg
        except Exception as e:
            msg = DatabaseMessages.CRITICAL_ERROR
            return msg

    def create_new_user(username:str, email:str, password:str) -> DatabaseMessages:
        msg = DatabaseMessages.NONE
        pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        try:
            with SessionLocal() as session:
                existing_user = session.execute(
                    select(Users).where(Users.username == username)
                ).scalar_one_or_none()
                if existing_user:
                    msg = DatabaseMessages.EXISTING_USER

                existing_email = session.execute(
                    select(Users).where(Users.email == email)
                ).scalar_one_or_none()
                if existing_email:
                    msg = DatabaseMessages.EXISTING_EMAIL

                session.add(Users(username=username, email=email, password=pw_hash))
                session.commit()
                return Database.check_user(username, password)
            return msg, -1
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