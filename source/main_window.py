# TODO: ujednolicić nazwy (komentarze po polsku, ZMIENNE I NAZWY PLIKÓW PO ANGIELSKU)

import os
import sys
from pathlib import Path
from random import randint

from las_processing import extract_data
import merge_predict

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QDesktopWidget

parent_path = str(Path(os.getcwd()).parent)
# print(parent_path)

class MapWindow(QMainWindow):  # klasa reprezentujaca okienko z mapa na której beda odnośniki do każdej z map
    def __init__(self):
        super(MapWindow, self).__init__()
        self.buttons = []
        self.dialogs = list()
        # self.setGeometry(0, 0, 0, 0)
        self.setFixedSize(753, 454)
        self.setWindowTitle("LaVaLanche")
        # self.set_image("..\\images\\tlo.png")
        self.set_image(parent_path + "/images/tlo.png")
        self.draw_map_link_buttons()

        # obiekty topograficzne znajdujące się na poszczególnych obszarach (okno szczegółowe)
        self.get_topo_objects(parent_path + "/data/obiekty_scraped.txt")

        # TUTAJ OKREŚLAMY RYZYKO PRZY POMOCY MODUŁU merge_predict

        # PONIŻEJ WYŚRODKOWANIE OKNA
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def get_topo_objects(self, objects_path):
        f = open(objects_path, 'r', encoding = "utf-8")
        data = f.readlines()

        self.topo_objects = {}

        for line in data:
            l = line.split(',')

            if l[0] not in self.topo_objects:
                self.topo_objects[l[0]] = [l[1]]
            elif len(self.topo_objects[l[0]]) <= 7: # wystarczy 7 nazw obiektów, czasami jest dużo więcej
                self.topo_objects[l[0]].append(l[1])

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
        details = DetailWindow(map_name, self.topo_objects[map_name[ : -1]]) # -1 z powodu znaku końca linii
        self.dialogs.append(details)
        details.show()


class MainWindow(QMainWindow):  # klasa reprezentujaca glowne okno aplikacji
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.setGeometry(500, 500, 753, 454)
        self.setFixedSize(753, 454)

        # PONIŻEJ WYŚRODKOWANIE OKNA
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

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
        self.show_map_button.clicked.connect(self.show_map)
        # .clicked.connect() przy przycisnieciu wola funkcje

    def set_image(self, img_path):
        oimage = QImage(img_path)
        simage = oimage.scaled(QSize(753, 454))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(simage))
        self.setPalette(palette)

    def draw_labels(self):
        self.label = QLabel(self)
        self.font = QFont("Times", 20, QFont.Bold)
        self.label.setGeometry(230, 0, 500, 50)
        self.label.setFont(self.font)
        self.label.setText("Witaj w LaVaLanche!")

        self.label2 = QLabel(self)
        self.font = QFont("Times", 20, )
        self.label2.setText("<font color='white'>Made by JachyCzkowicz Enterprises 2020</font>")
        self.label2.setGeometry(10, 430, 300, 20)

    def show_map(self):  # funkcja wołająca się gdy przyciskamy przycisk "POKAZ MAPE ZAGROZEN"
        self.closeEvent()
        mapa = MapWindow()  # tworzenie instancji klasy MapWindow()
        self.dialogs.append(mapa)  # dodanie okna z mapą do dialogów głównego okna MainWindow
        mapa.show()

    def klikniecie(self):
        print("dupa")

    def closeEvent(self):
        self.destroy()


class DetailWindow(QMainWindow):
    def __init__(self, map_name, topo_objects):
        super(DetailWindow, self).__init__()
        # self.setGeometry(100, 100, 450, 300)
        self.setFixedSize(300, 200)
        self.setWindowTitle("Detail Window of " + map_name.rstrip())

        # MUSI BYĆ WIDGET, ŻEBY DZIAŁAŁ LAYOUT
        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)

        # PONIŻEJ WYŚRODKOWANIE OKNA
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # self.map_data = extract_data(map_name.rstrip() + ".las")  # funkcja uzywajaca laspy do otwarcia mapy
        # wypisz obiekty znajdujące się na obszarze

        self.objects = QLabel(self)
        self.objects.setText("Obiekty: \n" + ''.join(topo_objects))

        self.objects2 = QLabel(self)
        self.objects2.setText("Obiekty: \n" + ''.join(topo_objects))

        self.risk = QLabel(self)
        self.risk.setText("Ryzyko: niskie/umiarkowane")

        # POŁOŻENIE ELEMENTÓW
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.addWidget(self.risk, 0, 1)
        self.gridLayout.addWidget(self.objects, 1, 0)
        self.gridLayout.addWidget(self.objects2, 1, 2)
        self.gridLayout.setVerticalSpacing(2)
        wid.setLayout(self.gridLayout)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    sys.exit(app.exec_())
