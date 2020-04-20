import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


class MapWindow(QMainWindow): # klasa reprezentujaca okienko z mapa na której beda odnośniki do każdej z map
    def __init__(self):
        super(MapWindow, self).__init__()
        # self.buttons =
        self.setGeometry(600, 600, 753, 454)
        self.setWindowTitle("LaVaLanche")
        self.set_image(os.path.join('images', 'tlo.png'))

    def set_image(self, img_path):
        oimage = QImage(img_path)
        simage = oimage.scaled(QSize(1506, 908))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(oimage))
        self.setPalette(palette)

    # def draw_map_link_buttons(self): # uzywajac button_map.txt jakos te przyciski naloze na mapke :P
    #     initial_y_coord = 80
    #     button_width = 21
    #     button_height = 22
    #     with open("button_map.txt") as buttonmap:
    #         for line in buttonmap:
    #             linia = line
    #             for ch in linia:
    #                 initial_x_coord = 80
    #                 if ch == "0": #jak 0 to skocz do nastepnego miejsca
    #                     initial_x_coord += button_width + 1
    #                     continue
    #                 elif ch == "1": #jak 1 to stworz guzik


class MainWindow(QMainWindow): # klasa reprezentujaca glowne okno aplikacji
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(500, 500, 753, 454)
        self.setWindowTitle("LaVaLanche")
        self.dialogs = list()
        self.draw_labels()
        self.draw_buttons()
        self.show()

    def draw_buttons(self):
        self.show_map_button = QPushButton(self)
        self.show_map_button.setText("SHOW HAZARD MAP")
        self.show_map_button.setGeometry(300, 100, 150, 30)
        self.show_map_button.clicked.connect(self.show_map)  # .clicked.connect() przy przycisnieciu wola funkcje

    def set_image(self, img_path):
        oimage = QImage(img_path)
        simage = oimage.scaled(QSize(753, 454))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(simage))
        self.setPalette(palette)

    def draw_labels(self):
        self.label = QtWidgets.QLabel(self)
        self.font = QFont("Times", 20, QFont.Bold)
        self.label.setGeometry(170, 0, 500, 50)
        self.label.setFont(self.font)
        self.label.setText("Witaj w (TEMPLATE APP NAME)")

        self.label2 = QtWidgets.QLabel(self)
        self.font = QFont("Times", 20,)
        self.label2.setText("<font color='white'>Made by JachyCzkowicz Enterprises 2020</font>")
        self.label2.setGeometry(10, 430, 300, 20)

    def show_map(self): # funkcja wołająca się gdy przyciskamy przycisk "POKAZ MAPE ZAGROZEN"
        mapa = MapWindow() # tworzenie instancji klasy MapWindow()
        self.dialogs.append(mapa) # dodanie okna z mapą do dialogów głównego okna MainWindow
        mapa.show()

    def klikniecie(self):
        print("dupa")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.set_image(os.path.join('images', 'main_bg.jpg'))
    sys.exit(app.exec_())