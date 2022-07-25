from tkinter import EventType
from PyQt5 import QtWidgets, QtGui, QtCore


class ImageViewer(QtWidgets.QGraphicsView):
    factor = 2.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHints(
            QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform
        )
        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.setBackgroundRole(QtGui.QPalette.Dark)

        scene = QtWidgets.QGraphicsScene()
        self.setScene(scene)

        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.num_snip = 0
        self.is_snipping = False

        self._pixmap_item = QtWidgets.QGraphicsPixmapItem()
        scene.addItem(self._pixmap_item)
        scene.installEventFilter(self)

    def load_image(self, fileName):
        pixmap = QtGui.QPixmap(fileName)
        if pixmap.isNull():
            return False
        self._pixmap_item.setPixmap(pixmap)
        return True

    def zoomIn(self):
        self.zoom(self.factor)

    def zoomOut(self):
        self.zoom(1 / self.factor)

    def zoom(self, f):
        self.scale(f, f)

    def resetZoom(self):
        self.resetTransform()

    def fitToWindow(self):
        self.fitInView(self.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def eventFilter(self, obj, event):
        # if obj is self.scene:
        # print(self.scene)
        # print(EventType)
        start = end = 0
        global x
        x = 0

        if event.type() == QtCore.QEvent.GraphicsSceneMousePress:
            print("click")
            spf = event.scenePos()
            lpf = self._pixmap_item.mapFromScene(spf)
            brf = self._pixmap_item.boundingRect()
            # print(brf)
            if brf.contains(lpf):
                # global sp
                sp = lpf.toPoint()
                print(f'start- {sp}')
                # x1,y1 = lp
                x = 5
                print(f'x = {x}')

        if event.type() == QtCore.QEvent.GraphicsSceneMouseRelease:
            print("release")

            spf = event.scenePos()
            lpf = self._pixmap_item.mapFromScene(spf)
            brf = self._pixmap_item.boundingRect()

            if brf.contains(lpf):
                # global ep
                ep = lpf.toPoint()

                print(f'end- {ep}')
                x += 10
                print(f'x = {x}')
                # crop_extent = QtCore.QRect(sp,ep)
                # crop_rect(crop_extent,self.scene)
                # x2,y2 = lp

        def crop_rect(rect_item, scene):
            is_visible = rect_item.isVisible()

            rect_item.hide()

            hide_view = QtWidgets.QGraphicsView(scene)
            hide_view.rotate(-rect_item.rotation())

            polygon = rect_item.mapToScene(rect_item.rect())
            pixmap = QtGui.QPixmap(rect_item.rect().size().toSize())
            pixmap.fill(QtCore.Qt.transparent)
            source_rect = hide_view.mapFromScene(polygon).boundingRect()

            painter = QtGui.QPainter(pixmap)
            hide_view.render(
                painter,
                target=QtCore.QRectF(pixmap.rect()),
                source=source_rect,
            )
            painter.end()

            rect_item.setVisible(is_visible)

            return pixmap

        # if  event.type() == QtCore.QEvent.Paint:
        #         if self.is_snipping:
        #             brush_color = (0, 255, 0, 255)
        #             lw = 0
        #             opacity = 0
        #         else:
        #             brush_color = (0, 128, 0, 128)
        #             lw = 8
        #             opacity = 0.3

        #         self.setWindowOpacity(opacity)
        #         qp = QtGui.QPainter(self)
        #         qp.setPen(QtGui.QPen(QtGui.QColor('black'), lw))
        #         qp.setBrush(QtGui.QColor(*brush_color))
        #         qp.drawRect(QtCore.QRect(self.begin, self.end))
        #     # self.num_snip += 1
        #     # x1 = min(self.begin.x(), self.end.x())
        #     # y1 = min(self.begin.y(), self.end.y())
        #     # x2 = max(self.begin.x(), self.end.x())
        #     # y2 = max(self.begin.y(), self.end.y())
        #     print(x1,y1,x2,y2)
        #     # self.getClickedPosition(event.pos())

        #     # self.is_snipping = True
        #     # self.repaint()
        #     # QtWidgets.QApplication.processEvents()
        #     # img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        #     # self.is_snipping = False
        #     # self.repaint()
        #     # QtWidgets.QApplication.processEvents()
        #     # # img_name = 'snip{}.png'.format(self.num_snip)
        #     # img_name = '{}_{}.jpg'.format(x1, y1)
        #     # img.save(img_name)
        #     # print(img_name, 'saved')
        #     # img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

        # rect_item = self.scene.addRect(sp,ep)
        # qpixmap = crop_rect(rect_item, self.scene)

        return super().eventFilter(obj, event)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.view = ImageViewer()
        self.setCentralWidget(self.view)

        self.setMouseTracking(True)

        self.createActions()
        self.createMenus()

        self.resize(640, 480)

    def open(self):
        image_formats = " ".join(
            [
                "*." + image_format.data().decode()
                for image_format in QtGui.QImageReader.supportedImageFormats()
            ]
        )

        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Open Image"),
            QtCore.QDir.currentPath(),
            self.tr("Image Files({})".format(image_formats)),
        )
        if fileName:
            is_loaded = self.view.load_image(fileName)
            self.fitToWindowAct.setEnabled(is_loaded)
            self.updateActions()

    def fitToWindow(self):
        if self.fitToWindowAct.isChecked():
            self.view.fitToWindow()
        else:
            self.view.resetZoom()
        self.updateActions()

    def about(self):
        QtWidgets.QMessageBox.about(
            self,
            "ImageViewer",
            "ImageViewer",
        )

    def createActions(self):
        self.openAct = QtWidgets.QAction(
            "&Open...", self, shortcut="Ctrl+O", triggered=self.open
        )
        self.exitAct = QtWidgets.QAction(
            "E&xit", self, shortcut="Ctrl+Q", triggered=self.close
        )
        self.zoomInAct = QtWidgets.QAction(
            self.tr("Zoom &In (25%)"),
            self,
            shortcut="Ctrl+=",
            enabled=False,
            triggered=self.view.zoomIn,
        )
        self.zoomOutAct = QtWidgets.QAction(
            self.tr("Zoom &Out (25%)"),
            self,
            shortcut="Ctrl+-",
            enabled=False,
            triggered=self.view.zoomOut,
        )
        self.normalSizeAct = QtWidgets.QAction(
            self.tr("&Normal Size"),
            self,
            shortcut="Ctrl+S",
            enabled=False,
            triggered=self.view.resetZoom,
        )
        self.fitToWindowAct = QtWidgets.QAction(
            self.tr("&Fit to Window"),
            self,
            enabled=False,
            checkable=True,
            shortcut="Ctrl+F",
            triggered=self.fitToWindow,
        )
        self.aboutAct = QtWidgets.QAction(
            self.tr("&About"),
            self,
            triggered=self.about)
        self.aboutQtAct = QtWidgets.QAction(
            self.tr("About &Qt"),
            self,
            triggered=QtWidgets.QApplication.aboutQt
        )

    def createMenus(self):
        self.fileMenu = QtWidgets.QMenu(self.tr("&File"), self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QtWidgets.QMenu(self.tr("&View"), self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.helpMenu = QtWidgets.QMenu(self.tr("&Help"), self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
