from PyQt4 import QtGui, QtCore
import urllib2
import thread
import ssl
import sys
import collections
import time
import httplib

class VideoScreen(QtGui.QGraphicsView):
    # Screen onto which the image is projected
    # View, Scene and Item rolled into one object
    def __init__(self, parent):
        super(VideoScreen, self).__init__(parent)
        self.added = False
        self._scene = QtGui.QGraphicsScene(self)
        self._photo = QtGui.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))
    # Update frame set on timer call in MainWindow
    def setFrame(self, pixmap=None):
        if pixmap and not pixmap.isNull():
            self._photo.setPixmap(pixmap)
            if self.added is False:
                self.added = True
        else:
            self._photo.setPixmap(QtGui.Pixmap())


class Window(QtGui.QMainWindow):

    def streamParser(self, url):

        request = urllib2.build_opener(urllib2.HTTPSHandler(
           key_file='/etc/ssl/testing.key',
           cert_file='/etc/ssl/testing.crt',
            ca_certs='/usr/share/ca-certificates/extra/testing_CA.crt'
            )
        )

        try:
            stream = request.open(url)
        except:
            while True:
                time.sleep(5)
                stream = request.open(url)
                if stream:
                    break

        bytes = ''

        while True:
            try:
                bytes += stream.read(1024)
                a = bytes.find('\xff\xd8')
                b = bytes.find('\xff\xd9')

                if a != -1 and b != -1:
                    jpg = bytes[a:b + 2]
                    bytes = bytes[b + 2:]
                    self.images.append(jpg)
            except httplib.IncompleteRead:
                # Handles unexpectedly closed connection
                print('IncompleteRead')
                time.sleep(5)
                thread.start_new_thread(self.streamParser, (self.url, ) )
                break


    def __init__(self, address):
        super(Window,self).__init__()
        # Init the frame image list
        self.url = "https://" + address + "/?action=stream"
        self.images = collections.deque(maxlen=5)
        self.statusBar().hide()
        # Init the video screen
        self.screen = VideoScreen(self)
        self.setCentralWidget(self.screen)
        # Start parsing the web stream for images
        thread.start_new_thread(self.streamParser, (self.url, ) )
        # On timeout, timer triggers a frame update
        QtCore.QTimer.singleShot(100, self.updateFrame)

    def updateFrame(self):

        # Uses the earliest available image data
        # but only if there's data in the queue
        try:
            jpg = self.images.pop()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(jpg)
            # Calls the VideoScreen function
            self.screen.setFrame(pixmap)
        except:
            pass
        finally:
            # set the timer for the next frame update
            QtCore.QTimer.singleShot(100, self.updateFrame)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window("192.168.21.113:8080")
    #window.streamParser()
    #window.updateFrame()
    #window.showMaximized()
    window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    window.setGeometry(0, 0, 1280, 720)
    window.show()
    sys.exit(app.exec_())
