'''
Thank you for using RoboGUI

Designed for BSM Robots

Created By Andrew Voss

How to run: python main.py

Arguments: use argument "windowed" to launch in windowed mode
Ex. python main.py windowed

Compatibility: Unix Systems (mac & linux) & windows

Not tested on windows

Notes:
- Tasks https://goo.gl/57n8XC & https://github.com/avoss19/RoboGUI
'''

import sys, os, time
import camera
from PyQt4.QtCore import SIGNAL, QThread, pyqtSlot, QSize, QTimer, QUrl
from PyQt4.QtGui import *


class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        #self.initScreenSize() # If window mode set to fullscreen window

        # window size and position
        #self.resize(1000, 600) # set screen size
        #self.setMinimumSize(800, 600) # set min screen size
        self.setFixedSize(1000, 600) # set fixed screen size; no resizing window
        self.center()

        self.pyQtResolution() # Get window resolution

        # Program icon
        app_icon = QIcon()
        app_icon.addFile('bsm.png')
        app.setWindowIcon(app_icon)

        # window title
        self.setWindowTitle("RoboGUI")

        # Display widgets
        self.videoStream()
        self.printIP()
        self.controllerButton()
        self.quitButton()

        self.debugButton() # For testing purposes


    def initScreenSize(self):
        # For fullscreen app
        screen_resolution = app.desktop().screenGeometry()
        self.x, self.y = screen_resolution.width(), screen_resolution.height()


    def debug(self):
        # For printing info to console
        #print sys.argv
        print "PyQt4 Resolution: ", self.x, " x ", self.y
        print self.size()

        rec = self.geometry();
        height = rec.height();
        width = rec.width();

        print width, height


    def debugButton(self):
        self.debugB = QPushButton("Debug", self)
        self.debugB.move(0,self.y-30)
        self.connect(self.debugB, SIGNAL("clicked()"),self.debug)


    def pyQtResolution(self):
        # Get resolution of window
        rec = self.geometry()
        self.x = rec.width()
        self.y = rec.height()


    def center(self):
        # Center window on display
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


    def videoStream(self):
        # Video Feed
        self.layout = QGridLayout(self)
        view = camera.camera(ip)

        # set size of camera stream
        view.setMaximumHeight(500)
        view.setMaximumWidth(500)

        # Add widget to display
        self.layout.addWidget(view)


    def printIP(self):
        # Print connected ip addresses to screen
        ipAddresses = "<b>Connected IP Address:</b>"
        nextLine = "<br />"

        # get ip address from ip.py
        ipAddresses = ipAddresses + nextLine + "kitBot" + ' = ' + ip

        # change color of ip address text (uses html syntax)
        ipAddresses = "<font color ='green'>" + ipAddresses + "</font>"

        # Create text on screen to display ip addresses
        self.ip = QLabel(ipAddresses, self)

        # position of ip address text & set size
        self.ip.resize(300,40)
        self.ip.move(self.x - 200,0)


    def controllerStart(self):
        # not best method to start python program, but threading doesn't play well with pyqt4
        os.system("python Controller.py &")


    def controllerButton(self):
        self.controller = QPushButton("Run Controller-Support", self)
        self.controller.move(0,5)
        self.connect(self.controller, SIGNAL("clicked()"),self.controllerStart)
        self.controller.resize(180,30)


    def quit(self):
        # quits all running python programs (not best method to kill program), but will kill controller-support
        # Only tested on mac osx; but should technically work
        from sys import platform

        if platform == "linux" or platform == "linux2":
            os.system("killall -9 python")
            os.system("killall -9 Python")

        # tested on two different macs and for some reason one python task is capitalized while the other isn't
        # not sure if it is an isolated situation
        elif platform == "darwin":
            os.system("killall -9 python")
            os.system("killall -9 Python")

        elif platform == "win32":
            os.system("taskkill /F /IM python.exe /T")


    def quitButton(self):
        self.q = QPushButton("Quit", self)
        self.q.setStyleSheet('QPushButton {color: red;}')
        self.q.move(0,30)
        self.connect(self.q, SIGNAL("clicked()"),self.quit)


def windowMode():
    try:
        if sys.argv[1] == "fullscreen":
            form.showFullScreen()
        else:
            form.show()
    except:
        form.show()


def main(ipAddresses):
    global app, form, ip
    ip = ipAddresses
    os.system("clear") # clear terminal on start of program
    app = QApplication(sys.argv)
    form = Form()
    windowMode() # show window
    #app.exec_() # This line is needed to use this program w/out connectKitBot.py
