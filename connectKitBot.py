import sys
import kitBotMain as main
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QDialog, QApplication, QPushButton, QLineEdit, QFormLayout, QIcon

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        # Program icon
        app_icon = QIcon()
        app_icon.addFile('bsm.png')
        app.setWindowIcon(app_icon)

        self.le = QLineEdit()
        self.le.setObjectName("host")
        self.le.setText("Host")

        self.pb = QPushButton()
        self.pb.setObjectName("connect")
        self.pb.setText("Connect")

        layout = QFormLayout()
        layout.addWidget(self.le)
        layout.addWidget(self.pb)

        self.setLayout(layout)
        self.connect(self.pb, SIGNAL("clicked()"),self.button_click)
        self.setWindowTitle("RoboGUI")

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def button_click(self):
        # shost is a QString object
        global shost
        shost = self.le.text()

        #app.closeAllWindows()

        main.main(shost)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
