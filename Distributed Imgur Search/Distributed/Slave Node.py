import socket
import json
from pprint import pprint


class Node:
    def __init__(self):
        pass

    def find_server(self):
        pass

    def get_url(self):
        pass

    def main(self):
        pass


class test:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("127.0.0.1", 9988))
        self.sock.setblocking(0)
        self.sock.settimeout(5)
        self.urls = []


        request = ["URLS",{"None":"None"}]
        z = json.dumps(request)
        self.sock.sendto(z, ("127.0.0.1", 9977))
        self.urls.append(self.sock.recv(1024))
        pprint(self.urls)


x = test()
