import os
import sys

from random import randint
from las_processing import extract_data
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from pathlib import Path

parent_path = str(Path(os.getcwd()).parent)
print(parent_path)


class MapWindow(QMainWindow):  # klasa reprezentujaca okienko z mapa na której beda odnośniki do każdej z map
    def __init__(self):
        super(MapWindow, self).__init__()
        self.buttons = []
        self.dialogs = list()
        self.setGeometry(600, 600, 753, 454)
        self.setFixedSize(753, 454)
        self.setWindowTitle("LaVaLanche")
        # self.set_image("..\\images\\tlo.png")
        self.set_image(parent_path + "/images/tlo.png")
        self.draw_map_link_buttons()

    def set_image(self, img_path):
        oimage = QImage(img_path)
        simage = oimage.scaled(QSize(1506, 908))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(oimage))
        self.setPalette(palette)

    def draw_map_link_buttons(self):
        draw = False
        button_width = 22
        button_height = 22
        with open(parent_path + "/data/button_coords.txt") as buttonmap:
            nazwy_map = open(parent_path + "/data/maps_sequence.txt")
            for line in buttonmap:
                if draw:
                    coords = line.rstrip().split(",")
                    for i in range(0, 2):
                        coords[i] = int(coords[i])
                    button = QPushButton(self)
                    risk_level = randint(0, 4)
                    self.risk_color(risk_level, button)
                    button.setGeometry(coords[0], coords[1], button_width, button_height)
                    button.clicked.connect(lambda checked, arg=nazwy_map.readline(): self.show_details(arg))
                else:
                    if "M-34-101-A-b-3-1-1" in nazwy_map.readline():
                        draw = True

    def risk_color(self, risk_level, button):
        if risk_level == 0:
            button.setStyleSheet("QPushButton{background:rgba(76, 175, 80, 0.25)}")
        elif risk_level == 1:
            button.setStyleSheet("QPushButton{background:rgba(255, 255, 0, 0.25)}")
        elif risk_level == 2:
            button.setStyleSheet("QPushButton{background:rgba(255, 127, 0, 0.25)}")
        elif risk_level == 3:
            button.setStyleSheet("QPushButton{background:rgba(255, 0, 0, 0.25)}")
        elif risk_level == 4:
            button.setStyleSheet("QPushButton{background:rgba(0, 0, 0, 0.25)}")

    def show_details(self, map_name):
        details = DetailWindow(map_name)
        self.dialogs.append(details)
        details.show()


class MainWindow(QMainWindow):  # klasa reprezentujaca glowne okno aplikacji
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(500, 500, 753, 454)
        self.setFixedSize(753, 454)
        self.setWindowTitle("LaVaLanche")
        self.dialogs = list()
        self.draw_labels()
        self.draw_buttons()
        # self.set_image("..\\images\\main_bg.jpg")
        self.set_image(parent_path + "/images/main_bg.jpg")
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
        self.label = QLabel(self)
        self.font = QFont("Times", 20, QFont.Bold)
        self.label.setGeometry(170, 0, 500, 50)
        self.label.setFont(self.font)
        self.label.setText("Witaj w (TEMPLATE APP NAME)")

        self.label2 = QLabel(self)
        self.font = QFont("Times", 20, )
        self.label2.setText("<font color='white'>Made by JachyCzkowicz Enterprises 2020</font>")
        self.label2.setGeometry(10, 430, 300, 20)

    def show_map(self):  # funkcja wołająca się gdy przyciskamy przycisk "POKAZ MAPE ZAGROZEN"
        mapa = MapWindow()  # tworzenie instancji klasy MapWindow()
        self.dialogs.append(mapa)  # dodanie okna z mapą do dialogów głównego okna MainWindow
        mapa.show()

    def klikniecie(self):
        print("dupa")


class DetailWindow(QMainWindow):
    def __init__(self, map_name):
        super(DetailWindow, self).__init__()
        self.setGeometry(100, 100, 450, 300)
        self.setWindowTitle("Detail Window of " + map_name.rstrip())

        self.map_data = extract_data(map_name.rstrip() + ".las")  # funkcja uzywajaca laspy do otwarcia mapy

        self.label = QLabel(self)
        self.label.setText("Sczegóły ryzyka dla: " + map_name.rstrip())
        self.label.setGeometry(20, 20, 300, 20)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    sys.exit(app.exec_())
