import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


class MapWindow: # klasa reprezentujaca okienko z mapa na której beda odnośniki do każdej z map
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.win = QMainWindow()
        self.win.setGeometry(600, 600, 753, 454)
        self.win.setWindowTitle("LaVaLanche")
        self.set_image(os.path.join('images', 'tlo.png'))

    def set_image(self, img_path):
        oimage = QImage(img_path)
        simage = oimage.scaled(QSize(1506, 908))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(oimage))
        self.win.setPalette(palette)

    def draw_map_link_buttons(self): # uzywajac button_map.txt jakos te przyciski naloze na mapke :P
        pass
    # w pliku maps_processing moga byc funkcje zwiazane z przetwarzaniem map


class MainWindow: # klasa reprezentujaca glowne okno aplikacji
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.win = QMainWindow()
        self.win.setGeometry(500, 500, 753, 454)
        self.win.setWindowTitle("LaVaLanche")
        self.dialogs = list()
        self.draw_labels()

        self.show_map_button = QPushButton(self.win)
        self.show_map_button.setText("SHOW HAZARD MAP")
        self.show_map_button.setGeometry(300, 100, 150, 30)
        self.show_map_button.clicked.connect(self.show_map) # .clicked.connect() przy przycisnieciu wola funkcje
        self.win.show()

    def draw_buttons(self):
        pass

    def set_image(self, img_path):
        oimage = QImage(img_path)
        simage = oimage.scaled(QSize(753, 454))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(simage))
        self.win.setPalette(palette)

    def draw_labels(self):
        self.label = QtWidgets.QLabel(self.win)
        self.font = QFont("Times", 20, QFont.Bold)
        self.label.setGeometry(170, 0, 500, 50)
        self.label.setFont(self.font)
        self.label.setText("Witaj w (TEMPLATE APP NAME)")

        self.label2 = QtWidgets.QLabel(self.win)
        self.font = QFont("Times", 20,)
        self.label2.setText("<font color='white'>Made by JachyCzkowicz Enterprises 2020</font>")
        self.label2.setGeometry(10, 430, 300, 20)

    def show_map(self): # funkcja wołająca się gdy przyciskamy przycisk "POKAZ MAPE ZAGROZEN"
        mapa = MapWindow() # tworzenie instancji klasy MapWindow()
        self.dialogs.append(mapa) # dodanie okna z mapą do dialogów głównego okna MainWindow
        mapa.win.show()

    def klikniecie(self):
        print("dupa")


if __name__ == "__main__":
    mainwindow = MainWindow()
    mainwindow.set_image(os.path.join('images', 'main_bg.jpg'))
    sys.exit(mainwindow.app.exec_())