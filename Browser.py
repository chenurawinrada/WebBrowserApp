# coding: utf-8
import sys
import time
import json
import threading
from pathlib import Path
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QCursor, QIcon

with open("settings/json_file_chooser.txt", "r") as file:
    file_name = file.read()
    file.close()
with open(f"settings/{file_name}", "r") as j:
    json_data = json.loads(j.read())
    j.close()

color1 = json_data['color1']
color2 = json_data['color2']
color3 = json_data['color3']
color4 = json_data['color4']
color5 = json_data['color5']
color6 = json_data['color6']
color7 = json_data['color7']
color8 = json_data['color8']
color9 = json_data['color9']
color10 = json_data['color10']
color11 = json_data['color11']
color12 = json_data['color12']
color13 = json_data['color13']
color14 = json_data['color14']
sp1 = json_data['sp1']
sp2 = json_data['sp2']

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.WIDTH = 400
        self.HEIGHT = 250
        self.resize(self.WIDTH, self.HEIGHT)
        self.centralwidget = QWidget(self)
        self.centralwidget.resize(self.WIDTH, self.HEIGHT)

        # Stylesheet
        self.setStyleSheet(f'''
        QPushButton{{
            color: {color1};
            font-size: 20px;
            font-weight: bold;
            font-family: Georgia;
            background: {color2};
            border-radius: 20px;
        }}
        QPushButton:hover{{
            color: {color3};
            background: {color4};
        }}
        QPushButton::pressed{{
            background: {color5};
        }}
        QLabel{{
            color: {color6};
            background: {color7};
            font-size: 20px;
            font-family: Georgia;
        }}
        ''')

        self.close_button = QPushButton('x', self)
        self.close_button.clicked.connect(self.close_ap)
        self.close_button.setGeometry(350, 10, 40, 40)

        self.lbl = QLabel("Settings", self)
        self.lbl.setGeometry(120, 20, 165, 40)

        self.white_theme_button = QPushButton('WhiteTheme', self)
        self.white_theme_button.clicked.connect(self.settings_changed_white)
        self.white_theme_button.setGeometry(100, 100, 200, 40)

        self.black_theme_button = QPushButton('Black Theme', self)
        self.black_theme_button.clicked.connect(self.settings_changed_black)
        self.black_theme_button.setGeometry(100, 150, 200, 40)

        # Initial
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.8)
        # self.setWindowOpacity(1)

        self.centralwidget.setStyleSheet(
            f"""
            background:{sp1};
            border-top-left-radius:30px;
            border-bottom-left-radius:30px;
            border-top-right-radius:30px;
            border-bottom-right-radius:30px;
            """
        )

    def close_ap(self):
        self.close()

    def settings_changed_white(self):
        with open("settings/json_file_chooser.txt", "w") as file:
            file.write("white.json")
            file.close()

    def settings_changed_black(self):
        with open("settings/json_file_chooser.txt", "w") as file:
            file.write("black.json")
            file.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.sw = None

        # Window size
        self.WIDTH = 1000
        self.HEIGHT = 800
        self.resize(self.WIDTH, self.HEIGHT)

        # Stylesheet
        self.setStyleSheet(f'''
        QPushButton{{
            color: {color8};
            font-size: 20px;
            font-weight: bold;
            font-family: Georgia;
            background: {color9};
            border-radius: 20px;
        }}
        QPushButton:hover{{
            color: {color10};
            background: {color11};
        }}
        QPushButton::pressed{{
            background: {color12};
        }}
        QLineEdit{{
            color: {color13};
            font-weight: bold;
            font-family: Georgia;
            font-size: 15px;
            background: transparent;
            border: 5px solid {color14};
            border-radius: 20px;
        }}
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

        self.settings_button = QPushButton('*' ,self)
        self.settings_button.clicked.connect(self.settings_window_open)
        self.settings_button.setStatusTip("   Settings")
        self.settings_button.setGeometry(850, 10, 40, 40)

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
        self.setWindowOpacity(0.6)
        # self.setWindowOpacity(1)

        self.centralwidget.setStyleSheet(
            f"""
            background:{sp2};
            border-top-left-radius:30px;
            border-bottom-left-radius:30px;
            border-top-right-radius:30px;
            border-bottom-right-radius:30px;
            """
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

    def settings_window_open(self, checked):
        try:
            if self.sw is None:
                self.sw = SettingsWindow()
            self.sw.show()
        except Exception:
            pass

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())