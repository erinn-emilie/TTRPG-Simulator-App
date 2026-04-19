
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


from enum import Enum
import random
import threading
from urllib.request import urlopen
import re
import socket
import bcrypt
from toolbox.Database import Database
from toolbox.Database import DatabaseMessages
import ipaddress
import base64
import miniupnpc
from queue import Queue



class SessionMessages(Enum):
    TERMINATE_CONNECTION = "TERMINATE CONNECTION"
    INIT_MAP = "INIT MAP"
    MAP_FIN = "MAP FIN"


class ClientSession:
    def __init__(self, account_ref, saved_maps_ref, hextile_map_ref):
        self.account_ref = account_ref
        self.saved_maps_ref = saved_maps_ref
        self.hextile_map_ref = hextile_map_ref
        self.home_window = None
        self.reading_map_dict = False
        self.map_dict_str = ""
        self.sock = None
        self.live = False

    def set_home_window(self, home_window):
        self.home_window = home_window

    def connect_to_host(self, username, password, port=80):
        self.live = True
        account_id = self.account_ref.get_account_id()
        if(account_id != -1):
            msg, ip_address, port, private_ip = Database.get_host_info(username, password)
            if(msg == DatabaseMessages.SUCCESS):
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((ip_address, port))   
                threading.Thread(target=self.listen_to_host).start()

    def listen_to_host(self):
        msg = b""
        while True:
            bmsg = self.sock.recv(4096)
            msg = bmsg.decode().strip()
            self.handle_message(msg)

    def handle_message(self, msg):
        print(msg)
        if(msg == SessionMessages.TERMINATE_CONNECTION.value):
            self.sock.close()
            self.live = False
        elif(msg == SessionMessages.INIT_MAP.value):
            self.reading_map_dict = True
        elif(self.reading_map_dict):
            self.map_dict_str = self.map_dict_str + msg
        elif(msg == SessionMessages.MAP_FIN):
            self.reading_map_dict = False
            self.map_dict_str = ""
            self.hextile_map_ref.loadSaveFromKey(eval(self.map_dict_str))
            self.home_window.load_save_from_session()



class ServerSession():
    def __init__(self, account_ref, saved_maps_ref, hextile_map_ref):
        self.account_ref = account_ref
        self.saved_maps_ref = saved_maps_ref
        self.hextile_map_ref = hextile_map_ref
        self.sock = None
        self.live = False
        self.messages = []



    def upnp_map(self, ext_port, int_port):
        u = miniupnpc.UPnP()
        u.discoverdelay = 200
        n_devices = u.discover()

        u.selectigd()

        ext_ip = u.externalipaddress()
        int_ip = u.lanaddr

        protocol = "TCP"
        description = "TTRPGSession"

        u.addportmapping(ext_port, protocol, int_ip, int_port, description, '')

        return int_ip, ext_ip


    def start_session(self):
        self.live = True
        account_id = self.account_ref.get_account_id()
        if(account_id != -1):
            random.seed()


            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            pswd = str(random.randint(10**5, 10**6 - 1))
            pswd_hash = bcrypt.hashpw(pswd.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            int_port = 80
            ext_port = 1024
            int_ip, ext_ip = self.upnp_map(ext_port, int_port)
            self.sock.bind(("0.0.0.0",int_port))
            Database.add_host_info_to_db(str(ext_ip), str(int_ip), account_id, pswd_hash, ext_port)

            self.sock.listen(5)
            threading.Thread(target=self.listen_for_client).start()
        return pswd

    def listen_for_client(self):
        while True:
            conn, addr = self.sock.accept()
            print(f"Connected by {addr}")
            new_queue = Queue()
            new_queue.put(SessionMessages.INIT_MAP.value)
            new_queue.put(str(self.saved_maps_ref.get_active_save_dict()))
            new_queue.put(SessionMessages.MAP_FIN.value)
            self.messages.append(new_queue)
            threading.Thread(target=self.watch_queue, args=(conn, new_queue, )).start()

    def watch_queue(self, conn, queue):
        while True:
            if(not queue.empty()):
                msg = bytes(queue.get(), "utf-8")
                conn.sendall(msg)


