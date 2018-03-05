'''
Thank you for using RoboGUI

Designed for BSM Robots

Created By Andrew Voss

Notes:
- switch QDialog to QMainWindow (line 21)
    - Fix size of widgets use setGeometry/geometry or rezise
- Camera stream https://gist.github.com/cms-/1cd8ff5083884a4355bd65f084eda927
'''

import sys, os, thread, time
import ip
from AppKit import NSScreen # Only for macs from Pyobjct
from PyQt4.QtCore import SIGNAL, QThread, pyqtSlot, QSize
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        # Get display resolution
        self.x = NSScreen.mainScreen().frame().size.width
        self.y = NSScreen.mainScreen().frame().size.height

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

    def printIP(self):
        ipAddresses = ''
        nextLine = "<br />"

        # get ip address from ip.py
        for i in ip.ips:
            if i[:1] != "_":
                exec("ipAddresses = ipAddresses + nextLine + i + ' = ' + ip." + str(i))

        # change color of ip address text
        ipAddresses = "<font color ='green'>" + ipAddresses + "</font>"

        # Create text on screen to display ip addresses
        self.ipTitle = QLabel("<font color ='green'><b>Connected IP Addresses:</b></font>", self)
        self.ip = QLabel(ipAddresses, self)

        # position of ip address text
        self.ipTitle.move(self.x-200,5)
        self.ip.move(self.x-200,5)

    def pic0(self):
        self.picName = QLabel("<b>Camera1</b>", self)
        self.picName.move(5, 85)

        # local image
        #self.pic = QLabel(self)
        #self.pic.setPixmap(QPixmap("pepe0.jpg"))
        #self.pic.move(5,100)

        html = '''
        <meta http-equiv='refresh' content='0.5' />
        <img src="pepe0.jpg" />
        '''

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
        os.system("clear")
        os.system("killall -9 Python")

app = QApplication(sys.argv)
form = Form()
form.showFullScreen()
app.exec_()
