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
- Make windows compatible (not issue due to everyone at BSM using unix based machines)
- switch QDialog to QMainWindow (line 30)
    - Fix size of widgets use setGeometry/geometry or rezise
- Camera stream https://gist.github.com/cms-/1cd8ff5083884a4355bd65f084eda927
'''

import sys, os, time
import ip
from PyQt4.QtCore import SIGNAL, QThread, pyqtSlot, QSize, QTimer
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.initScreenSize() # If window mode set to fullscreen window

        # window size and position
        self.resize(self.x,self.y) # setFixedSize disables window resizing
        self.move(0,0)

        self.pyQtResolution() # Get window resolution

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

        self.debugButton()

        #self.updateDisplayB()


    def updateDisplay(self):
        self.pyQtResolution()
        #self.debugB.move(0,self.y-30)

        self.debugB.move(0,self.y-30)
        self.ip.move(self.x - 200,5)

        self.update()


    def updateDisplayB(self):
        self.displayB = QPushButton("Update Display", self)
        self.displayB.move(0,400)
        self.connect(self.displayB, SIGNAL("clicked()"),self.updateDisplay)


    def debug(self):
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


    def initScreenSize(self):
        screen_resolution = app.desktop().screenGeometry()
        self.x, self.y = screen_resolution.width(), screen_resolution.height()


    def pyQtResolution(self):
        rec = self.geometry()
        self.x = rec.width()
        self.y = rec.height()


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

        self.pic = QLabel(self)
        self.pic.setPixmap(QPixmap("pepe0.jpg"))

        # http image
        #self.pic = QWebView(self)
        #self.pic.setHtml("<img src='http://" + ip.camera1 + ":8080?action=stream" + "' />") # robot video
        #self.pic.setHtml("<img src='http://localhost/pepe0.jpg' />") # test image

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


def windowMode():
    try:
        if sys.argv[1] == "windowed":
            form.show()
        else:
            form.showFullScreen()
    except:
        form.showFullScreen()

def main():
    global app, form
    os.system("clear")
    app = QApplication(sys.argv)
    form = Form()
    windowMode()
    #form.updateDisplay() # Fixes issues with misplaced widgets in windowed mode

    # Update display every second; Poor implementation
    timer = QTimer(form)
    timer.timeout.connect(form.updateDisplay)
    timer.start(1)

    app.exec_()

if __name__ == '__main__':
    main()
