
# To do any of this accounts shold be logged in
# When someone starts a session we want to create a session object that listens for clients
# The session object should also mark them as the host
# A client should first send a join message, at which point the session object creates a queue of
# messages for them and add an accepted join message to their queue
# It should also add their address and hostname (maybe) to a list to keep track of them
# If a client is already joined and sends a join message something is wrong and idk what id do about it
# When a client goes to join a session its session object should mark it as in a session and not a host (hosts vs not hosts can send diff messages)
# The clients session object should start a thread with a socket that just listens for the hosts updates (so host listens for multiple, client listens for one)

# When a host starts a session it should save their current map as the session map
# When a client connect the hosts should send them a map update message and then send the map information which the client loads


import socket
import threading
import random

import bcrypt

from toolbox.Database import Database

class Session():
    def __init__(self, acc_ref, live=False, host=False):
        self.live = live
        self.host = host

        self.acc_ref = acc_ref

    def get_live_status(self) -> bool:
        return self.live

    def get_host_status(self) -> bool:
        return self.host

    def end_session(self):
        self.live = False
        self.host = False


    def listen_for_client_as_host(sock):
        while True:
            conn, addr = sock.accept()
            print("Connected by " + str(addr))
            #threading.Thread(target=Session.handle_client, args=(conn, str(addr), )).start()


    def start_session_as_host(self, host = "", port="12345"):
        self.live = True
        self.host = True

        account_id = self.acc_ref.get_account_id()
        if(account_id != -1):
            random.seed()
            if(host == ""):
                host = socket.get_hostname()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((host,port))
            pswd = str(random.randint(10**9, 10**10 - 1))
            pswd_hash = bcrypt.hashpw(pswd.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            Database.add_host_info_to_db(host, account_id, pswd_hash, port)


            sock.listen(5)
            threading.Thread(target=Session.listen_for_client_as_host, args=(sock, )).start()


    def join_session_as_client(self):
        self.live = True




"""import socket
import threading
import os
from queue import Queue
import json
import time
import random
import bcrypt
import urllib
from enum import Enum

from sqlalchemy import create_engine, Column, Integer, String, select, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL


driver = "ODBC Driver 17 for SQL Server"  
database = "TTRPGDB"

#engine = create_engine(connection_url, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()

class Hosts(Base):
    __tablename__ = "Hosts"
    connection_id = Column(Integer, primary_key=True)
    hostname = Column(String(100), nullable=False)
    fk_user_id = Column(Integer, nullable=False)
    password = Column(String(60), nullable=False)
    port = Column(Integer, nullable=False)


class Requests(Enum):
    JOIN_SESSION = "Join Session"

class Messages:
    def __init__(self, addr="127.0.0.0"):
        self.addr = addr
        self.message_queue = Queue(maxsize=20)

    def get_addr(self) -> str:
        return self.addr

    def get_next_message(self) -> str:
        return self.message_queue.get()

    def clear_messages(self):
        self.message_queue.clear()

    def add_test_message(self):
        self.message_queue.put("Test Message")


class Server:
    def __init__(self, is_host=False, active=False):
        self.active = active
        self.is_host = is_host
        self.clients = []
        self.messages = []

    def set_active(self):
        self.active = True

    def set_as_host(self):
        self.is_host = True

    def set_inactive(self):
        self.active = False
        self.is_host = False

    def join_client(self, addr)
        self.clients.append(str(addr))
        new_message = Messages(addr=str(addr))
        self.messages.append(new_message)

    def handle_client(conn, addr):
        message = conn.recv(1024).decode('utf-8')
        match(message):
            case Requests.JOIN_SESSION:
                self.join_client(addr)

        print(message)

    def listen_for_client(sock):
        while True:
            conn, addr = sock.accept()
            print("Connected by " + str(addr))
            threading.Thread(target=Server.handle_client, args=(conn, str(addr), )).start()


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

    #def find_host_info(self, password): //should find the host info from the database

    #def request_to_join(password:str):
        #host, port = self.find_host_info(password)
        #Server.send_message(host=host, port=port, message=Requests.JOIN_SESSION)
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock.bind((host, port))

    def start_server(host="", port=12345, account_id=-1):
        account_id = 1
        if host == "":
            host = socket.gethostname()
        random.seed()
        self.set_active()
        self.set_as_host()
        pswd = str(random.randint(10**9, 10**10 - 1))
        pswd_hash = bcrypt.hashpw(pswd.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        Server.add_host_info_to_db(host, account_id, pswd_hash, port)


        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(5)
        threading.Thread(target=Server.listen_for_client, args=(sock, )).start()
        time.sleep(5)
        #Server.send_message(host=host, message = b"HERROOO")

    def send_message(host="Caligula", port=12345, message=b"default"):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.sendall(message)

        sock.close()"""