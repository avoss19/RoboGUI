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
- switch QDialog to QMainWindow (line 30)
    - Fix size of widgets use setGeometry/geometry or rezise
- Camera stream https://gist.github.com/cms-/1cd8ff5083884a4355bd65f084eda927
'''

import sys, os, time
import ip
import camera
from PyQt4.QtCore import SIGNAL, QThread, pyqtSlot, QSize, QTimer, QUrl
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
#from PyQt4.QtMultimediaWidgets import *
from PyQt4.QtMultimedia import *

class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.initScreenSize() # If window mode set to fullscreen window

        # window size and position
        self.resize(1000, 1000) # set screen size
        self.setMinimumSize(800, 600) # set min screen size
        self.center()

        self.pyQtResolution() # Get window resolution

        # Program icon
        app_icon = QIcon()
        app_icon.addFile('bsm.png')
        app.setWindowIcon(app_icon)

        # window title
        self.setWindowTitle("RoboGUI")

        self.videoStream()

        self.printIP()
        #self.pic0()
        self.controllerButton()
        #self.changePic()
        self.quitButton()

        self.debugButton()



        #self.updateDisplayB()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


    def updateDisplay(self):
        self.pyQtResolution()

        self.debugB.move(0,self.y-30)
        self.ip.move(self.x - 200,5)

        self.update()

    def videoStream(self):

        self.layout = QGridLayout(self)
        #self.layout.resize(100,100)
        #self.layout.setRowStretch(0, 3)

        view = camera.Player()
        #view.resize(100,100)

        #view = Browser()
        #view.load(QUrl('http://google.com'))
        view.setMaximumHeight(500)
        view.setMaximumWidth(500)

        self.layout.addWidget(view)
        #self.layout.setMaximum(100,100)

        #self.view.move(0,0)
        #self.view.resize(200,200)

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
        ipAddresses = "<b>Connected IP Address:</b>"
        nextLine = "<br />"

        # get ip address from ip.py
        ipAddresses = ipAddresses + nextLine + "kitBot" + ' = ' + ip

        # change color of ip address text
        ipAddresses = "<font color ='green'>" + ipAddresses + "</font>"

        # Create text on screen to display ip addresses
        self.layout.ip = QLabel(ipAddresses, self)

        # position of ip address text

        self.layout.ip.resize(300,40)
        self.layout.ip.move(self.x - 200,0)

        #self.ip.resize(1000,1000)


    def pic0(self):
        self.picName = QLabel("<b>Camera1</b>", self)
        self.picName.move(5, 85)

        #self.pic = QLabel(self)
        #self.pic.setPixmap(QPixmap("pepe0.jpg"))

        # http image
        self.pic = Browser()
        self.pic.load(QUrl('http://www.google.com'))

        #self.pic.setHtml("<img src='http://" + ips.camera1 + "8080/?action=stream") # robot video
        #self.pic.setHtml("<img src='http://localhost/pepe0.jpg' />") # test image

        self.pic.move(5,100)

        i = vlc.Instance('--verbose 2'.split())
        p = i.media_player_new()
        p.set_mrl('rtp://@224.1.1.1')
        p.play()

        self.camera = QMediaPlayer()
        self.cemera.QMediaContent(QUrl("http://192.168.42.129:8080/video"));


    def pic1(self):
        # doesn't work with web pic
        self.pic.setPixmap(QPixmap("pepe1.jpg"))


    def controllerButton(self):
        self.controller = QPushButton("Run Controller-Support", self)
        self.controller.move(0,5)
        self.connect(self.controller, SIGNAL("clicked()"),self.controllerStart)
        self.controller.resize(300,30)


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
        from sys import platform

        if platform == "linux" or platform == "linux2":
            os.system("killall -9 python")
            os.system("killall -9 Python")

        elif platform == "darwin":
            os.system("killall -9 python")
            os.system("killall -9 Python")

        elif platform == "win32":
            os.system("taskkill /F /IM python.exe /T")


class Browser(QWebView):

    def __init__(self):
        QWebView.__init__(self)
        self.loadFinished.connect(self._result_available)

    def _result_available(self, ok):
        frame = self.page().mainFrame()
        print unicode(frame.toHtml()).encode('utf-8')


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
    os.system("clear")
    app = QApplication(sys.argv)
    form = Form()


    #self.move(0,100)

    windowMode()

    #form.updateDisplay() # Fixes issues with misplaced widgets in windowed mode

    # Update display every second; Poor implementation
    #timer = QTimer(form)
    #timer.timeout.connect(form.updateDisplay)
    #timer.start(1)

    app.exec_()
