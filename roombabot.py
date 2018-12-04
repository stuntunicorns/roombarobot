#!/usr/bin/env python
###############################################################################################################
# Program Name: Browser_Client_Coder.html
# ================================
# This code is for controlling a robot by a web browser using web sockets
# http://www.dexterindustries.com/
# History
# ------------------------------------------------
# Author     Comments
# Joshwa     Initial Authoring
#
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)
#=================================
# This Code was modified by stuntunicorns for browser controlled roombabot
# Modificetions
# ------------------------------------------------
# 1. Changed to output to the gpio pins instead of using the Brick Pi.
# 2. Added shutdown process. 
# 
###############################################################################################################

#
#
# PREREQUISITES
# Tornado Web Server for Python
#
# TROUBLESHOOTING:
# Don't use Ctrl+Z to stop the program, use Ctrl+c.
# If you use Ctrl+Z, it will not close the socket and you won't be able to run the program the next time.
# If you get the following error:
#   "socket.error: [Errno 98] Address already in use "
# Run this on the terminal:
#   "sudo netstat -ap |grep :9093"
# Note down the PID of the process running it
# And kill that process using:
#   "kill pid"
# If it does not work use:
#   "kill -9 pid"
# If the error does not go away, try changin the port number '9093' both in the client and server code

import threading
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import time
import atexit
import os
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)


#Initialize TOrnado to use 'GET' and load index.html
class MainHandler(tornado.web.RequestHandler):
  def get(self):
    loader = tornado.template.Loader(".")
    self.write(loader.load("index.html").generate())

#Code for handling the data sent from the webpage
class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    print 'connection opened...'
  def check_origin(self,origin):
    return True
  def on_message(self, message):      # receives the data from the webpage and is stored in the variable message
    global c
    print 'received:', message        # prints the revived from the webpage 
    if message == "u":                # checks for the received data and assigns different values to c which controls the movement of robot.
      c = "8";
    if message == "d":
      c = "2"
    if message == "l":
      c = "6"
    if message == "r":
      c = "4"
    if message == "b":
      c = "5"
    if message == "p":
      c = "9"
    print c
    if c == '8' :

      print "Running Forward"
      GPIO.output(25, GPIO.HIGH)
      GPIO.output(24, GPIO.HIGH)
      GPIO.output(23, GPIO.LOW)
      GPIO.output(18, GPIO.HIGH)



    elif c == '2' :

      print "Running Reverse"
      GPIO.output(25, GPIO.LOW)
      GPIO.output(24, GPIO.HIGH)
      GPIO.output(23, GPIO.HIGH)
      GPIO.output(18, GPIO.HIGH)


    elif c == '4' :
      print "Turning Right"
      GPIO.output(25, GPIO.LOW)
      GPIO.output(24, GPIO.HIGH)
      GPIO.output(23, GPIO.LOW)
      GPIO.output(18, GPIO.HIGH)


    elif c == '6' :
      print "Turning Left"
      GPIO.output(25, GPIO.HIGH)
      GPIO.output(24, GPIO.HIGH)
      GPIO.output(23, GPIO.HIGH)
      GPIO.output(18, GPIO.HIGH)

    elif c == '9' :
      print "Shutting Down"
      GPIO.output(25, GPIO.LOW)
      GPIO.output(24, GPIO.LOW)
      GPIO.output(23, GPIO.LOW)
      GPIO.output(18, GPIO.LOW)
      os.system("sudo shutdown -h now")


    elif c == '5' :
      print "Stopped"
      GPIO.output(25, GPIO.LOW)
      GPIO.output(24, GPIO.LOW)
      GPIO.output(23, GPIO.LOW)
      GPIO.output(18, GPIO.LOW)


application = tornado.web.Application([
  (r'/ws', WSHandler),
  (r'/', MainHandler),
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
])



class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Ready"
        while running:
                        time.sleep(.2)              # sleep for 200 ms

if __name__ == "__main__":



  running = True
  thread1 = myThread(1, "Thread-1", 1)
  thread1.setDaemon(True)
  thread1.start()
  application.listen(9093)            #starts the websockets connection
  tornado.ioloop.IOLoop.instance().start()
