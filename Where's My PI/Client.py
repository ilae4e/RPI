__author__ = '13123935 - Jordan Harman'
import json
import socket
import time

import raspbian as Details


class Client():
    def __init__(self):
        print "Client Made"
        # server address
        self.server = False

        # listening address
        self.listening_address = ("", 9878)

        # broadcast response message
        self.response_message = "Understood"

        # defualt sleep time
        self.sleep = 1

        # create the variable to store the broadcasters details
        self.broadcaster_address = ()

        # default time out length
        self.timeout = 1

        # wait for broadcast time
        self.broadcast_wait = 5

        # SOCKETS
        # create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # bind the socket to the address
        self.sock.bind(self.listening_address)
        # set blocking
        self.sock.setblocking(False)
        # set the time out
        self.sock.settimeout(self.timeout)

    def listener(self):
        print "Listening"
        while True:
            try:
                message, address = self.sock.recvfrom(1024)
                message = json.loads(message)
                if message[0] == "I'm Looking for some tasty Pi":
                    print "\n"
                    self.get_server(message, address)
                elif message[0] == "Send Me Your Information":
                    print "\n"
                    self.General_Listening(message, address)
                else:
                    print "\tinvalid option"
            except socket.error:
                pass

    def get_server(self, message, address):
        print "\tGetting server"
        if message[0] == "I'm Looking for some tasty Pi":
            if not self.server:
                print "\t\tmessage is correct"
                attempts = 0
                while not self.server and attempts < 10:
                    try:
                        print "\t\tFound server: {}".format(address[0])
                        self.sock.sendto(json.dumps(
                            ("I am here Mr. Server",)
                        ), address)

                        print "\t\t Waiting for the server to acknowledge"
                        server_message, server_address = self.sock.recvfrom(1024)
                        server_message = json.loads(server_message)
                        if server_message[0] == "Hello Mr. Pi":
                            print "\tServer Acknowledged: Waiting to send information"
                            self.server = server_address
                            break
                        else:
                            print "\t\tServer returned the wrong message"

                    except socket.error:
                        attempts += 1
                else:
                    print "\tNo server found"
            else:
                print "\tAlready connected to a server"

    def General_Listening(self, message, address):
        print "\tListening for control messages"
        update_server = True
        message_delay = message[1]
        last_message = time.time()
        next_server_check = 60
        self.last_server_check = time.time()

        while self.server:
            try:
                server_message, server_address = self.sock.recvfrom(1024)
                if server_message and server_address:
                    message = json.loads(server_message)
                    if message[0] == "Stop Updating":
                        print "\t\tStopping Updating"
                        update_server = False

                    elif message[0] == "Start Updating":
                        print "\t\tStarting To Update"
                        update_server = True

                    elif message[0] == "Shutdown":
                        print "\t\tShutting Down"
                        self.sock.sendto(self.shutdown_details(), self.server)
                        self.shutdown()

                    elif message[0] == "Reboot":
                        print "\t\tRebooting"
                        self.sock.sendto(self.reboot_details(), self.server)
                        self.reboot()

            except socket.error:
                pass

            if time.time() - last_message >= message_delay and update_server:
                print "\t\tSending Details"
                data = (self.get_details())
                self.sock.sendto(data, self.server)
                last_message = time.time()

            if time.time() - self.last_server_check >= next_server_check:
                self.check_server()

        else:
            print "\tError: No server found, please find a server"

    def check_server(self):
        print "\t\t\tchecking server state"
        count = 0
        while True:
            try:
                data = json.dumps(("Server State?",))
                self.sock.sendto(data, self.server)

                message, address = self.sock.recvfrom(1024)
                if message and address:
                    message = json.loads(message)
                    if message[0] == "Yes I am online":
                        print "\t\t\t\tserver still exists"
                        self.last_server_check = time.time()
                        break
            except socket.error:
                count += 1
                print "\t\t\t\t\tFailed to find server - {} time(s)".format(count)
                if count >= 10:
                    print "\t\t\t\tlost connection to the server - Waiting to find a new server"
                    self.server = False
                    break

    def get_details(self):
        return Details.get_details()

    def shutdown_details(self):
        return Details.shutdown_details()

    def shutdown(self):
        Details.shutdown()

    def reboot_details(self):
        return Details.reboot_details()

    def reboot(self):
        Details.reboot()


x = Client()
x.listener()
