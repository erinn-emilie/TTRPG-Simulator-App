
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

