# TODO: ujednolicić nazwy (komentarze po polsku, ZMIENNE I NAZWY PLIKÓW PO ANGIELSKU)

import os
import sys
from pathlib import Path
from random import randint
from merge_predict import *
from weather_analysis import overall_weather_analysis
import get_weather_data_from_server
from las_processing import extract_data
import merge_predict

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt
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

        # ustalamy jakie są cechy
        self.get_features_names(parent_path + "/data/artif_data.txt")

        self.draw_map_link_buttons()

        # obiekty topograficzne znajdujące się na poszczególnych obszarach (okno szczegółowe)
        self.get_topo_objects(parent_path + "/data/obiekty_scraped.txt")

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

    def get_features_names(self, features_names_path):
        f = open(features_names_path, 'r', encoding = "utf-8")
        self.features_names = f.readline().split(',')

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

            records = add_weather(add_season(load_topo_data()), overall_weather_analysis())
            risks = get_risks(records)
            nazwy_map = open(parent_path + "/data/maps_sequence.txt")

            for line in buttonmap:
                if draw:
                    mapa = nazwy_map.readline()
                    coords = line.rstrip().split(",")
                    for i in range(0, 2):
                        coords[i] = int(coords[i])
                    button = QPushButton(self)
                    risk_level = risks[mapa.rstrip()]
                    self.risk_color(risk_level, button)
                    button.setGeometry(coords[0], coords[1], button_width, button_height)
                    button.clicked.connect(lambda checked, arg1 = mapa, arg2 = risk_level,
                    arg3 = records[mapa.rstrip()], arg4 = self.features_names
                                : self.show_details(arg1, arg2, arg3, arg4))
                else:
                    if "M-34-101-A-b-3-1-1" in nazwy_map.readline():
                        draw = True

    def risk_color(self, risk_level, button):
        if "brak" in risk_level:
            button.setStyleSheet("QPushButton{background:rgba(76, 175, 80, 0.25)}"
                                 "QPushButton:hover{background:rgba(76, 175, 80, 0.75)}")
        elif "niskie/umiarkowane" in risk_level:
            button.setStyleSheet("QPushButton{background:rgba(255, 255, 0, 0.25)}")
        elif "wysokie" in risk_level:
            button.setStyleSheet("QPushButton{background:rgba(255, 0, 0, 0.25)}")

    def show_details(self, map_name, risk_level, features, features_names):
        details = DetailWindow(map_name, self.topo_objects[map_name.rstrip()], risk_level, features, features_names)
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
        # AKTUALIZACJA DANYCH POGODOWYCH
        self.show()

    def draw_buttons(self):
        self.show_map_button = QPushButton(self)
        self.show_map_button.setText("Mapa zagrożeń")
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
        self.hide()
        mapa = MapWindow()  # tworzenie instancji klasy MapWindow()
        self.dialogs.append(mapa)  # dodanie okna z mapą do dialogów głównego okna MainWindow
        mapa.show()


class DetailWindow(QMainWindow):
    def __init__(self, map_name, topo_objects, risk_level, features, features_names):
        super(DetailWindow, self).__init__()
        # self.setGeometry(100, 100, 450, 300)
        self.setFixedSize(400, 500)
        self.setWindowTitle("Szczegóły dla obszaru " + map_name.rstrip())

        self.dialogs = []

        if 'brak' in risk_level:
            self.setStyleSheet("DetailWindow{background:rgba(76, 175, 80, 0.5)}")
        elif "niskie/umiarkowane" in risk_level:
            self.setStyleSheet("QPushButton{background:rgba(255, 255, 0, 0.5)}")
        elif "wysokie" in risk_level:
            self.setStyleSheet("QPushButton{background:rgba(255, 0, 0, 0.5)}")

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
        self.objects.setText("OBIEKTY TOPOGRAFICZNE: \n" + ''.join(topo_objects))
        self.objects.setAlignment(Qt.AlignCenter)

        inc_features = [feature for index, feature in enumerate(features_names) if features[index] == "True"]
        self.incs = QLabel(self)
        self.incs.setText("CECHY INC: \n" + '\n'.join(inc_features))
        self.incs.setAlignment(Qt.AlignCenter)

        self.risk = QLabel(self)
        self.risk.setText("RYZYKO:\n" + risk_level)
        self.risk.setAlignment(Qt.AlignCenter)

        self.display_button = QPushButton(self)
        self.display_button.setText("Wyświetl drzewo decyzyjne")
        self.display_button.clicked.connect(self.show_tree)

        # POŁOŻENIE ELEMENTÓW
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.risk)
        self.layout.addWidget(self.objects)
        self.layout.addWidget(self.incs)
        self.layout.addWidget(self.display_button)
        wid.setLayout(self.layout)

        self.show()

    def show_tree(self):
        tree_window = ImageWindow()
        self.dialogs.append(tree_window)


class ImageWindow(QMainWindow):
    def __init__(self):
        super(ImageWindow, self).__init__()
        self.setWindowTitle("Drzewo decyzyjne")
        self.scale = 1
        self.setFixedSize(1243 * self.scale, 896 * self.scale)
        self.set_image("../images/tree.png")
        self.show()

        # PONIŻEJ WYŚRODKOWANIE OKNA
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def set_image(self, img_path):
        oimage = QImage(img_path)
        simage = oimage.scaled(oimage.size() * self.scale)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(simage))
        self.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    sys.exit(app.exec_())
