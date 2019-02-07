# github.com/crash-horror
# qtclock.pyw


import os
import sys
import time
# pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QIcon, QImage, QPainter
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.firstrun = True
        self.size = 0
        self.secrotation = 0
        self.minrotation = 0
        self.hourrotation = 0
        self.alarmrotation = 0
        self.alarmtime = 0
        self.alarmvisible = 1
        self.showseconds = True
        self.initUI()


    def initUI(self):
        self.resize(350, 350)
        self.setWindowTitle('Clock')
        self.setWindowIcon(QIcon(resource_path('stuff/clock.ico')))

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        self.clockw = clockwidget()
        self.setCentralWidget(self.clockw)
        self.show()


    def resizeEvent(self, event):  # pylint: disable=W0613
        w = self.clockw.size().width()
        if w < 350:
            w = 350
        h = self.clockw.size().height()
        if h < 350:
            h = 350
        self.clockw.move((w-350)/2, (h-350)/2)


    def move_hands(self):
        self.setWindowTitle(time.strftime("%X", time.localtime(time.time())))
        if self.showseconds:
            self.secrotation = int(time.strftime("%S", time.localtime(time.time()))) * 6

        if self.firstrun or int(time.strftime("%S", time.localtime(time.time()))) == 0:
            self.minrotation = int(time.strftime("%M", time.localtime(time.time()))) * 6
            self.hourrotation = int(time.strftime("%H", time.localtime(time.time()))) * 30 +\
                int(time.strftime("%M", time.localtime(time.time()))) / 2

            if self.alarmtime == self.hourrotation % 360 and self.alarmvisible == 1:
                QSound.play(resource_path("stuff/alarm.wav"))
            self.firstrun = False
        self.clockw.update()


    def wheelEvent(self, event):
        if self.alarmvisible == 1:
            delta = event.angleDelta()/120*5
            self.alarmrotation += delta.y()
            self.clockw.update()
            self.alarmtime = self.alarmrotation % 360


    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            if self.alarmvisible == 1:
                self.alarmvisible = 0
            else:
                self.alarmvisible = 1
            self.clockw.update()

        if event.button() == Qt.MidButton:
            self.showseconds = not self.showseconds
            self.clockw.update()

        self.oldPos = event.globalPos()


    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint (event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()



class clockwidget(QWidget):

    def __init__(self):
        super().__init__()
        self.cfaceimage = QImage()
        self.cfaceimage.load(resource_path('stuff/cface_grad2.png'))
        self.alarmimage = QImage()
        self.alarmimage.load(resource_path('stuff/alarm.png'))
        self.alarmaskimage = QImage()
        self.alarmaskimage.load(resource_path('stuff/alarmask.png'))
        self.hourshandimage = QImage()
        self.hourshandimage.load(resource_path('stuff/hourshand_sq.png'))
        self.minuteshandimage = QImage()
        self.minuteshandimage.load(resource_path('stuff/minuteshand_sq.png'))
        self.sechandimage = QImage()
        self.sechandimage.load(resource_path('stuff/sechand.png'))
        self.centermaskimage = QImage()
        self.centermaskimage.load(resource_path('stuff/centermask.png'))


    def paintEvent(self, event):
        cfacepaint = QPainter(self)
        cfacepaint.translate(self.cfaceimage.width() /
                               2, self.cfaceimage.height()/2)
        cfacepaint.drawImage(-self.cfaceimage.width() /
                               2, -self.cfaceimage.height()/2, self.cfaceimage)

        alarmpaint = QPainter(self)
        alarmpaint.setRenderHint(QPainter.SmoothPixmapTransform, True)
        alarmpaint.translate(self.alarmimage.width()/2,
                               self.alarmimage.height()/2)
        alarmpaint.rotate(gui.alarmrotation)
        alarmpaint.setOpacity(gui.alarmvisible)
        alarmpaint.drawImage(-self.alarmimage.width()/2, -
                               self.alarmimage.height()/2, self.alarmimage)

        hourshandpaint = QPainter(self)
        hourshandpaint.setRenderHint(QPainter.SmoothPixmapTransform, True)
        hourshandpaint.translate(self.hourshandimage.width()/2,
                               self.hourshandimage.height()/2)
        hourshandpaint.rotate(gui.hourrotation)
        hourshandpaint.drawImage(-self.hourshandimage.width()/2, -
                               self.hourshandimage.height()/2, self.hourshandimage)

        minuteshandpaint = QPainter(self)
        minuteshandpaint.setRenderHint(QPainter.SmoothPixmapTransform, True)
        minuteshandpaint.translate(self.minuteshandimage.width()/2,
                              self.minuteshandimage.height()/2)
        minuteshandpaint.rotate(gui.minrotation)
        minuteshandpaint.drawImage(-self.minuteshandimage.width()/2, -
                              self.minuteshandimage.height()/2, self.minuteshandimage)

        if gui.showseconds:
            sechandpaint = QPainter(self)
            sechandpaint.setRenderHint(QPainter.SmoothPixmapTransform, True)
            sechandpaint.translate(self.sechandimage.width()/2,
                                self.sechandimage.height()/2)
            sechandpaint.rotate(gui.secrotation)
            sechandpaint.drawImage(-self.sechandimage.width()/2, -
                                self.sechandimage.height()/2, self.sechandimage)

        centermaskpaint = QPainter(self)
        centermaskpaint.translate(self.centermaskimage.width()/2,
                              self.centermaskimage.height()/2)
        centermaskpaint.drawImage(-self.centermaskimage.width()/2, -
                              self.centermaskimage.height()/2, self.centermaskimage)

        alarmaskpaint = QPainter(self)
        alarmaskpaint.translate(self.alarmaskimage.width()/2,
                              self.alarmaskimage.height()/2)
        alarmaskpaint.setOpacity(gui.alarmvisible)
        alarmaskpaint.drawImage(-self.alarmaskimage.width()/2, -
                              self.alarmaskimage.height()/2, self.alarmaskimage)



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = MainWindow()

    timer = QTimer()
    timer.timeout.connect(gui.move_hands)
    timer.start(1000)

    sys.exit(app.exec_())

