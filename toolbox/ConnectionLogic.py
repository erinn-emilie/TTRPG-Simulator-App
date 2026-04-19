
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



class SessionMessages(Enum):
    REQUEST_JOIN = "REQUEST JOIN"
    TERMINATE_CONNECTION = "TERMINATE CONNECTION"


class ClientSession:
    def __init__(self, account_ref):
        self.account_ref = account_ref
        self.sock = None
        self.live = False


    def get_private_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address

    def same_network(self, ip1, ip2, subnet_mask="255.255.255.0"):
        try:
            network = ipaddress.ip_network(f"{ip1}/{subnet_mask}", strict=False)
            return ipaddress.ip_address(ip2) in network
        except:
            return False

    def connect_to_host(self, username, password, port=80):
        self.live = True
        account_id = self.acc_ref.get_account_id()
        if(account_id != -1):
            msg, ip_address, port, private_ip = Database.get_host_info(username, password)
            if(msg == DatabaseMessages.SUCCESS):
                my_ip = self.get_private_ip()
                if(self.same_network(my_ip, private_ip)):
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.connect((private_ip, port))
                else:
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.connect((ip_address, port))   
                self.sock.sendall(SessionMessages.REQUEST_JOIN.value)
                threading.Thread(self.listen_to_host).start()

    def listen_to_host(self):
        buffer = b""
        while True:
            chunk = self.sock.recv(4096)
            while(b"\n" in buffer):
                line, buffer = buffer.split(b"\n", 1)
                msg = line.decode().strip()
                self.handle_message(msg)

    def handle_message(self, msg):
        if(msg == SessionMessages.TERMINATE_CONNECTION):
            self.sock.close()
            self.live = False

class ServerSession():
    def __init__(self, account_ref):
        self.account_ref = account_ref
        self.sock = None
        self.live = False

    def start_session(self, port=80):
        self.live = True
        account_id = self.account_ref.get_account_id()
        if(account_id != -1):
            random.seed()

            ip_address_private = self.get_private_ip()
            data = str(urlopen('http://checkip.dyndns.com/').read())
            ip_address_public = re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(("0.0.0.0",port))
            pswd = str(random.randint(10**5, 10**6 - 1))
            pswd_hash = bcrypt.hashpw(pswd.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            Database.add_host_info_to_db(str(ip_address_public), str(ip_address_private), account_id, pswd_hash, port)

            self.sock.listen(5)
            threading.Thread(self.listen_for_client).start()
        return pswd

    def listen_for_client(self):
        while True:
            conn, addr = self.sock.accept()
            print(f"Connected by {addr}")

