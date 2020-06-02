# Ten skrypt czyta wszystkie pliki w formacie .las i na podstawie punktów oblicza kolejno następujące cechy:
# eksp_sloneczna, nachylenie, pietro, wysokosc.

import os
from pathlib import Path
from laspy.file import File
import numpy as np
import pandas as pd
import pyvista as pv

directory = "/media/dittohead/36A8502FA84FEBC5/LAS"
files = os.listdir(directory)
f = open("almost_topo_features.txt", "w")

# --- WCZYTANIE PLIKU ---
for filename in files:
    file = File(directory + '/' + filename, mode = 'r')
    point_records = file.points # ndarray z w wszystkimi punktami

    x = file.x[::100000]
    y = file.y[::100000]
    z = file.z[::100000]

    points = [list(point) for point in zip(x, y, z)]
    points = np.array(points)

    features = [] # przyszły rekord, na podstawie obliczeń ustalimy odpowiednie wartości cech

    # --- TRIANGULACJA ---
    cloud = pv.PolyData(points)
    surf = cloud.delaunay_2d()

    # --- PRZEDSTAW TEREN W PRZESTRZENI ---
    """
    p = pv.Plotter()
    p.add_mesh(surf, color = "white", show_edges = True)
    p.show(cpos = "xz")
    """

    # --- OBLICZANIE EKSPOZYCJI ---
    xy_normal = np.array([0, 0, 1])

    compass = {}
    compass["N"] = np.array([0, 1, 0])
    compass["NE"] = np.array([1, 1, 0]) / np.linalg.norm(np.array([1, 1, 0]))
    compass["E"] = np.array([1, 0, 0])
    compass["SE"] = np.array([1, -1, 0]) / np.linalg.norm(np.array([1, -1, 0]))
    compass["S"] = -compass["N"]
    compass["SW"] = -compass["NE"]
    compass["W"] = -compass["E"]
    compass["NW"] = -compass["SE"]

    found = {}
    found["NE"] = False
    found["W"] = False
    found["E"] = False

    for i in range(surf.face_normals.shape[0]):
        face_normal = surf.face_normals[i]
        face_normal = face_normal if face_normal[2] >= 0 else -face_normal

        flattened_normal = np.array([face_normal[0], face_normal[1], 0])
        flattened_normal = flattened_normal / np.linalg.norm(flattened_normal)

        for dir in compass:
            angle = np.degrees(np.arccos(np.dot(compass[dir], flattened_normal)))

            if angle < 15 and dir in ["NE", "W", "E"]:
                # sprawdź, czy stok o danej ekspozycji ma również odpowiednie nachylenie
                face_normal = surf.face_normals[i]
                face_slope = np.degrees(np.arccos(np.dot(xy_normal, face_normal)))
                face_slope = face_slope if face_slope < 90 else 180 - face_slope

                if face_slope >= 30 and face_slope <= 40:
                    found[dir] = True

                break

        if found["NE"] and found["W"] and found["E"]:
            features.append("True")
            break

    if features == []: # nie znaleziono stoku o odpowiedniej ekspozycji i nachyleniu
        features.append("False")

    # --- OBLICZANIE NACHYLENIA ---
    # Uwaga! Nie wiemy, czy wektor normalny jest skierowany wgłąb góry czy na powierzchnię (tak, jak byśmy chieli),
    # dlatego sprawdziwmy wartość i ewentualnie weźmiemy tę dopełniającą do 180 stopni.
    slopes = []

    for i in range(surf.face_normals.shape[0]):
        face_normal = surf.face_normals[i]
        face_slope = np.degrees(np.arccos(np.dot(xy_normal, face_normal)))
        face_slope = face_slope if face_slope < 90 else 180 - face_slope
        slopes.append(face_slope)

    # Cecha dot. nachylenia przyjmie wartość True, gdy Q1 >= 30 && Q3 <= 45
    df = pd.DataFrame(slopes)
    if df.quantile(0.25).values[0] >= 25 and df.quantile(0.75).values[0] <= 50:
        features.append("True")
    else:
        features.append("False")

    # --- OKREŚLENIE PIĘTRA ---
    max_height = file.header.max[2]
    if max_height >= 1600:
        features.append("True")
    else:
        features.append("False")

    # --- OKREŚLENIE WYSOKOŚCI ---
    df = pd.DataFrame(file.z)
    if df.quantile(0.25).values[0] >= 1300 and df.quantile(0.75).values[0] <= 2100:
        features.append("True")
    else:
        features.append("False")

    # --- ZAPIS CECH DO PLIKU ---
    area_name = filename.split('.')[0] # usuwamy rozszerzenie pliku
    to_write = area_name + ',' + ','.join(features) + '\n'
    print("Writing to file: " + to_write, end = '')
    f.write(to_write)
