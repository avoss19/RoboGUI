from PyQt4.QtCore import SIGNAL, QThread, pyqtSlot, QSize
from PyQt4.QtGui import *
import sys

class Dialog(QDialog):

    def __init__(self):
        super(Dialog, self).__init__()
        self.resize(640,480)
        layout = QVBoxLayout(self)

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(-500,-500,1000,1000)
        self.view = GraphicsView(self)
        self.view.setScene(self.scene)
        layout.addWidget(self.view)

        text = self.scene.addText("Foo")

        self.view.updateCenter()



class GraphicsView(QGraphicsView):

    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)
        self._center = None

        self.resize(1000,1000)

    def resizeEvent(self, event):
        super(GraphicsView, self).resizeEvent(event)
        if self._center:
            self.centerOn(self._center)

    def updateCenter(self):
        center = self.geometry().center()
        self._center = self.mapToScene(center)



app = QApplication(sys.argv)
form = GraphicsView()
form.show()
app.exec_()
