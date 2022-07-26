from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene, QGraphicsView, QApplication
from PyQt5.QtGui import QBrush, QPainter, QPen, QPixmap, QPolygonF
import sys

app = QApplication(sys.argv)

scene = QGraphicsScene(0, 0, 400, 200)

rectitem = QGraphicsRectItem(0, 0, 360, 20)
rectitem.setPos(20, 20)
rectitem.setBrush(QBrush(Qt.red))
rectitem.setPen(QPen(Qt.cyan))
scene.addItem(rectitem)

textitem = scene.addText("QGraphics is fun!")
textitem.setPos(100, 100)

scene.addPolygon(
    QPolygonF(
        [
            QPointF(30, 60),
            QPointF(270, 40),
            QPointF(400, 200),
            QPointF(20, 150),
        ]),
    QPen(Qt.darkGreen),
)

pixmap = QPixmap("1490_274.jpg")
pixmapitem = scene.addPixmap(pixmap)
pixmapitem.setPos(250, 70)

view = QGraphicsView(scene)
view.setRenderHint(QPainter.Antialiasing)
view.show()

app.exec_()
