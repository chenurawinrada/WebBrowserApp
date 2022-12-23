# coding: utf-8
import sys
import time
import threading
from pathlib import Path
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QCursor, QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Window size
        self.WIDTH = 1000
        self.HEIGHT = 800
        self.resize(self.WIDTH, self.HEIGHT)
        self.setStyleSheet('''
        QPushButton{
            color: white;
            font-size: 20px;
            font-weight: bold;
            font-family: Georgia;
            background: black;
            border-radius: 20px;
        }
        QPushButton:hover{
            color: black;
            background: white;
        }
        QPushButton::pressed{
            background: black;
        }
        QLineEdit{
            color: black;
            font-weight: bold;
            font-family: Georgia;
            font-size: 15px;
            background: transparent;
            border: 5px solid black;
            border-radius: 20px;
        }
        ''')

        # Widget
        self.centralwidget = QWidget(self)
        self.centralwidget.resize(self.WIDTH, self.HEIGHT)

        # browser
        self.browser = QWebEngineView(self)
        self.browser.setUrl(QUrl("https://www.google.com"))
        # Download request
        self.browser.page().profile().downloadRequested.connect(self._download_requested)
        self.browser.setGeometry(10, 70, 970, 700)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Button
        self.close_button = QPushButton('x', self)
        self.close_button.setStatusTip("   Close")
        self.close_button.clicked.connect(self.close_ap)
        self.close_button.setGeometry(950, 10, 40, 40)

        self.mini_button = QPushButton('_' ,self)
        self.mini_button.clicked.connect(self.showMinimized)
        self.mini_button.setStatusTip("   Minimize")
        self.mini_button.setGeometry(905, 10, 40, 40)

        self.homebtn = QPushButton('H', self)
        self.homebtn.clicked.connect(self.navigate_home)
        self.homebtn.setStatusTip("   Return To Home Page")
        self.homebtn.setGeometry(10, 10, 40, 40)

        self.gobtn = QPushButton('Go', self)
        self.gobtn.clicked.connect(self.navigate_url)
        self.gobtn.setGeometry(755, 10, 40, 40)

        self.backbtn = QPushButton('<', self)
        self.backbtn.clicked.connect(self.browser.back)
        self.backbtn.setStatusTip("   Go Previous Page")
        self.backbtn.setGeometry(55, 10, 40, 40)

        self.refreshbtn = QPushButton('R', self)
        self.refreshbtn.clicked.connect(self.browser.reload)
        self.refreshbtn.setStatusTip("   Refresh This Page")
        self.refreshbtn.setGeometry(100, 10, 40, 40)

        self.stbtn = QPushButton('S', self)
        self.stbtn.clicked.connect(self.browser.stop)
        self.stbtn.setStatusTip("   Stop Loading")
        self.stbtn.setGeometry(145, 10, 40, 40)

        self.fowardbtn = QPushButton('>', self)
        self.fowardbtn.clicked.connect(self.browser.forward)
        self.fowardbtn.setStatusTip("   Go Next Page")
        self.fowardbtn.setGeometry(190, 10, 40, 40)

        # text area
        self.text_area = QLineEdit(self)
        # self.text_area.setGeometry(200, 100, 300, 50)
        self.text_area.returnPressed.connect(self.navigate_url)
        self.text_area.setGeometry(250, 10, 500, 40)

        self.browser.urlChanged.connect(self.update_text_area)

        # Menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.right_menu)

        # Initial
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowOpacity(0.6)
        self.setWindowOpacity(1)

        radius = 30
        self.centralwidget.setStyleSheet(
            """
            background:rgb(255, 255, 255);
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(radius)
        )

    def _download_requested(self, item):
        new_file_path, filter_type = QFileDialog.getSaveFileName(self, "Save this file as....", "", "All files (*)")
        if new_file_path:
            item.setDownloadFileName(new_file_path)
            item.accept()
        else:
            pass

    def close_ap(self):
        sys.exit(0)

    def right_menu(self, pos):
        menu = QMenu()
        exit_option = menu.addAction('Exit')
        exit_option.triggered.connect(lambda: exit(0))
        menu.exec_(self.mapToGlobal(pos))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moveFlag = True
            self.movePosition = event.globalPos() - self.pos()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            event.accept()

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.moveFlag:
            self.move(event.globalPos() - self.movePosition)
            event.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.moveFlag = False
        self.setCursor(Qt.CrossCursor)

    def navigate_url(self):
        a = QUrl(self.text_area.text())
        if a.scheme() == '':
            try:
                a.setScheme('https')
            except Exception:
                try:
                    a.setScheme('http')
                except Exception:
                    pass
        self.browser.setUrl(a)
        self.update_text_area()

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def update_text_area(self):
        self.text_area.setText(self.browser.url().toString())
        self.text_area.setCursorPosition(0)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())