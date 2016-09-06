__author__ = '13123935 - Jordan Harman'
import cookielib
import datetime
import os
import time

import mechanize


class Restart_Internet():
    def __init__(self, username, password):
        # Router Login Details
        self.username = username
        self.password = password

        # Browser Setup
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        self.browser.addheaders = [("User-Agent", "Mozilla/5.0")]

        self.cookies = cookielib.LWPCookieJar()
        self.browser.set_cookiejar(cookiejar=self.cookies)

        # Last Known External IP Address
        self.last_known_external_IP = ""

        # Internal IP of Router
        self.routerIP = "192.168.1.1"
        self.router_ip = "http://192.168.1.1/Docsis_system.asp"

        # Path To Log File Folder
        self.path_to_log = "/home/pi/Desktop"

    def check_internet_connection(self):
        while True:
            # first check
            try:
                self.browser.open("http://www.google.com")
                results = self.browser.response().read()
                if results:
                    results = True
                else:
                    print("Error has Occured\tat: {} ").format(
                        datetime.datetime.now().strftime("%I:%M:%S %p\ton: %A %d %B %Y"))
            except:
                results = False

            # internet connection exists - get external IP
            if results:
                try:
                    self.browser.open("http://ipecho.net/plain")
                    IP = self.browser.response().read()
                    if IP:
                        print "Connected to the Internet\tat:{}".format(
                            datetime.datetime.now().strftime("%I:%M:%S %p\ton: %A %d %B %Y"))
                        self.last_known_external_IP = IP
                        time.sleep(300)
                    else:
                        print "Error has Occured\tat: {}".format(
                            datetime.datetime.now().strftime("%I:%M:%S %p\ton: %A %d %B %Y"))
                        exit()
                except:
                    print "No response from IP Echo\tat: {}".format(
                        datetime.datetime.now().strftime("%I:%M:%S %p\ton: %A %d %B %Y"))
                    time.sleep(60)

            # internet connection does not exist - try once more
            elif not results:
                try:
                    self.browser.open("http://www.microsoft.com")
                    results = self.browser.response().read()
                    if results:
                        print "No Response from Google\tat: {}".format(
                            datetime.datetime.now().strftime("%I:%M:%S %p\ton: %A %d %B %Y"))
                        time.sleep(300)
                    else:
                        print("Error has Occured\tat: {}").format(
                            datetime.datetime.now().strftime("%I:%M:%S %p\ton: %A %d %B %Y"))
                        exit()
                except:
                    self.log_internet_restarts()
                    self.restart_internet_connection()
                    time.sleep(300)

    def restart_internet_connection(self):
        self.cookies.clear_session_cookies()
        self.cookies.clear()
        self.cookies.clear_expired_cookies()
        while True:
            try:
                self.browser.open("http://192.168.1.1/Docsis_system.asp")

                self.browser.select_form("Docsis_system")
                if self.browser["username_login"] == "" and self.browser["password_login"] == "":
                    self.browser["username_login"] = self.username
                    self.browser["password_login"] = self.password
                    self.browser.submit()
                    self.browser.response().read()

                    print "Router restart\tLogged in at: {}".format(
                        datetime.datetime.now().strftime("%I:%M:%S %p\ton: %A %d %B %Y"))
                else:
                    print "Router Restart\tAlready Logged in\t at: {}".format(
                        datetime.datetime.now().strftime("%I:%M:%S %p\ton: %A %d %B %Y"))

                self.browser.open("http://192.168.1.1/Devicerestart.asp")
                self.browser.select_form("devicerestart")

                if self.browser["devicerestrat_Password_check"] == "":
                    self.browser["devicerestrat_Password_check"] = self.password
                    self.browser.submit()
                    print "Router Restart\tRestarted Router at: {}".format(
                        datetime.datetime.now().strftime("%I:%M:%S %p\ton: %A %d %B %Y"))
                    break
                else:
                    print "Router Restart\tError: Cannot Restart Router at: {}".format(
                        datetime.datetime.now().strftime("%I:%M:%S %p\ton: %A %d %B %Y"))
                    time.sleep(60)

            except:
                print "Router Not Accessible\tat: {}".format(
                    datetime.datetime.now().strftime("%I:%M:%S %p\ton: %A %d %B %Y"))
                time.sleep(60)

    def log_internet_restarts(self):
        try:
            if os.path.isfile(os.path.join(self.path_to_log, "log.txt")):

                files = open(os.path.join(self.path_to_log, "log.txt"), "a")
                files.write(
                    "Router with IP: {}\twas restarted at: {}\t The Last Known IP was: {}\n"
                    "".format(self.routerIP,datetime.datetime.now().strftime("%I:%M:%S %p\ton: %A %d %B %Y")
                              ,str(self.last_known_external_IP)))
                files.close()
            else:
                files = open(os.path.join(self.path_to_log, "log.txt"), "w")
                files.close()
                self.log_internet_restarts()
        except IOError as e:
            if e[0] == 13:
                print("Error Writing to file\tat: {}").format(
                    datetime.datetime.now().strftime("%I:%M:%S %p\ton: %A %d %B %Y"))
                exit()
            else:
                print "wtf"


x = Restart_Internet()
x.check_internet_connection()
