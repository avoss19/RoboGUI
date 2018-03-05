'''
https://stackoverflow.com/questions/12200274/create-loop-that-doesnt-lock-up-the-window-pyqt4
'''
from PyQt4 import QtGui, QtCore

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.label = QtGui.QLabel('Count = 0', self)
        self.button = QtGui.QPushButton('Start', self)
        self.button.clicked.connect(self.handleButton)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self._active = False

    def handleButton(self):
        if not self._active:
            self._active = True
            self.button.setText('Stop')
            QtCore.QTimer.singleShot(0, self.runLoop)
        else:
            self._active = False

    def closeEvent(self, event):
        self._active = False

    def runLoop(self):
        from time import sleep
        for index in range(100):
            sleep(0.05)
            self.label.setText('Count = %d' % index)
            QtGui.qApp.processEvents()
            if not self._active:
                break
        self.button.setText('Start')
        self._active = False

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
