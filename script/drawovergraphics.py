
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QAction, QLabel, QMainWindow
from PyQt5.QtGui import QBrush, QImage, QPainter, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5 import QtWidgets, QtGui, QtCore

class Window(QMainWindow):

    def __init__(self):

        super().__init__()
        self.image = QImage("01.JPG")
        #self.showFullScreen()
        self.startPos = None
        self.rect = QRect()
        self.drawing = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.drawing:
            self.startPos = event.pos()
            print(self.startPos)
            self.rect = QRect(self.startPos, self.startPos)
            self.drawing = True
            self.update()

    def mouseMoveEvent(self, event):
        if self.drawing == True:
            self.rect = QRect(self.startPos, event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):

        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor(255, 0, 0))

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(255, 0, 0,128))
        brush.setStyle(Qt.SolidPattern)

        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)
        painter.setBrush(brush)
        painter.setPen(pen)
        if not self.rect.isNull():
            painter.drawRect(self.rect)
        painter.end()

if __name__ == "__main__":
    app=QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()