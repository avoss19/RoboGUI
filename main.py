'''
Thank you for using RoboGUI

Designed for BSM Robots

Created By Andrew Voss

Compatibility: Unix Systems (mac & linux) & windows

Not tested on windows

Notes:
- Make windows compatible (not issue due to everyone at BSM using unix based machines)
- switch QDialog to QMainWindow (line 25)
    - Fix size of widgets use setGeometry/geometry or rezise
- Camera stream https://gist.github.com/cms-/1cd8ff5083884a4355bd65f084eda927
'''

import sys, os, time
import ip
from PyQt4.QtCore import SIGNAL, QThread, pyqtSlot, QSize
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.pyQtResolution()

        #print "PyQt4 Resolution: ", self.x, " x ", self.y

        # window size and position
        self.resize(self.x,self.y)
        self.move(0,0)

        # Program icon
        app_icon = QIcon()
        app_icon.addFile('bsm.png')
        app.setWindowIcon(app_icon)

        # window title
        self.setWindowTitle("RoboGUI")

        self.printIP()
        self.pic0()
        self.controllerButton()
        self.changePic()
        self.quitButton()

    def pyQtResolution(self):
        screen_resolution = app.desktop().screenGeometry()
        self.x, self.y = screen_resolution.width(), screen_resolution.height()

    def printIP(self):
        ipAddresses = "<b>Connected IP Addresses:</b>"
        nextLine = "<br />"

        # get ip address from ip.py
        for i in ip.ips:
            if i[:1] != "_":
                exec("ipAddresses = ipAddresses + nextLine + i + ' = ' + ip." + str(i))

        # change color of ip address text
        ipAddresses = "<font color ='green'>" + ipAddresses + "</font>"

        # Create text on screen to display ip addresses
        self.ip = QLabel(ipAddresses, self)

        # position of ip address text
        self.ip.move(self.x - 200,5)

    def pic0(self):
        self.picName = QLabel("<b>Camera1</b>", self)
        self.picName.move(5, 85)

        # http image
        self.pic = QWebView(self)
        #self.pic.setHtml("<img src='http://" + ip.camera1 + ":8080?action=stream" + "' />") # robot video
        self.pic.setHtml("<img src='http://localhost/pepe0.jpg' />") # test image
        self.pic.move(5,100)

    def pic1(self):
        # doesn't work with web pic
        self.pic.setPixmap(QPixmap("pepe1.jpg"))

    def controllerButton(self):
        self.controller = QPushButton("Run Controller-Support", self)
        self.controller.move(0,5)
        self.connect(self.controller, SIGNAL("clicked()"),self.controllerStart)

    def controllerStart(self):
        # not best method to start python program, but threading doesn't play well with pyqt4
        os.system("python Controller.py &")

    def changePic(self):
        self.test = QPushButton("Change Pic", self)
        self.test.move(0,30)
        self.connect(self.test, SIGNAL("clicked()"),self.pic1)

    def quitButton(self):
        self.q = QPushButton("Quit", self)
        self.q.setStyleSheet('QPushButton {color: red;}')
        self.q.move(0,55)
        self.connect(self.q, SIGNAL("clicked()"),self.quit)

    def quit(self):
        # quits all running python programs (not best method to kill program)
        # tested on two different macs and for some reason one python task is capitalized while the other isn't
        try:
            os.system("killall -9 python")
            os.system("killall -9 Python")
        except:
            print "not on unix system"


        # not tested on windows
        try:
            os.system("taskkill /F /IM python.exe /T")
        except:
            print "unknown system"

app = QApplication(sys.argv)
form = Form()
form.showFullScreen()
app.exec_()
