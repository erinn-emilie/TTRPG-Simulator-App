import bcrypt
import urllib
from enum import Enum

from sqlalchemy import create_engine, Column, Integer, String, select, ForeignKey, LargeBinary
from sqlalchemy.orm import declarative_base, sessionmaker


from PIL import Image  
import io  

from Enums.TokenTypes import TokenTypes
 


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

class Tokens(Base):
    __tablename__ = "Tokens"
    token_id = Column(Integer, primary_key=True)
    fk_user_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False)
    user_token_key = Column(Integer, nullable=False)
    token_name = Column(String(200), nullable=False)
    token_type = Column(String(20), nullable=False)
    json_small_fields = Column(String(), nullable=False)
    json_large_fields = Column(String(), nullable=False)
    img_1 = Column(LargeBinary, nullable=True)
    img_2 = Column(LargeBinary, nullable=True)
    img_3 = Column(LargeBinary, nullable=True)
    img_4 = Column(LargeBinary, nullable=True)
    img_5 = Column(LargeBinary, nullable=True)
    map_asset = Column(LargeBinary, nullable=True)

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
    def compress_image(image_path, quality=85):  
        with Image.open(image_path) as img:  
            if img.mode in ("RGBA", "P"):  
                img = img.convert("RGB")  
            img_byte_arr = io.BytesIO()  
            img.save(img_byte_arr, format="PNG", quality=quality) 
            return img_byte_arr.getvalue() 

    def add_new_token(user_id:int, user_token_key:int, token_name:str, token_type:TokenTypes, json_small_fields:dict, json_large_fields:dict, map_asset="", images=[]):
        with SessionLocal() as session:
            new_token = Tokens(
                fk_user_id=user_id,
                user_token_key=user_token_key,
                token_name=token_name,
                token_type=TokenTypes.get_str_from_token_type(token_type),
                json_small_fields=str(json_small_fields),
                json_large_fields=str(json_large_fields)
            )
            session.add(new_token)
            session.commit()
            if(map_asset != ""):
                new_token.map_asset = map_asset
            for idx, img in images:
                compressed = Database.compress_image(img)
                match(idx):
                    case 1:
                        new_token.img_1 = compressed
                    case 2:
                        new_token.img_2 = compressed
                    case 3:
                        new_token.img_3 = compressed
                    case 4:
                        new_token.img_4 = compressed
                    case 5: 
                        new_token.img_5 = compressed
            session.commit()


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