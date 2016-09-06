import Tkinter
import json
import socket
import time
from threading import Thread

__author__ = '13123935 - Jordan Harman'

data = {}
stop = False


class Server_Search_and_Listen():
    def __init__(self):
        # the address and port to be broadcast on
        self.broadcast_address = ("<broadcast>", 9878)

        #
        self.information_time = 20

        # broadcast duration
        self.broadcast_duration = 15

        # the address and port to be listened on
        self.listening_address = ("", 9789)

        # broadcast message
        self.broadcast_message = "I'm looking for some tasty pi"

        # default sleep time
        self.sleep = 1

        # default timeout length
        self.timeout = 1

        # broadcasts
        self.broadcast_time_difference = 5

        # raspberry data storage
        self.data = {}

        # SOCKETS
        # create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # set socket to broadcast
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # bind socket
        self.sock.bind(self.listening_address)
        # set socket blocking
        self.sock.setblocking(False)
        # set the time out
        self.sock.settimeout(self.timeout)

    def start_broadcasting(self, broadcast_now=True):
        start_time = time.time()
        broadcast_time = time.time()
        end = True
        while broadcast_now or end:
            if stop:
                exit("Time to stop")
            if broadcast_now:
                # send broadcast
                self.sock.sendto(
                    json.dumps(("I'm Looking for some tasty Pi",)), self.broadcast_address)
                # set broadcast_now to false so it doesnt broadcast again until needed
                broadcast_now = False
                # set the last broadcast time
                broadcast_time = time.time()
            else:
                if time.time() - start_time >= self.broadcast_duration:
                    # time to stop broadcasting
                    end = False
                elif time.time() - broadcast_time >= self.broadcast_time_difference:
                    # time to broadcast again
                    broadcast_now = True
                else:
                    # waiting for clients to connect
                    try:
                        message, address = self.sock.recvfrom(1024)
                        if message and address:
                            message = json.loads(message)

                            if isinstance(message, list):
                                if message[0] == "I am here Mr. Server" and address:
                                    print "Client Found: {}".format(address[0])
                                    self.sock.sendto(json.dumps(("Hello Mr. Pi",)), address)
                                    self.data[address[0]] = ""
                                else:
                                    print "\twrong response"
                            else:
                                print "Clients are trying to send wrong data to the server - run the server again in a few minutes"
                                print "\t", message
                    except socket.error:
                        pass

    def start_sending_details(self):
        for each_machine in self.data.iterkeys():
            while True:
                try:
                    self.sock.sendto(json.dumps(("Send Me Your Information", self.information_time)),
                                     (each_machine, 9878))
                    break
                except socket.error:
                    pass

    def receive_details(self):
        global data
        global stop
        while True:
            try:
                message, address = self.sock.recvfrom(1024)
                message = json.loads(message)
                if stop:
                    exit("Time to stop")
                if message and address:
                    if isinstance(message, list):
                        if message[0] == "Server State?":
                            self.sock.sendto(json.dumps(("Yes I am online",)), address)

                    elif isinstance(message, dict):
                        data[address[0]] = {
                            "ip": address[0],
                            "hostname": message["hostname"],
                            "username": message["username"],
                            "temperature": message["temperature"],
                            "powerstate": message["powerstate"]
                        }

                        self.data[address[0]] = data[address[0]]
            except socket.error:
                pass


