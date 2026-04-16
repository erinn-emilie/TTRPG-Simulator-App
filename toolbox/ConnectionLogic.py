
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
import time

import bcrypt

from enum import Enum
import re
from urllib.request import urlopen

import ipaddress



from queue import Queue

from toolbox.Database import Database, DatabaseMessages


class SessionMessages(Enum):
    REQ_JOIN = "request to join"
    INIT_MAP_INFO = "initalize map information"

class MessageQueue():
    def __init__(self, conn, address):
        self.conn = conn
        self.address = address
        self.messages = Queue()

    def get_conn(self):
        return self.conn

    def get_address(self):
        return self.address

    def get_next_message(self):
        if(not self.messages.empty()):
            return self.messages.get()
        return None

    def add_message(self, msg):
        self.messages.put(msg)

class Session():
    def __init__(self, acc_ref, saved_maps_ref, hextile_map_ref, live=False, host=False):
        self.live = live
        self.host = host

        self.messages = []


        self.acc_ref = acc_ref
        self.saved_maps_ref = saved_maps_ref
        self.hextile_map_ref = hextile_map_ref

    def get_live_status(self) -> bool:
        return self.live

    def get_host_status(self) -> bool:
        return self.host

    def end_session(self):
        self.live = False
        self.host = False

    def watch_queue(self, message_ref):
        while True:
            message = message_ref.get_next_message()
            if(not message is None):
                conn = message_ref.get_conn()
                conn.send(message).encode("utf-8")
            time.sleep(10)


    def handle_client_as_host(self, conn, addr):
        data = conn.recv(1024).decode("utf-8")
        if(data == SessionMessages.REQ_JOIN):
            print("joined")
            new_queue = MessageQueue(conn, addr)
            new_queue.put(SessionMessages.INIT_MAP_INFO.value)
            new_queue.put(str(self.saved_maps_ref.get_active_save_dict()))
            self.messages.append(new_queue)
            threading.Thread(target=self.watch_queue, args=(new_queue, )).start()



    def listen_for_client_as_host(self, sock):
        while True:
            conn, addr = sock.accept()
            threading.Thread(target=self.handle_client_as_host, args=(conn, addr, )).start()

    def wait_for_host_updates(self, sock):
        init_map_info = False
        sock.send(SessionMessages.REQ_JOIN.value.encode("utf-8"))
        while True:
            data = sock.recv(1024).decode("utf-8")
            if(init_map_info):
                init_map_info = False
                self.saved_maps_ref.set_active_save_dict(eval(data))
                self.saved_maps_ref.set_active_save_name("Session Map")
                self.hextile_map_ref.loadSavedMap("Session Map", active_save_dict=True)
            if(data == SessionMessages.INIT_MAP_INFO):
                init_map_info = True
            time.sleep(5)

    
    def get_private_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address



    def start_session_as_host(self, port=80):
        self.live = True
        self.host = True

        account_id = self.acc_ref.get_account_id()
        if(account_id != -1):
            random.seed()

            ip_address_private = self.get_private_ip()
            data = str(urlopen('http://checkip.dyndns.com/').read())
            ip_address_public = re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("0.0.0.0",port))
            pswd = str(random.randint(10**5, 10**6 - 1))
            pswd_hash = bcrypt.hashpw(pswd.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            Database.add_host_info_to_db(str(ip_address_public), str(ip_address_private), account_id, pswd_hash, port)


            sock.listen(5)
            threading.Thread(target=self.listen_for_client_as_host, args=(sock, )).start()
        return pswd

    def same_network(self, ip1, ip2, subnet_mask="255.255.255.0"):
        try:
            network = ipaddress.ip_network(f"{ip1}/{subnet_mask}", strict=False)
            return ipaddress.ip_address(ip2) in network
        except:
            return False

    def join_session_as_client(self, username, password):
        self.live = True
        account_id = self.acc_ref.get_account_id()
        if(account_id != -1):
            msg, ip_address, port, private_ip = Database.get_host_info(username, password)
            if(msg == DatabaseMessages.SUCCESS):
                my_ip = self.get_private_ip()
                if(self.same_network(my_ip, private_ip)):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((private_ip, port))

                    threading.Thread(target=self.wait_for_host_updates, args=(sock, )).start()
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((ip_address, port))

                    threading.Thread(target=self.wait_for_host_updates, args=(sock, )).start()