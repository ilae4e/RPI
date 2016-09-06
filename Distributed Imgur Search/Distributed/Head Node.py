import Queue
import json
import socket
import threading

import imgurpython
from imgurpython.helpers.error import ImgurClientError
import time

stop = False
kill = False
Search = set()
LinkList = Queue.Queue()


class Command_Line_Control(object):
    pass


class Email_Control_Actions(object):
    pass


class Crawl(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.client_id = "5dc03917c314aea"
        self.client_secret = "819a0497278a78f8032b4cc69fb03dcbe2b6d3a0"

    def run(self):
        global LinkList
        global stop
        global kill

        page = 0
        client = imgurpython.ImgurClient(self.client_id, self.client_secret)
        while not kill:
            if stop:
                time.sleep(10)
            else:
                while LinkList.empty():
                    try:
                        print "[*] Adding to queue from page:", str(page)
                        content = client.gallery(section="user", sort="time", page=page, window="day", show_viral=False)
                        for contents in content:
                            LinkList.put(contents.link)
                        page += 1
                        print "next page"
                    except ImgurClientError as e:
                        stop = True
                        exit(e)
        else:
            quit("Quiting")


class Client_handler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", 9977))
        self.sock.setblocking(False)

    def run(self):
        global LinkList
        global stop
        global kill
        while not kill:
            try:
                if stop:
                    time.sleep(10)

                self.sock.settimeout(5)
                data, address = self.sock.recvfrom(1024)  # recieve data
                if data:  # if data is true check the values inside data after loading it from json
                    data = json.loads(data)

                    if data[0] == "DATA":
                        self.recieve_data(data)
                        self.send_urls(address)

                    elif data[0] == "URLS":
                        self.send_urls(address)

                    else:
                        print "Unknown Data"
                else:
                    print "No Data to read"
            except socket.error as e:
                if e[0] == "timed out":
                    pass
                else:
                    print "Stopping"
                    stop = True
        else:
            quit("Quiting")

    def recieve_data(self, data):
        global stop
        if stop:
            pass
        else:
            for each in data[1]:
                if each["data"] in Search:
                    print "Image found: {}".format(each["data"])

    def send_urls(self, addr):
        global stop
        if stop:
            pass
        else:
            urls = []
            for x in range(0, 10):
                if LinkList.empty():
                    time.sleep(5)
                    print "sleeping"
                urls.append(LinkList.get())
            self.sock.sendto(json.dumps(urls), addr)

if __name__=="__main__":
    Client_Handler = Client_handler()
    Data_Gatherer = Crawl()
    Client_Handler.start()
    Data_Gatherer.start()
    Data_Gatherer.join()
    Client_Handler.join()