class Server_Control():
    def __init__(self):
        # the address and port to be broadcast on
        self.broadcast_address = ("<broadcast>", 9878)

        # the address and port to be listened on
        self.listening_address = ("", 9789)

        # default timeout length
        self.timeout = 1

        # SOCKETS
        # create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # set socket to broadcast
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # bind socket
        # self.sock.bind(self.listening_address)
        # set socket blocking
        self.sock.setblocking(False)
        # set the time out
        self.sock.settimeout(self.timeout)

    # Stop Broadcasting Commands
    def stop_all(self):
        try:
            self.sock.sendto(json.dumps(["Stop Updating"]), ("<broadcast>", 9878))
        except socket.error:
            print "socket error stopped the stop all command"

    def stop_individual(self, ip):
        try:
            self.sock.sendto(json.dumps(["Stop Updating"]), (ip, 9878))
        except socket.error:
            print "could not stop: {}".format(ip)

    # Start Broadcasting Commands
    def start_all(self):
        try:
            self.sock.sendto(json.dumps(["Start Updating"]), ("<broadcast>", 9878))
        except socket.error:
            print "socket error stopped the stop all command"

    def start_individual(self, ip):
        try:
            self.sock.sendto(json.dumps(["Start Updating"]), (ip, 9878))
        except socket.error:
            print "socket error stopped the stop all command"

    # Reboot Commands
    def reboot_all(self):
        try:
            self.sock.sendto(json.dumps(["Reboot"]), ("<broadcast>", 9878))
        except socket.error:
            print "socket error stopped the stop all command"

    def reboot_individual(self, ip):
        try:
            self.sock.sendto(json.dumps(["Reboot"]), (ip, 9878))
        except socket.error:
            print "socket error stopped the stop all command"

            # Shutdown Commands

    # Shutdown Commands
    def shutdown_all(self):
        try:
            self.sock.sendto(json.dumps(["Shutdown"]), ("<broadcast>", 9878))
        except socket.error:
            print "socket error stopped the stop all command"

    def shutdown_individual(self, ip):
        try:
            self.sock.sendto(json.dumps(["Shutdown"]), (ip, 9878))
        except socket.error:
            print "socket error stopped the stop all command"


class GUI():
    def __init__(self):
        self.frame = Tkinter.Tk()
        self.frame.state("zoomed")
        self.frame.iconbitmap("photo.ico")
        self.frame.title("Raspberry Pi Control Panel")
        # Create control
        self.Control = Server_Control()

        # internal data
        self.output = {}

        # Main Control Buttons
        self.StopAllButton = Tkinter.Button(self.frame, command=self.Control.stop_all, text="Stop All", width="15",
                                            state="active").grid(row=100, column=1, padx="5")
        self.StartAllButton = Tkinter.Button(self.frame, command=self.Control.start_all, text="Start All", width="15",
                                             state="active").grid(row=100, column=2, padx="5")
        self.ShutdownAllButton = Tkinter.Button(self.frame, command=self.Control.shutdown_all, text="Shutdown All",
                                                width="15", state="active").grid(row=100, column=3, padx="5")
        self.RestartAllButton = Tkinter.Button(self.frame, command=self.Control.reboot_all, text="Restart All",
                                               width="15", state="active").grid(row=100, column=4, padx="5")
        self.update()
        self.frame.protocol("WM_DELETE_WINDOW", self.on_close)
        self.frame.mainloop()

    def update(self):
        global data
        for each_pi in data.iterkeys():
            self.output[data[each_pi]["ip"]] = {
                "ip": Tkinter.Label(self.frame, text=data[each_pi]["ip"]),
                "hostname": Tkinter.Label(self.frame, text=data[each_pi]["hostname"]),
                "username": Tkinter.Label(self.frame, text=data[each_pi]["username"]),
                "powerstate": Tkinter.Label(self.frame, text=data[each_pi]["powerstate"]),
                "temperature": Tkinter.Label(self.frame, text=data[each_pi]["temperature"]),

                "Start": Tkinter.Button(self.frame, text="Restart", width=10),
                "Stop": Tkinter.Button(self.frame, text="Stop", width=10),
                "Reboot": Tkinter.Button(self.frame, text="Reboot", width=10),
                "Shutdown": Tkinter.Button(self.frame, text="Shutdown", width=10)}
            self.output_GUI()

    def output_GUI(self):
        Row = 1
        for each in self.output:
            each["ip"].grid(row=Row, column=1)
            each["hostname"].grid(row=Row, column=2, padx=3)
            each[each]["username"].grid(row=Row, column=3, padx=3)
            each[each]["powerstate"].grid(row=Row, column=4, padx=3)
            each[each]["temperature"].grid(row=Row, column=5, padx=3)
            each[each]["Start"].grid(row=Row, column=6, padx=3)
            each[each]["Stop"].grid(row=Row, column=7, padx=3)
            each[each]["Reboot"].grid(row=Row, column=8, padx=3)
            each[each]["Shutdown"].grid(row=Row, column=9, padx=3)
            Row += 1
        self.frame.after(5000, self.update)

    def on_close(self):
        global stop
        stop = True
        self.frame.destroy()


def run_Server_Listening():
    Server = Server_Search_and_Listen()
    y = Thread(target=GUI)
    y.start()
    while True:
        if Server.data:
            Server.start_sending_details()
            Server.receive_details()

        else:
            Server.start_broadcasting()


x = run_Server_Listening()
